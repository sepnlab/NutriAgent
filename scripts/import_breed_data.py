r"""
Import breed data from Chinese Markdown manual to project CSVs,
with LLM verification loop.

Usage:
  # 查看所有品种的列表
  .venv\Scripts\python scripts/import_breed_data.py --list-manuals

  # 导入单个品种（第一轮：替换 AI-gen）
  .venv\Scripts\python scripts/import_breed_data.py ^
    --md-file "D:/Geqi_series/饲养管理手册/海兰W36/海兰 W36 商品代蛋鸡饲养管理手册（数据整理版）.md" ^
    --breed "Hy-Line W-36" --species layer --replace

  # 导入新品种（追加）
  .venv\Scripts\python scripts/import_breed_data.py ^
    --md-file "D:/Geqi_series/饲养管理手册/京红1号3.0/京红 1 号蛋鸡配套生产与营养标准汇总.md" ^
    --breed "Jinghong 1 v3.0" --species layer

  # 只提取部分数据类别
  .venv\\Scripts\\python scripts/import_breed_data.py ^
    --md-file "xxx.md" --breed "Beinong 1" --species layer ^
    --only performance

  # 跳过验证（调试用）
  .venv\Scripts\python scripts/import_breed_data.py ^
    --md-file "xxx.md" --breed "Test" --species layer --skip-verify
"""
import argparse
import csv
import json
import os
import re
import sys
import time

# 加入项目根目录
_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, _PROJECT_ROOT)

from dotenv import load_dotenv
load_dotenv()

# ── CSV Schema ──────────────────────────────────────────────────────────────

PERFORMANCE_HEADER = [
    "Breed", "Week", "HenDay_Prod_Pct", "Egg_Wt_g", "Egg_Mass_g_per_d",
    "FI_g_per_d", "Feed_per_Dozen_kg", "Feed_per_kg_Egg_kg", "BW_g",
    "Mortality_Pct", "Shell_Strength_N", "Haugh_Unit", "Cumul_Egg_Count",
    "Water_Intake_ml_d", "raw_range", "source",
]

NUTRIENT_HEADER = [
    "Breed", "Phase", "ME_kcal_kg", "CP_pct", "Ca_pct", "Avail_P_pct",
    "Na_pct", "Lys_pct", "Met_pct", "M_C_pct", "Thr_pct", "Trp_pct",
    "Val_pct", "Arg_pct", "Ile_pct", "SID_Lys_pct", "SID_Met_pct",
    "SID_M_C_pct", "SID_Thr_pct", "SID_Trp_pct", "Choline_mg_kg",
    "Linoleic_Acid_pct", "raw_range", "source",
]

VITAMIN_HEADER = [
    "Breed", "Phase", "Vitamin_A_IU_kg", "Vitamin_D3_IU_kg",
    "Vitamin_E_IU_kg", "Vitamin_K3_mg_kg", "Vitamin_B1_mg_kg",
    "Vitamin_B2_mg_kg", "Vitamin_B6_mg_kg", "Vitamin_B12_mcg_kg",
    "Niacin_mg_kg", "Pantothenic_Acid_mg_kg", "Folic_Acid_mg_kg",
    "Biotin_mcg_kg", "Fe_mg_kg", "Cu_mg_kg", "Zn_mg_kg", "Mn_mg_kg",
    "Se_mg_kg", "I_mg_kg", "raw_range", "source",
]

BROILER_PERFORMANCE_HEADER = [
    "Genetic_Line", "Sex", "Day", "BW_g", "ADG_g", "FI_g_per_day",
    "Cumulative_FI_g", "FCR", "raw_range", "source",
]

# ── LLM Client ─────────────────────────────────────────────────────────────

def _get_client():
    """Create OpenAI-compatible client from project config."""
    from openai import OpenAI
    base_url = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    api_key = os.getenv("SILICONFLOW_API_KEY", "")
    return OpenAI(base_url=base_url, api_key=api_key), base_url, api_key


def _call_llm(system_prompt, user_prompt, model=None, temperature=0.1,
              response_format=None, max_tokens=4096, timeout=60):
    """Call LLM with retry."""
    client, base_url, api_key = _get_client()
    model = model or os.getenv("LLM_MODEL", "deepseek-ai/DeepSeek-V4-Flash")

    kwargs = dict(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    if response_format:
        kwargs["response_format"] = response_format

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content
        except Exception as e:
            print(f"  [LLM retry {attempt + 1}/3] {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after 3 retries")


# ── Markdown Reading ───────────────────────────────────────────────────────

def _read_md(filepath):
    """Read Markdown file, return raw text and sections."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 按 ## 一级标题切分
    sections = re.split(r"\n(?=##\s)", text)
    return text, sections


def _find_sections_by_keywords(sections, keywords):
    """Find sections whose title contains any of the keywords."""
    matched = []
    for sec in sections:
        first_line = sec.split("\n")[0].strip()
        for kw in keywords:
            if kw in first_line.lower():
                matched.append(sec)
                break
    return matched


# ── Extraction Prompts ─────────────────────────────────────────────────────

EXTRACT_PERFORMANCE_SYSTEM = """你是一个家禽营养数据提取专家。你的任务是从中文蛋鸡饲养管理手册的 Markdown 表格中，提取周龄生产性能数据并转为 JSON。

规则：
1. 只输出一个 JSON 数组，数组每个元素是一个周的数据
2. WEEK 列 —— 从表格第一列提取周龄
3. 数值如有范围（如 "95-96"），取中值（95.5）
4. 单位统一：体重用克(g)、采食用克/天、蛋重用克、产蛋率用%
5. RAW_RANGE 列保留原始范围文本（如 "95-96"），定值则为空字符串
6. 某字段表格中无数据则输出 null
7. SOURCE 列固定填 "Hy-Line Official Manual"（对应品牌替换）
8. BREED 列固定为指定的品种名
9. 字段名使用下面的 schema 定义

字段定义（-> 前是 CSV 列名，-> 后是说明）：
- week: 周龄（整数）
- hen_day_prod_pct: 饲养日产蛋率（%）
- egg_wt_g: 平均蛋重（克）
- fi_g_per_d: 日采食量（克/只/天）
- bw_g: 体重（克）
- mortality_pct: 死淘率（%）
- shell_strength_n: 蛋壳强度
- haugh_unit: 哈氏单位
- cumul_egg_count: 累计饲养日产蛋数（枚）
- water_intake_ml_d: 日饮水量（毫升/只/天）
- raw_range: 原始范围文本

输出示例：
[
  {
    "breed": "Hy-Line W-36",
    "week": 1,
    "hen_day_prod_pct": 0,
    "egg_wt_g": null,
    "fi_g_per_d": 14.5,
    "bw_g": 66.5,
    "mortality_pct": 0.75,
    "shell_strength_n": null,
    "haugh_unit": null,
    "cumul_egg_count": null,
    "water_intake_ml_d": 26,
    "raw_range": "60-73"
  }
]

注意：育雏育成期（周龄<18）产蛋率为0，蛋重为null。
"""

EXTRACT_NUTRIENT_SYSTEM = """你是一个家禽营养数据提取专家。你的任务是从中文蛋鸡饲养管理手册的 Markdown 表格中，提取分阶段营养需要量并转为 JSON。

规则：
1. 只输出一个 JSON 数组
2. PHASE 列 —— 根据表格列标题判断阶段名称，统一用英文（如 Starter 0-3w, Grower 4-6w, Layer I 21-40w 等）
3. 数值如有范围取中值
4. RAW_RANGE 列保留原始范围文本
5. 无数据则输出 null
6. SOURCE 列固定为 "Hy-Line Official Manual"（对应品牌）
7. BREED 列固定为指定的品种名

字段：
- breed: 品种名
- phase: 阶段名（用英文）
- me_kcal_kg: 代谢能（千卡/千克）
- cp_pct: 粗蛋白（%）
- ca_pct: 钙（%）
- avail_p_pct: 有效磷（%）
- na_pct: 钠（%）
- lys_pct: 赖氨酸（%）
- met_pct: 蛋氨酸（%）
- m_c_pct: 蛋氨酸+胱氨酸（%）
- thr_pct: 苏氨酸（%）
- trp_pct: 色氨酸（%）
- val_pct: 缬氨酸（%）
- arg_pct: 精氨酸（%）
- ile_pct: 异亮氨酸（%）
- sid_lys_pct: 可消化赖氨酸（%）
- sid_met_pct: 可消化蛋氨酸（%）
- sid_m_c_pct: 可消化蛋氨酸+胱氨酸（%）
- sid_thr_pct: 可消化苏氨酸（%）
- sid_trp_pct: 可消化色氨酸（%）
- choline_mg_kg: 胆碱（毫克/千克）
- linoleic_acid_pct: 亚油酸（%）
- raw_range: 原始范围文本

注意：
- 中文"有效磷"=Avail_P_pct
- 中文"可利用磷"=Avail_P_pct
- "代谢能"若无千卡单位但有兆焦，需转换（1 MJ = 239 kcal）
- 表格列名可能含"可消化"或"SID"前缀
"""

EXTRACT_VITAMIN_SYSTEM = """你是一个家禽营养数据提取专家。你的任务是从中文蛋鸡饲养管理手册中提取维生素和微量元素添加标准并转为 JSON。

规则：
1. 只输出一个 JSON 数组
2. PHASE 列用英文（如 Starter 0-18w, Layer 等）
3. 数值如有范围取中值
4. 单位注意：维生素 A/D3 用 IU/kg，B族用 mg/kg，B12/生物素用 mcg/kg
5. 如果表格中的值是"每1000kg饲料"的量，换算到每kg
6. RAW_RANGE 保留原始范围文本
7. 无数据则输出 null

字段：
- breed, phase, raw_range
- vitamin_a_iu_kg, vitamin_d3_iu_kg, vitamin_e_iu_kg, vitamin_k3_mg_kg
- vitamin_b1_mg_kg, vitamin_b2_mg_kg, vitamin_b6_mg_kg, vitamin_b12_mcg_kg
- niacin_mg_kg, pantothenic_acid_mg_kg, folic_acid_mg_kg, biotin_mcg_kg
- fe_mg_kg, cu_mg_kg, zn_mg_kg, mn_mg_kg, se_mg_kg, i_mg_kg
"""

EXTRACT_BROILER_SYSTEM = """你是一个家禽数据提取专家。从肉鸡饲养手册中提取日龄生产性能数据并转为 JSON。

规则：同上（范围取中值、单位统一等）。

字段：
- genetic_line: 品种名
- sex: 性别（"Mixed" 默认）
- day: 日龄
- bw_g: 体重（克）
- adg_g: 日增重（克）
- fi_g_per_day: 日采食量（克/天）
- cumulative_fi_g: 累计采食量（克）
- fcr: 饲料转化比
- raw_range: 原始范围文本
"""

# ── Verification Prompt ────────────────────────────────────────────────────

VERIFY_SYSTEM = """你是一个数据质量检查员。你的任务是比较"原始 Markdown 内容"与"提取的 CSV 数据"，找出不一致之处。

检查要点：
1. 数值一致性：CSV 中的值是否与 Markdown 表格中对应（取中值后）
2. 行数完整性：是否有漏掉的行（某些周龄或阶段未提取）
3. 列映射正确性：是否把产蛋率填到了蛋重列等
4. 阶段命名合理性：阶段名称是否反映了正确的周龄范围
5. 单位正确性：是否混淆了千克/克等

输出格式（严格 JSON）：
{"status": "PASS"}

或发现问题时：
{
  "status": "FAIL",
  "issues": [
    {
      "row": "week 30",
      "field": "hen_day_prod_pct",
      "expected": 96.0,
      "got": 95.5,
      "note": "30周产蛋率应该是96.0%不是95.5%"
    }
  ],
  "corrected_data": [
    {
      ... 修正后的完整数据行
    }
  ]
}

注意：
- 数值差异在±0.5以内算正确（四舍五入差异）
- 如果多项错误，全部列出
- corrected_data 应包含所有行（不仅仅是错误行），用修正后的值替换错误值
"""


# ── CSV I/O ────────────────────────────────────────────────────────────────

def _get_csv_path(species, data_type):
    """Get path to target CSV file."""
    if species == "broiler" and data_type == "performance":
        return os.path.join(_PROJECT_ROOT, "corpus", "broiler", "performance_management.csv")
    base = os.path.join(_PROJECT_ROOT, "corpus", species)
    files = {
        "performance": "performance_management.csv",
        "nutrient": "nutrient_requirements.csv",
        "vitamin": "nutrient_vitamin_mineral.csv",
    }
    return os.path.join(base, files[data_type])


def _read_csv(path):
    """Read CSV into list of dicts."""
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows


def _write_csv(path, rows, header):
    """Write list of dicts to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _append_csv(path, new_rows, header):
    """Append new rows to existing CSV, updating if breed exists."""
    existing = _read_csv(path)
    breed_col = header[0]  # 第一列是品种名

    # 过滤掉要替换/更新的品种
    if new_rows:
        target_breed = new_rows[0].get(breed_col, "")
        existing = [r for r in existing if r.get(breed_col, "") != target_breed]

    # 合并
    all_rows = existing + new_rows

    # 确保所有行都有所有列
    for row in all_rows:
        for col in header:
            if col not in row:
                row[col] = ""

    _write_csv(path, all_rows, header)
    print(f"  -> {path} ({len(new_rows)} rows added, total {len(all_rows)})")


# ── Extract → Verify → Fix Loop ────────────────────────────────────────────

def _extract_json(text, system_prompt, breed, source_label, max_retries=3):
    """Send Markdown text to LLM, get JSON array back."""
    user_prompt = (
        f"品种名: {breed}\n"
        f"来源标签: {source_label}\n\n"
        f"以下是需要提取的 Markdown 内容:\n\n{text}\n\n"
        f"输出 JSON 数组。如无相关数据，输出 []。"
    )

    for attempt in range(max_retries):
        print(f"  [LLM extract attempt {attempt + 1}/{max_retries}]")
        raw = _call_llm(system_prompt, user_prompt)

        # 从回复中提取 JSON
        json_str = _extract_json_from_text(raw)
        if not json_str:
            print(f"    WARN: No JSON found in LLM response, retrying...")
            continue

        try:
            data = json.loads(json_str)
            if not isinstance(data, list):
                data = [data]
            print(f"    -> {len(data)} rows extracted")
            return data
        except json.JSONDecodeError as e:
            print(f"    JSON parse error: {e}, retrying...")
            continue

    print(f"    FAILED to extract after {max_retries} attempts")
    return []


def _extract_json_from_text(text):
    """Extract JSON array/object from text that may contain markdown fences."""
    # 去掉 ``` 代码块标记
    text_clean = re.sub(r"```(?:json)?\s*\n?", "", text)
    text_clean = re.sub(r"\n?```", "", text_clean).strip()

    # 尝试找 JSON 数组 [ ... ]
    # 用 stack 匹配最外层 []
    if "[" in text_clean:
        start = text_clean.index("[")
        depth = 0
        for i in range(start, len(text_clean)):
            if text_clean[i] == "[":
                depth += 1
            elif text_clean[i] == "]":
                depth -= 1
                if depth == 0:
                    candidate = text_clean[start:i+1]
                    try:
                        json.loads(candidate)
                        return candidate
                    except json.JSONDecodeError:
                        pass
        # 如果完整数组解析失败，试试松散解析
        try:
            json.loads(text_clean[start:])
            return text_clean[start:]
        except json.JSONDecodeError:
            pass

    # 尝试找 JSON 对象 { ... }
    if "{" in text_clean:
        start = text_clean.index("{")
        depth = 0
        for i in range(start, len(text_clean)):
            if text_clean[i] == "{":
                depth += 1
            elif text_clean[i] == "}":
                depth -= 1
                if depth == 0:
                    candidate = text_clean[start:i+1]
                    try:
                        json.loads(candidate)
                        return candidate
                    except json.JSONDecodeError:
                        pass

    return None


def _map_json_to_csv(data, header, breed, source_label, data_type="performance"):
    """Map JSON keys to CSV columns."""
    key_map = {
        # performance
        "week": "Week",
        "hen_day_prod_pct": "HenDay_Prod_Pct",
        "egg_wt_g": "Egg_Wt_g",
        "egg_mass_g_per_d": "Egg_Mass_g_per_d",
        "fi_g_per_d": "FI_g_per_d",
        "feed_per_dozen_kg": "Feed_per_Dozen_kg",
        "feed_per_kg_egg_kg": "Feed_per_kg_Egg_kg",
        "bw_g": "BW_g",
        "mortality_pct": "Mortality_Pct",
        "shell_strength_n": "Shell_Strength_N",
        "haugh_unit": "Haugh_Unit",
        "cumul_egg_count": "Cumul_Egg_Count",
        "water_intake_ml_d": "Water_Intake_ml_d",
        # nutrient
        "phase": "Phase",
        "me_kcal_kg": "ME_kcal_kg",
        "cp_pct": "CP_pct",
        "ca_pct": "Ca_pct",
        "avail_p_pct": "Avail_P_pct",
        "na_pct": "Na_pct",
        "lys_pct": "Lys_pct",
        "met_pct": "Met_pct",
        "m_c_pct": "M_C_pct",
        "thr_pct": "Thr_pct",
        "trp_pct": "Trp_pct",
        "val_pct": "Val_pct",
        "arg_pct": "Arg_pct",
        "ile_pct": "Ile_pct",
        "sid_lys_pct": "SID_Lys_pct",
        "sid_met_pct": "SID_Met_pct",
        "sid_m_c_pct": "SID_M_C_pct",
        "sid_thr_pct": "SID_Thr_pct",
        "sid_trp_pct": "SID_Trp_pct",
        "choline_mg_kg": "Choline_mg_kg",
        "linoleic_acid_pct": "Linoleic_Acid_pct",
        # vitamin
        "vitamin_a_iu_kg": "Vitamin_A_IU_kg",
        "vitamin_d3_iu_kg": "Vitamin_D3_IU_kg",
        "vitamin_e_iu_kg": "Vitamin_E_IU_kg",
        "vitamin_k3_mg_kg": "Vitamin_K3_mg_kg",
        "vitamin_b1_mg_kg": "Vitamin_B1_mg_kg",
        "vitamin_b2_mg_kg": "Vitamin_B2_mg_kg",
        "vitamin_b6_mg_kg": "Vitamin_B6_mg_kg",
        "vitamin_b12_mcg_kg": "Vitamin_B12_mcg_kg",
        "niacin_mg_kg": "Niacin_mg_kg",
        "pantothenic_acid_mg_kg": "Pantothenic_Acid_mg_kg",
        "folic_acid_mg_kg": "Folic_Acid_mg_kg",
        "biotin_mcg_kg": "Biotin_mcg_kg",
        "fe_mg_kg": "Fe_mg_kg",
        "cu_mg_kg": "Cu_mg_kg",
        "zn_mg_kg": "Zn_mg_kg",
        "mn_mg_kg": "Mn_mg_kg",
        "se_mg_kg": "Se_mg_kg",
        "i_mg_kg": "I_mg_kg",
        # broiler
        "genetic_line": "Genetic_Line",
        "sex": "Sex",
        "day": "Day",
        "adg_g": "ADG_g",
        "fi_g_per_day": "FI_g_per_day",
        "cumulative_fi_g": "Cumulative_FI_g",
        "fcr": "FCR",
    }

    rows = []
    for item in data:
        row = {}
        # 品种名列
        if "breed" in item:
            row[header[0]] = item["breed"]
        elif "genetic_line" in item:
            row["Genetic_Line"] = item["genetic_line"]
        else:
            row[header[0]] = breed

        # 来源列
        if "source" not in item and header[-1] == "source":
            row["source"] = source_label
        if "raw_range" in item and "raw_range" in header:
            row["raw_range"] = item.get("raw_range", "")

        # 映射其他字段
        for json_key, csv_key in key_map.items():
            if csv_key not in header:
                continue
            if json_key in item and item[json_key] is not None:
                row[csv_key] = str(item[json_key])
            elif csv_key not in row:
                row[csv_key] = ""

        rows.append(row)

    return rows


def _verify_extraction(md_text, csv_rows, header, data_type):
    """Use LLM to verify extracted CSV data against original Markdown."""
    # Serialize CSV rows for verification
    csv_preview = "\n".join([",".join(str(r.get(c, "")) for c in header) for r in csv_rows[:30]])
    if len(csv_rows) > 30:
        csv_preview += f"\n... ({len(csv_rows)} total rows)"

    user_prompt = (
        f"## 原始 Markdown 内容\n\n{md_text[:4000]}\n\n"
        f"## 提取的 CSV 数据（{data_type}）\n\n"
        f"Header: {','.join(header)}\n"
        f"Rows:\n{csv_preview}\n\n"
        f"请检查数据是否正确提取。输出 JSON 格式: {{\"status\": \"PASS\"}} 或 {{\"status\": \"FAIL\", \"issues\": [...], \"corrected_data\": [...]}}"
    )

    raw = _call_llm(VERIFY_SYSTEM, user_prompt, temperature=0.0)
    json_str = _extract_json_from_text(raw)

    if not json_str:
        print(f"    [VERIFY] WARN: No JSON in verification response")
        return {"status": "WARN", "message": "Verification response unparseable"}

    try:
        result = json.loads(json_str)
        # LLM might return [] (no issues) instead of {"status": "PASS"}
        if isinstance(result, list):
            if len(result) == 0:
                return {"status": "PASS", "message": "No issues found (empty array)"}
            # List of issues - convert to FAIL format
            return {"status": "FAIL", "issues": result, "corrected_data": []}
        return result
    except json.JSONDecodeError:
        return {"status": "WARN", "message": "Verification response not valid JSON"}


# ── Main Import Logic ──────────────────────────────────────────────────────

def process_breed(md_path, breed_name, species, source_label, replace,
                  data_types, skip_verify):
    """Process a breed: extract → verify → fix loop."""
    print(f"\n{'='*60}")
    print(f"Processing: {breed_name} ({species})")
    print(f"  MD: {md_path}")
    print(f"  Data types: {data_types}")
    print(f"  Replace existing: {replace}")
    print(f"  Skip verify: {skip_verify}")
    print(f"{'='*60}")

    # Read the Markdown
    md_text, sections = _read_md(md_path)
    print(f"  Sections found: {len(sections)}")

    # ── Performance ──
    if "performance" in data_types:
        print("\n--- Performance ---")
        # Find relevant sections
        perf_keywords = ["生产性能", "周龄生产", "产蛋", "育雏", "育成",
                         "体重", "耗料", "采食"]
        perf_sections = _find_sections_by_keywords(sections, perf_keywords)
        perf_md = "\n\n".join(perf_sections) if perf_sections else md_text[:6000]

        # Extract
        data = _extract_json(perf_md, EXTRACT_PERFORMANCE_SYSTEM,
                             breed_name, source_label)
        if not data:
            print("  No performance data extracted")
        else:
            # Map to CSV
            if species == "broiler":
                header = BROILER_PERFORMANCE_HEADER
            else:
                header = PERFORMANCE_HEADER
            csv_rows = _map_json_to_csv(data, header, breed_name,
                                        source_label, "performance")

            if not skip_verify:
                # Verify
                for v_attempt in range(3):
                    print(f"  [Verify attempt {v_attempt + 1}/3]")
                    v_result = _verify_extraction(
                        perf_md[:5000], csv_rows, header, "performance")

                    if v_result.get("status") == "PASS":
                        print("    [OK] Verification PASSED")
                        break
                    elif v_result.get("status") == "FAIL":
                        print(f"    [ISSUES] Found {len(v_result.get('issues', []))}")
                        for issue in v_result.get("issues", []):
                            print(f"       - {issue.get('row')}/{issue.get('field')}: "
                                  f"expected {issue.get('expected')}, got {issue.get('got')}")
                        # Apply corrections
                        corrected = v_result.get("corrected_data")
                        if corrected:
                            csv_rows = _map_json_to_csv(
                                corrected, header, breed_name,
                                source_label, "performance")
                            print(f"    Corrected data applied ({len(csv_rows)} rows)")
                        continue
                    else:
                        print(f"    [?] Verification uncertain: {v_result.get('message', '')}")
                        break
                else:
                    print("    [WARN] Max verify attempts reached, using last version")

            # Write to CSV
            csv_path = _get_csv_path(species, "performance")
            _append_csv(csv_path, csv_rows, header)

    # ── Nutrient ──
    if "nutrient" in data_types:
        print("\n--- Nutrient ---")
        nut_keywords = ["营养", "营养需求", "营养标准", "营养浓度",
                        "氨基酸", "蛋白", "代谢能"]
        nut_sections = _find_sections_by_keywords(sections, nut_keywords)
        nut_md = "\n\n".join(nut_sections) if nut_sections else ""

        if nut_md.strip():
            data = _extract_json(nut_md, EXTRACT_NUTRIENT_SYSTEM,
                                 breed_name, source_label)
            if data:
                header = NUTRIENT_HEADER
                csv_rows = _map_json_to_csv(data, header, breed_name,
                                            source_label, "nutrient")
                if not skip_verify:
                    for v_attempt in range(3):
                        v_result = _verify_extraction(
                            nut_md[:5000], csv_rows, header, "nutrient")
                        if v_result.get("status") == "PASS":
                            break
                        elif v_result.get("status") == "FAIL":
                            corrected = v_result.get("corrected_data")
                            if corrected:
                                csv_rows = _map_json_to_csv(
                                    corrected, header, breed_name,
                                    source_label, "nutrient")
                            continue
                        else:
                            break

                csv_path = _get_csv_path(species, "nutrient")
                _append_csv(csv_path, csv_rows, header)
            else:
                print("  No nutrient data extracted")
        else:
            print("  No nutrient sections found in MD")

    # ── Vitamin/Mineral ──
    if "vitamin" in data_types:
        print("\n--- Vitamin/Mineral ---")
        vit_keywords = ["维生素", "微量元素", "维矿", "矿物质"]
        vit_sections = _find_sections_by_keywords(sections, vit_keywords)
        vit_md = "\n\n".join(vit_sections) if vit_sections else ""

        if vit_md.strip():
            data = _extract_json(vit_md, EXTRACT_VITAMIN_SYSTEM,
                                 breed_name, source_label)
            if data:
                header = VITAMIN_HEADER
                csv_rows = _map_json_to_csv(data, header, breed_name,
                                            source_label, "vitamin")
                if not skip_verify:
                    for v_attempt in range(3):
                        v_result = _verify_extraction(
                            vit_md[:4000], csv_rows, header, "vitamin")
                        if v_result.get("status") == "PASS":
                            break
                        elif v_result.get("status") == "FAIL":
                            corrected = v_result.get("corrected_data")
                            if corrected:
                                csv_rows = _map_json_to_csv(
                                    corrected, header, breed_name,
                                    source_label, "vitamin")
                            continue
                        else:
                            break

                csv_path = _get_csv_path(species, "vitamin")
                _append_csv(csv_path, csv_rows, header)
            else:
                print("  No vitamin data extracted")
        else:
            print("  No vitamin sections found in MD")

    print(f"\n[DONE] {breed_name}")


# ── CLI ────────────────────────────────────────────────────────────────────

def _list_manuals():
    """List all breed manuals found."""
    manuals_dir = "D:/Geqi_series/饲养管理手册"
    if not os.path.exists(manuals_dir):
        print(f"Manuals directory not found: {manuals_dir}")
        return

    for folder in sorted(os.listdir(manuals_dir)):
        folder_path = os.path.join(manuals_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        mds = [f for f in os.listdir(folder_path) if f.endswith(".md")]
        for md in mds:
            md_path = os.path.join(folder_path, md)
            size = os.path.getsize(md_path)
            # Count tables
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
            table_count = len(re.findall(r"^\|.*\|$", content, re.MULTILINE)) // 3  # approx
            line_count = content.count("\n")
            has_nutrition = bool(re.search(r"营养|蛋白|氨基酸|代谢能", content))
            has_vitamin = bool(re.search(r"维生素|维矿|微量元素", content))
            has_weekly = bool(re.search(r"周龄\s*\|", content))

            tags = []
            if has_nutrition: tags.append("营养")
            if has_vitamin: tags.append("维矿")
            if has_weekly: tags.append("周龄表")
            tag_str = ",".join(tags) if tags else "简表"

            print(f"  {folder:20s} | {line_count:4d}行 | {table_count:2d}表 | "
                  f"{tag_str:12s} | {size//1024:3d}KB")


def main():
    parser = argparse.ArgumentParser(
        description="Import breed data from Chinese Markdown manuals to project CSVs")
    parser.add_argument("--md-file", help="Path to the Markdown file")
    parser.add_argument("--breed", help="English breed name (e.g. 'Hy-Line W-36')")
    parser.add_argument("--species", default="layer",
                        choices=["layer", "broiler"],
                        help="Species type (default: layer)")
    parser.add_argument("--source", default=None,
                        help="Source label (default: '{Breed} Official Manual')")
    parser.add_argument("--replace", action="store_true",
                        help="Replace existing data for this breed")
    parser.add_argument("--skip-verify", action="store_true",
                        help="Skip LLM verification (debug)")
    parser.add_argument("--only", nargs="+",
                        choices=["performance", "nutrient", "vitamin"],
                        help="Only process specific data types")
    parser.add_argument("--list-manuals", action="store_true",
                        help="List all available breed manuals")

    args = parser.parse_args()

    if args.list_manuals:
        _list_manuals()
        return

    if not args.md_file or not args.breed:
        parser.print_help()
        print("\nError: --md-file and --breed are required (or use --list-manuals)")
        sys.exit(1)

    source = args.source or f"{args.breed} Official Manual"

    data_types = args.only or ["performance", "nutrient", "vitamin"]

    process_breed(
        md_path=args.md_file,
        breed_name=args.breed,
        species=args.species,
        source_label=source,
        replace=args.replace,
        data_types=data_types,
        skip_verify=args.skip_verify,
    )


if __name__ == "__main__":
    main()
