"""E15: entity-resolution perturbation test for the feed-ingredient tool.

The feed tool uses a case-insensitive substring index and silently returns the
first matching row. This test quantifies resolution and family-level correctness
for exact names, commodity short names, case/whitespace variants, misspellings,
Chinese aliases, and ambiguous families.

Usage:
    python scripts/paper/e15_entity_resolution.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "e15_entity_resolution.json"
BANK = PROJECT_ROOT / "corpus" / "shared" / "feed_ingredient_bank.csv"
ALIASES = PROJECT_ROOT / "corpus" / "shared" / "ingredient_alias.csv"


def family(name: str) -> str:
    return str(name).split(",")[0].strip().lower()


def build_cases() -> list[dict]:
    bank = pd.read_csv(BANK)
    names = [n for n in bank["Ingredient"].dropna().astype(str).tolist()]
    # Prefer recognizable commodity groups, keep the full canonical string.
    preferred = ["Maize", "Wheat", "Barley", "Limestone", "Soybean meal", "Fish meal", "Alfalfa"]
    exact = []
    for p in preferred:
        hit = next((n for n in names if n.startswith(p)), None)
        if hit:
            exact.append(hit)
    exact = exact[:8]

    cases = []
    for n in exact:
        cases.append({"input": n, "expected_family": family(n), "category": "exact_canonical"})
    for n in exact:
        cases.append({"input": family(n), "expected_family": family(n), "category": "commodity_short"})
    for n in exact[:4]:
        cases.append({"input": f"  {n.upper()}  ", "expected_family": family(n), "category": "case_whitespace"})

    misspellings = [
        ("maise", "maize"),
        ("soyabean meal", "soybean meal"),
        ("lime stone", "limestone"),
        ("wheatt", "wheat"),
        ("barleyy", "barley"),
        ("fishmeal", "fish meal"),
        ("soya meal", "soybean meal"),
        ("corn meal", "maize"),
    ]
    for text, fam in misspellings:
        cases.append({"input": text, "expected_family": fam, "category": "misspelling"})

    aliases = pd.read_csv(ALIASES)
    chinese = aliases[
        aliases["alias"].astype(str).str.contains(r"[\u4e00-\u9fff]", regex=True)
    ].drop_duplicates("alias").head(8)
    for _, row in chinese.iterrows():
        cases.append(
            {
                "input": str(row["alias"]),
                "expected_family": family(row["canonical_name"]),
                "category": "chinese_alias",
            }
        )

    for fam in ["soybean meal", "fish meal", "wheat", "barley", "maize"]:
        cases.append({"input": fam, "expected_family": fam, "category": "ambiguous_family"})

    return cases


def main() -> None:
    from src.tools.feed_ingredient_bank import FeedIngredientBankTool

    tool = FeedIngredientBankTool()
    rows = []
    for c in build_cases():
        out = tool._run(c["input"])
        resolved = out.startswith("Feed Ingredient:")
        got_family = family(out.split("Feed Ingredient:", 1)[1].splitlines()[0]) if resolved else None
        rows.append(
            {
                **c,
                "resolved": resolved,
                "got_family": got_family,
                "family_correct": bool(resolved and got_family == c["expected_family"]),
                "response_head": out.splitlines()[0][:120],
            }
        )

    by_cat = {}
    for cat in sorted({r["category"] for r in rows}):
        sub = [r for r in rows if r["category"] == cat]
        by_cat[cat] = {
            "n": len(sub),
            "resolved": round(sum(r["resolved"] for r in sub) / len(sub), 3),
            "family_correct": round(sum(r["family_correct"] for r in sub) / len(sub), 3),
        }

    summary = {
        "n_cases": len(rows),
        "resolved_rate": round(sum(r["resolved"] for r in rows) / len(rows), 3),
        "family_correct_rate": round(sum(r["family_correct"] for r in rows) / len(rows), 3),
        "by_category": by_cat,
    }
    OUT.write_text(json.dumps({"summary": summary, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# E15: entity-resolution perturbation test",
        "",
        f"Cases: {summary['n_cases']}; resolved {summary['resolved_rate']:.1%}; "
        f"family-correct {summary['family_correct_rate']:.1%}.",
        "",
        "| Category | n | Resolved | Family-correct |",
        "|---|---:|---:|---:|",
    ]
    for cat, s in by_cat.items():
        md.append(f"| {cat} | {s['n']} | {s['resolved']:.1%} | {s['family_correct']:.1%} |")
    md += ["", "## Failures", "", "| Input | Category | Expected | Got |", "|---|---|---|---|"]
    for r in rows:
        if not r["family_correct"]:
            md.append(f"| {r['input']} | {r['category']} | {r['expected_family']} | {r['got_family'] or 'not found'} |")
    OUT.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
