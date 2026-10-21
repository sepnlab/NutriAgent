"""
Export expert scoring sheets for the expanded expert evaluation.

Generates:
  1. expert_scoring_sheet.csv — for human experts (26 new queries only)
  2. expert_scoring_template.json — JSON template for programmatic use

Usage:
    python scripts/export_expert_scoring_sheets.py
"""

import csv
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# ── Paths ────────────────────────────────────────────────────────────────
EXPANDED_QUERIES = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expanded_queries.json",
)
EXPANDED_RESPONSES = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expanded_responses.json",
)
EXISTING_SCORES = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expert_v3_scores_remapped.json",
)
OUTPUT_CSV = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expert_scoring_sheet.csv",
)
OUTPUT_JSON = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expert_scoring_template.json",
)


def main():
    # ── 1. Load data ──
    with open(EXPANDED_QUERIES, "r", encoding="utf-8") as f:
        queries_data = json.load(f)
    with open(EXPANDED_RESPONSES, "r", encoding="utf-8") as f:
        responses = json.load(f)

    # Build response lookup by key
    resp_by_key = {r["key"]: r for r in responses}

    # Build lookup for already-scored keys
    already_scored = set()
    if os.path.exists(EXISTING_SCORES):
        with open(EXISTING_SCORES, "r", encoding="utf-8") as f:
            existing = json.load(f)
        already_scored = set(r["key"] for r in existing)

    selected = queries_data["selected_queries"]

    # ── 2. Build scoring rows (new queries only) ──
    rows = []
    for q in selected:
        qid = q["id"]
        resp = resp_by_key.get(qid, {})

        # Sub-category stamped on the query object at selection time
        subcat = q.get("sub_category", "")

        # Check if already scored
        key_variants = [qid, f"B-{qid}", f"L-{qid}"]
        is_scored = any(k in already_scored for k in key_variants)

        rows.append({
            "query_id": qid,
            "sub_category": subcat or "",
            "species": q["species"],
            "language": q.get("language", "en"),
            "query": q["query"],
            "response": resp.get("response", ""),
            "already_scored": "YES" if is_scored else "",
            # Scoring columns (to be filled by expert)
            "correctness": "",
            "precision": "",
            "scientific_depth": "",
            "justification": "",
        })

    # Sort: unscored first, then by species, then by id
    rows.sort(key=lambda r: (
        r["already_scored"],  # unscored first
        0 if r["species"] == "broiler" else 1,
        r["query_id"],
    ))

    # ── 3. Write CSV ──
    fieldnames = [
        "query_id", "sub_category", "species", "language",
        "query", "response",
        "already_scored", "correctness", "precision",
        "scientific_depth", "justification",
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    unscored_count = sum(1 for r in rows if not r["already_scored"])
    print(f"CSV saved: {OUTPUT_CSV}")
    print(f"  Total rows: {len(rows)}")
    print(f"  Already scored (reference): {len(rows) - unscored_count}")
    print(f"  Need expert scoring: {unscored_count}")

    # ── 4. Write JSON template ──
    template = []
    for r in rows:
        template.append({
            "key": r["query_id"],
            "category": r["sub_category"],
            "species": r["species"],
            "language": r["language"],
            "query": r["query"],
            "response": r["response"],
            "expert": {
                "correctness": None,
                "precision": None,
                "scientific_depth": None,
                "justification": "",
            },
            "already_scored": bool(r["already_scored"]),
        })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    print(f"JSON template saved: {OUTPUT_JSON}")

    # ── 5. Print summary statistics ──
    print("\n--- Query Summary ---")
    by_cat = {}
    for r in rows:
        cat = r["sub_category"] or "Unknown"
        if cat not in by_cat:
            by_cat[cat] = {"total": 0, "unscored": 0, "broiler": 0, "layer": 0, "zh": 0, "en": 0}
        by_cat[cat]["total"] += 1
        if not r["already_scored"]:
            by_cat[cat]["unscored"] += 1
        by_cat[cat][r["species"]] += 1
        by_cat[cat][r["language"]] += 1

    for cat in sorted(by_cat):
        info = by_cat[cat]
        print(f"  {cat}: {info['total']:2d} queries "
              f"(need scoring: {info['unscored']:2d}, "
              f"broiler={info['broiler']} layer={info['layer']}, "
              f"zh={info['zh']} en={info['en']})")


if __name__ == "__main__":
    main()
