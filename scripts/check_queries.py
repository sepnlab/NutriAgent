"""Check query files and existing ablation queries."""
import json, os

for species in ["broiler", "layer"]:
    fpath = f"queries/{species}/evaluation_queries_curated.json"
    if os.path.exists(fpath):
        d = json.load(open(fpath, encoding="utf-8"))
        if isinstance(d, list):
            print(f"{fpath}: {len(d)} queries (list)")
        elif isinstance(d, dict):
            ks = list(d.keys())[:5]
            if "queries" in d:
                print(f"{fpath}: {len(d['queries'])} queries (dict with queries key)")
            else:
                print(f"{fpath}: dict with keys {ks}")
    else:
        print(f"{fpath}: NOT FOUND")

# Check what the existing ablation has
d = json.load(open("logs/v1_ablation_1782715425/responses.json", encoding="utf-8"))
print(f"\nExisting ablation: {len(d['queries'])} queries")
from collections import Counter
types = Counter(q.get("type","") for q in d["queries"])
print(f"Types: {dict(types)}")
# Show ID range
ids = [q["id"] for q in d["queries"]]
print(f"IDs: {ids[:3]} ... {ids[-3:]}")
# Check for layer IDs
layer_ids = [q["id"] for q in d["queries"] if q["id"].startswith("L-")]
print(f"Layer queries: {len(layer_ids)}")
print(f"Layer ID examples: {layer_ids[:5]}")
