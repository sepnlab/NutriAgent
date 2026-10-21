"""Extract and validate the three completed expert workbooks.

Writes normalized CSVs to docs/paper/audit/ and a validation report.
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(r"D:\Geqi_series\NutriChat")
SRC = Path(r"C:\Users\young\Desktop\专家评分")
AUDIT = ROOT / "docs" / "paper" / "audit"
MAP = json.loads((AUDIT / "expert_label_map.json").read_text(encoding="utf-8"))
LABELS = {f"Model_{c}" for c in "ABCDEFG"}

FILES = {
    "primary": "主专家_评分完成_20261021.xlsx",
    "second": "第二专家_评分完成_20261021.xlsx",
    "third": "第三专家_评分完成_20261021.xlsx",
}


def parse_score(value, metric: str):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        value = float(value)
        return int(value) if value.is_integer() else value
    text = str(value).strip()
    if text == "":
        return None
    if metric == "precision" and text.upper() in {"N/A", "NA", "N.A."}:
        return "N/A"
    if metric == "provenance" and text.upper() in {"N/A", "NA", "NONE"}:
        return None
    try:
        number = float(text)
        return int(number) if number.is_integer() else number
    except ValueError:
        return text


def load(path: Path):
    wb = load_workbook(path, data_only=True)
    ws = wb["评分表"]
    headers = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
    idx = {h: i + 1 for i, h in enumerate(headers) if h}
    # Header names contain newlines; map by prefix.
    def col(prefix):
        for h, i in idx.items():
            if str(h).split("\n")[0].strip().lower() == prefix.lower():
                return i
        raise KeyError(prefix)

    c_qid, c_model = col("query_id"), col("model_id")
    c_cat, c_type, c_lang = col("category"), col("query_type"), col("language")
    c_c, c_p, c_d, c_prov = col("correctness"), col("precision"), col("scientific_depth"), col("provenance")
    c_notes = col("notes")

    rows = []
    for r in range(2, ws.max_row + 1):
        qid = ws.cell(r, c_qid).value
        if not qid:
            continue
        rows.append(
            {
                "query_id": str(qid).strip(),
                "model_id": str(ws.cell(r, c_model).value).strip(),
                "category": ws.cell(r, c_cat).value,
                "query_type": ws.cell(r, c_type).value,
                "language": ws.cell(r, c_lang).value,
                "correctness": parse_score(ws.cell(r, c_c).value, "correctness"),
                "precision": parse_score(ws.cell(r, c_p).value, "precision"),
                "scientific_depth": parse_score(ws.cell(r, c_d).value, "scientific_depth"),
                "provenance": parse_score(ws.cell(r, c_prov).value, "provenance"),
                "notes": ws.cell(r, c_notes).value,
            }
        )
    return rows


def validate_role(role: str, rows: list[dict]) -> dict:
    issues = []
    for r in rows:
        for metric in ("correctness", "scientific_depth"):
            v = r[metric]
            if not isinstance(v, int) or not 1 <= v <= 5:
                issues.append(f"{r['query_id']} {r['model_id']} {metric}={v!r}")
        p = r["precision"]
        if not (p == "N/A" or (isinstance(p, int) and 1 <= p <= 5)):
            issues.append(f"{r['query_id']} {r['model_id']} precision={p!r}")
        prov = r["provenance"]
        if prov is not None and not (isinstance(prov, int) and 0 <= prov <= 2):
            issues.append(f"{r['query_id']} {r['model_id']} provenance={prov!r}")
        if r["model_id"] not in LABELS:
            issues.append(f"unknown model {r['model_id']}")

    models = Counter(r["model_id"] for r in rows)
    queries = len({r["query_id"] for r in rows})
    return {
        "role": role,
        "rows": len(rows),
        "queries": queries,
        "models": dict(models),
        "issues": issues,
        "missing_notes": sum(1 for r in rows if r["notes"] not in (None, "")),
    }


def main() -> None:
    all_rows = {}
    reports = []
    for role, fname in FILES.items():
        rows = load(SRC / fname)
        all_rows[role] = rows
        reports.append(validate_role(role, rows))

        out = AUDIT / f"expert_scores_{role}.csv"
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print("wrote", out, len(rows))

    # Overlap / identity checks
    def keys(rows):
        return {(r["query_id"], r["model_id"]) for r in rows}

    kp, ks, kt = keys(all_rows["primary"]), keys(all_rows["second"]), keys(all_rows["third"])
    overlap = {
        "primary_second": len(kp & ks),
        "primary_third": len(kp & kt),
        "second_third": len(ks & kt),
        "second_only": len(ks - kt),
        "third_only": len(kt - ks),
    }

    # Exact score agreement between second and third on shared keys
    by_s = {(r["query_id"], r["model_id"]): r for r in all_rows["second"]}
    by_t = {(r["query_id"], r["model_id"]): r for r in all_rows["third"]}
    shared = sorted(ks & kt)
    agree = {}
    for metric in ("correctness", "precision", "scientific_depth", "provenance"):
        pairs = [(by_s[k][metric], by_t[k][metric]) for k in shared]
        pairs = [(a, b) for a, b in pairs if isinstance(a, int) and isinstance(b, int)]
        agree[metric] = {
            "n": len(pairs),
            "exact": sum(a == b for a, b in pairs),
            "mean_abs_diff": round(statistics.mean(abs(a - b) for a, b in pairs), 3) if pairs else None,
        }

    report = {
        "reports": reports,
        "overlap": overlap,
        "second_third_agreement": agree,
        "same_second_third_rows": ks == kt,
    }
    (AUDIT / "expert_scores_validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
