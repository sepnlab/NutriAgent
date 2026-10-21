"""生成精选查询集 v2 — 全面优化版。

优化项：
  1. 类型均衡：single-value 提升到 20+，definition 精简到 6
  2. 新增 time-series 和 double-value 查询
  3. 难度分级修正：L1/L2/L3 边界清晰化
  4. C-XD-005 GT 值修正（调大 CP 降幅）
  5. 品种特异性增强：减少品种间重叠
  6. 中文查询自然化
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.utils.csv_cache import load_csv


# ── CSV 数据读取 ──────────────────────────────────────────────


def _get_feed_value(ingredient: str, col: str) -> float:
    df = load_csv(Config.FEED_INGREDIENT_BANK_FILE, normalize_cols=["Ingredient"])
    use_regex = any(c in ingredient for c in "$^.*+?[]|()")
    match = df[df["Ingredient"].str.contains(ingredient, case=False, na=False, regex=use_regex)]
    if match.empty:
        raise ValueError(f"Ingredient '{ingredient}' not found")
    return float(match.iloc[0][col])


def _get_aa_value(ingredient: str, col: str) -> float:
    df = load_csv(Config.FEED_INGREDIENT_AA_FILE, normalize_cols=["Ingredient"])
    use_regex = any(c in ingredient for c in "$^.*+?[]|()")
    match = df[df["Ingredient"].str.contains(ingredient, case=False, na=False, regex=use_regex)]
    if match.empty:
        raise ValueError(f"Ingredient '{ingredient}' not found in AA")
    return float(match.iloc[0][col])


def _get_sid_value(ingredient: str, col: str) -> float:
    df = load_csv(Config.FEED_INGREDIENT_DIGESTIBILITY_FILE, normalize_cols=["Ingredient"])
    use_regex = any(c in ingredient for c in "$^.*+?[]|()")
    match = df[df["Ingredient"].str.contains(ingredient, case=False, na=False, regex=use_regex)]
    if match.empty:
        raise ValueError(f"Ingredient '{ingredient}' not found in SID")
    return float(match.iloc[0][col])


def _get_nr(breed, phase, col, breed_col="Breed", species="layer"):
    corpus_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
    df = load_csv(os.path.join(corpus_dir, species, "nutrient_requirements.csv"), normalize_cols=[breed_col])
    bm = df[df[breed_col].str.contains(breed, case=False, na=False, regex=False)]
    if bm.empty:
        raise ValueError(f"Breed '{breed}' not found")
    pm = bm[bm["Phase"].str.contains(phase, case=False, na=False, regex=False)]
    if pm.empty:
        raise ValueError(f"Phase '{phase}' not found for {breed}")
    return float(pm.iloc[0][col])


def _get_pm(breed, timepoint, col, breed_col="Breed", time_col="Week", species="layer"):
    corpus_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
    df = load_csv(os.path.join(corpus_dir, species, "performance_management.csv"), normalize_cols=[breed_col])
    bm = df[df[breed_col].str.contains(breed, case=False, na=False, regex=False)]
    if bm.empty:
        raise ValueError(f"Breed '{breed}' not found")
    tm = bm[bm[time_col] == timepoint]
    if tm.empty:
        raise ValueError(f"{time_col}={timepoint} not found for {breed}")
    val = tm.iloc[0][col]
    if str(val) == "nan":
        raise ValueError(f"NaN for {breed} {time_col}={timepoint}")
    return float(val)


def _q(id, query, qtype, category, gt=None, difficulty="L1", lang="en", **extra):
    d = {"id": id, "query": query, "type": qtype, "category": category,
         "difficulty": difficulty, "language": lang}
    if gt is not None:
        d["expected_value"] = gt
    d.update(extra)
    return d


# ── 品种元数据 ────────────────────────────────────────────────


LAYER_META = {
    "breeds": {"isa brown": "伊莎褐", "hy-line brown": "海兰褐",
               "jinghong 1": "京红1号", "jinghong 1 v3.0": "京红1号3.0",
               "dawu jinfeng": "大午金凤"},
    "phases": {"Lay I": "产蛋前期", "Lay II": "产蛋中期",
               "Lay III": "产蛋后期", "Layer I": "产蛋I期",
               "Layer II": "产蛋II期", "Developer": "育成期",
               "Starter": "开产期"},
    "breed_col": "Breed",
    "time_col": "Week",
    "fi_col": "FI_g_per_d",
    "val_col": "HenDay_Prod_Pct",
    "val_name": "hen-day production",
    "val_name_zh": "产蛋率",
}

BROILER_META = {
    "breeds": {"aa+": "AA+", "yisheng 909": "益生909"},
    "phases": {"Starter": "开产期", "Grower": "生长期", "Finisher": "育成期"},
    "breed_col": "Genetic_Line",
    "time_col": "Day",
    "fi_col": "FI_g_per_day",
    "val_col": "BW_g",
    "val_name": "body weight",
    "val_name_zh": "体重",
}


def _meta(species):
    return LAYER_META if species == "layer" else BROILER_META


# ── Feed Ingredient Bank (10 条) ──────────────────────────────


def feed_queries():
    qs = []
    maize_cp = _get_feed_value("maize$", "CP")
    maize_me = _get_feed_value("maize$", "ME_kcal_kg")
    limestone_ca = _get_feed_value("limestone", "Ca")
    wheat_me = _get_feed_value("wheat, soft", "ME_kcal_kg")
    sbm_cp = _get_feed_value("soybean meal.*48", "CP")
    cm_cp = _get_feed_value("canola meal", "CP")
    sbm_me = _get_feed_value("soybean meal.*48", "ME_kcal_kg")
    cm_me = _get_feed_value("canola meal", "ME_kcal_kg")

    # L1: single-value × 3
    qs.append(_q("C-FIB-001", "What is the crude protein content of maize?",
        "single-value", "Feed Ingredient Bank", difficulty="L1", gt=maize_cp))
    qs.append(_q("C-FIB-002", "What is the calcium content of limestone?",
        "single-value", "Feed Ingredient Bank", difficulty="L1", gt=limestone_ca))
    qs.append(_q("C-FIB-003", "What is the metabolizable energy of soybean meal 48% in kcal/kg?",
        "single-value", "Feed Ingredient Bank", difficulty="L1", gt=sbm_me))

    # L1: comparison × 2
    qs.append(_q("C-FIB-004",
        "Which has higher metabolizable energy, maize or soft wheat? State both values.",
        "comparison", "Feed Ingredient Bank", difficulty="L1", gt=max(maize_me, wheat_me)))
    qs.append(_q("C-FIB-005",
        "Compare the crude protein of soybean meal 48% and canola meal. Which is higher and by how much?",
        "comparison", "Feed Ingredient Bank", difficulty="L1", gt=round(abs(sbm_cp - cm_cp), 1)))

    # L2: open-ended × 2
    qs.append(_q("C-FIB-006",
        "List three plant protein sources from the feed ingredient bank with crude protein above 30%. Cite exact CP values.",
        "open-ended", "Feed Ingredient Bank", difficulty="L2"))
    qs.append(_q("C-FIB-007",
        "Compare the SID lysine digestibility of maize and soybean meal 48%. What does this imply for formulation?",
        "open-ended", "Feed Ingredient Bank", difficulty="L2"))

    # L1: definition × 1
    qs.append(_q("C-FIB-008", "Define metabolizable energy (ME). How does it differ from gross energy?",
        "definition", "Feed Ingredient Bank", difficulty="L1"))

    # L1: Chinese × 2
    qs.append(_q("C-FIB-009", "玉米的粗蛋白含量是多少？",
        "single-value", "Feed Ingredient Bank", difficulty="L1", gt=maize_cp, lang="zh"))
    qs.append(_q("C-FIB-010", "豆粕48和菜粕的代谢能各是多少？哪个更高？",
        "comparison", "Feed Ingredient Bank", difficulty="L1", gt=max(sbm_me, cm_me), lang="zh"))

    return qs


# ── Nutrient Requirements (12 条) ─────────────────────────────


def nutrient_queries(species="layer"):
    qs = []
    m = _meta(species)
    kw = dict(breed_col=m["breed_col"], species=species)

    if species == "layer":
        b1, p1 = "isa brown", "Lay I"
        b2, p2 = "isa brown", "Lay III"
        b3, p3 = "jinghong 1", "Layer I"
        b4, p4 = "dawu jinfeng", "Layer I"
    else:
        b1, p1 = "ross 308", "Starter"
        b2, p2 = "ross 308", "Finisher"
        b3, p3 = "ross 308", "Grower"
        b4, p4 = "ross 308", "Starter"

    ca1 = _get_nr(b1, p1, "Ca_pct", **kw)
    ca2 = _get_nr(b2, p2, "Ca_pct", **kw)
    cp3 = _get_nr(b3, p3, "CP_pct", **kw)
    lys1 = _get_nr(b1, p1, "SID_Lys_pct", **kw)
    met1 = _get_nr(b1, p1, "SID_Met_pct", **kw)
    b1_zh = m["breeds"].get(b1, b1)
    b2_zh = m["breeds"].get(b2, b2)
    b3_zh = m["breeds"].get(b3, b3)
    p1_zh = m["phases"].get(p1, p1)
    p2_zh = m["phases"].get(p2, p2)
    p3_zh = m["phases"].get(p3, p3)

    # L1: single-value × 3
    qs.append(_q("C-NR-001",
        f"What is the calcium requirement for {b1.title()} in {p1}?",
        "single-value", "Nutrient Requirements", difficulty="L1", gt=ca1))
    qs.append(_q("C-NR-002",
        f"What is the SID methionine requirement for {b1.title()} in {p1}?",
        "single-value", "Nutrient Requirements", difficulty="L1", gt=met1))
    qs.append(_q("C-NR-003",
        f"What is the crude protein requirement for {b3.title()} in {p3}?",
        "single-value", "Nutrient Requirements", difficulty="L1", gt=cp3))

    # L1: comparison × 2
    qs.append(_q("C-NR-004",
        f"Compare calcium requirement: {b1.title()} {p1} vs {p2}. Which is higher?",
        "comparison", "Nutrient Requirements", difficulty="L1", gt=max(ca1, ca2)))

    if species == "layer":
        ca4 = _get_nr(b4, p4, "Ca_pct", **kw)
        qs.append(_q("C-NR-005",
            f"Compare calcium requirement: {b1.title()} vs {b4.title()}, both in {p1}. Which is higher?",
            "comparison", "Nutrient Requirements", difficulty="L1", gt=max(ca1, ca4)))
    else:
        lys3 = _get_nr(b3, p3, "SID_Lys_pct", **kw)
        qs.append(_q("C-NR-005",
            f"Compare SID lysine: {b1.title()} {p1} vs {p3}. Which is higher?",
            "comparison", "Nutrient Requirements", difficulty="L1", gt=max(lys1, lys3)))

    # L2: time-series — requires looking up multiple data points
    if species == "layer":
        phases = ["Developer", "Lay I", "Lay II", "Lay III"]
        ca_values = []
        for ph in phases:
            try:
                ca_values.append(_get_nr(b1, ph, "Ca_pct", **kw))
            except ValueError:
                pass
        if len(ca_values) >= 2:
            qs.append(_q("C-NR-006",
                f"How does the calcium requirement for {b1.title()} change from Developer through Lay III? "
                f"State the Ca% for each phase.",
                "open-ended", "Nutrient Requirements", difficulty="L2"))
    else:
        phases = ["Starter", "Grower", "Finisher"]
        cp_values = []
        for ph in phases:
            try:
                cp_values.append(_get_nr(b1, ph, "CP_pct", **kw))
            except ValueError:
                pass
        if len(cp_values) >= 2:
            qs.append(_q("C-NR-006",
                f"How does the crude protein requirement for {b1.title()} change from Starter to Finisher? "
                f"State the CP% for each phase.",
                "open-ended", "Nutrient Requirements", difficulty="L2"))

    # L2: calculation — SID lysine from total lysine × digestibility
    qs.append(_q("C-NR-007",
        "A feed ingredient has total lysine of 0.85% and SID lysine digestibility of 88%. "
        "What is the SID lysine content (in %)?",
        "single-value", "Nutrient Requirements", difficulty="L2", gt=round(0.85 * 0.88, 3)))

    # L2: calculation — available phosphorus with phytase
    qs.append(_q("C-NR-008",
        "A diet has 0.45% total phosphorus and 0.30% phytate phosphorus. "
        "If phytase improves phytate P release by 50%, what is the effective available phosphorus?",
        "single-value", "Nutrient Requirements", difficulty="L2", gt=round(0.15 + 0.30 * 0.50, 2)))

    # L1: definition
    qs.append(_q("C-NR-009", "Define SID (Standardized Ileal Digestible) amino acids. Why is it preferred over total amino acids?",
        "definition", "Nutrient Requirements", difficulty="L1"))

    # L1: Chinese × 3 — 按数据可用性分配品种
    # 大午金凤：产蛋期 SID 数据完整（NR）；京粉6号：100 周 PM 数据完整
    if species == "layer":
        cn1, cp1 = "dawu jinfeng", "Layer I"
        cn2, cp2 = "dawu jinfeng", "Layer III"
        cn3, cp3 = "dawu jinfeng", "Layer I"
        cn1_zh, cp1_zh = "大午金凤", "产蛋I期"
        cn2_zh, cp2_zh = "大午金凤", "产蛋III期"
        cn3_zh, cp3_zh = "大午金凤", "产蛋I期"
    else:
        cn1, cp1 = b1, p1
        cn2, cp2 = b2, p2
        cn3, cp3 = b3, p3
        cn1_zh, cp1_zh = b1_zh, p1_zh
        cn2_zh, cp2_zh = b2_zh, p2_zh
        cn3_zh, cp3_zh = b3_zh, p3_zh

    ca_cn1 = _get_nr(cn1, cp1, "Ca_pct", **kw)
    ca_cn2 = _get_nr(cn2, cp2, "Ca_pct", **kw)
    met_cn1 = _get_nr(cn3, cp3, "SID_Met_pct", **kw)

    qs.append(_q("C-NR-010", f"{cn1_zh}在{cp1_zh}的钙需要量是多少？",
        "single-value", "Nutrient Requirements", difficulty="L1", gt=ca_cn1, lang="zh"))
    qs.append(_q("C-NR-011", f"{cn1_zh}从{cp1_zh}到{cp2_zh}，钙需要量怎么变化？",
        "comparison", "Nutrient Requirements", difficulty="L1", gt=max(ca_cn1, ca_cn2), lang="zh"))
    qs.append(_q("C-NR-012", f"{cn3_zh}在{cp3_zh}的SID蛋氨酸需要量是多少？",
        "single-value", "Nutrient Requirements", difficulty="L1", gt=met_cn1, lang="zh"))

    return qs


# ── Performance Management (12 条) ────────────────────────────


def performance_queries(species="layer"):
    qs = []
    m = _meta(species)
    kw = dict(breed_col=m["breed_col"], time_col=m["time_col"], species=species)

    if species == "layer":
        b1, w1 = "isa brown", 30
        b2, w2 = "hy-line brown", 30
        b3, w3 = "jinghong 1 v3.0", 30
        vc = m["val_col"]
    else:
        b1, w1 = "aa+", 35
        b2, w2 = "aa+", 42
        b3, w3 = "yisheng 909", 35
        vc = m["val_col"]

    v1 = _get_pm(b1, w1, vc, **kw)
    v2 = _get_pm(b2, w2, vc, **kw)
    fi1 = _get_pm(b1, w1, m["fi_col"], **kw)
    fi2 = _get_pm(b2, w2, m["fi_col"], **kw)
    b1_zh = m["breeds"].get(b1, b1)
    b2_zh = m["breeds"].get(b2, b2)
    vn = m["val_name"]
    vn_zh = m["val_name_zh"]

    # L1: single-value × 2
    qs.append(_q("C-PM-001", f"What is the {vn} for {b1.title()} at week {w1}?",
        "single-value", "Performance Management", difficulty="L1", gt=v1))
    if species == "layer":
        ew2 = _get_pm(b2, w2, "Egg_Wt_g", **kw)
        qs.append(_q("C-PM-002", f"What is the egg weight for {b2.title()} at week {w2}?",
            "single-value", "Performance Management", difficulty="L1", gt=ew2))
    else:
        qs.append(_q("C-PM-002", f"What is the daily feed intake for {b2.title()} at day {w2}?",
            "single-value", "Performance Management", difficulty="L1", gt=fi2))

    # L1: comparison × 2
    qs.append(_q("C-PM-003",
        f"Compare {vn}: {b1.title()} week {w1} vs {b2.title()} week {w2}. Which is higher?",
        "comparison", "Performance Management", difficulty="L1", gt=max(v1, v2)))
    qs.append(_q("C-PM-004",
        f"Compare daily feed intake: {b1.title()} week {w1} vs {b2.title()} week {w2}.",
        "comparison", "Performance Management", difficulty="L1", gt=max(fi1, fi2)))

    # L2: time-series — requires multiple data points
    if species == "layer":
        w5, w10, w15 = 5, 10, 15
        try:
            v5 = _get_pm(b1, w5, "BW_g", **kw)
            v10 = _get_pm(b1, w10, "BW_g", **kw)
            v15 = _get_pm(b1, w15, "BW_g", **kw)
            qs.append(_q("C-PM-005",
                f"Track the body weight of {b1.title()} pullets at week 5, 10, and 15. "
                f"What is the weight at each point?",
                "open-ended", "Performance Management", difficulty="L2"))
        except ValueError:
            qs.append(_q("C-PM-005",
                f"What factors affect feed efficiency in {b1.title()} flocks?",
                "open-ended", "Performance Management", difficulty="L2"))
    else:
        try:
            v7 = _get_pm(b1, 7, vc, **kw)
            v14 = _get_pm(b1, 14, vc, **kw)
            v21 = _get_pm(b1, 21, vc, **kw)
            qs.append(_q("C-PM-005",
                f"Track the body weight of {b1.title()} broilers at day 7, 14, and 21. "
                f"What is the weight at each point?",
                "open-ended", "Performance Management", difficulty="L2"))
        except ValueError:
            qs.append(_q("C-PM-005",
                f"What factors affect feed efficiency in {b1.title()} broilers?",
                "open-ended", "Performance Management", difficulty="L2"))

    # L3: cross-domain — Performance × Nutrient
    if species == "layer":
        ca_req = _get_nr("isa brown", "Lay I", "Ca_pct", breed_col="Breed", species="layer")
        ca_intake = fi1 * ca_req / 100 * 1000
        qs.append(_q("C-PM-006",
            f"{b1.title()} at week {w1}: feed intake {fi1:.0f} g/day, Ca requirement {ca_req:.2f}%. "
            f"Estimate daily calcium intake in mg/hen/day. Is it sufficient for eggshell (~4000 mg/day)?",
            "open-ended", "Performance Management", difficulty="L3", gt=round(ca_intake, 0)))
    else:
        cp_req = _get_nr("ross 308", "Starter", "CP_pct", breed_col="Genetic_Line", species="broiler")
        cp_intake = fi1 * cp_req / 100
        qs.append(_q("C-PM-006",
            f"{b1.title()} at day {w1}: feed intake {fi1:.0f} g/day, CP requirement {cp_req:.1f}%. "
            f"Estimate daily crude protein intake in g/bird/day.",
            "open-ended", "Performance Management", difficulty="L3", gt=round(cp_intake, 1)))

    # L2: calculation — egg mass / FCR
    if species == "layer":
        qs.append(_q("C-PM-007",
            f"{b1.title()} at week {w1}: hen-day production {v1}%, average egg weight 61.5g. "
            f"Calculate egg mass in g/hen/day.",
            "single-value", "Performance Management", difficulty="L2", gt=round(v1 / 100 * 61.5, 1)))
    else:
        cum_fi = _get_pm(b1, w1, "Cumulative_FI_g", **kw)
        qs.append(_q("C-PM-007",
            f"{b1.title()} at day {w1}: BW={v1:.0f}g, cumulative feed intake={cum_fi:.0f}g. "
            f"Calculate the FCR.",
            "single-value", "Performance Management", difficulty="L2", gt=round(cum_fi / v1, 3)))

    # L1: definition
    qs.append(_q("C-PM-008", "Define hen-day egg production. How is it calculated?",
        "definition", "Performance Management", difficulty="L1"))

    # L1: Chinese × 2 — 京粉6号（PM 数据 100 周完整）
    if species == "layer":
        cn_b1, cn_w1 = "jingfen 6", 30
        cn_b2, cn_w2 = "hy-line brown", 30
        cn_b1_zh, cn_b2_zh = "京粉6号", "海兰褐"
        cn_v1 = _get_pm(cn_b1, cn_w1, m["val_col"], **kw)
        cn_v2 = _get_pm(cn_b2, cn_w2, m["val_col"], **kw)
    else:
        cn_b1, cn_w1 = b1, w1
        cn_b2, cn_w2 = b2, w2
        cn_b1_zh, cn_b2_zh = b1_zh, b2_zh
        cn_v1, cn_v2 = v1, v2

    qs.append(_q("C-PM-009", f"{cn_b1_zh}在第{cn_w1}周的{vn_zh}是多少？",
        "single-value", "Performance Management", difficulty="L1", gt=cn_v1, lang="zh"))
    qs.append(_q("C-PM-010", f"{cn_b1_zh}和{cn_b2_zh}在第{cn_w1}周的{vn_zh}各是多少？哪个更高？",
        "comparison", "Performance Management", difficulty="L1", gt=max(cn_v1, cn_v2), lang="zh"))

    # L2: double-value (Chinese)
    if species == "layer":
        cn_ew = _get_pm(cn_b1, cn_w1, "Egg_Wt_g", **kw)
        qs.append(_q("C-PM-011",
            f"{cn_b1_zh}第{cn_w1}周的产蛋率和蛋重各是多少？",
            "single-value", "Performance Management", difficulty="L2", lang="zh",
            expected_value=cn_v1, expected_value_2=cn_ew))

    return qs


# ── Definitions (6 条) ────────────────────────────────────────


def definitions_queries():
    qs = []

    # L1: pure definitions × 3
    qs.append(_q("C-DEF-001", "Define metabolizable energy (ME). How does it differ from digestible energy (DE)?",
        "definition", "Definitions", difficulty="L1"))
    qs.append(_q("C-DEF-002", "Define available phosphorus. Why is it different from total phosphorus?",
        "definition", "Definitions", difficulty="L1"))
    qs.append(_q("C-DEF-003", "What is feed conversion ratio (FCR)? How is it calculated?",
        "definition", "Definitions", difficulty="L1"))

    # L2: application × 1
    qs.append(_q("C-DEF-004",
        "A feed sample has 2.5% nitrogen. Using N×6.25, what is the crude protein percentage?",
        "single-value", "Definitions", difficulty="L2", gt=15.625))

    # L1: Chinese × 2
    qs.append(_q("C-DEF-005", "什么是代谢能？它和消化能有什么区别？",
        "definition", "Definitions", difficulty="L1", lang="zh"))
    qs.append(_q("C-DEF-006", "蛋鸡饲料配方为什么优先用代谢能而不是消化能？",
        "open-ended", "Definitions", difficulty="L1", lang="zh"))

    return qs


# ── Cross-Domain (10 条) ──────────────────────────────────────


def cross_domain_queries(species="layer"):
    qs = []
    m = _meta(species)
    kw = dict(breed_col=m["breed_col"], species=species)

    maize_lys = _get_aa_value("maize$", "Lys")
    maize_sid = _get_sid_value("maize$", "Lys_sid")
    sbm_lys = _get_aa_value("soybean meal.*48", "Lys")
    sbm_sid = _get_sid_value("soybean meal.*48", "Lys_sid")
    sid_maize = maize_lys * maize_sid / 100
    sid_sbm = sbm_lys * sbm_sid / 100
    limestone_ca = _get_feed_value("limestone", "Ca")
    maize_cp = _get_feed_value("maize$", "CP")
    sbm_cp = _get_feed_value("soybean meal.*48", "CP")
    cm_cp = _get_feed_value("canola meal", "CP")

    if species == "layer":
        lys_req = _get_nr("isa brown", "Lay I", "SID_Lys_pct", **kw)
        ca_req = _get_nr("isa brown", "Lay I", "Ca_pct", **kw)
        bl = "伊莎褐蛋鸡"
        pl = "产蛋前期"
        bl_en = "ISA Brown layers"
        pl_en = "Lay I"
    else:
        lys_req = _get_nr("ross 308", "Starter", "SID_Lys_pct", **kw)
        ca_req = _get_nr("ross 308", "Starter", "Ca_pct", **kw)
        bl = "罗斯308雏鸡"
        pl = "开产期"
        bl_en = "Ross 308 starters"
        pl_en = "Starter"

    needed_pct = round(ca_req / (limestone_ca / 100), 1)

    # L2: multi-hop × 2
    combined = sid_maize * 0.60 + sid_sbm * 0.25
    qs.append(_q("C-XD-001",
        f"A {pl_en} diet uses 60% maize (total lysine={maize_lys:.3f}%, SID={maize_sid:.0f}%) "
        f"and 25% SBM48 (total lysine={sbm_lys:.3f}%, SID={sbm_sid:.0f}%). "
        f"Calculate the SID lysine contribution. Does it meet the {bl_en} requirement ({lys_req:.2f}%)?",
        "multi-hop", "Cross-Domain", difficulty="L2", gt=round(combined, 3)))

    qs.append(_q("C-XD-002",
        f"Ca requirement for {bl_en} is {ca_req:.2f}%. Limestone has {limestone_ca:.0f}% Ca. "
        f"What % of limestone is needed in the diet?",
        "multi-hop", "Cross-Domain", difficulty="L2", gt=needed_pct))

    # L2: constraint × 2
    qs.append(_q("C-XD-003",
        f"Can limestone at 9% inclusion meet the Ca requirement of {ca_req:.2f}% for {bl_en}? "
        f"Calculate the Ca contribution.",
        "constraint", "Cross-Domain", difficulty="L2", gt=round(limestone_ca * 0.09, 2)))

    qs.append(_q("C-XD-004",
        f"A {pl_en} diet: 55% maize + 30% SBM48. Using SID lysine values, calculate total SID lysine. "
        f"Does it meet {lys_req:.2f}%?",
        "constraint", "Cross-Domain", difficulty="L2", gt=round(sid_maize * 0.55 + sid_sbm * 0.30, 3)))

    # L3: counterfactual × 2
    qs.append(_q("C-XD-005",
        f"Maize CP drops from {maize_cp:.1f}% to 5.0% (severe drought). Original formula: 60% maize. "
        f"By how many percentage points must SBM48 (CP={sbm_cp:.1f}%) increase to maintain total CP?",
        "counterfactual", "Cross-Domain", difficulty="L3",
        gt=round((maize_cp - 5.0) * 0.60 / sbm_cp, 2)))

    qs.append(_q("C-XD-006",
        f"SBM price doubles. Replace 50% of SBM with canola meal. Original: 25% SBM (CP={sbm_cp:.1f}%). "
        f"New: 12.5% SBM + 12.5% canola (CP={cm_cp:.1f}%). Calculate the CP contribution change.",
        "counterfactual", "Cross-Domain", difficulty="L3", gt=round(0.125 * sbm_cp + 0.125 * cm_cp, 2)))

    # L3: multi-hop — Performance × Nutrient
    if species == "layer":
        fi30 = _get_pm("isa brown", 30, "FI_g_per_d", breed_col="Breed", time_col="Week", species="layer")
        ca_intake = fi30 * ca_req / 100 * 1000
        qs.append(_q("C-XD-007",
            f"ISA Brown at week 30: feed intake {fi30:.0f} g/day, Ca requirement {ca_req:.2f}%. "
            f"Estimate daily Ca intake (mg/hen/day). Sufficient for eggshell?",
            "multi-hop", "Cross-Domain", difficulty="L3", gt=round(ca_intake, 0)))
    else:
        fi35 = _get_pm("aa+", 35, "FI_g_per_day", breed_col="Genetic_Line", time_col="Day", species="broiler")
        cp_req = _get_nr("ross 308", "Starter", "CP_pct", breed_col="Genetic_Line", species="broiler")
        qs.append(_q("C-XD-007",
            f"AA+ at day 35: feed intake {fi35:.0f} g/day, CP requirement {cp_req:.1f}%. "
            f"Estimate daily CP intake (g/bird/day).",
            "multi-hop", "Cross-Domain", difficulty="L3", gt=round(fi35 * cp_req / 100, 1)))

    # L3: open-ended
    qs.append(_q("C-XD-008",
        "A nutritionist has maize, SBM48, limestone, and dicalcium phosphate. "
        "Explain how to balance Ca and P in a layer diet. What constraints must be satisfied?",
        "open-ended", "Cross-Domain", difficulty="L3"))

    # L2: Chinese — 用中国品种
    if species == "layer":
        cn_bl = "大午金凤蛋鸡"
        cn_pl = "产蛋I期"
        cn_lys = _get_nr("dawu jinfeng", "Layer I", "SID_Lys_pct", **kw)
        cn_ca = _get_nr("dawu jinfeng", "Layer I", "Ca_pct", **kw)
        cn_combined = sid_maize * 0.60 + sid_sbm * 0.25
        cn_needed = round(cn_ca / (limestone_ca / 100), 1)
    else:
        cn_bl = bl
        cn_pl = pl
        cn_lys = lys_req
        cn_ca = ca_req
        cn_combined = combined
        cn_needed = needed_pct

    qs.append(_q("C-XD-009",
        f"一个{cn_pl}配方用60%玉米（总赖氨酸{maize_lys:.3f}%，SID消化率{maize_sid:.0f}%）"
        f"和25%豆粕48（总赖氨酸{sbm_lys:.3f}%，SID消化率{sbm_sid:.0f}%）。"
        f"这两样原料的SID赖氨酸加起来是多少？能不能满足{cn_bl}的需要量（{cn_lys:.2f}%）？",
        "multi-hop", "Cross-Domain", difficulty="L2", gt=round(cn_combined, 3), lang="zh"))

    qs.append(_q("C-XD-010",
        f"石灰石含钙{limestone_ca:.0f}%，{cn_bl}的钙需要量是{cn_ca:.2f}%。"
        f"配方里要加多少石灰石才能满足？",
        "constraint", "Cross-Domain", difficulty="L2", gt=cn_needed, lang="zh"))

    return qs


# ── Edge Cases (5 条) ─────────────────────────────────────────


def edge_case_queries(species="layer"):
    qs = []

    qs.append(_q("C-EC-001",
        "What is the crude protein content of unicorn feed?",
        "single-value", "Edge Cases", difficulty="L1",
        expected_behavior="Should indicate ingredient not found in database"))

    qs.append(_q("C-EC-002",
        "What is the calcium requirement for Lohmann Tinted in Lay I?",
        "single-value", "Edge Cases", difficulty="L1",
        expected_behavior="Should indicate breed not found; list available breeds"))

    if species == "layer":
        qs.append(_q("C-EC-003",
            "What is the body weight of ISA Brown broilers at day 35?",
            "single-value", "Edge Cases", difficulty="L1",
            expected_behavior="Should clarify ISA Brown is a layer breed, not broiler"))
    else:
        qs.append(_q("C-EC-003",
            "What is the hen-day production of Ross 308 layers at week 30?",
            "single-value", "Edge Cases", difficulty="L1",
            expected_behavior="Should clarify Ross 308 is a broiler breed, not layer"))

    qs.append(_q("C-EC-004",
        "What is the methionine requirement for ISA Brown in Lay I?",
        "single-value", "Edge Cases", difficulty="L1",
        expected_behavior="Should either provide the value or indicate column name difference (SID_Met_pct vs methionine)"))

    qs.append(_q("C-EC-005",
        "Compare the metabolizable energy of fish meal and limestone.",
        "comparison", "Edge Cases", difficulty="L2",
        expected_behavior="Should note limestone has 0 ME (mineral, not energy source)"))

    return qs


# ── 主函数 ────────────────────────────────────────────────────


def generate_curated_queries(species="layer"):
    queries = {}
    queries["Feed Ingredient Bank"] = feed_queries()
    queries["Nutrient Requirements"] = nutrient_queries(species)
    queries["Performance Management"] = performance_queries(species)
    queries["Definitions"] = definitions_queries()
    queries["Cross-Domain"] = cross_domain_queries(species)
    queries["Edge Cases"] = edge_case_queries(species)

    total = sum(len(v) for v in queries.values())
    with_gt = sum(1 for v in queries.values() for q in v if q.get("expected_value"))

    # Type distribution
    by_type = {}
    for qs in queries.values():
        for q in qs:
            t = q["type"]
            by_type[t] = by_type.get(t, 0) + 1

    print(f"Generated {total} queries ({with_gt} with GT, {with_gt*100//total}%)")
    print(f"Types: {dict(sorted(by_type.items()))}")
    for cat, qs in queries.items():
        gt_count = sum(1 for q in qs if q.get("expected_value"))
        print(f"  {cat}: {len(qs)} queries ({gt_count} with GT)")
    return queries


def main():
    parser = argparse.ArgumentParser(description="Generate curated query set v2")
    parser.add_argument("--species", choices=["layer", "broiler", "both"], default="both")
    args = parser.parse_args()

    species_list = ["layer", "broiler"] if args.species == "both" else [args.species]
    for species in species_list:
        print(f"\n=== {species.upper()} ===")
        queries = generate_curated_queries(species)
        out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "queries", species)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "evaluation_queries_curated.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(queries, f, indent=2, ensure_ascii=False)
        print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
