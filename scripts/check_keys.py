"""Check key structure mismatch."""
import json
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")

# Queries with B-/L- prefix
queries = []
for species, prefix in [("broiler", "B-"), ("layer", "L-")]:
    qfile = ROOT / "queries" / species / "evaluation_queries_curated.json"
    raw = json.loads(qfile.read_text(encoding="utf-8"))
    qs = raw if isinstance(raw, list) else raw.get("queries", [])
    for q in qs:
        if isinstance(q, dict):
            qid = q.get("id", "")
            if qid:
                queries.append(f"{prefix}{qid}")

print(f"Queries with B-/L- prefix: {len(queries)}")
print(f"First 3: {queries[:3]}")
print(f"Last 3: {queries[-3:]}")

# Responses
responses = json.loads((ROOT / "logs" / "v1_full_eval_1782331340" / "responses.json").read_text(encoding="utf-8"))
keys = list(responses.keys())
print(f"\nResponses: {len(responses)}")
print(f"First 3: {keys[:3]}")
print(f"Last 3: {keys[-3:]}")

# What prefix?
b_keys = [k for k in keys if k.startswith("B-")]
l_keys = [k for k in keys if k.startswith("L-")]
no_prefix = [k for k in keys if not k.startswith(("B-", "L-"))]
print(f"\nB-prefixed: {len(b_keys)}, L-prefixed: {len(l_keys)}, no-prefix: {len(no_prefix)}")
print(f"Last 3 no-prefix: {no_prefix[-3:]}")

# Matches
b_match = sum(1 for k in queries if k in responses)
no_prefix_q = [q for q in queries if not q.startswith(("B-", "L-"))]
l_match = sum(1 for k in no_prefix_q if k in responses)
print(f"\nMatches with B- prefix: {b_match}")
print(f"Matches without prefix: {l_match}")
