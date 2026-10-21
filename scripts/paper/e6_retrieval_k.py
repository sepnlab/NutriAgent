"""E6: PoultryDB retrieval hit@k and MRR (k = 1, 3, 5).

Uses the curated queries' `target_doc` annotations. A retrieved document counts
as a hit when its source matches the target's source prefix and its content
contains the target identifier (for "Breed/Phase" targets, both parts must
appear). This measures retrieval, not answer quality, and does not call an LLM.

Usage:
    python scripts/paper/e6_retrieval_k.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SPECIES", "layer")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e6_retrieval_k.json"


SOURCE_ALIASES = {
    "feed_ingredient_bank": "feed ingredient bank",
    "feed_ingredient_amino_acids": "feed ingredient bank",
    "feed_ingredient_digestibility": "feed ingredient bank",
    "definitions": "definitions",
    "nutrient_requirements": "nutrient requirements",
    "performance_management": "performance management",
}


def target_parts(target: str) -> tuple[str, list[str]]:
    source, ident = target.split(":", 1)
    parts = [p.strip().lower() for p in ident.replace("/", "|").split("|") if p.strip()]
    return SOURCE_ALIASES.get(source.lower(), source.lower().replace("_", " ")), parts


def is_hit(result: dict, target: str) -> bool:
    source, parts = target_parts(target)
    got_source = str(result.get("source", "")).lower().replace("_", " ")
    content = str(result.get("content", "")).lower()
    if source not in got_source:
        return False
    return all(p in content for p in parts)


def main() -> None:
    from src.rag.poultry_db import PoultryDB

    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    rows = [dict(q, category=cat) for cat, items in data.items() for q in items]
    rows = [q for q in rows if q.get("target_doc")]

    db = PoultryDB()
    records = []
    for q in rows:
        results = db.search(q["query"], k=5)
        hits = []
        for rank, r in enumerate(results, 1):
            hits.append(any(is_hit(r, t) for t in q["target_doc"]))
        first = next((i for i, h in enumerate(hits, 1) if h), None)
        records.append(
            {
                "id": q["id"],
                "type": q.get("type"),
                "category": q.get("category"),
                "hit@1": bool(hits and hits[0]),
                "hit@3": any(hits[:3]),
                "hit@5": any(hits[:5]),
                "first_hit_rank": first,
                "n_targets": len(q["target_doc"]),
            }
        )

    def rate(key: str) -> float:
        return round(sum(r[key] for r in records) / len(records), 3)

    summary = {
        "n_queries": len(records),
        "hit@1": rate("hit@1"),
        "hit@3": rate("hit@3"),
        "hit@5": rate("hit@5"),
        "mrr": round(
            sum(1.0 / r["first_hit_rank"] for r in records if r["first_hit_rank"]) / len(records),
            3,
        ),
    }
    by_type = {}
    for qtype in sorted({r["type"] for r in records}):
        sub = [r for r in records if r["type"] == qtype]
        by_type[qtype] = {
            "n": len(sub),
            "hit@1": round(sum(r["hit@1"] for r in sub) / len(sub), 3),
            "hit@5": round(sum(r["hit@5"] for r in sub) / len(sub), 3),
        }

    OUT.write_text(json.dumps({"summary": summary, "by_type": by_type, "rows": records}, indent=2), encoding="utf-8")
    md = [
        "# E6: PoultryDB retrieval hit@k",
        "",
        f"Queries with target_doc: {summary['n_queries']}.",
        "",
        f"- hit@1: {summary['hit@1']:.1%}",
        f"- hit@3: {summary['hit@3']:.1%}",
        f"- hit@5: {summary['hit@5']:.1%}",
        f"- MRR: {summary['mrr']}",
        "",
        "| Type | n | hit@1 | hit@5 |",
        "|---|---:|---:|---:|",
    ]
    for t, s in by_type.items():
        md.append(f"| {t} | {s['n']} | {s['hit@1']:.1%} | {s['hit@5']:.1%} |")
    md += ["", "## Misses at k=5", "", "| ID | Type | Targets |", "|---|---|---|"]
    for r in records:
        if not r["hit@5"]:
            md.append(f"| {r['id']} | {r['type']} | {r['n_targets']} |")
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "by_type": by_type}, indent=2))


if __name__ == "__main__":
    main()
