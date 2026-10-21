# NutriAgent

NutriAgent is a specialist-routed multi-agent system for layer-hen nutrition
question answering. Four domain specialists (Feed, Nutrition, Performance,
Terminology) use isolated tools and a shared retrieval layer; a synthesis stage
checks cross-specialist consistency and integrates their outputs.

This repository contains the source code, configuration, evaluation queries,
de-identified expert scores, audit artifacts, and manuscript materials for the
Rev.1 submission.

## What is in this repository

- `src/` — agents, tools, retrieval, evaluation, and reporting code.
- `config/` — model, experiment, and pricing configuration; no API keys.
- `queries/layer/` — the 195-query candidate pool and the 54-query curated set.
- `docs/paper/` — manuscript, supplementary material, cover/response letters,
  and audit files.
- `docs/paper/audit/` — de-identified expert scores, per-query scores, and
  reproducibility reports.
- `tests/` — unit and regression tests.

The layer-hen corpus is **not redistributed** in this public release because
some source documents (notably Chinese domestic-breed specifications compiled
through jbzyw.com) carry terms that do not clearly permit redistribution. The
per-breed source mapping and extraction procedure are documented in
`docs/paper/supplementary_material.md` (Table S3) and in the manuscript. To run
the full system, place the corpus under `corpus/` using the documented sources.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # add your own API keys
python -m pytest tests/ -q
```

The unit tests that require corpus files will be skipped or fail until the
corpus is placed under `corpus/`; the code and evaluation scripts are provided
for inspection and reuse.

## Evaluation and expert scores

The 54-query expert-scored comparison is in
`docs/paper/audit/expert_scores_primary.csv` (378 responses). The independent
120-response reliability check is `expert_scores_third.csv`; the same-expert
repeat sheet is `expert_scores_second.csv` and is reported as intra-rater
consistency, not as an independent rater. Raw expert workbooks, names, and the
label map are not included.

## Reproducing the paper

- `docs/paper/audit/reproduce.md` — figure and analysis commands.
- `scripts/paper/` — expert-score extraction/analysis, PDF build, page map,
  and final consistency audit.
- `docs/paper/audit/final_consistency_report.md` — table/figure and numeric
  consistency checks.

## Data and licensing

Code is released under the MIT License (see `LICENSE`). The corpus is derived
from public feed tables and breeder/company documentation; per-breed provenance
and source terms are recorded in `docs/paper/supplementary_material.md` (Table
S3). Third-party data remain subject to their original terms.

## Citation

If you use this repository, please cite the NutriAgent manuscript (citation
details will be updated after publication).
