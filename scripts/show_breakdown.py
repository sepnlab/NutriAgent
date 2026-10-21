"""Show per-type breakdown for all ablation conditions."""
import csv

rows = []
with open("logs/v1_ablation_1782715425/breakdown.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["group"] == "query_type":
            rows.append(row)

# Print both_off rows
print("=== both_off ===")
for r in rows:
    if "both_off" in r["method"]:
        print(f"{r['category']:25s} C={r['correctness_mean']:>6s} P={r['precision_mean']:>6s} D={r['scientific_depth_mean']:>6s}")

print("\n=== full ===")
for r in rows:
    if "full" in r["method"] and "both_off" not in r["method"]:
        print(f"{r['category']:25s} C={r['correctness_mean']:>6s} P={r['precision_mean']:>6s} D={r['scientific_depth_mean']:>6s}")

print("\n=== no_graphrag ===")
for r in rows:
    if "no_graphrag" in r["method"]:
        print(f"{r['category']:25s} C={r['correctness_mean']:>6s} P={r['precision_mean']:>6s} D={r['scientific_depth_mean']:>6s}")

print("\n=== no_tools ===")
for r in rows:
    if "no_tools" in r["method"]:
        print(f"{r['category']:25s} C={r['correctness_mean']:>6s} P={r['precision_mean']:>6s} D={r['scientific_depth_mean']:>6s}")
