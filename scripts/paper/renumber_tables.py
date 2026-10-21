"""Renumber main-text tables into appearance order (one-time typesetting pass).

Mapping by first appearance:
  1->1, 2->2, 6->3, 3->4, 4->5, 7->6, 8->7, 5->8
Table S* references are untouched.
"""

from __future__ import annotations

import re
from pathlib import Path

P = Path("docs/paper/NutriAgent_paper.md")
MAP = {"1": "1", "2": "2", "6": "3", "3": "4", "4": "5", "7": "6", "8": "7", "5": "8"}

text = P.read_text(encoding="utf-8")
# Compound plural references first.
text = text.replace("Tables 4 and 7", "Tables @@5@@ and @@6@@")
text = text.replace("Tables 7 and S11", "Tables @@6@@ and S11")
text = re.sub(r"Table (\d+)", lambda m: f"Table @@{MAP[m.group(1)]}@@", text)
text = text.replace("@@", "")
P.write_text(text, encoding="utf-8")

for m in re.finditer(r"^\*\*(Table) (\d+)\.", text, re.M):
    print("caption", m.group(2))
