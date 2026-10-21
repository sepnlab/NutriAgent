"""Generate supplementary data tables S1-S3 from the audit artifacts.

Outputs a markdown fragment with:
  Table S1  data schema and completeness
  Table S2  phase crosswalk (59 labels)
  Table S3  provenance summary (50 rows)

The fragment is inserted into `docs/paper/supplementary_material.md`.

Usage:
    python scripts/paper/build_supplement_data.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUDIT = PROJECT_ROOT / "docs" / "paper" / "audit" / "data_audit.json"
CROSSWALK = PROJECT_ROOT / "corpus" / "layer" / "phase_crosswalk.csv"
PROVENANCE = PROJECT_ROOT / "corpus" / "provenance.csv"
OUT = PROJECT_ROOT / "docs" / "paper" / "audit" / "supplement_data.md"


def table_s1() -> str:
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    lines = [
        "## Table S1. Data schema and completeness",
        "",
        "Nominal cells = rows × parameters. Populated cells count non-missing values; "
        "the difference is reported rather than hidden.",
        "",
        "| Module | File | Rows | Parameters | Nominal cells | Populated | Completeness | Fully empty parameters |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for name, ds in data["datasets"].items():
        if ds.get("no_params"):
            lines.append(
                f"| {ds['label']} | `{ds['file']}` | {ds['rows']} | — | — | — | — | — |"
            )
        else:
            empty = ", ".join(ds.get("fully_empty_columns", [])[:8])
            if len(ds.get("fully_empty_columns", [])) > 8:
                empty += ", …"
            lines.append(
                f"| {ds['label']} | `{ds['file']}` | {ds['rows']} | {ds['n_parameters']} | "
                f"{ds['nominal_cells']} | {ds['present_cells']} | {ds['completeness']:.1%} | "
                f"{empty or '—'} |"
            )
    lines += [
        "",
        "**Layer nutrient requirement parameters (20):** metabolizable energy; crude protein; "
        "calcium; available phosphorus; sodium; total lysine, methionine, methionine–cysteine, "
        "threonine, tryptophan, valine, arginine, isoleucine; SID coefficients for lysine, "
        "methionine, methionine–cysteine, threonine, tryptophan; choline; linoleic acid.",
        "",
        "**Layer production parameters (12):** hen-day production; egg weight; egg mass per hen "
        "per day; daily feed intake; feed per dozen eggs; feed per kg egg mass; body weight; "
        "mortality; shell breaking strength; Haugh unit; cumulative egg count; daily water intake.",
        "",
        "**Vitamin/mineral parameters (18):** vitamins A, D3, E, K3, B1, B2, B6, B12, niacin, "
        "pantothenic acid, folic acid, biotin; Fe, Cu, Zn, Mn, Se, I.",
        "",
    ]
    return "\n".join(lines)


def table_s2() -> str:
    df = pd.read_csv(CROSSWALK)
    lines = [
        "## Table S2. Phase crosswalk (original breeder labels → seven reference phases)",
        "",
        "Every original label is mapped explicitly. `mapping_type` is one of exact, within, "
        "boundary, semantic, composite, or ambiguous; composite and ambiguous labels are not "
        "forced into a single phase.",
        "",
        "| Original label | Reference phase | Mapping type | Breeds (nutrition) | Note |",
        "|---|---|---|---|---|",
    ]
    for _, r in df.iterrows():
        breeds = str(r["used_by_nutrition"]) if pd.notna(r["used_by_nutrition"]) else ""
        if len(breeds) > 70:
            breeds = breeds[:67] + "…"
        note = str(r["note"]) if pd.notna(r["note"]) else ""
        lines.append(
            f"| {r['phase_label']} | {r['standard_phase']} | {r['mapping_type']} | "
            f"{breeds or '—'} | {note or '—'} |"
        )
    lines.append("")
    return "\n".join(lines)


def table_s3() -> str:
    df = pd.read_csv(PROVENANCE)
    lines = [
        "## Table S3. Per-breed provenance summary",
        "",
        "Full machine-readable table with URLs, versions, access dates, and licenses: "
        "`corpus/provenance.csv`. `needs_primary_source` marks Chinese domestic rows that were "
        "compiled through jbzyw.com; `needs_version_and_url` marks breeder guides whose exact "
        "version still has to be recorded.",
        "",
        "| Dataset | Scope | Source label | Source type | Status |",
        "|---|---|---|---|---|",
    ]
    for _, r in df.iterrows():
        lines.append(
            f"| {r['dataset']} | {r['scope']} | {str(r['source_label'])[:70]} | "
            f"{r['source_type']} | {r['status']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    text = "\n".join([table_s1(), table_s2(), table_s3()])
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} ({len(text)} chars)")


if __name__ == "__main__":
    main()
