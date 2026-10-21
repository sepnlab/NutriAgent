"""E9: repeat-run variability of the multi-agent pipeline.

Runs a stratified 10-query subset three times with temperature 0.0 and cache
disabled, then reports pairwise text similarity, exact-match rate, and latency
variation. This tests stability, not correctness.

Usage:
    python scripts/paper/e9_repeatability.py
"""

from __future__ import annotations

import json
import os
import statistics
import sys
from difflib import SequenceMatcher
from pathlib import Path

os.environ.setdefault("SPECIES", "layer")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e9_repeatability.json"


def select_queries() -> list[dict]:
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    rows = [dict(q, category=cat) for cat, items in data.items() for q in items]
    by_type: dict[str, list[dict]] = {}
    for q in rows:
        by_type.setdefault(q.get("type", "unknown"), []).append(q)
    selected = []
    for qtype, items in by_type.items():
        selected.extend(items[:2])
    return selected[:10]


def main() -> None:
    from src.main import setup_engine

    queries = select_queries()
    engine = setup_engine(mode="multi", rag_enabled=True, verbose=False)
    rows = []
    for q in queries:
        runs = []
        for _ in range(3):
            result = engine.answer(q["query"], use_cache=False)
            runs.append(
                {
                    "response": result.get("response", ""),
                    "elapsed_s": result.get("elapsed_s"),
                }
            )
        texts = [r["response"] for r in runs]
        sims = [
            SequenceMatcher(None, texts[i], texts[j]).ratio()
            for i in range(3)
            for j in range(i + 1, 3)
        ]
        rows.append(
            {
                "id": q.get("id"),
                "type": q.get("type"),
                "category": q.get("category"),
                "similarity": round(statistics.mean(sims), 4),
                "similarity_min": round(min(sims), 4),
                "exact_match": len(set(texts)) == 1,
                "latencies_s": [round(r["elapsed_s"], 2) if r["elapsed_s"] else None for r in runs],
            }
        )
        print(q.get("id"), rows[-1]["similarity"], rows[-1]["exact_match"], flush=True)

    all_sims = [r["similarity"] for r in rows]
    summary = {
        "n_queries": len(rows),
        "n_runs_per_query": 3,
        "mean_similarity": round(statistics.mean(all_sims), 4),
        "min_similarity": round(min(all_sims), 4),
        "max_similarity": round(max(all_sims), 4),
        "exact_match_rate": round(sum(r["exact_match"] for r in rows) / len(rows), 3),
        "mean_latency_s": round(
            statistics.mean(
                [x for r in rows for x in r["latencies_s"] if isinstance(x, (int, float))]
            ),
            2,
        ),
    }
    out = {"summary": summary, "rows": rows}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [
        "# E9: repeat-run variability",
        "",
        f"Queries: {summary['n_queries']}; runs per query: 3; temperature 0.0; cache disabled.",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Mean pairwise similarity | {summary['mean_similarity']} |",
        f"| Min / max | {summary['min_similarity']} / {summary['max_similarity']} |",
        f"| Exact-match rate | {summary['exact_match_rate']} |",
        f"| Mean latency (s) | {summary['mean_latency_s']} |",
    ]
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
