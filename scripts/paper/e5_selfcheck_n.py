"""E5: SelfCheckGPT-NLI N sensitivity (N = 5 / 10 / 20).

Runs the multi-N scorer on the NutriAgent responses from the E18 main-comparison
run, using one sample-generation pass per query (max N = 20) and slicing the
first N samples for each score. Outputs per-query scores and aggregates.

Usage:
    python scripts/paper/e5_selfcheck_n.py \
        --log-dir logs/comp_layer_20261020_190019 \
        --out docs/paper/audit/e5_selfcheck_n.json
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
    parser.add_argument("--out", default=str(PROJECT_ROOT / "docs" / "paper" / "audit" / "e5_selfcheck_n.json"))
    parser.add_argument("--model", default="NutriCHAT")
    parser.add_argument("--limit", type=int, default=0, help="0 = all queries; otherwise first N")
    args = parser.parse_args()

    from src.evaluation.selfcheck import SelfCheckGPT

    data = json.loads((Path(args.log_dir) / "responses.json").read_text(encoding="utf-8"))
    queries = data["queries"]
    model = next(m for m in data["models"] if args.model in m)
    responses = data["responses"][model]
    if args.limit:
        queries = queries[: args.limit]
        responses = responses[: args.limit]

    try:
        sc = SelfCheckGPT(device="cuda")
    except Exception:
        sc = SelfCheckGPT(device="cpu")

    rows = []
    for i, (q, r) in enumerate(zip(queries, responses), 1):
        scores = sc.compute_score_multi_n(r, query=q["query"], n_values=[5, 10, 20])
        rows.append({"id": q.get("id"), "type": q.get("type"), "scores": {str(k): v for k, v in scores.items()}})
        if i % 10 == 0:
            print(f"{i}/{len(queries)}", flush=True)

    summary = {}
    for n in (5, 10, 20):
        vals = [row["scores"][str(n)] for row in rows if row["scores"].get(str(n)) is not None]
        summary[str(n)] = {
            "mean": round(statistics.mean(vals), 4) if vals else None,
            "std": round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0,
            "n": len(vals),
        }

    def corr(a, b):
        import numpy as np

        pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
        if len(pairs) < 3:
            return None
        x, y = zip(*pairs)
        return round(float(np.corrcoef(x, y)[0, 1]), 4)

    n5 = [row["scores"].get("5") for row in rows]
    n10 = [row["scores"].get("10") for row in rows]
    n20 = [row["scores"].get("20") for row in rows]
    out = {
        "model": model,
        "n_queries": len(rows),
        "summary": summary,
        "pearson": {"5_vs_10": corr(n5, n10), "5_vs_20": corr(n5, n20), "10_vs_20": corr(n10, n20)},
        "rows": rows,
    }
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# E5: SelfCheckGPT-NLI N sensitivity",
        "",
        f"Model: {model}; queries: {len(rows)}.",
        "",
        "| N | Mean | SD | n |",
        "|---|---:|---:|---:|",
    ]
    for n, s in summary.items():
        md.append(f"| {n} | {s['mean']} | {s['std']} | {s['n']} |")
    md += ["", "Pearson correlations: " + ", ".join(f"{k} = {v}" for k, v in out["pearson"].items())]
    path.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "pearson": out["pearson"]}, indent=2))


if __name__ == "__main__":
    main()
