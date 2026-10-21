"""Convert ReAct baseline results into the standard responses.json format
compatible with main.py --score-from.
"""
import json
import os
from datetime import datetime

LOG_DIR = f"logs/react_eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(LOG_DIR, exist_ok=True)

all_per_query = []
for species in ("broiler", "layer"):
    in_p = f"logs/react_{species}_clean.json"
    with open(in_p, encoding="utf-8") as f:
        data = json.load(f)
    all_per_query.extend(data["per_query"])

queries = [
    {
        "id": r["query_id"],
        "query": r["query"],
        "category": r["category"],
        "type": r["query_type"],
        "species": r.get("species", ""),
    }
    for r in all_per_query
]
responses = {
    "ReAct-Baseline": [r["response"] for r in all_per_query]
}

out = {"queries": queries, "responses": responses}

with open(os.path.join(LOG_DIR, "responses.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

with open(os.path.join(LOG_DIR, "config.yaml"), "w", encoding="utf-8") as f:
    f.write(f"method: ReAct-Baseline (k=3, max_iter=3)\nspecies: both\nqueries: {len(queries)}\n")

print(f"Wrote {len(queries)} queries to {LOG_DIR}/responses.json")
print(f"Now run: python main.py --score-from {LOG_DIR}")
