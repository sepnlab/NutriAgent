"""Build the 195-query candidate pool from the four source files."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("queries/layer")
FILES = [
    "evaluation_queries.json",
    "evaluation_queries_advanced.json",
    "evaluation_queries_chinese.json",
    "evaluation_queries_chinese_advanced.json",
]
OUT = ROOT / "evaluation_queries_pool195.json"

merged: dict[str, list[dict]] = {}
seen: set[str] = set()
for fname in FILES:
    data = json.loads((ROOT / fname).read_text(encoding="utf-8"))
    for cat, items in data.items():
        key = f"{cat} [{fname.replace('evaluation_queries', '').strip('_').replace('.json', '') or 'base'}]"
        for q in items:
            qid = q.get("id") or q.get("query", "")[:30]
            if qid in seen:
                continue
            seen.add(qid)
            merged.setdefault(key, []).append(q)

OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
n = sum(len(v) for v in merged.values())
print("wrote", OUT, "queries", n, "categories", len(merged))
for k, v in merged.items():
    print(f"  {k}: {len(v)}")
