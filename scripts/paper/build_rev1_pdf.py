"""Build the Rev.1 PDF with line numbers and emit a page map.

- raw LaTeX figures (no duplicate Pandoc captions)
- page breaks before Tables 9 and 10
- line numbers for reviewer-response anchors
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(r"D:\Geqi_series\NutriChat")
PAPER = ROOT / "docs" / "paper"
SRC = PAPER / "NutriAgent_paper.md"
TMP = PAPER / "_build_rev1.md"
HEADER = PAPER / "_build_header.tex"
PDF = PAPER / "NutriAgent_paper_rev1.pdf"
MAP_MD = ROOT / "docs" / "paper" / "audit" / "manuscript_page_map.md"
MAP_JSON = ROOT / "docs" / "paper" / "audit" / "manuscript_page_map.json"

text = SRC.read_text(encoding="utf-8")


def latex_escape(s: str) -> str:
    for a, b in [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        s = s.replace(a, b)
    return s


def fig_repl(m):
    """Bind each image to its caption and place it exactly where it appears."""
    path = m.group(2)
    label = m.group(3)
    caption = " ".join(m.group(4).split())
    return (
        "\\begin{figure}[htbp]\n\\centering\n"
        f"\\includegraphics[width=0.95\\linewidth]{{{path}}}\n"
        "\\vspace{2pt}\n"
        "\\begin{minipage}{0.95\\linewidth}\n\\small "
        f"\\textbf{{{label}}} {latex_escape(caption)}\n"
        "\\end{minipage}\n"
        "\\end{figure}"
    )


text = re.sub(
    r"^!\[([^\]]*)\]\(([^)]+)\)\s*\n+\*\*(Fig\. \d+\.)\*\*\s*(.+?)(?=\n\n|\Z)",
    fig_repl,
    text,
    flags=re.M | re.S,
)
for marker in ("**Table 7.**",):
    text = text.replace(marker, "\\newpage\n\n" + marker, 1)

TMP.write_text(text, encoding="utf-8")
HEADER.write_text(
    "\\usepackage{graphicx}\n\\usepackage{lineno}\n\\linenumbers\n\\usepackage{float}\n",
    encoding="utf-8",
)

subprocess.run(
    [
        "pandoc", str(TMP), "-o", str(PDF),
        "--pdf-engine=xelatex",
        "--include-in-header", str(HEADER),
        "-V", "geometry:a4paper,margin=2cm",
        "-V", "mainfont=Times New Roman",
        "-V", "CJKmainfont=SimSun",
        "-V", "fontsize=10pt",
        "--resource-path", str(PAPER),
    ],
    check=True,
    cwd=PAPER,
)

txt = subprocess.run(
    ["pdftotext", "-layout", str(PDF), "-"],
    check=True, capture_output=True, text=True, encoding="utf-8", errors="ignore",
).stdout
pages = [p for p in txt.split("\f") if p.strip()]
targets = {
    "3.2 Overall Performance": "Section 3.2",
    "3.3 Performance Across Query Types": "Section 3.3",
    "3.4 Faithfulness": "Section 3.4",
    "3.5 Cross-Lingual": "Section 3.5",
    "3.6.1": "Section 3.6.1",
    "4. Conclusion": "Conclusion",
    "Limitations": "Limitations",
    "Data and code availability": "Data availability",
    "Table 8.": "Table 8",
    "Table 9.": "Table 9",
    "Table 10.": "Table 10",
    "Table 11.": "Table 11",
    "Fig. 5.": "Fig. 5",
    "Fig. 8.": "Fig. 8",
    "Fig. 9.": "Fig. 9",
    "Fig. 10.": "Fig. 10",
}
found = {}
for label, name in targets.items():
    hits = [i + 1 for i, p in enumerate(pages) if label in p]
    if hits:
        found[name] = hits

for p in (TMP, HEADER):
    p.unlink(missing_ok=True)

MAP_JSON.write_text(json.dumps(found, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# Manuscript page map (Rev.1 PDF)", "",
         f"PDF: `{PDF.name}`; {len(pages)} pages; A4; line numbers enabled.", "",
         "| Item | Page(s) |", "|---|---|"]
for name, pages_ in found.items():
    lines.append(f"| {name} | {', '.join(map(str, pages_))} |")
MAP_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote", PDF)
print(MAP_JSON.read_text(encoding="utf-8"))
