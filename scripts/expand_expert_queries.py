"""
Expand expert evaluation from 36 to ~72 queries.

Strategy:
  1. Load the 36 already-scored queries from expert_v3_scores_remapped.json
  2. Load the full query pool (broiler + layer curated JSON files)
  3. For each of the 11 SV/AD sub-categories, add queries to reach target
  4. Rule: advanced types (multi-hop/constraint/counterfactual) -> AD;
     standard types: layer -> AD, broiler -> round-robin SV/AD per domain.

Output: v1/experiments/expert_validation/expanded_queries.json
"""

import json
import os
import sys
from collections import defaultdict, Counter

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# -- Paths ----------------------------------------------------------------
EXPERT_FILE = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expert_v3_scores_remapped.json",
)
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "v1", "experiments", "expert_validation",
    "expanded_queries.json",
)
BROILER_FILE = os.path.join(PROJECT_ROOT, "queries", "broiler", "evaluation_queries_curated.json")
LAYER_FILE = os.path.join(PROJECT_ROOT, "queries", "layer", "evaluation_queries_curated.json")
BROILER_ADV_FILE = os.path.join(PROJECT_ROOT, "queries", "broiler", "evaluation_queries_advanced.json")
LAYER_ADV_FILE = os.path.join(PROJECT_ROOT, "queries", "layer", "evaluation_queries_advanced.json")
BROILER_CN_FILE = os.path.join(PROJECT_ROOT, "queries", "broiler", "evaluation_queries_chinese.json")
LAYER_CN_FILE = os.path.join(PROJECT_ROOT, "queries", "layer", "evaluation_queries_chinese.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# -- Domain name -> abbreviation ------------------------------------------
DOMAIN_MAP = {
    "Feed Ingredient Bank": "FIB",
    "Nutrient Requirements": "NR",
    "Performance Management": "PM",
    "Definitions": "DEF",
    "Edge Cases": "EC",
    "Cross-Domain": "XD",
}

ADVANCED_TYPES = {"multi-hop", "constraint", "counterfactual"}


def load_curated_queries(filepath: str, species: str) -> list:
    """Load queries from a curated JSON file."""
    data = load_json(filepath)
    queries = []
    for section, qs in data.items():
        for q in qs:
            q["species"] = species
            q["source_file"] = os.path.basename(filepath)
            if "category" not in q:
                q["category"] = section
            if "type" not in q and "query_type" in q:
                q["type"] = q["query_type"]
            queries.append(q)
    return queries


def load_advanced_queries(filepath: str, species: str) -> list:
    """Load advanced query files (multi-hop, constraint, counterfactual)."""
    if not os.path.exists(filepath):
        return []
    data = load_json(filepath)
    SECTION_CATEGORY = {
        "Multi-hop Queries": "Cross-Domain",
        "Constraint Queries": "Cross-Domain",
        "Counterfactual Queries": "Cross-Domain",
        "Cross-validate Queries": "Cross-Domain",
        "Scenario Queries": "Cross-Domain",
        "Chinese Multi-Hop (Broiler)": "Cross-Domain",
        "Chinese Constraint (Broiler)": "Cross-Domain",
        "Chinese Counterfactual (Broiler)": "Cross-Domain",
        "Chinese Multi-Hop (Layer)": "Cross-Domain",
        "Chinese Constraint (Layer)": "Cross-Domain",
        "Chinese Counterfactual (Layer)": "Cross-Domain",
    }
    TYPE_MAP = {
        "Multi-hop": "multi-hop", "Constraint": "constraint",
        "Counterfactual": "counterfactual",
    }
    queries = []
    for section, qs in data.items():
        qtype = None
        for key, val in TYPE_MAP.items():
            if key.lower() in section.lower():
                qtype = val
                break
        qtype = qtype or "multi-hop"
        for q in qs:
            q["species"] = species
            q["source_file"] = os.path.basename(filepath)
            q["category"] = SECTION_CATEGORY.get(section, "Cross-Domain")
            q["type"] = q.get("type", qtype)
            queries.append(q)
    return queries


def load_chinese_queries(filepath: str, species: str) -> list:
    """Load Chinese query files."""
    if not os.path.exists(filepath):
        return []
    data = load_json(filepath)
    SECTION_CATEGORY = {
        "Chinese White-Feathered Broiler Performance": "Performance Management",
        "Chinese Yellow-Feathered Broiler Performance": "Performance Management",
        "Chinese Broiler Nutrient Requirements": "Nutrient Requirements",
        "Cross-Breed Comparison (Broiler)": "Performance Management",
        "Chinese Layer Performance": "Performance Management",
        "Chinese Layer Nutrient Requirements": "Nutrient Requirements",
        "Chinese Multi-Hop (Broiler)": "Cross-Domain",
        "Chinese Constraint (Broiler)": "Cross-Domain",
        "Chinese Counterfactual (Broiler)": "Cross-Domain",
    }
    queries = []
    for section, qs in data.items():
        cat = SECTION_CATEGORY.get(section, "Cross-Domain")
        for q in qs:
            q["species"] = species
            q["source_file"] = os.path.basename(filepath)
            q["category"] = cat
            q["type"] = q.get("type", "single-value")
            queries.append(q)
    return queries


# -- Sub-category assignment ----------------------------------------------
_svad_counter = {}


def assign_subcat(q: dict) -> str:
    """Assign a query to one of the 11 SV/AD sub-categories.

    - Advanced types -> AD-{domain}
    - Layer standard -> AD-{domain}
    - Broiler standard -> round-robin SV/AD per domain
    """
    domain = DOMAIN_MAP.get(q.get("category", ""), q.get("category", "Unknown")[:3].upper())
    qtype = q.get("type", "")
    species = q.get("species", "broiler")

    if qtype in ADVANCED_TYPES:
        return f"AD-{domain}"
    if species == "layer":
        return f"AD-{domain}"
    # Broiler standard: round-robin
    if domain not in _svad_counter:
        _svad_counter[domain] = 0
    _svad_counter[domain] += 1
    return f"AD-{domain}" if _svad_counter[domain] % 2 == 0 else f"SV-{domain}"


def get_key_variants(qid: str) -> list:
    """Generate possible expert-set key formats for dedup."""
    return [f"B-{qid}", qid, f"L-{qid}"]


def main():
    import locale
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

    # -- 1. Load already-scored expert queries ---------------------------
    expert_records = load_json(EXPERT_FILE)
    scored_keys = set(r["key"] for r in expert_records)
    print(f"Loaded {len(scored_keys)} already-scored unique keys from expert set")

    cat_unique = defaultdict(set)
    for r in expert_records:
        cat_unique[r["category"]].add(r["key"])

    print("Current distribution:")
    for c in sorted(cat_unique):
        print(f"  {c}: {len(cat_unique[c])} queries")
    print(f"  Total: {sum(len(v) for v in cat_unique.values())} unique queries\n")

    # -- 2. Load full query pool -----------------------------------------
    pool = []
    pool.extend(load_curated_queries(BROILER_FILE, "broiler"))
    pool.extend(load_curated_queries(LAYER_FILE, "layer"))
    pool.extend(load_advanced_queries(BROILER_ADV_FILE, "broiler"))
    pool.extend(load_advanced_queries(LAYER_ADV_FILE, "layer"))
    pool.extend(load_chinese_queries(BROILER_CN_FILE, "broiler"))
    pool.extend(load_chinese_queries(LAYER_CN_FILE, "layer"))

    print(f"Total pool: {len(pool)} queries")

    # -- 3. Dedup (keep species variants, remove true duplicates) --------
    seen = set()
    deduped_pool = []
    for q in pool:
        key = (q.get("id", ""), q.get("query", "").strip(), q.get("species", ""))
        if key not in seen:
            seen.add(key)
            deduped_pool.append(q)
    pool = deduped_pool
    print(f"After dedup: {len(pool)} queries")

    # -- 4. Filter out already-scored queries ----------------------------
    available = []
    skipped = 0
    for q in pool:
        qid = q.get("id", "")
        variants = get_key_variants(qid)
        if any(v in scored_keys for v in variants):
            skipped += 1
            continue
        available.append(q)

    print(f"Skipped (already scored): {skipped}")
    print(f"Available for expansion: {len(available)}\n")

    # -- 5. Group available queries by sub-category ----------------------
    avail_by_cat = defaultdict(list)
    for q in available:
        subcat = assign_subcat(q)
        avail_by_cat[subcat].append(q)

    print("Available queries per sub-category:")
    for c in sorted(avail_by_cat):
        sp = Counter(q["species"] for q in avail_by_cat[c])
        langs = Counter(q.get("language", "en") for q in avail_by_cat[c])
        print(f"  {c}: {len(avail_by_cat[c]):3d} queries (species={dict(sp)}, lang={dict(langs)})")

    # -- 6. Set targets --------------------------------------------------
    TARGETS = {
        "SV-FIB": 7, "SV-NR": 7, "SV-PM": 7,
        "SV-DEF": 6, "SV-EC": 6, "SV-XD": 6,
        "AD-FIB": 6, "AD-NR": 6, "AD-PM": 6,
        "AD-DEF": 6, "AD-XD": 6,
    }

    # -- 7. Select additional queries ------------------------------------
    selected = []
    selection_info = {}

    for subcat in sorted(TARGETS):
        needed = TARGETS[subcat]
        current_n = len(cat_unique.get(subcat, set()))
        to_add = needed - current_n
        if to_add <= 0:
            selection_info[subcat] = {"current": current_n, "target": needed,
                                       "to_add": 0, "selected": 0,
                                       "status": "already at target", "ids": []}
            continue

        candidates = avail_by_cat.get(subcat, [])
        candidates.sort(key=lambda q: (
            0 if q["species"] == "layer" else 1,
            0 if q.get("language") == "zh" else 1,
            q["id"],
        ))

        n_take = min(to_add, len(candidates))
        taken = candidates[:n_take]

        # Intra-category text dedup
        already_selected_texts = set()
        deduped_taken = []
        for q in taken:
            text_key = (q.get("id", ""), q.get("query", "").strip())
            if text_key not in already_selected_texts:
                already_selected_texts.add(text_key)
                deduped_taken.append(q)

        # Fill remaining slots from extra candidates
        if len(deduped_taken) < n_take:
            extra_needed = n_take - len(deduped_taken)
            for q in candidates[n_take:]:
                if extra_needed <= 0:
                    break
                text_key = (q.get("id", ""), q.get("query", "").strip())
                if text_key not in already_selected_texts:
                    already_selected_texts.add(text_key)
                    deduped_taken.append(q)
                    extra_needed -= 1

        # Stamp sub-category on each selected query at selection time
        for q in deduped_taken:
            q["sub_category"] = subcat
        selected.extend(deduped_taken)
        n_take = len(deduped_taken)

        selection_info[subcat] = {
            "current": current_n,
            "target": needed,
            "to_add": to_add,
            "selected": n_take,
            "available": len(candidates),
            "status": "full" if n_take == to_add else f"partial (only {len(candidates)} avail)",
            "species": dict(Counter(q["species"] for q in taken)),
            "language": dict(Counter(q.get("language", "en") for q in taken)),
            "ids": [q["id"] for q in deduped_taken],
        }

    # -- 8. Global text dedup --------------------------------------------
    seen_texts = set()
    truly_selected = []
    dedup_removed = 0
    for q in selected:
        text_key = (q.get("id", ""), q.get("query", "").strip())
        if text_key not in seen_texts:
            seen_texts.add(text_key)
            truly_selected.append(q)
        else:
            dedup_removed += 1

    if dedup_removed > 0:
        print(f"\nGlobal text dedup removed {dedup_removed} duplicates")
    selected = truly_selected

    # -- 9. Summary ------------------------------------------------------
    print("\n" + "=" * 65)
    print("SELECTION SUMMARY")
    print("=" * 65)
    total_selected = 0
    for c in sorted(selection_info):
        info = selection_info[c]
        total_selected += info["selected"]
        print(f"  {c}: {info['current']} -> {info['target']} "
              f"(+{info['selected']}/{info['to_add']}) [{info['status']}] "
              f"species={info.get('species', {})}")

    existing_36 = set()
    for r in expert_records:
        existing_36.add(r["key"])

    all_layer = sum(1 for q in selected if q["species"] == "layer")
    all_broiler = sum(1 for q in selected if q["species"] == "broiler")
    all_zh = sum(1 for q in selected if q.get("language") == "zh")
    all_en = sum(1 for q in selected if q.get("language") != "zh")

    print(f"\nSummary: {len(existing_36)} existing + {len(selected)} new queries selected")
    print(f"New: {all_layer} layer + {all_broiler} broiler, {all_zh} zh + {all_en} en")

    # -- 10. Save -----------------------------------------------
    output = {
        "metadata": {
            "description": "Expanded expert evaluation queries",
            "original_count": len(existing_36),
            "added_count": len(selected),
            "estimated_total": len(existing_36) + len(selected),
            "targets": TARGETS,
        },
        "selection_summary": selection_info,
        "selected_queries": selected,
    }
    save_json(OUTPUT_FILE, output)
    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
