"""E14: numeric error audit with the Rev.1 relative-error tolerance.

For each query with an expected value, classify the NutriAgent response as:
  correct             - a parsed number is within 5% relative error
  wrong_value         - numbers exist but none is within tolerance
  no_numeric_answer   - no parsed number

Also reports the pass rate under the submitted interval rule for comparison.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.evaluation.evaluator import check_tolerance, parse_numeric  # noqa: E402

LOG = PROJECT_ROOT / "logs" / "comp_layer_20261020_190019"
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e14_tolerance_errors.json"


def old_rule(predicted: float, gt: float, tol: float = 0.05) -> bool:
    return predicted * (1 - tol) <= gt <= predicted * (1 + tol)


def expected_number(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip().split()[0])
    except Exception:
        return None


def main() -> None:
    data = json.loads((LOG / "responses.json").read_text(encoding="utf-8"))
    model = next(m for m in data["models"] if "NutriCHAT" in m)
    responses = data["responses"][model]
    # Use the current curated metadata (expected values may have been corrected),
    # not the copy embedded in the old run log.
    source = json.loads(QUERIES.read_text(encoding="utf-8"))
    by_id = {q["id"]: dict(q, category=cat) for cat, items in source.items() for q in items}
    queries = [by_id.get(q["id"], q) for q in data["queries"]]

    rows = []
    for q, r in zip(queries, responses):
        gt = expected_number(q.get("expected_value"))
        if gt is None:
            continue
        nums = [x[0] for x in parse_numeric(r)] if r else []
        if not nums:
            label = "no_numeric_answer"
            new_pass = old_pass = False
            new2 = old2 = False
        else:
            best = min(nums, key=lambda x: abs(x - gt))
            new_pass = check_tolerance(best, gt, 0.05)
            old_pass = old_rule(best, gt, 0.05)
            new2 = check_tolerance(best, gt, 0.02)
            old2 = old_rule(best, gt, 0.02)
            label = "correct" if new_pass else "wrong_value"
        rows.append(
            {
                "id": q.get("id"),
                "type": q.get("type"),
                "expected": gt,
                "n_numbers": len(nums),
                "best": min(nums, key=lambda x: abs(x - gt)) if nums else None,
                "new_pass": bool(new_pass),
                "old_pass": bool(old_pass),
                "new_pass_2": bool(new2),
                "old_pass_2": bool(old2),
                "label": label,
            }
        )

    counts = {"correct": 0, "wrong_value": 0, "no_numeric_answer": 0}
    for r in rows:
        counts[r["label"]] += 1
    n = len(rows)
    summary = {
        "n_queries": n,
        "labels": counts,
        "new_pass_rate": round(sum(r["new_pass"] for r in rows) / n, 3),
        "old_pass_rate": round(sum(r["old_pass"] for r in rows) / n, 3),
        "new_pass_rate_2": round(sum(r["new_pass_2"] for r in rows) / n, 3),
        "old_pass_rate_2": round(sum(r["old_pass_2"] for r in rows) / n, 3),
        "changed_by_rule": [r["id"] for r in rows if r["new_pass"] != r["old_pass"]],
    }
    OUT.write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# E14: numeric error audit (relative-error tolerance)",
        "",
        f"Numeric queries: {n}.",
        "",
        "| Label | n |",
        "|---|---:|",
        f"| correct | {counts['correct']} |",
        f"| wrong_value | {counts['wrong_value']} |",
        f"| no_numeric_answer | {counts['no_numeric_answer']} |",
        "",
        f"Pass rate: new relative-error rule {summary['new_pass_rate']:.1%}; "
        f"old interval rule {summary['old_pass_rate']:.1%}.",
        f"At ±2%: new {summary['new_pass_rate_2']:.1%}; old {summary['old_pass_rate_2']:.1%}.",
        "",
        "## Failures",
        "",
        "| ID | Type | Expected | Best parsed | Label |",
        "|---|---|---:|---:|---|",
    ]
    for r in rows:
        if r["label"] != "correct":
            md.append(f"| {r['id']} | {r['type']} | {r['expected']} | {r['best']} | {r['label']} |")
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
