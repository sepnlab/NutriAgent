"""Merge both_off results into existing ablation responses.json."""
import json, os, shutil

EXISTING = "logs/v1_ablation_1782715425/responses.json"
BOTH_OFF = "logs/both_off_raw.json"

d = json.load(open(EXISTING, encoding="utf-8"))
bo = json.load(open(BOTH_OFF, encoding="utf-8"))

# Verify query order matches
for i, (eq, bq) in enumerate(zip(d["queries"], bo["queries"])):
    if eq["query"] != bq["query"]:
        print(f"MISMATCH at {i}: {eq.get('id','?')} vs {bq.get('id','?')}")
        print(f"  existing: {eq['query'][:60]}")
        print(f"  both_off: {bq['query'][:60]}")
        exit(1)

print(f"All {len(d['queries'])} queries match. Adding both_off...")

# Add both_off responses
both_off_responses = []
for r in bo["results"]:
    both_off_responses.append(r["response"])

d["responses"]["NutriCHAT (both_off)"] = both_off_responses
print(f"New response keys: {list(d['responses'].keys())}")

# Backup original
shutil.copy2(EXISTING, EXISTING + ".bak")
print(f"Backup saved to {EXISTING}.bak")

# Save merged
with open(EXISTING, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f"Merged saved to {EXISTING}")
