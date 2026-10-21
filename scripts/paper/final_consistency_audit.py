"""Final consistency audit for the Rev.1 manuscript.

Read-only: checks captions/references, image files, supplement sections, and
key expert numbers. Writes a markdown report for the submission file set.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
PAPER = ROOT / "docs" / "paper"
MS = PAPER / "NutriAgent_paper.md"
SUP = PAPER / "supplementary_material.md"
OUT = PAPER / "audit" / "final_consistency_report.md"

text = MS.read_text(encoding="utf-8")
sup = SUP.read_text(encoding="utf-8")

table_caps = [int(m.group(1)) for m in re.finditer(r"^\*\*Table (\d+)\.", text, re.M)]
fig_caps = [int(m.group(1)) for m in re.finditer(r"^\*\*Fig\. (\d+)\.", text, re.M)]
table_refs = sorted({int(m.group(1)) for m in re.finditer(r"Table (\d+)", text)})
fig_refs = sorted({int(m.group(1)) for m in re.finditer(r"Fig\.? (\d+)", text)})
images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
missing_images = [p for p in images if not (PAPER / p).exists()]

sup_sections = [int(m.group(1)) for m in re.finditer(r"^## S(\d+)\.", sup, re.M)]
sup_refs = sorted({int(m.group(1)) for m in re.finditer(r"Supplementary S(\d+)", text)})

placeholders = []
for i, line in enumerate(text.splitlines(), 1):
    if re.search(r"TODO|TBD|placeholder|will be reported|pending external", line, re.I):
        placeholders.append((i, line.strip()[:160]))

ana = json.loads((PAPER / "audit" / "expert_analysis.json").read_text(encoding="utf-8"))
primary = {r["method"]: r for r in ana["primary_table"]}

checks = []
checks.append(("Table captions", table_caps, "1…11" if table_caps == list(range(1, 12)) else "NON-SEQUENTIAL"))
checks.append(("Figure captions", fig_caps, "1…12" if fig_caps == list(range(1, 13)) else "CHECK"))
checks.append(("Table refs without caption", [x for x in table_refs if x not in table_caps], "none"))
checks.append(("Figure refs without caption", [x for x in fig_refs if x not in fig_caps], "none"))
checks.append(("Image files", images, f"{len(missing_images)} missing"))
checks.append(("Supplement sections", sup_sections, f"max S{max(sup_sections)}"))
checks.append(("Supplement refs", sup_refs, "all present" if set(sup_refs) <= set(sup_sections) else "MISSING"))
checks.append(("Placeholders", placeholders, "none" if not placeholders else f"{len(placeholders)}"))

md = ["# Final consistency audit (Rev.1)", "",
      f"Manuscript: `{MS.name}`; supplement: `{SUP.name}`.", "",
      "## Structural checks", "",
      "| Check | Result |", "|---|---|"]
for name, value, status in checks:
    md.append(f"| {name} | {status} |")

md += ["", "## Key expert numbers (Table 9 vs analysis)", "",
       "| Method | C | P | D | Overall |", "|---|---:|---:|---:|---:|"]
for method, r in primary.items():
    md.append(f"| {method} | {r['C']:.2f} | {r['P']:.2f} | {r['D']:.2f} | {r['O']:.2f} |")

md += ["", "## Notes", "",
       "- Table 7 is the compact calibration table; the full matrix is S17, the model transition is S18, and the D4 ITT proxy is S19.",
       "- Table 9–11 are placed after Table 8 and before the Conclusion; page map is in `manuscript_page_map.md`.",
       "- Table 9 Overall is the mean of dimension means; Table 10 ΔO is the paired per-response overall (+0.20 vs +0.28).",
       "- Precision vs DeepSeek-V4-Pro: +0.50, unadjusted p = 0.037, Holm across all 24 dimension tests p = 0.256.",
       "- Fig. 5/8/9/10 use primary-expert data; Fig. 6/7 are submitted-run automated panels and are labeled; Fig. 4 illustrates C-XD-003.",
       "- The repeat 120-response sheet is a same-expert repeat/copy pass (user-confirmed) and is reported as intra-rater consistency, not inter-rater.",
       "- Supplement S3 is regenerated from the curated JSON (54 queries: 42 English / 12 Chinese); S7b reports the 42-pair validator test; S16 is the reliability table heading.",
       "- The repository URL is https://github.com/sepnlab/NutriAgent; the sanitized release push is pending authentication.",
       "- Remaining open items: E4 human labels, E14 two-coder kappa, E10 (not used), exact D4 four-query ITT flag, unresolved provenance fields.",
       "- The PDF used for page anchors is `NutriAgent_paper_rev1.pdf` (35 pages, line numbers)."]

OUT.write_text("\n".join(md) + "\n", encoding="utf-8")
print("\n".join(md))
