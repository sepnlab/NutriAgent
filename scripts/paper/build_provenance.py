"""Build a field-level provenance table for the layer corpus.

The manuscript describes the data as sourced from "official breed management
guides" and, for Chinese domestic strains, from jbzyw.com (an aggregation
platform). The corpus `source` column, however, labels every breed row as
"<Breed> Official Manual", which conflates primary breeder documents with
aggregator pages (audit finding F9; reviewer comments R2.20, R3.12, R4).

This script makes the distinction explicit and records what is still missing
(version/date/URL/license), so the revision can publish an honest provenance
table instead of an unsupported claim.

Output: corpus/provenance.csv
Usage:
    python scripts/paper/build_provenance.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS = PROJECT_ROOT / "corpus"
OUT = CORPUS / "provenance.csv"

INTERNATIONAL = {
    "Hy-Line W-36",
    "Hy-Line Brown",
    "Hy-Line Pink",
    "ISA Brown",
    "Lohmann Grey",
    "Lohmann Pink",
    "Hisex Brown",
}

CHINESE = {
    "Jingfen 6",
    "Jinghong 1 v3.0",
    "Jingbai 939",
    "Dawu Jinfeng",
    "Dawu He",
    "Dawu Fen 1",
    "Nongda 3",
    "Nongda 6",
    "Beinong 1",
    "Beinong 2",
}

# Dataset-level source metadata (to be completed with author-provided details).
DATASET_META = {
    "feed_ingredient_bank.csv": {
        "source_type": "public_feed_table",
        "document": "INRAE-CIRAD-AFZ feed tables (feedtables.com)",
        "url": "https://feedtables.com/",
        "status": "needs_license_check",
        "note": "CVB feed table is also cited in the manuscript but is not recorded in the `source` column.",
    },
    "feed_ingredient_amino_acids.csv": {
        "source_type": "public_feed_table",
        "document": "INRAE-CIRAD-AFZ feed tables (feedtables.com)",
        "url": "https://feedtables.com/",
        "status": "needs_license_check",
        "note": "",
    },
    "feed_ingredient_digestibility.csv": {
        "source_type": "public_feed_table",
        "document": "INRAE-CIRAD-AFZ feed tables (feedtables.com)",
        "url": "https://feedtables.com/",
        "status": "needs_license_check",
        "note": "",
    },
    "definitions.csv": {
        "source_type": "unspecified",
        "document": "Compiled from textbooks / industry guidelines (per manuscript)",
        "url": "",
        "status": "needs_author_input",
        "note": "All 556 rows carry `source=other-Sourced`; per-entry attribution is missing.",
    },
}

LAYER_FILES = [
    "nutrient_requirements.csv",
    "nutrient_vitamin_mineral.csv",
    "performance_management.csv",
]


def layer_rows(filename: str) -> list[dict]:
    path = CORPUS / "layer" / filename
    df = pd.read_csv(path)
    rows = []
    for (breed, source), group in df.groupby(["Breed", "source"], dropna=False):
        if breed in INTERNATIONAL:
            source_type = "breeder_management_guide"
            document = f"{breed} management guide"
            url = ""
            status = "needs_version_and_url"
            note = "Breeder/company document; version and URL must be supplied."
        elif breed in CHINESE:
            source_type = "aggregator_mirror"
            document = f"{breed} specifications via jbzyw.com (aggregator)"
            url = "https://www.jbzyw.com/"
            status = "needs_primary_source"
            note = (
                "The corpus labels this row 'Official Manual', but the manuscript "
                "states Chinese data were compiled through jbzyw.com. The primary "
                "breeder/technical document, version and extraction date are missing."
            )
        else:
            source_type = "unknown"
            document = str(source)
            url = ""
            status = "needs_author_input"
            note = "Breed not in the international/Chinese lists."

        rows.append(
            {
                "dataset": filename,
                "scope": breed,
                "n_records": len(group),
                "source_label": str(source),
                "source_type": source_type,
                "document_title": document,
                "version_or_date": "",
                "url": url,
                "accessed": "",
                "license": "",
                "status": status,
                "note": note,
            }
        )
    return rows


def main() -> None:
    rows: list[dict] = []

    for filename, meta in DATASET_META.items():
        path = CORPUS / "shared" / filename
        df = pd.read_csv(path)
        rows.append(
            {
                "dataset": filename,
                "scope": "all entries",
                "n_records": len(df),
                "source_label": "; ".join(
                    sorted(df["source"].dropna().astype(str).unique())
                ),
                "source_type": meta["source_type"],
                "document_title": meta["document"],
                "version_or_date": "",
                "url": meta["url"],
                "accessed": "",
                "license": "",
                "status": meta["status"],
                "note": meta["note"],
            }
        )

    for filename in LAYER_FILES:
        rows.extend(layer_rows(filename))

    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False, encoding="utf-8")
    print(f"wrote {OUT} ({len(out)} rows)")
    print(out.groupby(["dataset", "source_type"]).size().to_string())
    print("\nstatus:")
    print(out["status"].value_counts().to_string())


if __name__ == "__main__":
    main()
