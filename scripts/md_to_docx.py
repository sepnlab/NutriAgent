"""
Convert supplementary_material.md to a properly formatted .docx file.
Usage: .venv\Scripts\python scripts\md_to_docx.py
"""

import re
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

MD_PATH = Path("docs/paper/supplementary_material.md")
DOCX_PATH = Path("docs/paper/supplementary_material.docx")


def set_cell_shading(cell, color_hex):
    """Set cell background shading."""
    shading = parse_xml(
        f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>'
    )
    cell._tc.get_or_add_tcPr().append(shading)


def parse_inline(text):
    """Parse inline formatting: **bold**, *italic*, `code`."""
    parts = []
    # Split on **...**, *...*, `...` patterns
    pattern = r"(\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`)"
    last_end = 0
    for m in re.finditer(pattern, text):
        if m.start() > last_end:
            parts.append(("text", text[last_end : m.start()]))
        if m.group(1) and m.group(1).startswith("**"):
            parts.append(("bold", m.group(2)))
        elif m.group(1) and m.group(1).startswith("*") and not m.group(1).startswith("**"):
            parts.append(("italic", m.group(3)))
        elif m.group(4) is not None:
            parts.append(("code", m.group(4)))
        last_end = m.end()
    if last_end < len(text):
        parts.append(("text", text[last_end:]))
    return parts


def add_rich_text(paragraph, text):
    """Add formatted runs to a paragraph from inline-markdown text."""
    for kind, content in parse_inline(text):
        run = paragraph.add_run(content)
        if kind == "bold":
            run.bold = True
        elif kind == "italic":
            run.italic = True
        elif kind == "code":
            run.font.name = "Consolas"
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x20, 0x20, 0x20)
        # text: no extra formatting


def parse_table_row(cells_text):
    """Parse a markdown table row into cell strings."""
    return [c.strip() for c in cells_text.split("|")[1:-1]]


def is_separator_row(row_text):
    """Check if a table row is a separator (e.g., |---|---|)."""
    cells = row_text.split("|")
    return all(re.match(r"^[\s:-]+$", c.strip()) for c in cells if c.strip())


def convert_md_to_docx():
    doc = Document()

    # -- Style tweaks --
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    for level in range(1, 4):
        h_style = doc.styles[f"Heading {level}"]
        h_style.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)
        if level == 1:
            h_style.font.size = Pt(22)
        elif level == 2:
            h_style.font.size = Pt(16)
        else:
            h_style.font.size = Pt(13)

    lines = MD_PATH.read_text(encoding="utf-8").splitlines()

    i = 0
    in_code_block = False
    code_lines = []
    in_table = False
    table_header = None
    table_rows = []

    while i < len(lines):
        line = lines[i]

        # --- Code blocks ---
        if line.strip().startswith("```"):
            if in_code_block:
                # End code block → dump as monospace paragraph
                p = doc.add_paragraph()
                p.style = doc.styles["Normal"]
                fmt = p.paragraph_format
                fmt.left_indent = Cm(1)
                fmt.space_before = Pt(4)
                fmt.space_after = Pt(4)
                code_text = "\n".join(code_lines)
                run = p.add_run(code_text)
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # --- Tables ---
        if "|" in line and line.strip().startswith("|") and line.strip().endswith("|"):
            stripped = line.strip()
            if is_separator_row(stripped):
                i += 1
                continue
            if not in_table:
                # Start new table
                table_header = parse_table_row(stripped)
                in_table = True
                table_rows = []
            else:
                table_rows.append(parse_table_row(stripped))
            i += 1
            # Check if next line ends the table
            if i < len(lines):
                next_line = lines[i].strip()
                if not (next_line.startswith("|") and next_line.endswith("|")):
                    # Flush table
                    flush_table(doc, table_header, table_rows)
                    in_table = False
                    table_header = None
                    table_rows = []
            continue

        if in_table:
            # Line doesn't start with | → flush table
            flush_table(doc, table_header, table_rows)
            in_table = False
            table_header = None
            table_rows = []
            # Don't advance i; process this line next

        # --- Horizontal rule ---
        if line.strip() == "---":
            # Add a bottom-border-only paragraph as separator
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(
                f'<w:pBdr {nsdecls("w")}>'
                '  <w:bottom w:val="single" w:sz="6" w:space="1" w:color="999999"/>'
                "</w:pBdr>"
            )
            pPr.append(pBdr)
            i += 1
            continue

        # --- Headings ---
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            if level > 3:
                level = 3  # docx supports up to Heading 3 easily
            text = heading_match.group(2).strip()
            # Remove trailing {#anchor} if present
            text = re.sub(r"\s*\{#[^}]+\}$", "", text).strip()
            p = doc.add_heading(text, level=level)
            i += 1
            continue

        # --- Bullet lists ---
        list_match = re.match(r"^(\s*)[-*+]\s+(.+)$", line)
        if list_match:
            text = list_match.group(2).strip()
            p = doc.add_paragraph(style="List Bullet")
            add_rich_text(p, text)
            i += 1
            continue

        # --- Plain paragraph ---
        if line.strip():
            p = doc.add_paragraph()
            add_rich_text(p, line.strip())
        else:
            # Empty line — add a small spacer
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)

        i += 1

    # Flush any remaining table
    if in_table and table_header and table_rows:
        flush_table(doc, table_header, table_rows)

    # -- Page setup --
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    doc.save(DOCX_PATH)
    print(f"Saved to {DOCX_PATH}")


def flush_table(doc, header, rows):
    """Create a Word table from parsed header and rows."""
    if not header:
        return

    # Ensure consistent column count
    ncols = len(header)
    table = doc.add_table(rows=1 + len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    # Header row
    for j, cell_text in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(cell_text)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_cell_shading(cell, "2F5496")

    # Data rows
    for r_idx, row_data in enumerate(rows):
        for c_idx, cell_text in enumerate(row_data):
            if c_idx >= ncols:
                break
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            add_rich_text(p, cell_text)
            for run in p.runs:
                run.font.size = Pt(10)
            # Alternate row shading
            if r_idx % 2 == 1:
                set_cell_shading(cell, "F2F2F2")

    # Set table font
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.space_before = Pt(2)
                paragraph.paragraph_format.space_after = Pt(2)

    # Add spacer after table
    doc.add_paragraph()


if __name__ == "__main__":
    convert_md_to_docx()
