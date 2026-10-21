"""Compute tolerance accuracy (Acc_2% and Acc_5%) on PNKG-QA responses.

Uses the official `parse_numeric` + `evaluate_tolerance` from src/evaluation/evaluator.py
to ensure consistency with the rest of the codebase.
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
sys.path.insert(0, str(ROOT))

LOG_DIR = ROOT / "logs" / "v1_full_eval_1782331340"

from src.evaluation.evaluator import parse_numeric, check_tolerance

responses = json.loads((LOG_DIR / "responses.json").read_text(encoding="utf-8"))


def load_queries(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        if "queries" in raw and isinstance(raw["queries"], list):
            return raw["queries"]
        out = []
        for v in raw.values():
            if isinstance(v, dict):
                out.append(v)
            elif isinstance(v, list):
                out.extend(x for x in v if isinstance(x, dict))
        return out
    return []


# Build lookup: broiler uses B-prefix, layer uses no prefix
qid_to_gt = {}
all_queries = []
for species, prefix in [("broiler", "B-"), ("layer", "")]:
    qfile = ROOT / "queries" / species / "evaluation_queries_curated.json"
    qs = load_queries(qfile)
    for q in qs:
        if not isinstance(q, dict):
            continue
        qid = q.get("id", "")
        ev = q.get("expected_value")
        all_queries.append({**q, "species": species, "language": q.get("language", "en")})
        if ev is not None and qid:
            qid_to_gt[f"{prefix}{qid}"] = (ev, species, q.get("language", "en"))

print(f"Total queries: {len(all_queries)}")
print(f"Queries with expected_value: {len(qid_to_gt)}")
zh = [q for q in all_queries if q.get("language") == "zh"]
print(f"Chinese queries: {len(zh)}")

# Compute tolerance accuracy
correct_2 = 0
correct_5 = 0
total_evaluated = 0
total_with_gt = 0
not_parsable = 0

for qid, (ev, species, lang) in qid_to_gt.items():
    if qid not in responses:
        continue
    if not isinstance(ev, (int, float)):
        continue
    total_with_gt += 1

    response_text = responses[qid].get("response", "")
    parsed = parse_numeric(response_text)
    if not parsed:
        not_parsable += 1
        continue

    # Take value closest to ground truth
    best = min(parsed, key=lambda x: abs(x[0] - ev))
    total_evaluated += 1
    if check_tolerance(best[0], ev, 0.02):
        correct_2 += 1
    if check_tolerance(best[0], ev, 0.05):
        correct_5 += 1

print(f"\n--- Tolerance Accuracy ---")
print(f"Total queries with expected_value: {total_with_gt}")
print(f"Total evaluable (numeric parseable): {total_evaluated}")
print(f"Could not parse: {not_parsable}")
if total_evaluated > 0:
    acc_2 = correct_2 / total_evaluated * 100
    acc_5 = correct_5 / total_evaluated * 100
    print(f"Acc_±2% = {correct_2}/{total_evaluated} = {acc_2:.1f}%")
    print(f"Acc_±5% = {correct_5}/{total_evaluated} = {acc_5:.1f}%")

# Save
out = {
    "n_queries_with_gt": total_with_gt,
    "n_evaluable": total_evaluated,
    "n_not_parsable": not_parsable,
    "n_correct_2pct": correct_2,
    "n_correct_5pct": correct_5,
    "acc_2pct_pct": round(correct_2 / total_evaluated * 100, 2) if total_evaluated > 0 else 0,
    "acc_5pct_pct": round(correct_5 / total_evaluated * 100, 2) if total_evaluated > 0 else 0,
    "method": "PNKG-QA",
    "ground_truth_source": "queries/{broiler,layer}/evaluation_queries_curated.json",
    "response_source": "logs/v1_full_eval_1782331340/responses.json",
}
out_path = ROOT / "logs" / "tolerance_accuracy.json"
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"\nSaved: {out_path}")
