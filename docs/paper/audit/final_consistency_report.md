# Final consistency audit (Rev.1)

Manuscript: `NutriAgent_paper.md`; supplement: `supplementary_material.md`.

## Structural checks

| Check | Result |
|---|---|
| Table captions | 1…11 |
| Figure captions | 1…12 |
| Table refs without caption | none |
| Figure refs without caption | none |
| Image files | 0 missing |
| Supplement sections | max S19 |
| Supplement refs | all present |
| Placeholders | none |

## Key expert numbers (Table 9 vs analysis)

| Method | C | P | D | Overall |
|---|---:|---:|---:|---:|
| NutriAgent | 4.46 | 4.47 | 4.07 | 4.34 |
| DeepSeek-V4-Pro | 4.26 | 3.97 | 3.93 | 4.05 |
| DeepSeek-V4-Flash | 4.06 | 3.74 | 4.33 | 4.04 |
| Qwen3.8-Flash | 3.96 | 3.79 | 4.28 | 4.01 |
| GLM-4.5-Air | 3.74 | 3.63 | 3.28 | 3.55 |
| Qwen3-8B | 3.13 | 2.87 | 3.13 | 3.04 |
| MiniMax-M2.5 | 2.80 | 2.53 | 2.56 | 2.63 |

## Notes

- Table 7 is the compact calibration table; the full matrix is S17, the model transition is S18, and the D4 ITT proxy is S19.
- Table 9–11 are placed after Table 8 and before the Conclusion; page map is in `manuscript_page_map.md`.
- Table 9 Overall is the mean of dimension means; Table 10 ΔO is the paired per-response overall (+0.20 vs +0.28).
- Precision vs DeepSeek-V4-Pro: +0.50, unadjusted p = 0.037, Holm across all 24 dimension tests p = 0.256.
- Fig. 5/8/9/10 use primary-expert data; Fig. 6/7 are submitted-run automated panels and are labeled; Fig. 4 illustrates C-XD-003.
- The repeat 120-response sheet is a same-expert repeat/copy pass (user-confirmed) and is reported as intra-rater consistency, not inter-rater.
- Supplement S3 is regenerated from the curated JSON (54 queries: 42 English / 12 Chinese); S7b reports the 42-pair validator test; S16 is the reliability table heading.
- The repository is public at https://github.com/sepnlab/NutriAgent (`main`); the layer-hen corpus is not redistributed because some source terms do not clearly permit it.
- Remaining open items: E4 human labels, E14 two-coder kappa, E10 (not used), exact D4 four-query ITT flag, unresolved provenance fields.
- The PDF used for page anchors is `NutriAgent_paper_rev1.pdf` (35 pages, line numbers).
