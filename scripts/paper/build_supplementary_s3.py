"""Generate Supplementary S3 from the curated query JSON (single source of truth).

The submitted Supplementary S3 lists query texts that do not match
`queries/layer/evaluation_queries_curated.json` (audit finding F8). This script
regenerates S3 from the JSON and, with --compare, reports every mismatch with
the current supplement.

Usage:
    python scripts/paper/build_supplementary_s3.py
    python scripts/paper/build_supplementary_s3.py --compare
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
SUPPLEMENT = PROJECT_ROOT / "docs" / "paper" / "supplementary_material.md"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "s3_queries.md"
RECON = PROJECT_ROOT / "docs" / "paper" / "audit" / "s3_reconciliation.md"

TYPE_ORDER = [
    "single-value",
    "comparison",
    "open-ended",
    "definition",
    "multi-hop",
    "constraint",
    "counterfactual",
]


def load() -> dict:
    return json.loads(QUERIES.read_text(encoding="utf-8"))


def build_markdown(data: dict) -> str:
    rows = [(cat, q) for cat, items in data.items() for q in items]
    by_lang = Counter(q.get("language", "en") for _, q in rows)
    by_type = Counter(q.get("type") for _, q in rows)
    n_gt = sum(1 for _, q in rows if q.get("expected_value") is not None)
    n_beh = sum(1 for _, q in rows if q.get("expected_behavior") is not None)

    lines = [
        "## S3. Evaluation Query Sets",
        "",
        "### S3.1 Curated Evaluation Set (54 queries)",
        "",
        "> Auto-generated from `queries/layer/evaluation_queries_curated.json` by "
        "`scripts/paper/build_supplementary_s3.py`. Do not edit by hand.",
        "",
        f"- Total: **{len(rows)}** queries "
        f"({by_lang.get('en', 0)} English / {by_lang.get('zh', 0)} Chinese)",
        f"- Query types: {dict(by_type)}",
        f"- Numeric ground truth: **{n_gt}**; expected-behaviour annotations: **{n_beh}**",
        "",
    ]

    for cat, items in data.items():
        lines.append(f"**{cat} ({len(items)} queries)**")
        lines.append("")
        for q in items:
            lang = q.get("language", "en").upper()
            unit = f"; unit={q['expected_unit']}" if q.get("expected_unit") else ""
            target = (
                f"; target={', '.join(q['target_doc'])}" if q.get("target_doc") else ""
            )
            lines.append(
                f"- {q['id']}: {q['query']} "
                f"[{q.get('type')}, {lang}{unit}{target}]"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_supplement(path: Path) -> dict[str, str]:
    """Extract `- ID: query [type, LANG]` lines from the current S3 section."""
    text = path.read_text(encoding="utf-8")
    start = text.find("### S3.1")
    end = text.find("---", start) if start != -1 else -1
    section = text[start:end] if start != -1 else text
    out: dict[str, str] = {}
    for line in section.splitlines():
        m = re.match(r"^- ([A-Z]+-[A-Z]+-\d+): (.*?) \[[^\]]*\]\s*$", line.strip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def compare(data: dict) -> str:
    current = parse_supplement(SUPPLEMENT)
    rows = {q["id"]: q for _, q in ((c, q) for c, items in data.items() for q in items)}
    missing = sorted(set(rows) - set(current))
    extra = sorted(set(current) - set(rows))
    mismatched = []
    for qid in sorted(set(rows) & set(current)):
        if rows[qid]["query"].strip() != current[qid].strip():
            mismatched.append((qid, current[qid], rows[qid]["query"]))

    lines = [
        "# S3 Reconciliation (submitted supplement vs curated JSON)",
        "",
        f"- JSON queries: {len(rows)}; supplement rows parsed: {len(current)}",
        f"- In JSON but missing from supplement: {len(missing)} {missing}",
        f"- In supplement but not in JSON: {len(extra)} {extra}",
        f"- Text mismatches: {len(mismatched)}",
        "",
        "| ID | Submitted S3 text | Curated JSON text |",
        "|---|---|---|",
    ]
    for qid, old, new in mismatched:
        lines.append(f"| {qid} | {old} | {new} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare", action="store_true")
    args = parser.parse_args()

    data = load()
    OUT.write_text(build_markdown(data), encoding="utf-8")
    print(f"wrote {OUT}")

    if args.compare:
        RECON.write_text(compare(data), encoding="utf-8")
        print(f"wrote {RECON}")
        print(RECON.read_text(encoding="utf-8")[:1200])


if __name__ == "__main__":
    main()
