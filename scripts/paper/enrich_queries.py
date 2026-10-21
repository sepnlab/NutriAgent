"""Attach retrieval/evaluation metadata to the curated 54-query set.

The manuscript's query descriptions are not sufficient to evaluate retrieval
quality or to reconcile the supplementary table with the benchmark (audit
finding F8). This script adds, for every query:

    breed   list of breeds/ingredients referenced (canonical corpus names)
    phase   production phase if the query names one
    unit    unit of the expected numerical answer
    target  corpus records needed to answer (dataset:entity[/phase])
    review  flag for queries that need human review (e.g. multi-hop)

The query text and expected values are not modified.

Usage:
    python scripts/paper/enrich_queries.py
    python scripts/paper/enrich_queries.py --check   # do not write
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"

SBM48 = "Soybean meal, oil < 5%, 48% protein + oil"

META: dict[str, dict] = {
    # ── Feed Ingredient Bank ────────────────────────────────
    "C-FIB-001": {"breed": ["Maize"], "unit": "%", "target": ["feed_ingredient_bank:Maize"]},
    "C-FIB-002": {"breed": ["Limestone"], "unit": "%", "target": ["feed_ingredient_bank:Limestone"]},
    "C-FIB-003": {"breed": [SBM48], "unit": "kcal/kg", "target": [f"feed_ingredient_bank:{SBM48}"]},
    "C-FIB-004": {
        "breed": ["Maize", "Wheat, soft"],
        "unit": "kcal/kg",
        "target": ["feed_ingredient_bank:Maize", "feed_ingredient_bank:Wheat, soft"],
    },
    "C-FIB-005": {
        "breed": [SBM48, "Canola meal, oil < 5%"],
        "unit": "%",
        "target": [f"feed_ingredient_bank:{SBM48}", "feed_ingredient_bank:Canola meal, oil < 5%"],
    },
    "C-FIB-006": {"breed": [], "unit": "%", "review": "open-ended; multiple ingredient records"},
    "C-FIB-007": {
        "breed": ["Maize", SBM48],
        "unit": "%",
        "target": ["feed_ingredient_digestibility:Maize", f"feed_ingredient_digestibility:{SBM48}"],
    },
    "C-FIB-008": {"breed": [], "unit": None, "target": ["definitions:metabolizable energy"]},
    "C-FIB-009": {"breed": ["Maize"], "unit": "%", "target": ["feed_ingredient_bank:Maize"]},
    "C-FIB-010": {
        "breed": [SBM48, "Rapeseed meal, oil < 5%"],
        "unit": "kcal/kg",
        "target": [f"feed_ingredient_bank:{SBM48}", "feed_ingredient_bank:Rapeseed meal, oil < 5%"],
    },
    # ── Nutrient Requirements ───────────────────────────────
    "C-NR-001": {"breed": ["ISA Brown"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I"]},
    "C-NR-002": {"breed": ["ISA Brown"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I"]},
    "C-NR-003": {"breed": ["Jinghong 1 v3.0"], "phase": "Layer I", "unit": "%", "target": ["nutrient_requirements:Jinghong 1 v3.0/Layer I"]},
    "C-NR-004": {"breed": ["ISA Brown"], "phase": "Lay I/Lay III", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I", "nutrient_requirements:ISA Brown/Lay III"]},
    "C-NR-005": {"breed": ["ISA Brown", "Dawu Jinfeng"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I", "nutrient_requirements:Dawu Jinfeng/Lay I"]},
    "C-NR-006": {"breed": ["ISA Brown"], "phase": "Developer-Lay III", "unit": "%", "review": "multi-phase trend", "target": ["nutrient_requirements:ISA Brown"]},
    "C-NR-007": {"breed": [], "unit": "%", "review": "arithmetic: total AA x SID coefficient"},
    "C-NR-008": {"breed": [], "unit": "%", "review": "arithmetic: total P / phytate P / phytase"},
    "C-NR-009": {"breed": [], "unit": None, "target": ["definitions:standardized ileal digestibility"]},
    "C-NR-010": {"breed": ["Dawu Jinfeng"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:Dawu Jinfeng/Lay I"]},
    "C-NR-011": {"breed": ["Dawu Jinfeng"], "phase": "Lay I-Lay III", "unit": "%", "target": ["nutrient_requirements:Dawu Jinfeng"]},
    "C-NR-012": {"breed": ["Dawu Jinfeng"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:Dawu Jinfeng/Lay I"]},
    # ── Production Performance ──────────────────────────────
    "C-PM-001": {"breed": ["ISA Brown"], "phase": "week 30", "unit": "%", "target": ["performance_management:ISA Brown/week 30"]},
    "C-PM-002": {"breed": ["Hy-Line Brown"], "phase": "week 30", "unit": "g", "target": ["performance_management:Hy-Line Brown/week 30"]},
    "C-PM-003": {"breed": ["ISA Brown", "Hy-Line Brown"], "phase": "week 30", "unit": "%", "target": ["performance_management:ISA Brown/week 30", "performance_management:Hy-Line Brown/week 30"]},
    "C-PM-004": {"breed": ["ISA Brown", "Hy-Line Brown"], "phase": "week 30", "unit": "g/d", "target": ["performance_management:ISA Brown/week 30", "performance_management:Hy-Line Brown/week 30"]},
    "C-PM-005": {"breed": ["ISA Brown"], "phase": "weeks 5/10/15", "unit": "g", "target": ["performance_management:ISA Brown/weeks 5,10,15"]},
    "C-PM-006": {"breed": ["ISA Brown"], "phase": "week 30", "unit": "mg/hen/day", "review": "multi-hop; combines performance and nutrient data", "target": ["performance_management:ISA Brown/week 30", "nutrient_requirements:ISA Brown/Lay I"]},
    "C-PM-007": {"breed": ["ISA Brown"], "phase": "week 30", "unit": "g/hen/day", "review": "arithmetic: HD% x egg weight", "target": ["performance_management:ISA Brown/week 30"]},
    "C-PM-008": {"breed": [], "unit": None, "target": ["definitions:hen-day egg production"]},
    "C-PM-009": {"breed": ["Jingfen 6"], "phase": "week 30", "unit": "%", "target": ["performance_management:Jingfen 6/week 30"]},
    "C-PM-010": {"breed": ["Jingfen 6", "Hy-Line Brown"], "phase": "week 30", "unit": "%", "target": ["performance_management:Jingfen 6/week 30", "performance_management:Hy-Line Brown/week 30"]},
    "C-PM-011": {"breed": ["Jingfen 6"], "phase": "week 30", "unit": "% / g", "target": ["performance_management:Jingfen 6/week 30"]},
    # ── Definitions ─────────────────────────────────────────
    "C-DEF-001": {"breed": [], "unit": None, "target": ["definitions:metabolizable energy", "definitions:digestible energy"]},
    "C-DEF-002": {"breed": [], "unit": None, "target": ["definitions:available phosphorus", "definitions:total phosphorus"]},
    "C-DEF-003": {"breed": [], "unit": None, "target": ["definitions:feed conversion ratio"]},
    "C-DEF-004": {"breed": [], "unit": "%", "review": "arithmetic: N x 6.25"},
    "C-DEF-005": {"breed": [], "unit": None, "target": ["definitions:metabolizable energy", "definitions:digestible energy"]},
    "C-DEF-006": {"breed": [], "unit": None, "target": ["definitions:metabolizable energy", "definitions:digestible energy"]},
    # ── Cross-Domain ────────────────────────────────────────
    "C-XD-001": {"breed": [], "phase": "Lay I", "unit": "%", "review": "multi-hop; diet formulation arithmetic"},
    "C-XD-002": {"breed": ["ISA Brown"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I", "feed_ingredient_bank:Limestone"]},
    "C-XD-003": {"breed": ["ISA Brown"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I", "feed_ingredient_bank:Limestone"]},
    "C-XD-004": {"breed": [], "phase": "Lay I", "unit": "%", "review": "multi-hop; diet formulation arithmetic"},
    "C-XD-005": {"breed": ["Maize"], "unit": "percentage points", "target": ["feed_ingredient_bank:Maize"]},
    "C-XD-006": {"breed": [SBM48, "Canola meal, oil < 5%"], "unit": "%", "target": [f"feed_ingredient_bank:{SBM48}", "feed_ingredient_bank:Canola meal, oil < 5%"]},
    "C-XD-007": {"breed": ["ISA Brown"], "phase": "week 30", "unit": "mg/hen/day", "target": ["nutrient_requirements:ISA Brown/Lay I", "performance_management:ISA Brown/week 30"]},
    "C-XD-008": {"breed": [], "unit": None, "review": "open-ended diet formulation; no single target record"},
    "C-XD-009": {"breed": ["Dawu Jinfeng"], "phase": "Lay I", "unit": "%", "review": "multi-hop; diet formulation arithmetic", "target": ["nutrient_requirements:Dawu Jinfeng/Lay I"]},
    "C-XD-010": {"breed": ["Dawu Jinfeng"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:Dawu Jinfeng/Lay I", "feed_ingredient_bank:Limestone"]},
    # ── Edge Cases ──────────────────────────────────────────
    "C-EC-001": {"breed": [], "unit": None, "review": "out-of-scope ingredient; expected refusal"},
    "C-EC-002": {"breed": ["Lohmann Tinted"], "unit": "%", "review": "breed not in corpus; expected clarification"},
    "C-EC-003": {"breed": ["ISA Brown"], "phase": "day 35", "unit": "g", "review": "broiler query against a layer corpus"},
    "C-EC-004": {"breed": ["ISA Brown"], "phase": "Lay I", "unit": "%", "target": ["nutrient_requirements:ISA Brown/Lay I"]},
    "C-EC-005": {"breed": ["Fish meal, protein 65%", "Limestone"], "unit": "kcal/kg", "target": ["feed_ingredient_bank:Fish meal, protein 65%", "feed_ingredient_bank:Limestone"]},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, do not write")
    args = parser.parse_args()

    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    all_ids = [q["id"] for items in data.values() for q in items]

    missing = sorted(set(all_ids) - set(META))
    extra = sorted(set(META) - set(all_ids))
    if missing or extra:
        raise SystemExit(f"metadata mismatch: missing={missing} extra={extra}")

    for items in data.values():
        for q in items:
            meta = META[q["id"]]
            q["breed"] = meta.get("breed", [])
            q["phase"] = meta.get("phase")
            q["expected_unit"] = meta.get("unit")
            q["target_doc"] = meta.get("target", [])
            q["review"] = meta.get("review")
            q["language"] = q.get("language", "en")

    if not args.check:
        QUERIES.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    n_review = sum(1 for items in data.values() for q in items if q.get("review"))
    n_target = sum(1 for items in data.values() for q in items if q.get("target_doc"))
    print(f"queries={len(all_ids)} with_target_doc={n_target} needs_review={n_review}")
    print("wrote" if not args.check else "checked", QUERIES)


if __name__ == "__main__":
    main()
