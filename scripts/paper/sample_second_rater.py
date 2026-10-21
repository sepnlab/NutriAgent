"""Sample the second-rater subset from the blinded expert sheet.

Design: two randomly selected responses per query (54 x 2 = 108), plus 12
additional responses sampled without replacement from the remainder, for 120.
The subset keeps the same anonymized columns as `expert_eval_all.csv`; the
second rater scores it independently.

Usage:
    python scripts/paper/sample_second_rater.py \
        --sheet logs/comp_layer_20261020_190019/expert_eval_all.csv \
        --out logs/comp_layer_20261020_190019/expert_eval_second_rater.csv
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import pandas as pd

SEED = 42


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sheet", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--n", type=int, default=120)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    df = pd.read_csv(args.sheet)
    rng = random.Random(args.seed)

    picked = []
    for _, group in df.groupby("query_id", sort=False):
        k = 2 if len(group) >= 2 else len(group)
        picked.extend(group.sample(n=k, random_state=rng.randint(0, 10**9)).index.tolist())

    remaining = [i for i in df.index if i not in set(picked)]
    extra = rng.sample(remaining, k=min(args.n - len(picked), len(remaining)))
    picked.extend(extra)

    subset = df.loc[picked].sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    out = args.out or args.sheet.with_name("expert_eval_second_rater.csv")
    subset.to_csv(out, index=False, encoding="utf-8")

    manifest = {
        "seed": args.seed,
        "n": len(subset),
        "n_queries": int(subset["query_id"].nunique()),
        "per_model": subset["model_id"].value_counts().to_dict(),
        "sheet": str(args.sheet),
        "out": str(out),
    }
    out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({k: manifest[k] for k in ("n", "n_queries", "per_model")}, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
