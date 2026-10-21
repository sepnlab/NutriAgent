"""Rebuild the 78-item reviewer tracker in a clean, status-first format.

Preserves each item's short concern/type/severity/action, rewrites stale
PENDING labels, and adds a consistent status + location column.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
SRC = ROOT / "docs" / "paper" / "response_to_reviewers.md"
OUT = SRC

# Items that remain partial or need author input after the Rev.1 work.
PARTIAL = {
    "R1.2", "R1.3", "R2.10", "R2.14", "R2.15", "R2.16", "R2.23",
    "R2.24", "R2.26", "R2.27", "R2.28", "R2.41", "R3.3", "R3.6",
    "R3.8", "R3.10", "R3.14", "R3.16", "R3.18", "R4.2", "R4.13",
}
LIMITATION = {"R4.5"}
AUTHOR_INPUT = {"R4.10"}

text = SRC.read_text(encoding="utf-8", errors="ignore")
rows = []
for line in text.splitlines():
    if not re.match(r"^\| R[1-4]\.\d+ \|", line):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 6:
        continue
    rid, concern, typ, severity, action, old_status = cells[:6]
    old_status = re.sub(r"\bPENDING-E\d+\b;?\s*", "", old_status)
    old_status = re.sub(r"\bPENDING\b;?\s*", "", old_status)
    old_status = old_status.replace("搂", "§").replace("鈥?", "—").strip(" ;/")
    if rid in AUTHOR_INPUT:
        status = "AUTHOR_INPUT"
    elif rid in LIMITATION:
        status = "LIMITATION"
    elif rid in PARTIAL:
        status = "PARTIAL"
    else:
        status = "DONE"
    rows.append((rid, concern, typ, severity, action, status, old_status or "see response letter"))

counts = Counter(r[5] for r in rows)
lines = [
    "# Response to Reviewers — NutriAgent (AGRCOM-D-26-00673)",
    "",
    "> **Status**: tracker (working package). The submission letter is `response_letter.md`.",
    "> Reviewer comments are preserved in `docs/paper/review_round1/extracted/reviews.txt`.",
    "> Status definitions: `DONE` = new evidence/text with a location; `PARTIAL` = addressed",
    "> with an explicit remaining limitation; `LIMITATION` = not done, stated as a boundary;",
    "> `AUTHOR_INPUT` = author/repository detail still needed.",
    "",
    "## Status summary",
    "",
    f"- DONE: **{counts.get('DONE', 0)}**",
    f"- PARTIAL: **{counts.get('PARTIAL', 0)}**",
    f"- LIMITATION: **{counts.get('LIMITATION', 0)}**",
    f"- AUTHOR_INPUT: **{counts.get('AUTHOR_INPUT', 0)}**",
    f"- Total: **{len(rows)}** (R1 = 5, R2 = 42, R3 = 18, R4 = 13)",
    "",
    "The letter does not claim all comments are fully satisfied; it states that all are",
    "addressed and identifies the remaining limitations.",
    "",
    "## Comment-response tracker",
    "",
    "| ID | Concern (short) | Type | Severity | Action | Status | Location / note |",
    "|---|---|---|---|---|---|---|",
]
for rid, concern, typ, severity, action, status, old in rows:
    lines.append(f"| {rid} | {concern} | {typ} | {severity} | {action} | **{status}** | {old} |")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("rows", len(rows), dict(counts))
