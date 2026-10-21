"""
Merge original 36 human expert scores + 26 simulated expert scores
into a single file compatible with calc_weighted_kappa.py.

Output: v1/experiments/expert_validation/expert_combined_scores.json
"""

import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

ORIGINAL = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                         "expert_v3_scores_remapped.json")
SIMULATED = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                          "expert_simulated_scores.json")
RESPONSES = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                          "expanded_responses.json")
OUTPUT = os.path.join(PROJECT_ROOT, "v1", "experiments", "expert_validation",
                       "expert_combined_scores.json")


def main():
    with open(ORIGINAL, "r", encoding="utf-8") as f:
        original = json.load(f)

    with open(SIMULATED, "r", encoding="utf-8") as f:
        simulated = json.load(f)

    # Convert simulated entries to match original format
    new_entries = []
    for r in simulated:
        entry = {
            "key": r["key"],
            "category": r.get("category", ""),
            "query": r["query"],
            "evaluator_correctness": None,  # Would need separate EvaluatorLLM run
            "evaluator_precision": None,
            "evaluator_scientific_depth": None,
            "expert_name": r["expert_name"],
            "expert_model": r["expert_model"],
            "latency_s": None,
            "expert": {
                "correctness": r["expert"]["correctness"],
                "precision": r["expert"]["precision"],
                "scientific_depth": r["expert"]["scientific_depth"],
                "justification": r["expert"].get("justification", ""),
            }
        }
        new_entries.append(entry)

    # Combine
    combined = original + new_entries
    print(f"Original entries: {len(original)}")
    print(f"New entries: {len(new_entries)}")
    print(f"Combined: {len(combined)}")

    # Count unique keys
    orig_keys = set(r["key"] for r in original)
    new_keys = set(r["key"] for r in new_entries)
    total_keys = orig_keys | new_keys
    overlap = orig_keys & new_keys
    print(f"Original unique keys: {len(orig_keys)}")
    print(f"New unique keys: {len(new_keys)}")
    print(f"Overlap: {len(overlap)}")
    print(f"Total unique keys: {len(total_keys)}")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
