"""Add the rubric-v2 provenance column to the blinded expert sheets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

AUDIT = Path("docs/paper/audit")
FILES = ["expert_eval_all.csv", "expert_eval_second_rater.csv"]
COL = "provenance_(0-2_or_NA)"

for name in FILES:
    path = AUDIT / name
    df = pd.read_csv(path)
    if COL not in df.columns:
        df[COL] = ""
    df.to_csv(path, index=False, encoding="utf-8")
    print(name, df.shape, list(df.columns))
