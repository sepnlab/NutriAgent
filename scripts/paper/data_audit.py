"""Data audit for the NutriAgent manuscript (Rev.1).

Computes, for every corpus table used by the paper:
  - rows / unique entities
  - nominal vs present cells and completeness
  - fully empty columns
  - breed / phase coverage
and, for the curated query set:
  - language / type / category composition
  - ground-truth and expected-behaviour counts
  - breed mentions (with Chinese name mapping)

Outputs a JSON ledger (machine-readable) and a Markdown report
(human-readable) so that every number quoted in the manuscript can be
traced to one source.

Usage:
    python scripts/paper/data_audit.py
    python scripts/paper/data_audit.py --out docs/paper/audit
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS = PROJECT_ROOT / "corpus"
QUERIES = PROJECT_ROOT / "queries" / "layer" / "evaluation_queries_curated.json"

# dataset -> (key columns, extra columns to exclude from parameter counts)
DATASETS = {
    "feed_ingredient_bank": {
        "path": CORPUS / "shared" / "feed_ingredient_bank.csv",
        "keys": ["Ingredient"],
        "label": "Feed ingredient bank",
    },
    "feed_ingredient_amino_acids": {
        "path": CORPUS / "shared" / "feed_ingredient_amino_acids.csv",
        "keys": ["Ingredient"],
        "label": "Feed ingredient amino acids",
    },
    "feed_ingredient_digestibility": {
        "path": CORPUS / "shared" / "feed_ingredient_digestibility.csv",
        "keys": ["Ingredient"],
        "label": "Feed ingredient digestibility",
    },
    "nutrient_requirements": {
        "path": CORPUS / "layer" / "nutrient_requirements.csv",
        "keys": ["Breed", "Phase"],
        "label": "Layer nutrient requirements",
    },
    "nutrient_vitamin_mineral": {
        "path": CORPUS / "layer" / "nutrient_vitamin_mineral.csv",
        "keys": ["Breed", "Phase"],
        "label": "Layer vitamin / mineral specifications",
    },
    "performance_management": {
        "path": CORPUS / "layer" / "performance_management.csv",
        "keys": ["Breed", "Week"],
        "label": "Layer production benchmarks",
    },
    "definitions": {
        "path": CORPUS / "shared" / "definitions.csv",
        "keys": ["Term"],
        "label": "Terminology definitions",
        "no_params": True,
    },
}

# Chinese breed names used in the 12 zh queries -> canonical corpus names
ZH_BREED_MAP = {
    "京粉6号": "Jingfen 6",
    "京红1号": "Jinghong 1 v3.0",
    "京白939": "Jingbai 939",
    "大午金凤": "Dawu Jinfeng",
    "大午褐": "Dawu He",
    "大午粉1号": "Dawu Fen 1",
    "农大3号": "Nongda 3",
    "农大6号": "Nongda 6",
    "北农1号": "Beinong 1",
    "北农2号": "Beinong 2",
    "海兰褐": "Hy-Line Brown",
    "海兰W-36": "Hy-Line W-36",
    "伊莎褐": "ISA Brown",
    "罗曼灰": "Lohmann Grey",
    "罗曼粉": "Lohmann Pink",
    "海赛克斯褐": "Hisex Brown",
}

NON_PARAM_COLUMNS = {"source", "Source", "reference", "Reference", "notes", "Notes"}


def audit_dataset(name: str, spec: dict) -> dict:
    path: Path = spec["path"]
    df = pd.read_csv(path)
    keys = [k for k in spec["keys"] if k in df.columns]
    param_cols = [
        c for c in df.columns if c not in keys and c not in NON_PARAM_COLUMNS
    ]
    row = {
        "dataset": name,
        "label": spec["label"],
        "file": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "key_columns": keys,
        "n_parameters": 0 if spec.get("no_params") else len(param_cols),
        "parameter_columns": param_cols,
        "no_params": bool(spec.get("no_params", False)),
    }

    if spec.get("no_params"):
        row.update(
            {
                "unique_entities": int(df[keys[0]].nunique()) if keys else None,
                "nominal_cells": None,
                "present_cells": None,
                "completeness": None,
                "fully_empty_columns": [],
            }
        )
        return row

    nominal = len(df) * len(param_cols)
    present = int(df[param_cols].notna().sum().sum())
    fully_empty = [c for c in param_cols if int(df[c].notna().sum()) == 0]
    mostly_empty = [
        c
        for c in param_cols
        if 0 < int(df[c].notna().sum()) < len(df) * 0.25
    ]
    row.update(
        {
            "unique_entities": int(df[keys[0]].nunique()) if keys else None,
            "nominal_cells": nominal,
            "present_cells": present,
            "completeness": round(present / nominal, 4) if nominal else None,
            "fully_empty_columns": fully_empty,
            "mostly_empty_columns": mostly_empty,
            "per_column_present": {
                c: int(df[c].notna().sum()) for c in param_cols
            },
        }
    )

    if "Breed" in df.columns:
        row["n_breeds"] = int(df["Breed"].nunique())
        row["breeds"] = sorted(df["Breed"].dropna().unique().tolist())
        row["rows_per_breed"] = (
            df["Breed"].value_counts().sort_index().to_dict()
        )
    if "Phase" in df.columns:
        phases = sorted(df["Phase"].dropna().unique().tolist())
        row["n_phase_labels"] = len(phases)
        row["phase_labels"] = phases
        row["phases_per_breed"] = (
            df.groupby("Breed")["Phase"].nunique().sort_index().to_dict()
        )
    if "Week" in df.columns:
        row["week_min"] = int(df["Week"].min())
        row["week_max"] = int(df["Week"].max())
    return row


def audit_queries(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = [dict(q, _category=cat) for cat, items in data.items() for q in items]
    zh = [q for q in rows if q.get("language") == "zh"]
    breed_mentions: Counter = Counter()
    for q in zh:
        for zh_name, en_name in ZH_BREED_MAP.items():
            if zh_name in q["query"]:
                breed_mentions[en_name] += 1
    return {
        "file": str(path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "n_queries": len(rows),
        "by_language": dict(Counter(q.get("language") for q in rows)),
        "by_type": dict(Counter(q.get("type") for q in rows)),
        "by_category": dict(Counter(q["_category"] for q in rows)),
        "n_expected_value": sum(1 for q in rows if q.get("expected_value") is not None),
        "n_expected_behavior": sum(
            1 for q in rows if q.get("expected_behavior") is not None
        ),
        "zh_queries": [
            {"id": q["id"], "type": q.get("type"), "query": q["query"]} for q in zh
        ],
        "zh_breed_mentions": dict(breed_mentions),
        "ids": [q["id"] for q in rows],
    }


def count_totals(datasets: dict) -> dict:
    """Recompute the manuscript's 'data points' under explicit conventions."""
    ing = datasets["feed_ingredient_bank"]
    aa = datasets["feed_ingredient_amino_acids"]
    dig = datasets["feed_ingredient_digestibility"]
    nr = datasets["nutrient_requirements"]
    vm = datasets["nutrient_vitamin_mineral"]
    perf = datasets["performance_management"]
    defs = datasets["definitions"]

    ingredient_nominal = len(ing["parameter_columns"]) + len(
        aa["parameter_columns"]
    ) + len(dig["parameter_columns"])
    records = {
        "feed_entries": ing["rows"],
        "nutrition_breed_phase_entries": nr["rows"],
        "vitamin_mineral_entries": vm["rows"],
        "performance_records": perf["rows"],
        "definitions": defs["rows"],
    }
    scalar_nominal = (
        ing["nominal_cells"]
        + aa["nominal_cells"]
        + dig["nominal_cells"]
        + nr["nominal_cells"]
        + vm["nominal_cells"]
        + perf["nominal_cells"]
    )
    scalar_present = (
        ing["present_cells"]
        + aa["present_cells"]
        + dig["present_cells"]
        + nr["present_cells"]
        + vm["present_cells"]
        + perf["present_cells"]
    )
    return {
        "ingredient_parameters_total": ingredient_nominal,
        "records": records,
        "records_total": sum(records.values()),
        "scalar_cells_nominal": scalar_nominal,
        "scalar_cells_present": scalar_present,
        "scalar_plus_definitions_nominal": scalar_nominal + defs["rows"],
        "scalar_plus_definitions_present": scalar_present + defs["rows"],
        "paper_claim_14800_convention": (
            "feed 108x97 + nutrition 2,060 + vitamin 540 + performance 1,131 "
            "+ definitions 556 = 14,767 (mixes scalar cells with records and definitions)"
        ),
        "poultrydb_documents": (
            ing["rows"] * 3 + nr["rows"] + vm["rows"] + perf["rows"] + defs["rows"]
        ),
    }


def to_markdown(report: dict) -> str:
    lines = [
        "# 数据审计报告（自动生成）",
        "",
        f"> 生成时间：{report['generated_at']}  ",
        f"> 查询集：`{report['queries']['file']}`  ",
        f"> 脚本：`scripts/paper/data_audit.py`",
        "",
        "## 1. 数据集完备度",
        "",
        "| 数据集 | 文件 | 行 | 键 | 参数列 | 名义单元格 | 实有 | 完备度 | 全空列数 |",
        "|---|---|---:|---|---:|---:|---:|---:|---:|",
    ]
    for name, ds in report["datasets"].items():
        if ds.get("no_params"):
            lines.append(
                f"| {ds['label']} | `{ds['file']}` | {ds['rows']} | "
                f"{'/'.join(ds['key_columns'])} | — | — | — | — | — |"
            )
        else:
            lines.append(
                f"| {ds['label']} | `{ds['file']}` | {ds['rows']} | "
                f"{'/'.join(ds['key_columns'])} | {ds['n_parameters']} | "
                f"{ds['nominal_cells']} | {ds['present_cells']} | "
                f"{ds['completeness']:.1%} | {len(ds['fully_empty_columns'])} |"
            )

    lines += ["", "## 2. 品种与 phase", ""]
    for key in ("nutrient_requirements", "nutrient_vitamin_mineral", "performance_management"):
        ds = report["datasets"][key]
        if "n_breeds" in ds:
            lines.append(
                f"- **{ds['label']}**：{ds['n_breeds']} 个品种；"
                f"phase 标签 {ds.get('n_phase_labels', '—')} 个；"
                f"每品种 phase 数 {ds.get('phases_per_breed', '—')}"
            )
    lines += ["", "## 3. 计数口径", ""]
    totals = report["totals"]
    lines += [
        f"- 记录数合计：**{totals['records_total']}**（{totals['records']}）",
        f"- 标量单元格（名义）：**{totals['scalar_cells_nominal']}**",
        f"- 标量单元格（实有）：**{totals['scalar_cells_present']}**",
        f"- 标量 + 定义（名义）：**{totals['scalar_plus_definitions_nominal']}**",
        f"- 标量 + 定义（实有）：**{totals['scalar_plus_definitions_present']}**",
        f"- PoultryDB 文档：**{totals['poultrydb_documents']}**",
        "",
        f"> 论文 14,800 的口径：{totals['paper_claim_14800_convention']}",
    ]
    lines += ["", "## 4. 查询集", ""]
    q = report["queries"]
    lines += [
        f"- 总数：**{q['n_queries']}**",
        f"- 语言：{q['by_language']}",
        f"- 类型：{q['by_type']}",
        f"- 领域：{q['by_category']}",
        f"- expected_value：**{q['n_expected_value']}**；expected_behavior：**{q['n_expected_behavior']}**",
        f"- 中文题品种提及：{q['zh_breed_mentions']}",
        "",
        "### 中文题清单",
        "",
        "| ID | 类型 | 查询 |",
        "|---|---|---|",
    ]
    for item in q["zh_queries"]:
        lines.append(f"| {item['id']} | {item['type']} | {item['query']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "docs" / "paper" / "audit"),
        help="Output directory for data_audit.json / data_audit.md",
    )
    parser.add_argument(
        "--queries",
        default=str(QUERIES),
        help="Curated query JSON path",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    datasets = {}
    for name, spec in DATASETS.items():
        if not spec["path"].exists():
            print(f"[warn] missing dataset: {spec['path']}")
            continue
        datasets[name] = audit_dataset(name, spec)

    report = {
        "generated_at": pd.Timestamp.now(tz="Asia/Shanghai").isoformat(),
        "datasets": datasets,
        "totals": count_totals(datasets),
        "queries": audit_queries(Path(args.queries)),
    }

    json_path = out_dir / "data_audit.json"
    md_path = out_dir / "data_audit.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    md_path.write_text(to_markdown(report), encoding="utf-8")

    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    for name, ds in datasets.items():
        if ds.get("no_params"):
            print(f"{name:32s} rows={ds['rows']}")
        else:
            print(
                f"{name:32s} rows={ds['rows']:5d} params={ds['n_parameters']:3d} "
                f"complete={ds['completeness']:.1%} empty_cols={len(ds['fully_empty_columns'])}"
            )
    print("queries:", report["queries"]["n_queries"], report["queries"]["by_language"])


if __name__ == "__main__":
    main()
