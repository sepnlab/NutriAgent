"""Correct incomplete/ambiguous query metadata found in the 54-query audit.

Text is left unchanged so the generated responses still correspond; the
clarification is recorded in expected_behavior and in the expert package's
query_note column.
"""

import json
from pathlib import Path

P = Path("queries/layer/evaluation_queries_curated.json")
data = json.loads(P.read_text(encoding="utf-8"))

OVERRIDES = {
    "C-XD-005": {
        "expected_value": 4.33,
        "expected_unit": "percentage points",
        "expected_behavior": "Assume the remaining 40% is SBM48; original SBM48 40% -> 44.33%, increase 4.33 pp.",
        "review": "multi-hop; original formula 60% maize + 40% SBM48; answer is +4.33 pp",
    },
    "C-XD-006": {
        "expected_value": 1.45,
        "expected_unit": "percentage points (decrease)",
        "expected_behavior": "New CP contribution 11.70%; change is a decrease of 1.45 pp (13.15 -> 11.70).",
        "review": "arithmetic: report the change, not the new contribution",
    },
    "C-FIB-004": {"expected_behavior": "Maize 3090 kcal/kg; soft wheat 2860 kcal/kg; maize higher by 230 kcal/kg."},
    "C-FIB-005": {"expected_behavior": "SBM48 52.6%; canola meal 41.0%; SBM48 higher by 11.6 pp."},
    "C-FIB-010": {"expected_behavior": "SBM48 2260 kcal/kg; rapeseed meal 1450 kcal/kg; SBM48 higher by 810 kcal/kg; MJ/kg conversions accepted."},
    "C-PM-005": {"expected_behavior": "Week 5 370 g; week 10 894.5 g; week 15 1307.5 g."},
    "C-PM-011": {"expected_behavior": "Jingfen 6 week 30: hen-day 95.5%; egg weight 55.0 g."},
    "C-FIB-006": {"expected_behavior": "Any three plant-protein sources with CP>30; e.g. SBM48 52.6%, canola 41.0%, rapeseed 38.1%."},
    "C-FIB-007": {"expected_behavior": "Maize Lys SID 90%, SBM48 88%; absolute SID Lys 1.89 vs 22.26 g/kg; SBM contributes more."},
    "C-NR-006": {"expected_behavior": "Developer 1.01%; Pre-Lay 2.52%; Lay I 4.04%; Lay II 4.24%; Lay III 4.44%."},
    "C-NR-004": {"expected_behavior": "Lay I 4.04%; Lay III 4.44%; Lay III higher by 0.40 pp."},
    "C-NR-005": {"expected_behavior": "ISA Brown 4.04%; Dawu Jinfeng 3.90%; ISA higher by 0.14 pp."},
    "C-NR-011": {"expected_behavior": "Lay I 3.90%; Lay III 4.20%; increase 0.30 pp."},
    "C-PM-003": {"expected_behavior": "ISA 95.5%; Hy-Line 95.7%; Hy-Line higher by 0.2 pp."},
    "C-PM-004": {"expected_behavior": "ISA 112 g/d; Hy-Line 113 g/d; Hy-Line higher by 1 g/d."},
    "C-PM-010": {"expected_behavior": "Jingfen 6 95.5%; Hy-Line 95.7%; Hy-Line higher by 0.2 pp."},
    "C-XD-001": {"expected_behavior": "SID Lys 0.27%; requirement 0.77%; does not meet."},
    "C-XD-003": {"expected_behavior": "9% x 35% = 3.15% Ca; below 4.04%; does not meet."},
    "C-XD-004": {"expected_behavior": "SID Lys 0.286%; requirement 0.77%; does not meet."},
    "C-XD-009": {"expected_behavior": "SID Lys 0.27%; requirement 0.76%; does not meet."},
    "C-EC-005": {"expected_behavior": "Fish meal 3180 kcal/kg; limestone 0 kcal/kg; fish meal higher; limestone is a mineral."},
}

changed = 0
for items in data.values():
    for q in items:
        if q["id"] in OVERRIDES:
            q.update(OVERRIDES[q["id"]])
            changed += 1

P.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("updated", changed, "queries")
