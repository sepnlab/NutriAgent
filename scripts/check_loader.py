"""Check how query_loader works."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.query_loader import load_queries as ql

for species in ["broiler", "layer"]:
    fpath = f"queries/{species}/evaluation_queries_curated.json"
    qs = ql(queries_file=fpath, query_set="all")
    print(f"{species}: {len(qs)} queries")
    if qs:
        print(f"  First: {qs[0]['id']} - {qs[0]['query'][:40]}")
        print(f"  Keys: {list(qs[0].keys())}")

# Also check the dict structure directly
d = json.load(open("queries/broiler/evaluation_queries_curated.json", encoding="utf-8"))
total = 0
for cat, items in d.items():
    if isinstance(items, list):
        total += len(items)
        print(f"  Broiler category {cat}: {len(items)} queries")
    elif isinstance(items, dict):
        for subcat, subitems in items.items():
            total += len(subitems)
            print(f"  Broiler {cat}/{subcat}: {len(subitems)} queries")
print(f"Broiler total from dict: {total}")
