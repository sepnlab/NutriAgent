"""E3: evaluate the entity/attribute/unit-aware consistency validator.

Builds a labeled set of paired specialist statements:
  - conflict: same entity + attribute + basis, different values (> tolerance)
  - consistent: same value, or a unit-converted equivalent
  - distractor: different entity, different attribute, same specialist, or no
    confident entity match; the validator should stay silent

The validator is the production `extract_claims` + `compare_claims` pair.
Outputs `docs/paper/audit/e3_validator_eval.{json,md}`.

Usage:
    python scripts/paper/e3_validator_eval.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.validation import compare_claims, extract_claims  # noqa: E402

OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e3_validator_eval.json"
OUT_MD = PROJECT_ROOT / "docs" / "paper" / "audit" / "e3_validator_eval.md"


# (id, category, text_a, specialist_a, text_b, specialist_b, expected_conflict)
CASES = [
    # ---- true conflicts -------------------------------------------------
    ("C01", "conflict", "Limestone contains 35% calcium.", "feed",
     "Limestone contains 38% calcium.", "nutrition", True),
    ("C02", "conflict", "Maize contains 8.8% crude protein.", "feed",
     "Maize contains 9.6% crude protein.", "nutrition", True),
    ("C03", "conflict", "Soybean meal contains 44% crude protein.", "feed",
     "Soybean meal contains 48% crude protein.", "nutrition", True),
    ("C04", "conflict", "Lay I requires 4.04% calcium.", "nutrition",
     "Lay I requires 4.40% calcium.", "performance", True),
    ("C05", "conflict", "Limestone contains 0.02% phosphorus.", "feed",
     "Limestone contains 0.05% phosphorus.", "nutrition", True),
    ("C06", "conflict", "Hy-Line Brown Lay I requires 4.2% calcium.", "nutrition",
     "Hy-Line Brown Lay I requires 4.6% calcium.", "performance", True),
    ("C07", "conflict", "Maize metabolizable energy is 3350 kcal/kg.", "feed",
     "Maize metabolizable energy is 3100 kcal/kg.", "nutrition", True),
    ("C08", "conflict", "Soybean meal contains 2.9% lysine.", "feed",
     "Soybean meal contains 3.3% lysine.", "nutrition", True),
    ("C09", "conflict", "Wheat contains 12.0% crude protein.", "feed",
     "Wheat contains 13.0% crude protein.", "nutrition", True),
    ("C10", "conflict", "Fish meal contains 62% crude protein.", "feed",
     "Fish meal contains 66% crude protein.", "nutrition", True),
    ("C11", "conflict", "Limestone contains 350 g/kg calcium.", "feed",
     "Limestone contains 38% calcium.", "nutrition", True),
    ("C12", "conflict", "Maize metabolizable energy is 13.0 MJ/kg.", "feed",
     "Maize metabolizable energy is 3350 kcal/kg.", "nutrition", True),
    ("C13", "conflict", "Soybean meal contains 0.65% methionine.", "feed",
     "Soybean meal contains 0.72% methionine.", "nutrition", True),
    ("C14", "conflict", "Wheat contains 0.35% lysine.", "feed",
     "Wheat contains 0.40% lysine.", "nutrition", True),
    ("C15", "conflict", "Barley contains 11.0% crude protein.", "feed",
     "Barley contains 12.0% crude protein.", "nutrition", True),
    # ---- consistent / unit-converted -----------------------------------
    ("S01", "consistent", "Limestone contains 35% calcium.", "feed",
     "Limestone contains 35% calcium.", "nutrition", False),
    ("S02", "consistent", "Maize contains 8.8% crude protein.", "feed",
     "Maize contains 8.8% crude protein.", "nutrition", False),
    ("S03", "consistent", "Limestone contains 350 g/kg calcium.", "feed",
     "Limestone contains 35% calcium.", "nutrition", False),
    ("S04", "consistent", "Maize metabolizable energy is 3350 kcal/kg.", "feed",
     "Maize metabolizable energy is 3350 kcal/kg.", "nutrition", False),
    ("S05", "consistent", "Soybean meal contains 44% crude protein.", "feed",
     "Soybean meal contains 44% crude protein.", "nutrition", False),
    ("S06", "consistent", "Limestone contains 35% calcium.", "feed",
     "Limestone contains 35.5% calcium.", "nutrition", False),
    ("S07", "consistent", "Maize contains 8.8% crude protein.", "feed",
     "Maize contains 9.0% crude protein.", "nutrition", False),
    ("S08", "consistent", "Wheat contains 12.0% crude protein.", "feed",
     "Wheat contains 12.3% crude protein.", "nutrition", False),
    ("S09", "consistent", "Soybean meal contains 2.9% lysine.", "feed",
     "Soybean meal contains 2.95% lysine.", "nutrition", False),
    ("S10", "consistent", "Maize metabolizable energy is 14.0 MJ/kg.", "feed",
     "Maize metabolizable energy is 3350 kcal/kg.", "nutrition", False),
    ("S11", "consistent", "Limestone contains 0.02% phosphorus.", "feed",
     "Limestone contains 0.021% phosphorus.", "nutrition", False),
    ("S12", "consistent", "Fish meal contains 62% crude protein.", "feed",
     "Fish meal contains 63% crude protein.", "nutrition", False),
    # ---- distractors: must stay silent --------------------------------
    ("D01", "distractor", "Limestone contains 35% calcium.", "feed",
     "Oyster shell contains 38% calcium.", "nutrition", False),
    ("D02", "distractor", "Limestone contains 35% calcium.", "feed",
     "Limestone contains 0.02% phosphorus.", "nutrition", False),
    ("D03", "distractor", "Limestone contains 35% calcium.", "feed",
     "Limestone contains 38% calcium.", "feed", False),
    ("D04", "distractor", "Calcium is 35%.", "feed",
     "Calcium is 38%.", "nutrition", False),
    ("D05", "distractor", "Maize contains 8.8% crude protein.", "feed",
     "Wheat contains 9.6% crude protein.", "nutrition", False),
    ("D06", "distractor", "Lay I requires 4.04% calcium.", "nutrition",
     "Lay I requires 4.40% calcium.", "nutrition", False),
    ("D07", "distractor", "Maize contains 8.8% crude protein.", "feed",
     "Maize metabolizable energy is 3350 kcal/kg.", "nutrition", False),
    ("D08", "distractor", "Soybean meal contains 44% crude protein.", "feed",
     "Fish meal contains 48% crude protein.", "nutrition", False),
    ("D09", "distractor", "Hy-Line Brown Lay I requires 4.2% calcium.", "performance",
     "Hy-Line Brown Lay I requires 4.6% calcium.", "performance", False),
    ("D10", "distractor", "Crude protein is 44%.", "feed",
     "Crude protein is 48%.", "nutrition", False),
    ("D11", "distractor", "Limestone contains 35% calcium.", "feed",
     "Maize contains 0.02% calcium.", "nutrition", False),
    ("D12", "distractor", "Soybean meal contains 2.9% lysine.", "feed",
     "Soybean meal contains 44% crude protein.", "nutrition", False),
    ("D13", "distractor", "Maize metabolizable energy is 3350 kcal/kg.", "feed",
     "Maize metabolizable energy is 3200 kcal/kg.", "feed", False),
    ("D14", "distractor", "Limestone calcium 35% and phosphorus 0.02%.", "feed",
     "Limestone calcium 38% and phosphorus 0.05%.", "nutrition", False),
    # Alias resolution: corn/maize should be the same entity -> a conflict.
    ("A01", "conflict", "Corn contains 8.8% crude protein.", "feed",
     "Maize contains 9.6% crude protein.", "nutrition", True),
]


def evaluate() -> dict:
    rows = []
    for cid, cat, ta, sa, tb, sb, expected in CASES:
        ca = extract_claims(ta, sa)
        cb = extract_claims(tb, sb)
        result = compare_claims(ca + cb)
        predicted = bool(result.warnings)
        rows.append(
            {
                "id": cid,
                "category": cat,
                "expected_conflict": expected,
                "predicted_conflict": predicted,
                "correct": predicted == expected,
                "n_claims_a": len(ca),
                "n_claims_b": len(cb),
                "warnings": result.warnings,
                "compared_pairs": result.compared_pairs,
            }
        )

    tp = sum(1 for r in rows if r["expected_conflict"] and r["predicted_conflict"])
    fp = sum(1 for r in rows if not r["expected_conflict"] and r["predicted_conflict"])
    fn = sum(1 for r in rows if r["expected_conflict"] and not r["predicted_conflict"])
    tn = sum(1 for r in rows if not r["expected_conflict"] and not r["predicted_conflict"])
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = (2 * precision * recall / (precision + recall)) if precision and recall else None
    by_cat = {}
    for cat in sorted({r["category"] for r in rows}):
        sub = [r for r in rows if r["category"] == cat]
        by_cat[cat] = {
            "n": len(sub),
            "correct": sum(r["correct"] for r in sub),
            "accuracy": round(sum(r["correct"] for r in sub) / len(sub), 3),
        }

    return {
        "n_cases": len(rows),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 3) if precision is not None else None,
        "recall": round(recall, 3) if recall is not None else None,
        "f1": round(f1, 3) if f1 is not None else None,
        "accuracy": round(sum(r["correct"] for r in rows) / len(rows), 3),
        "by_category": by_cat,
        "errors": [
            {k: r[k] for k in ("id", "category", "expected_conflict", "predicted_conflict", "warnings")}
            for r in rows if not r["correct"]
        ],
        "cases": rows,
    }


def main() -> None:
    data = evaluate()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# E3: consistency validator evaluation",
        "",
        f"Cases: {data['n_cases']} (conflict {data['tp'] + data['fn']}, "
        f"consistent/distractor {data['tn'] + data['fp']}).",
        "",
        f"- Precision: {data['precision']}",
        f"- Recall: {data['recall']}",
        f"- F1: {data['f1']}",
        f"- Accuracy: {data['accuracy']}",
        "",
        "| Category | n | Correct | Accuracy |",
        "|---|---:|---:|---:|",
    ]
    for cat, s in data["by_category"].items():
        lines.append(f"| {cat} | {s['n']} | {s['correct']} | {s['accuracy']} |")
    if data["errors"]:
        lines += ["", "## Errors", "", "| ID | Category | Expected | Predicted | Warnings |", "|---|---|---|---|---|"]
        for e in data["errors"]:
            lines.append(
                f"| {e['id']} | {e['category']} | {e['expected_conflict']} | "
                f"{e['predicted_conflict']} | {'; '.join(e['warnings']) or '—'} |"
            )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: data[k] for k in ("n_cases", "precision", "recall", "f1", "accuracy")}, indent=2))
    print("errors:", [e["id"] for e in data["errors"]])


if __name__ == "__main__":
    main()
