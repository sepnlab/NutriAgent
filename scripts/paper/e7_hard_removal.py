"""E7: hard data removal for the Feed specialist.

Two conditions on the same 20 Feed/Cross-Domain queries:
  full            - normal multi-agent pipeline
  hard_removal    - Feed specialist deleted AND feed documents filtered out of RAG
This is stricter than D2, which removes the specialist/tool but leaves the shared
corpus accessible. Responses are scored with EvaluatorLLM absolute scoring.

Usage:
    python scripts/paper/e7_hard_removal.py
"""

from __future__ import annotations

import json
import os
import statistics
import sys
from pathlib import Path

os.environ.setdefault("SPECIES", "layer")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e7_hard_removal.json"


def load_queries() -> list[dict]:
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    rows = []
    for cat in ("Feed Ingredient Bank", "Cross-Domain"):
        for q in data.get(cat, [])[:10]:
            rows.append(dict(q, category=cat))
    return rows


def filter_feed_rag(engine) -> None:
    db = engine.multi_agent.poultry_db
    if db is None:
        return
    original = db.search

    def search_filtered(query, k=None):
        results = original(query, k)
        return [r for r in results if "feed ingredient" not in str(r.get("source", "")).lower()]

    db.search = search_filtered


def run_condition(queries: list[dict], hard: bool) -> list[str]:
    from src.main import setup_engine

    engine = setup_engine(mode="multi", rag_enabled=True, verbose=False)
    if hard:
        specialists = engine.multi_agent.specialists
        if "feed" in specialists:
            del specialists["feed"]
        filter_feed_rag(engine)
    responses = []
    for i, q in enumerate(queries, 1):
        result = engine.answer(q["query"], use_cache=False)
        responses.append(result.get("response", ""))
        print(("hard" if hard else "full"), i, "/", len(queries), flush=True)
    return responses


def score(queries: list[dict], responses: list[str]) -> dict:
    from src.evaluation.evaluator_llm import EvaluatorLLM

    ev = EvaluatorLLM()
    scores = ev.score_bulk(queries, responses, batch_size=3) or []
    per = []
    for i, (q, r) in enumerate(zip(queries, responses)):
        s = scores[i] if i < len(scores) else None
        if not s or s.get("correctness") is None:
            try:
                single = ev.score_responses(q["query"], {"response": r})
                s = (single or {}).get("response")
            except Exception:
                s = None
        per.append(
            {
                "id": q["id"],
                "correctness": (s or {}).get("correctness"),
                "precision": (s or {}).get("precision"),
                "scientific_depth": (s or {}).get("scientific_depth"),
            }
        )

    def agg(key):
        vals = [x[key] for x in per if isinstance(x[key], (int, float))]
        return {
            "mean": round(statistics.mean(vals), 4) if vals else None,
            "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
            "n": len(vals),
        }

    return {"correctness": agg("correctness"), "precision": agg("precision"),
            "scientific_depth": agg("scientific_depth"), "per_query": per}


def main() -> None:
    queries = load_queries()
    print(f"{len(queries)} queries")
    full = run_condition(queries, hard=False)
    hard = run_condition(queries, hard=True)
    result = {
        "n_queries": len(queries),
        "full": score(queries, full),
        "hard_removal": score(queries, hard),
        "responses": {"full": full, "hard_removal": hard},
    }
    diffs = {}
    for metric in ("correctness", "precision", "scientific_depth"):
        a = result["hard_removal"][metric]["mean"]
        b = result["full"][metric]["mean"]
        diffs[metric] = round(a - b, 4) if a is not None and b is not None else None
    result["hard_minus_full"] = diffs
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# E7: Feed specialist hard data removal",
        "",
        f"Queries: {len(queries)} (10 Feed Ingredient Bank + 10 Cross-Domain).",
        "",
        "| Metric | Full | Hard removal | Δ |",
        "|---|---:|---:|---:|",
    ]
    for m in ("correctness", "precision", "scientific_depth"):
        md.append(
            f"| {m} | {result['full'][m]['mean']} (n={result['full'][m]['n']}) | "
            f"{result['hard_removal'][m]['mean']} (n={result['hard_removal'][m]['n']}) | "
            f"{diffs[m]} |"
        )
    md += ["", "Hard removal deletes the Feed specialist and filters Feed Ingredient Bank documents out of RAG."]
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"diffs": diffs, "full": result["full"]["correctness"],
                      "hard": result["hard_removal"]["correctness"]}, indent=2))


if __name__ == "__main__":
    main()
