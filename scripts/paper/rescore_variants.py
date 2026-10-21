"""Re-score ablation variants whose EvaluatorLLM batch returned partial results.

`score_bulk` can silently drop items when the evaluator's JSON is malformed or
truncated, leaving a variant with n < 54. This script re-scores the full
response set for selected variants from the ablation cache, with a smaller
batch size and a per-item fallback, and writes per-query scores plus aggregates.

Usage:
    python scripts/paper/rescore_variants.py \
        --log-dir logs/ablation_architecture_factorial_layer_20261020_181143 \
        --variants "Single ReAct + tools + RAG + synthesis" "Multi-Agent (validation on)" \
        --out docs/paper/audit/e1_rescored.json
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


def load_queries() -> list[dict]:
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    return [dict(q, category=cat) for cat, items in data.items() for q in items]


def get_response(entry):
    if isinstance(entry, dict):
        return entry.get("resp", "")
    return entry or ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--variants", nargs="+", required=True)
    parser.add_argument("--out", default=str(PROJECT_ROOT / "docs" / "paper" / "audit" / "e1_rescored.json"))
    parser.add_argument("--batch-size", type=int, default=5)
    args = parser.parse_args()

    cache = json.loads(
        (Path(args.log_dir) / ".ablation_cache.json").read_text(encoding="utf-8")
    )
    queries = load_queries()
    by_text = {q["query"]: q for q in queries}

    from src.evaluation.evaluator_llm import EvaluatorLLM

    ev = EvaluatorLLM()
    result = {}
    for variant in args.variants:
        entries = cache.get(variant, {})
        selected = []
        for text, entry in entries.items():
            q = by_text.get(text)
            if q is None:
                # Cache keys may differ by whitespace; match loosely.
                q = next((x for x in queries if x["query"].strip() == text.strip()), None)
            if q is None:
                continue
            selected.append((q, get_response(entry)))
        print(f"{variant}: {len(selected)} responses")

        qs = [q for q, _ in selected]
        rs = [r for _, r in selected]
        scores = ev.score_bulk(qs, rs, batch_size=args.batch_size) or []
        # Align by index; fill missing with a per-item absolute score.
        per_query = []
        for i, (q, r) in enumerate(selected):
            score = scores[i] if i < len(scores) else None
            if not score or score.get("correctness") is None:
                try:
                    single = ev.score_responses(q["query"], {"response": r})
                    score = (single or {}).get("response")
                except Exception:
                    score = None
            per_query.append(
                {
                    "id": q["id"],
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

        result[variant] = {
            "correctness": agg("correctness"),
            "precision": agg("precision"),
            "scientific_depth": agg("scientific_depth"),
            "per_query": per_query,
        }
        print(" ", {k: result[variant][k] for k in ("correctness", "precision", "scientific_depth")})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
