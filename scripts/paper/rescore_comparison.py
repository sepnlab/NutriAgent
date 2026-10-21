"""Re-score a `--compare` run with a smaller EvaluatorLLM batch size.

`score_bulk` can drop items when the judge returns malformed JSON. This script
re-scores all responses in `responses.json` with batch size 5 and a per-item
fallback, then writes per-query scores and per-method aggregates.

Usage:
    python scripts/paper/rescore_comparison.py \
        --log-dir logs/comp_layer_20261020_190019 \
        --out docs/paper/audit/e18_rescored.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--out", default=str(PROJECT_ROOT / "docs" / "paper" / "audit" / "e18_rescored.json"))
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--models", default="", help="comma-separated substring filter")
    args = parser.parse_args()

    from src.evaluation.evaluator_llm import EvaluatorLLM

    data = json.loads((Path(args.log_dir) / "responses.json").read_text(encoding="utf-8"))
    queries = data["queries"]
    responses = data["responses"]
    ev = EvaluatorLLM()

    result = {}
    wanted = [s.strip() for s in args.models.split(",") if s.strip()]
    for model, rows in responses.items():
        if wanted and not any(w.lower() in model.lower() for w in wanted):
            continue
        print(f"{model}: {len(rows)} responses")
        scores = ev.score_bulk(queries, rows, batch_size=args.batch_size) or []
        per_query = []
        for i, (q, r) in enumerate(zip(queries, rows)):
            score = scores[i] if i < len(scores) else None
            if not score or score.get("correctness") is None:
                try:
                    single = ev.score_responses(q["query"], {"response": r})
                    score = (single or {}).get("response")
                except Exception:
                    score = None
            per_query.append(
                {
                    "id": q.get("id"),
                    "type": q.get("type"),
                    "category": q.get("category"),
                    "correctness": (score or {}).get("correctness"),
                    "precision": (score or {}).get("precision"),
                    "scientific_depth": (score or {}).get("scientific_depth"),
                }
            )

        def agg(key):
            vals = [x[key] for x in per_query if isinstance(x[key], (int, float))]
            if not vals:
                return {"mean": None, "std": None, "n": 0}
            return {
                "mean": round(statistics.mean(vals), 4),
                "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
                "n": len(vals),
            }

        result[model] = {
            "correctness": agg("correctness"),
            "precision": agg("precision"),
            "scientific_depth": agg("scientific_depth"),
            "per_query": per_query,
        }
        print(" ", {k: result[model][k] for k in ("correctness", "precision", "scientific_depth")})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
