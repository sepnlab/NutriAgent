"""Update tracker statuses/locations after Fig. 2, D4 proxy ITT, and repo creation."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

P = Path(r"D:\Geqi_series\NutriChat\docs\paper\response_to_reviewers.md")
lines = P.read_text(encoding="utf-8").splitlines()

status = {}
loc = {
    "R1.2": "Fig. 2 regenerated with Stages 1–3 and consistency-check label",
    "R1.3": "Fig. 2 caption/label changed to consistency checks + integration",
    "R2.6": "§2.3.1/S3: purposeful selection; two team-internal experts; no random seed",
    "R2.27": "D4 proxy ITT in S19; exact four-query failure flag not recoverable",
    "R3.10": "D4 proxy ITT in S19; complete-case null",
    "R3.15": "§2.3.1/S3: purposeful selection; two team-internal experts; no random seed",
    "R4.10": "Repository created; sanitized release push pending",
}
for rid in ("R1.2", "R1.3", "R2.6", "R3.15"):
    status[rid] = "DONE"
for rid in ("R2.27", "R3.10"):
    status[rid] = "PARTIAL"
status["R4.10"] = "AUTHOR_INPUT"

out = []
for line in lines:
    m = re.match(r"^\| (R[1-4]\.\d+) \|", line)
    if not m:
        out.append(line)
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    rid = cells[0]
    if rid in status:
        cells[5] = f"**{status[rid]}**"
        cells[6] = loc.get(rid, cells[6])
    out.append("| " + " | ".join(cells) + " |")

rows = [l for l in out if re.match(r"^\| R[1-4]\.\d+ \|", l)]
counts = Counter()
for l in rows:
    cells = [c.strip() for c in l.strip("|").split("|")]
    counts[cells[5].replace("*", "")] += 1

text = "\n".join(out) + "\n"
text = re.sub(r"- DONE: \*\*\d+\*\*", f"- DONE: **{counts.get('DONE', 0)}**", text)
text = re.sub(r"- PARTIAL: \*\*\d+\*\*", f"- PARTIAL: **{counts.get('PARTIAL', 0)}**", text)
text = re.sub(r"- LIMITATION: \*\*\d+\*\*", f"- LIMITATION: **{counts.get('LIMITATION', 0)}**", text)
text = re.sub(r"- AUTHOR_INPUT: \*\*\d+\*\*", f"- AUTHOR_INPUT: **{counts.get('AUTHOR_INPUT', 0)}**", text)
P.write_text(text, encoding="utf-8")
print("rows", len(rows), dict(counts))
