"""Per-item re-scoring for one ablation variant.

`score_bulk` is unreliable for some providers (empty/malformed JSON). This script
scores each response individually with `score_responses`, which returns a small
JSON object and is much less likely to fail.

Usage:
    python scripts/paper/score_variant_per_item.py \
        --log-dir logs/ablation_specialist_layer_20261020_200015 \
        --variant "Without Nutrition" \
        --out docs/paper/audit/d2_wo_nutrition_n54.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"


def load_queries():
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    return [dict(q, category=c) for c, items in data.items() for q in items]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    from src.evaluation.evaluator_llm import EvaluatorLLM

    cache = json.loads((Path(args.log_dir) / ".ablation_cache.json").read_text(encoding="utf-8"))
    entries = cache[args.variant]
    queries = load_queries()
    by_text = {q["query"].strip(): q for q in queries}

    ev = EvaluatorLLM()
    per_query = []
    for i, (text, entry) in enumerate(entries.items(), 1):
        q = by_text.get(text.strip())
        if q is None:
            continue
        response = entry.get("resp", "") if isinstance(entry, dict) else str(entry)
        score = None
        try:
            single = ev.score_responses(q["query"], {"response": response})
            score = (single or {}).get("response")
        except Exception as exc:
            print("ERR", q["id"], type(exc).__name__, str(exc)[:80], flush=True)
        per_query.append(
            {
                "id": q["id"],
                "correctness": (score or {}).get("correctness"),
                "precision": (score or {}).get("precision"),
                "scientific_depth": (score or {}).get("scientific_depth"),
            }
        )
        if i % 10 == 0:
            print(i, "/", len(entries), flush=True)

    def agg(key):
        vals = [x[key] for x in per_query if isinstance(x[key], (int, float))]
        return {
            "mean": round(statistics.mean(vals), 4) if vals else None,
            "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
            "n": len(vals),
        }

    out = {
        "variant": args.variant,
        "correctness": agg("correctness"),
        "precision": agg("precision"),
        "scientific_depth": agg("scientific_depth"),
        "per_query": per_query,
    }
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("correctness", "precision", "scientific_depth")}, indent=2))


if __name__ == "__main__":
    main()
