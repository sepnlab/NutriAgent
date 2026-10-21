"""
CSV 写入工具 —— 用于将 Claude 提取的结构化数据写入项目 CSVs。

用法: 在 Python 中 import 后调用 write_breed_data()

主要函数:
  write_breed_data(breed, species, data_type, rows)
    - breed: "Hy-Line W-36"
    - species: "layer" | "broiler"
    - data_type: "performance" | "nutrient" | "vitamin"
    - rows: list[dict], 键与 CSV 列名一致

  list_breeds(species, data_type) -> 查看当前 CSV 中有哪些品种
  remove_breed(breed, species, data_type) -> 删除某个品种的数据
"""
import csv
import os
import sys

_PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# CSV schema 定义
HEADERS = {
    ("layer", "performance"): [
        "Breed", "Week", "HenDay_Prod_Pct", "Egg_Wt_g", "Egg_Mass_g_per_d",
        "FI_g_per_d", "Feed_per_Dozen_kg", "Feed_per_kg_Egg_kg", "BW_g",
        "Mortality_Pct", "Shell_Strength_N", "Haugh_Unit", "Cumul_Egg_Count",
        "Water_Intake_ml_d", "source",
    ],
    ("layer", "nutrient"): [
        "Breed", "Phase", "ME_kcal_kg", "CP_pct", "Ca_pct", "Avail_P_pct",
        "Na_pct", "Lys_pct", "Met_pct", "M_C_pct", "Thr_pct", "Trp_pct",
        "Val_pct", "Arg_pct", "Ile_pct", "SID_Lys_pct", "SID_Met_pct",
        "SID_M_C_pct", "SID_Thr_pct", "SID_Trp_pct", "Choline_mg_kg",
        "Linoleic_Acid_pct", "source",
    ],
    ("layer", "vitamin"): [
        "Breed", "Phase", "Vitamin_A_IU_kg", "Vitamin_D3_IU_kg",
        "Vitamin_E_IU_kg", "Vitamin_K3_mg_kg", "Vitamin_B1_mg_kg",
        "Vitamin_B2_mg_kg", "Vitamin_B6_mg_kg", "Vitamin_B12_mcg_kg",
        "Niacin_mg_kg", "Pantothenic_Acid_mg_kg", "Folic_Acid_mg_kg",
        "Biotin_mcg_kg", "Fe_mg_kg", "Cu_mg_kg", "Zn_mg_kg", "Mn_mg_kg",
        "Se_mg_kg", "I_mg_kg", "source",
    ],
    ("broiler", "performance"): [
        "Genetic_Line", "Sex", "Day", "BW_g", "ADG_g", "FI_g_per_day",
        "Cumulative_FI_g", "FCR", "source",
    ],
    ("broiler", "nutrient"): [
        "Genetic_Line", "Sex", "Phase", "ME_kcal_kg", "CP_pct", "Ca_pct",
        "Avail_P_pct", "Na_pct", "Lys_pct", "Met_pct", "M_C_pct", "Thr_pct",
        "Trp_pct", "source",
    ],
}


def _csv_path(species, data_type):
    dir_map = {"performance": "performance_management.csv",
               "nutrient": "nutrient_requirements.csv",
               "vitamin": "nutrient_vitamin_mineral.csv"}
    return os.path.join(_PROJECT_ROOT, "corpus", species, dir_map[data_type])


def _read(path):
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
    except FileNotFoundError:
        pass
    return rows


def _write(path, rows, header):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)


def list_breeds(species, data_type):
    """列出 CSV 中已有的品种。"""
    path = _csv_path(species, data_type)
    if not os.path.exists(path):
        print(f"[{species}/{data_type}] 文件不存在: {path}")
        return []
    rows = _read(path)
    breed_col = HEADERS[(species, data_type)][0]
    breeds = sorted(set(r.get(breed_col, "") for r in rows if r.get(breed_col)))
    print(f"[{species}/{data_type}] {len(rows)} 行, {len(breeds)} 品种:")
    for b in breeds:
        count = sum(1 for r in rows if r.get(breed_col) == b)
        print(f"  - {b}: {count} 行")
    return breeds


def remove_breed(breed, species, data_type):
    """删除指定品种的所有数据。"""
    path = _csv_path(species, data_type)
    if not os.path.exists(path):
        print(f"[{species}/{data_type}] 文件不存在")
        return False
    header = HEADERS[(species, data_type)]
    rows = _read(path)
    breed_col = header[0]
    before = len(rows)
    rows = [r for r in rows if r.get(breed_col, "") != breed]
    removed = before - len(rows)
    _write(path, rows, header)
    print(f"[{species}/{data_type}] 已删除 {breed}: {removed} 行, 剩余 {len(rows)} 行")
    return removed > 0


def write_breed_data(breed, species, data_type, rows, replace=True):
    """
    写入品种数据到 CSV。

    参数:
      breed:     "Hy-Line W-36"
      species:   "layer" | "broiler"
      data_type: "performance" | "nutrient" | "vitamin"
      rows:      list[dict], 每 dict 的键与 CSV 列名一致
      replace:   True=替换已有数据, False=追加
    """
    header = HEADERS.get((species, data_type))
    if not header:
        raise ValueError(f"Unknown schema: {species}/{data_type}")

    path = _csv_path(species, data_type)
    breed_col = header[0]

    # 读取现有数据
    existing = _read(path)

    # 补齐缺失列
    for row in rows:
        for col in header:
            row.setdefault(col, "")

    # 替换或追加
    if replace:
        before = len(existing)
        existing = [r for r in existing if r.get(breed_col, "") != breed]
        print(f"  [替换] 移除了 {before - len(existing)} 行旧的 {breed} 数据")

    all_rows = existing + rows
    _write(path, all_rows, header)

    print(f"  [写入] {path}")
    print(f"  [结果] {breed}: {len(rows)} 行, 共 {len(all_rows)} 行")
    print(f"  [来源] source='{rows[0].get('source', 'N/A')}'" if rows else "")

    # 验证：读回来检查
    verify = _read(path)
    written = [r for r in verify if r.get(breed_col) == breed]
    if len(written) == len(rows):
        print(f"  [验证] OK: 写入 {len(written)} 行, 读出 {len(written)} 行")
    else:
        print(f"  [验证] 警告: 写入 {len(rows)} 行, 读出 {len(written)} 行")

    return True
