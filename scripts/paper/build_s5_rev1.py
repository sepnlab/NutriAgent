"""Regenerate Supplementary Table S5 from the Rev.1 NutriAgent auto scores."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCORES = PROJECT_ROOT / "docs" / "paper" / "audit" / "e18_rescored.json"
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
SUPP = PROJECT_ROOT / "docs" / "paper" / "supplementary_material.md"


def fmt(v):
    return "—" if v is None else f"{v:g}"


def main() -> None:
    scores = json.loads(SCORES.read_text(encoding="utf-8"))
    model = next(iter(scores))
    per_query = {row["id"]: row for row in scores[model]["per_query"]}

    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    meta = {
        q["id"]: dict(q, _category=cat)
        for cat, items in data.items()
        for q in items
    }

    lines = [
        "## S5. Per-query EvaluatorLLM results (Rev.1 NutriAgent)",
        "",
        "Per-query MiMo-V2.5-Pro absolute scores for NutriAgent on the frozen Rev.1 model set "
        "(single run). Expert scores for the main comparison are being collected; this table "
        "is the automated-score record and is not the primary expert table.",
        "",
        "**Table S5.** Per-query automated scores for NutriAgent (DeepSeek-V4-Flash, multi-agent, "
        "validation on). C = correctness, P = precision, D = scientific depth; — = not scored. "
        "SelfCheckGPT-NLI and tolerance are reported in aggregate elsewhere, not per query here.",
        "",
        "| ID | Category | Type | C | P | D |",
        "|---|---|---|---:|---:|---:|",
    ]
    for qid in sorted(per_query):
        row = per_query[qid]
        q = meta.get(qid, {})
        lines.append(
            f"| {qid} | {q.get('category', q.get('_category', '—'))} | {q.get('type', '—')} | "
            f"{fmt(row.get('correctness'))} | {fmt(row.get('precision'))} | {fmt(row.get('scientific_depth'))} |"
        )
    block = "\n".join(lines) + "\n\n"

    text = SUPP.read_text(encoding="utf-8")
    start = text.index("## S5.")
    end = text.index("## S6.")
    SUPP.write_text(text[:start] + block + text[end:], encoding="utf-8")
    print(f"replaced S5 with {len(per_query)} rows")


if __name__ == "__main__":
    main()
