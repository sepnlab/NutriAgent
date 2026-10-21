"""Merge the NutriAgent and baseline expert sheets into one blinded sheet.

The default exporter writes `expert_eval_nutriagent.csv` and
`expert_eval_baselines.csv` separately, which tells the rater which responses
come from the proposed system. This script assigns the system a seventh
anonymous label, merges both files, and shuffles responses within each query so
the rater cannot infer the condition from row position or file membership.

Usage:
    python scripts/paper/build_blinded_expert_sheet.py logs/comp_layer_...
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
    parser.add_argument("log_dir", type=Path)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()

    log_dir = args.log_dir
    nutri = pd.read_csv(log_dir / "expert_eval_nutriagent.csv")
    base = pd.read_csv(log_dir / "expert_eval_baselines.csv")
    base_map = json.loads((log_dir / "expert_eval_anon_map.json").read_text(encoding="utf-8"))

    # The system gets the seventh anonymous label, not a descriptive one.
    used = set(base_map.values())
    labels = [f"Model_{c}" for c in "ABCDEFG"]
    system_label = next(c for c in labels if c not in used)
    nutri.insert(5, "model_id", system_label)

    merged = pd.concat([nutri, base], ignore_index=True)
    # Keep the original response order out of the row order.
    rng = random.Random(args.seed)
    merged = merged.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    merged = merged.sort_values(["query_id"], kind="stable").reset_index(drop=True)
    # Shuffle within each query so the anonymous labels are not in a fixed order.
    parts = []
    for _, group in merged.groupby("query_id", sort=False):
        parts.append(group.sample(frac=1.0, random_state=rng.randint(0, 10**9)))
    merged = pd.concat(parts, ignore_index=True)

    out = log_dir / "expert_eval_all.csv"
    merged.to_csv(out, index=False, encoding="utf-8")

    mapping = dict(base_map)
    mapping[system_label] = "NutriAgent"
    (log_dir / "expert_eval_all_map.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    counts = merged.groupby("query_id")["model_id"].nunique()
    print(f"wrote {out} rows={len(merged)} queries={merged['query_id'].nunique()}")
    print(f"system label={system_label}; models per query: min={counts.min()} max={counts.max()}")
    print("labels:", ", ".join(f"{k}={v}" for k, v in sorted(mapping.items())))


if __name__ == "__main__":
    main()
