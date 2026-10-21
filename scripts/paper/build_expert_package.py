"""Build the expert-scoring package for the Rev.1 revision.

Creates a folder on the Desktop with:
  - primary 378-row workbook
  - second-rater 120-row workbook
  - ground-truth workbook
  - Chinese instructions (docx + md)
  - raw CSVs
No model-identity map is copied.
"""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(r"D:\Geqi_series\NutriChat")
AUDIT = ROOT / "docs" / "paper" / "audit"
QUERIES = ROOT / "queries" / "layer" / "evaluation_queries_curated.json"
DESKTOP = Path(r"C:\Users\young\Desktop")
OUT = DESKTOP / "NutriAgent_专家评分_20261021"

QUERY_NOTES = {
    "C-XD-005": "题面澄清：其余 40% 为 SBM48，因此原配方 SBM48 为 40%。",
    "C-XD-006": "题面澄清：报告新配方减原配方的 CP 贡献变化（百分点），不是只报新贡献 11.70%。",
    "C-FIB-004": "请使用 feed ingredient bank 的 ME 值，以 kcal/kg 表示。",
    "C-FIB-005": "请使用 feed ingredient bank 的 CP 值，以 % 表示。",
    "C-FIB-010": "请使用 feed ingredient bank 的 ME 值，以 kcal/kg 表示（可接受 MJ/kg 换算）。",
    "C-EC-005": "请说明鱼粉与石灰石的 ME；石灰石为矿物质，ME=0。",
}
RAW = OUT / "原始CSV"

PRIMARY_CSV = AUDIT / "expert_eval_all.csv"
SECOND_CSV = AUDIT / "expert_eval_second_rater.csv"

# ---------------------------------------------------------------- data

def load_queries() -> list[dict]:
    data = json.loads(QUERIES.read_text(encoding="utf-8"))
    return [dict(q, category=q.get("category", cat)) for cat, items in data.items() for q in items]


def load_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def flatten(q: dict) -> dict:
    return {
        "query_id": q["id"],
        "category": q.get("category", ""),
        "query_type": q.get("type", ""),
        "language": q.get("language", "en"),
        "query": q["query"],
        "query_note": QUERY_NOTES.get(q["id"], ""),
        "expected_value": "" if q.get("expected_value") is None else q["expected_value"],
        "expected_unit": q.get("expected_unit") or "",
        "expected_behavior": q.get("expected_behavior") or "",
        "target_doc": "; ".join(q.get("target_doc") or []),
        "review": q.get("review") or "",
    }


def scoring_note(q: dict) -> str:
    t = q.get("type", "")
    if q.get("expected_behavior"):
        return "按 expected_behavior 判断是否应拒答/澄清/指出不适用；若真值表无预期数值，Precision 填 N/A。"
    if t == "multi-hop":
        return "按最终数值评分；中间步骤错误但最终值正确时，Correctness 降、Precision 可高。"
    if t == "comparison":
        return "需给出两个对象及比较方向；只答一个对象算部分正确。"
    if t == "definition":
        return "无数值，Precision 填 N/A；需定义准确并说明与相关概念的区别。"
    if t == "open-ended":
        return "无数值，Precision 填 N/A；按完整性、准确性、机制深度评分。"
    if t == "constraint":
        return "检查是否满足题目约束；若真值表无预期数值，Precision 填 N/A。"
    if t == "counterfactual":
        return "需识别前提不成立或给出条件性答案；按真值表判断。"
    return "按真值表数值与单位评分；合理换算/四舍五入不扣分。"

# ---------------------------------------------------------------- styles

NAVY = "1F3864"
BLUE = "2F5597"
LIGHT_BLUE = "D9E2F3"
ORANGE = "FCE4D6"
YELLOW = "FFF2CC"
GREY = "F2F2F2"
WHITE = "FFFFFF"

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HEADER_FONT = Font(name="微软雅黑", size=10, bold=True, color=WHITE)
BODY_FONT = Font(name="微软雅黑", size=10)
TITLE_FONT = Font(name="微软雅黑", size=16, bold=True, color=NAVY)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def set_widths(ws, widths: dict[str, int]) -> None:
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def style_header(ws, ncols: int) -> None:
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = HEADER_FONT
        cell.fill = PatternFill("solid", fgColor=BLUE)
        cell.alignment = CENTER
        cell.border = BORDER
    ws.row_dimensions[1].height = 42


def add_score_validation(ws, last_row: int) -> None:
    dv15 = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=False,
                          showErrorMessage=True, errorTitle="评分范围",
                          error="请填写 1–5 的整数。")
    dv_prec = DataValidation(type="list", formula1='"1,2,3,4,5,N/A"', allow_blank=False,
                             showErrorMessage=True, errorTitle="Precision 范围",
                             error="数值题填 1–5；无预期数值的题填 N/A。")
    dv_prov = DataValidation(type="list", formula1='"0,1,2,NA"', allow_blank=True,
                             showErrorMessage=True, errorTitle="Provenance 范围",
                             error="填 0、1、2 或 NA（也可留空）。")
    for dv in (dv15, dv_prec, dv_prov):
        ws.add_data_validation(dv)
    dv15.add(f"J2:J{last_row}")
    dv15.add(f"L2:L{last_row}")
    dv_prec.add(f"K2:K{last_row}")
    dv_prov.add(f"M2:M{last_row}")


def add_blank_highlight(ws, last_row: int) -> None:
    rng = f"J2:L{last_row}"
    ws.conditional_formatting.add(
        rng,
        FormulaRule(formula=["LEN(TRIM(J2))=0"], fill=PatternFill("solid", fgColor=YELLOW)),
    )


def build_sheet(wb: Workbook, rows: list[dict], grouped: bool = True) -> None:
    ws = wb.active
    ws.title = "评分表"
    headers = ["序号", "query_id", "category", "query_type", "language", "query",
               "query_note\n(题面澄清)", "model_id", "response",
               "correctness\n(1-5)", "precision\n(1-5 / N/A)",
               "scientific_depth\n(1-5)", "provenance\n(0-2 / NA)", "notes\n(optional)"]
    ws.append(headers)
    style_header(ws, len(headers))
    set_widths(ws, {"A": 6, "B": 12, "C": 20, "D": 13, "E": 8, "F": 42, "G": 30,
                    "H": 10, "I": 70, "J": 11, "K": 12, "L": 12, "M": 11, "N": 30})

    last_query = None
    shade = False
    for idx, r in enumerate(rows, 1):
        if grouped and r["query_id"] != last_query:
            shade = not shade
            last_query = r["query_id"]
        ws.append([
            idx, r["query_id"], r["category"], r["query_type"], r["language"],
            r["query"], QUERY_NOTES.get(r["query_id"], ""), r["model_id"], r["response"],
            "", "", "", "", "",
        ])
        row = ws.max_row
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=row, column=c)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = CENTER if c in (1, 2, 4, 5, 8, 10, 11, 12, 13) else WRAP
            if shade and c <= 9:
                cell.fill = PatternFill("solid", fgColor=GREY)
        ws.row_dimensions[row].height = 140

    last_row = ws.max_row
    add_score_validation(ws, last_row)
    add_blank_highlight(ws, last_row)
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = f"A1:N{last_row}"
    ws.sheet_view.zoomScale = 85
    ws.print_title_rows = "1:1"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def build_record_sheet(wb: Workbook) -> None:
    ws = wb.create_sheet("评分记录")
    ws.sheet_view.showGridLines = False
    ws["A1"] = "评分记录（请填写）"
    ws["A1"].font = TITLE_FONT
    fields = [
        ("专家姓名", ""),
        ("单位 / 职称", ""),
        ("评分日期", ""),
        ("开始时间", ""),
        ("结束时间", ""),
        ("总时长（小时）", ""),
        ("是否评分 provenance", "是 / 否（可留空）"),
        ("备注", ""),
    ]
    for i, (label, value) in enumerate(fields, start=3):
        ws.cell(row=i, column=1, value=label).font = Font(name="微软雅黑", size=10, bold=True)
        ws.cell(row=i, column=2, value=value).font = BODY_FONT
        ws.cell(row=i, column=2).alignment = Alignment(horizontal="left")
        ws.cell(row=i, column=1).fill = PatternFill("solid", fgColor=LIGHT_BLUE)
        ws.cell(row=i, column=1).border = BORDER
        ws.cell(row=i, column=2).border = BORDER
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 45
    ws["A13"] = "说明：评分过程可分段进行，但请记录总时长；不要参考其他评分者的结果。"
    ws["A13"].font = Font(name="微软雅黑", size=9, italic=True, color="595959")


def build_instructions_sheet(wb: Workbook, n_rows: int, role: str) -> None:
    ws = wb.create_sheet("填写说明", 0)
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:F1")
    ws["A1"] = f"NutriAgent 修订版专家评分表 — {role}（{n_rows} 条）"
    ws["A1"].font = TITLE_FONT
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 34

    intro = [
        "感谢您参与本次盲评。本表用于 Agriculture Communications 大修稿的独立专家评分。",
        "7 个系统已匿名化为 Model_A–Model_G；同一 query_id 下的响应顺序已随机化。",
        "请独立评分，不要搜索原文、不要与作者讨论、不要尝试识别具体模型。",
        "中文题的回答为中文，英文题为英文；两种语言都需阅读。",
    ]
    for i, text in enumerate(intro, start=2):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        ws.cell(row=i, column=1, value=text).font = BODY_FONT
        ws.cell(row=i, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 22

    ws["A6"] = "评分维度"
    ws["A6"].font = Font(name="微软雅黑", size=12, bold=True, color=NAVY)
    headers = ["分数", "Correctness（正确性）", "Precision（数值精度）", "Scientific depth（科学深度）"]
    for j, h in enumerate(headers, start=1):
        c = ws.cell(row=7, column=j, value=h)
        c.font = HEADER_FONT
        c.fill = PatternFill("solid", fgColor=BLUE)
        c.alignment = CENTER
        c.border = BORDER
    rubric = [
        ("5", "所有事实准确，直接回答问题", "精确点估计，与参考值一致", "机制清楚，有实践语境"),
        ("4", "基本准确，仅有小瑕疵", "接近参考值（约 ±5% 内）", "领域知识较好"),
        ("3", "部分正确，有明显错误", "方向正确但偏差明显", "够用但停留在表层"),
        ("2", "多处事实错误", "模糊或明显不准确", "肤浅"),
        ("1", "完全错误或答非所问", "应给数值却没有给", "没有科学内容"),
    ]
    for i, row in enumerate(rubric, start=8):
        for j, value in enumerate(row, start=1):
            c = ws.cell(row=i, column=j, value=value)
            c.font = BODY_FONT
            c.alignment = CENTER if j == 1 else WRAP
            c.border = BORDER
    ws.column_dimensions["A"].width = 7
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 32
    ws.column_dimensions["D"].width = 32

    rules = [
        "Correctness 只评事实正确性；不要因文风、长度、是否引用来源而加减分。",
        "Precision 只用于有预期数值的题；定义、开放式、无数值边缘题填 N/A。",
        "多跳题按最终数值评 Precision；中间步骤错误但最终值对，Correctness 降、Precision 可高。",
        "定义题：定义准确、与相关概念的区别清楚可给 5；缺关键区别给 3–4。",
        "边缘题按真值表的 expected_behavior 判断（例如应说明“未找到”，不应编造）。",
        "Provenance（0–2）单独评分：0 无来源；1 部分关键数字有来源；2 全部关键数字有具名来源。",
        "Provenance 不影响 Correctness；如不愿评可留空。",
        "所有评分为 1–5 的整数，不要 0.5；除 Precision=N/A、Provenance 可空外不要留空。",
        "不要修改 query_id、顺序或 response 文本；notes 可记录歧义或真值疑问。",
    ]
    ws["A15"] = "关键规则"
    ws["A15"].font = Font(name="微软雅黑", size=12, bold=True, color=NAVY)
    for i, text in enumerate(rules, start=16):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        c = ws.cell(row=i, column=1, value="• " + text)
        c.font = BODY_FONT
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[i].height = 30

    ws["A26"] = "返回前检查"
    ws["A26"].font = Font(name="微软雅黑", size=12, bold=True, color=NAVY)
    checks = [
        f"评分表行数为 {n_rows}，query_id 未被改动；",
        "Correctness、Scientific depth 全部为 1–5 整数；",
        "Precision 在数值题上为 1–5、在非数值题上为 N/A；",
        "Provenance 为 0–2 或 NA/空；",
        "“评分记录”页已填写姓名/单位/时间；",
        "抽查 5 条，notes 与分数不矛盾。",
    ]
    for i, text in enumerate(checks, start=27):
        ws.merge_cells(start_row=i, start_column=1, end_row=i, end_column=6)
        ws.cell(row=i, column=1, value="□ " + text).font = BODY_FONT
        ws.row_dimensions[i].height = 20

    ws.merge_cells("A34:F34")
    ws["A34"] = "完整评分要求见同文件夹《01_评分要求与流程.docx》。"
    ws["A34"].font = Font(name="微软雅黑", size=9, italic=True, color="595959")


def build_workbook(path: Path, rows: list[dict], role: str) -> None:
    wb = Workbook()
    build_sheet(wb, rows)
    build_record_sheet(wb)
    build_instructions_sheet(wb, len(rows), role)
    wb.active = 0
    wb.save(path)

# ---------------------------------------------------------------- ground truth

def build_ground_truth(queries: list[dict]) -> None:
    rows = []
    for q in queries:
        base = flatten(q)
        base["scoring_note"] = scoring_note(q)
        rows.append(base)

    csv_path = RAW / "查询真值表.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path = OUT / "查询真值表.json"
    json_path.write_text(json.dumps({"queries": rows}, ensure_ascii=False, indent=2), encoding="utf-8")

    wb = Workbook()
    ws = wb.active
    ws.title = "查询真值表"
    headers = ["query_id", "category", "query_type", "language", "query", "query_note",
               "expected_value", "expected_unit", "expected_behavior", "target_doc",
               "review", "scoring_note"]
    ws.append(headers)
    style_header(ws, len(headers))
    set_widths(ws, {"A": 12, "B": 20, "C": 13, "D": 8, "E": 45, "F": 30,
                    "G": 12, "H": 10, "I": 38, "J": 35, "K": 22, "L": 45})
    for r in rows:
        ws.append([r[h] for h in headers])
        row = ws.max_row
        for c in range(1, len(headers) + 1):
            cell = ws.cell(row=row, column=c)
            cell.font = BODY_FONT
            cell.border = BORDER
            cell.alignment = CENTER if c in (1, 3, 4, 7, 8) else WRAP
        ws.row_dimensions[row].height = 42
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:L{ws.max_row}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    info = wb.create_sheet("使用说明", 0)
    info.sheet_view.showGridLines = False
    info["A1"] = "查询真值表 — 仅供评分参考"
    info["A1"].font = TITLE_FONT
    info.merge_cells("A3:H3")
    info["A3"] = ("本表给出 54 条查询的参考答案/预期行为。数值题为 expected_value + expected_unit；"
                  "定义/开放式/边缘题的 expected_behavior 或 scoring_note 说明评分要点。")
    info["A3"].font = BODY_FONT
    info["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    info.row_dimensions[3].height = 50
    notes = [
        "数值题允许合理单位换算和四舍五入；±5% 内可视为接近。",
        "多跳题按最终数值评分；中间步骤错误但最终值正确，Correctness 降、Precision 可高。",
        "定义题无预期数值，Precision 填 N/A。",
        "边缘题按 expected_behavior 判断：应说明未找到/不适用，而不是编造。",
        "若您认为真值有误，请在评分表 notes 中注明，不要自行修改真值表。",
    ]
    for i, text in enumerate(notes, start=5):
        info.merge_cells(start_row=i, start_column=1, end_row=i, end_column=8)
        info.cell(row=i, column=1, value="• " + text).font = BODY_FONT
        info.cell(row=i, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        info.row_dimensions[i].height = 30
    wb.save(OUT / "04_查询真值表.xlsx")

# ---------------------------------------------------------------- docx

def set_cn(run, size=10.5, bold=False, color=None):
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color


def add_para(doc, text, size=10.5, bold=False, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    set_cn(p.add_run(text), size, bold)
    return p


def add_bullets(doc, items):
    for text in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.2
        set_cn(p.add_run(text), 10.5)


def build_docx(path: Path) -> None:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cn(title.add_run("NutriAgent 修订版专家评分说明"), 18, True)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cn(sub.add_run("Agriculture Communications 大修 · 匿名专家评分"), 10.5, False)

    add_para(doc, "一、背景与目的", 13, True)
    add_para(doc, "本评分用于 Agriculture Communications 大修稿的独立专家复核。7 个系统已匿名化为 "
                  "Model_A–Model_G；主表 378 条（54 题 × 7 系统），第二专家子集 120 条（覆盖全部 54 题）。"
                  "评分将替换投稿版专家分，并用于计算评分者间一致性（ICC、weighted kappa、Bland–Altman）。")

    add_para(doc, "二、文件清单", 13, True)
    add_bullets(doc, [
        "02_主专家评分表_378条.xlsx：主专家填写；含“评分表”“评分记录”“填写说明”三页。",
        "03_第二专家评分表_120条.xlsx：第二专家填写；结构相同，120 条。",
        "04_查询真值表.xlsx：54 题参考答案/预期行为，仅供评分参考（另附 JSON 版）。",
        "原始CSV/：与 Excel 内容相同的 CSV，便于程序读取或备份。",
    ])

    add_para(doc, "二·补充：题面澄清", 13, True)
    add_bullets(doc, [
        "C-XD-005：其余 40% 为 SBM48，因此原配方 SBM48 为 40%；答案为 +4.33 个百分点。",
        "C-XD-006：请报告新配方减原配方的 CP 贡献变化（百分点），不是只报新贡献 11.70%；应为下降 1.45 个百分点。",
        "C-FIB-004 / C-FIB-010：请使用 feed ingredient bank 的 ME 值，以 kcal/kg 表示（可接受 MJ/kg 换算）。",
        "C-FIB-005：请使用 feed ingredient bank 的 CP 值，以 % 表示。",
        "C-EC-005：请说明鱼粉与石灰石的 ME；石灰石为矿物质，ME=0。",
    ])

    add_para(doc, "三、盲评规则", 13, True)
    add_bullets(doc, [
        "不要搜索响应原文、不要与作者讨论评分、不要尝试识别具体模型。",
        "按 query_id 逐题评分；同一题的 7 条响应顺序已随机化，不要跨题比较。",
        "中文题的回答为中文，英文题为英文；两种语言都需阅读。",
        "不要修改 query_id、响应顺序或 response 文本；notes 可记录歧义。",
        "主专家与第二专家应独立评分，不互相参考。",
    ])

    add_para(doc, "四、评分维度", 13, True)
    add_para(doc, "1. Correctness（正确性，1–5）", 11, True)
    add_bullets(doc, [
        "5 = 所有事实准确，直接回答问题；4 = 基本准确，仅有小瑕疵；3 = 部分正确，有明显错误；"
        "2 = 多处事实错误；1 = 完全错误或答非所问。",
        "只评事实正确性；不要因文风、长度、是否引用来源而加减分。",
        "与参考答案不一致但给出合理单位换算/四舍五入，不扣分。",
    ])
    add_para(doc, "2. Precision（数值精度，1–5 或 N/A）", 11, True)
    add_bullets(doc, [
        "仅用于有预期数值的题；定义、开放式、无数值边缘题填 N/A。",
        "5 = 精确匹配；4 = 接近（约 ±5% 内或合理舍入）；3 = 方向对但偏差明显；"
        "2 = 模糊或明显不准确；1 = 应给数值却没有给。",
        "多跳题按最终数值评；中间步骤错误但最终值对，Correctness 降、Precision 可高。",
    ])
    add_para(doc, "3. Scientific depth（科学深度，1–5）", 11, True)
    add_bullets(doc, [
        "5 = 机制清楚且有实践语境；4 = 领域知识较好；3 = 够用但表层；2 = 肤浅；1 = 无科学内容。",
    ])
    add_para(doc, "4. Provenance（来源标注，0–2，可选）", 11, True)
    add_bullets(doc, [
        "0 = 无来源；1 = 部分关键数字有工具/来源；2 = 全部关键数字有具名工具/来源。",
        "独立于 Correctness，不因引用加分；如不愿评可留空。",
    ])

    add_para(doc, "五、评分标准表", 13, True)
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = ["分数", "Correctness", "Precision（数值）", "Scientific depth"]
    for i, h in enumerate(hdr):
        cell = table.rows[0].cells[i]
        cell.text = ""
        set_cn(cell.paragraphs[0].add_run(h), 9.5, True)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    rubric = [
        ("5", "所有事实准确，直接回答", "精确点估计，与参考一致", "机制清楚，有实践语境"),
        ("4", "基本准确，仅有小瑕疵", "接近参考（约 ±5% 内）", "领域知识较好"),
        ("3", "部分正确，有明显错误", "方向对但偏差明显", "够用但表层"),
        ("2", "多处事实错误", "模糊或明显不准确", "肤浅"),
        ("1", "完全错误或答非所问", "应给数值却没给", "无科学内容"),
    ]
    for row in rubric:
        cells = table.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            set_cn(cells[i].paragraphs[0].add_run(v), 9)
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
    for row in table.rows:
        for cell in row.cells:
            cell.width = Cm(4.0)

    add_para(doc, "六、填表规则", 13, True)
    add_bullets(doc, [
        "所有 1–5 分为整数，不要 0.5；除 Precision=N/A、Provenance 可空外不要留空。",
        "不要合并单元格、不要插入/删除行、不要改列名。",
        "notes 可选：记录歧义、真值疑问、明显错误；不要写模型猜测。",
        "若 response 单元格显示不全，可拉高行高或在编辑栏查看完整文本；不要修改文本。",
        "“评分记录”页填写姓名、单位、日期、开始/结束时间、总时长。",
    ])

    add_para(doc, "七、时间与返回", 13, True)
    add_bullets(doc, [
        "主表预计 2–3 个工作日；第二专家子集预计 1–2 个工作日。",
        "返回文件名：主专家_评分完成_日期.xlsx；第二专家_评分完成_日期.xlsx。",
        "返回前请按“填写说明”页的检查清单核对行数与空值。",
        "联系人/返回邮箱：[请作者填写]。",
    ])

    add_para(doc, "八、保密与致谢", 13, True)
    add_para(doc, "评分表与响应内容仅用于本稿评审，不对外传播；模型身份映射由通讯作者保管，不随表发送。"
                  "两位评分者应独立于系统开发，与作者无财务/利益关系；如存在需事先说明。"
                  "我们将在致谢中列明两位专家的贡献（审稿期间匿名）。")

    doc.save(path)

# ---------------------------------------------------------------- README

def build_readme() -> None:
    text = """# NutriAgent 专家评分包（2026-10-21）

本文件夹用于 Agriculture Communications 大修稿的独立专家评分。请先读
`01_评分要求与流程.docx`，再填写对应的 Excel 表。

## 文件

| 文件 | 用途 |
|---|---|
| `01_评分要求与流程.docx` | 完整评分要求、rubric、填表与返回规则 |
| `02_主专家评分表_378条.xlsx` | 主专家：54 题 × 7 匿名系统 = 378 条 |
| `03_第二专家评分表_120条.xlsx` | 第二专家：覆盖 54 题的 120 条子集 |
| `04_查询真值表.xlsx` | 54 题参考答案/预期行为；评分时参考 |
| `原始CSV/` | 同内容的 CSV，便于程序读取/备份 |

## 题面澄清

评分表新增 `query_note` 列，标出需要说明的题面；真值表 `expected_behavior` 给出完整参考答案。重点：

- `C-XD-005`：其余 40% 为 SBM48；答案 +4.33 个百分点。
- `C-XD-006`：报告“变化”，不是只报新贡献 11.70%；应为下降 1.45 个百分点。
- `C-FIB-004 / C-FIB-010`：使用 feed ingredient bank 的 ME，kcal/kg。
- `C-FIB-005`：使用 feed ingredient bank 的 CP，%。
- `C-EC-005`：鱼粉 vs 石灰石；石灰石 ME=0。

## 快速步骤

1. 打开对应 Excel，先看“填写说明”页；
2. 按 `query_id` 逐题评分，同一题内 7 条（或 2 条）响应一起看；
3. 填 `correctness`、`precision`（无数值填 N/A）、`scientific_depth`；
4. `provenance` 可选（0–2）；`notes` 可选；
5. 若 response 显示不全，可拉高行高或在编辑栏查看；
6. 在“评分记录”页填写姓名/单位/时间；
7. 另存为 `主专家_评分完成_日期.xlsx` 或 `第二专家_评分完成_日期.xlsx` 返回。

## 重要

- 7 个系统匿名化为 `Model_A`–`Model_G`；请勿尝试识别具体模型。
- 中文题的回答为中文，英文题为英文；两种语言都需阅读。
- 不要搜索响应原文、不要与作者讨论评分、不要修改 response 文本。
- 主专家与第二专家必须独立评分。
- 评分者应独立于系统开发，与作者无财务/利益关系；如存在请事先说明。
- 若认为某题真值有误，请在 `notes` 中注明，不要改真值表。

联系人/返回邮箱：[请作者填写]
"""
    (OUT / "README_先读我.md").write_text(text, encoding="utf-8")

# ---------------------------------------------------------------- main

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(exist_ok=True)

    queries = load_queries()
    primary = load_rows(PRIMARY_CSV)
    second = load_rows(SECOND_CSV)

    # Keep the primary order (grouped by query, shuffled within query).
    # Sort the second-rater subset by query_id so each query's two responses are adjacent.
    second = sorted(second, key=lambda r: (r["query_id"], r["model_id"]))

    build_workbook(OUT / "02_主专家评分表_378条.xlsx", primary, "主专家")
    build_workbook(OUT / "03_第二专家评分表_120条.xlsx", second, "第二专家")
    build_ground_truth(queries)
    build_docx(OUT / "01_评分要求与流程.docx")
    build_readme()

    shutil.copy2(PRIMARY_CSV, RAW / "主专家_原始表_378.csv")
    shutil.copy2(SECOND_CSV, RAW / "第二专家_原始表_120.csv")

    print("Wrote", OUT)
    for p in sorted(OUT.rglob("*")):
        print(" ", p.relative_to(OUT), p.stat().st_size if p.is_file() else "")


if __name__ == "__main__":
    main()
