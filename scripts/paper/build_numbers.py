"""Build the single numbers ledger for the Rev.1 manuscript.

Every headline number in the manuscript must be traceable to one entry here.
The script reads the audit artifacts (data completeness, agreement, and an
optional evaluation report) and emits `docs/paper/audit/numbers.yaml`.

Usage:
    python scripts/paper/build_numbers.py
    python scripts/paper/build_numbers.py --report logs/<rev1>/report.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT_DIR = PROJECT_ROOT / "docs" / "paper" / "audit"
DEFAULT_REPORT = PROJECT_ROOT / "logs" / "comp_layer_20260612_183548" / "report.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report_section(report: dict) -> dict:
    methods = {}
    for key, value in report.items():
        if key == "_cost":
            continue
        methods[key] = {
            "correctness": value.get("correctness"),
            "precision": value.get("precision"),
            "scientific_depth": value.get("scientific_depth"),
            "overall": value.get("overall_weighted_score"),
            "inconsistency": value.get("inconsistency")
            or value.get("hallucination"),
            "flesch": value.get("flesch_reading_ease"),
            "tolerance_p2": value.get("tolerance_p2"),
            "tolerance_p5": value.get("tolerance_p5"),
            "faithfulness_numeric": value.get("faithfulness"),
            "faithfulness_semantic": value.get("faithfulness_semantic"),
        }
    cost = {
        key: value
        for key, value in report.get("_cost", {}).items()
        if key != "_total"
    }
    return {"methods": methods, "cost": cost}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-audit", default=str(AUDIT_DIR / "data_audit.json")
    )
    parser.add_argument(
        "--agreement", default=str(AUDIT_DIR / "agreement_report.json")
    )
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--out", default=str(AUDIT_DIR / "numbers.yaml"))
    args = parser.parse_args()

    data_audit = _load_json(Path(args.data_audit))
    agreement = _load_json(Path(args.agreement))
    report_path = Path(args.report)
    report = _load_json(report_path) if report_path.exists() else {}

    dataset = {}
    for name, ds in data_audit["datasets"].items():
        dataset[name] = {
            "rows": ds["rows"],
            "n_parameters": ds.get("n_parameters"),
            "nominal_cells": ds.get("nominal_cells"),
            "present_cells": ds.get("present_cells"),
            "completeness": ds.get("completeness"),
            "n_breeds": ds.get("n_breeds"),
            "n_phase_labels": ds.get("n_phase_labels"),
            "file": ds["file"],
        }

    ledger = {
        "meta": {
            "paper": "AGRCOM-D-26-00673",
            "manuscript": "NutriAgent",
            "generated_at": data_audit["generated_at"],
            "sources": {
                "data_audit": str(Path(args.data_audit).relative_to(PROJECT_ROOT)),
                "agreement": str(Path(args.agreement).relative_to(PROJECT_ROOT)),
                "report": str(report_path.relative_to(PROJECT_ROOT))
                if report_path.exists()
                else None,
            },
            "rule": "Every number in the manuscript must match an entry here.",
        },
        "dataset": dataset,
        "totals": data_audit["totals"],
        "queries": {
            "n_total": data_audit["queries"]["n_queries"],
            "by_language": data_audit["queries"]["by_language"],
            "by_type": data_audit["queries"]["by_type"],
            "by_category": data_audit["queries"]["by_category"],
            "n_expected_value": data_audit["queries"]["n_expected_value"],
            "n_expected_behavior": data_audit["queries"]["n_expected_behavior"],
            "zh_breed_mentions": data_audit["queries"]["zh_breed_mentions"],
        },
        "agreement": agreement.get("agreement", {}),
        "paired_vs_baselines": agreement.get("paired_vs_baselines", {}),
        "second_rater": agreement.get("second_rater"),
        "evaluation": build_report_section(report) if report else None,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        yaml.safe_dump(ledger, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    print(f"wrote {out}")
    print(
        f"datasets={len(dataset)} queries={ledger['queries']['n_total']} "
        f"agreement_entries={len(ledger['agreement'])} "
        f"methods={len(ledger['evaluation']['methods']) if report else 0}"
    )


if __name__ == "__main__":
    main()
