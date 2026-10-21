"""Generate layer (egg-type chicken) nutrition datasets for NutriCHAT.

Creates species-specific CSV files in data/layer/ for:
1. Performance Management - egg production, egg quality, body weight across lay cycle
2. Nutrient Requirements - phase-specific specifications for layer breeds
3. Evaluation Queries - 120 layer-specific evaluation questions

Shared datasets (feed ingredient bank, definitions) remain in data/shared/.
"""
import csv
import json
import os
import random

DATA_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "corpus", "layer")
)
QUERIES_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "queries", "layer")
)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(QUERIES_DIR, exist_ok=True)
random.seed(42)


# ============================================================
# 1. PERFORMANCE MANAGEMENT - layer hens
# ============================================================
def generate_performance():
    """Generate layer performance data.

    Breeds: Hy-Line W-36 (White), Hy-Line Brown, ISA Brown, Lohmann LSL-Classic
    Metrics: Hen-day production %, egg weight (g), egg mass (g/hen/d),
             feed intake (g/hen/d), feed/dozen eggs (kg), feed/kg egg (kg),
             body weight (g), mortality (%), shell breaking strength (N),
             Haugh unit, albumen height (mm)
    """
    fields = [
        "Breed", "Week", "HenDay_Prod_Pct", "Egg_Wt_g",
        "Egg_Mass_g_per_d", "FI_g_per_d", "Feed_per_Dozen_kg",
        "Feed_per_kg_Egg_kg", "BW_g", "Mortality_Pct",
        "Shell_Strength_N", "Haugh_Unit",
    ]

    # Production curves for each breed (peak ~95% around wk 28-32, gradual decline)
    def layer_curve(breed, week):
        """Generate realistic layer production parameters by week."""
        if breed == "Hy-Line W-36":
            # Hen-day %: starts at 0, rises to peak ~96%, then gradual decline
            prod = 0
            if week < 18:
                prod = 0
            elif week <= 24:
                prod = 2.5 * (week - 18) + 10  # ramp up to ~95 by wk 24
            elif week <= 32:
                prod = 96 - 0.2 * (week - 24)  # peak ~96
            elif week <= 60:
                prod = 94 - 0.3 * (week - 32)  # gradual decline
            elif week <= 80:
                prod = 86 - 0.4 * (week - 60)
            else:
                prod = 78 - 0.3 * (week - 80)
            prod = max(0, min(97, prod))

            ew = 0
            if week < 18:
                ew = 0
            elif week <= 24:
                ew = 35 + 4.5 * (week - 18)
            elif week <= 40:
                ew = 62 + 0.2 * (week - 24)
            elif week <= 60:
                ew = 65.2 + 0.05 * (week - 40)
            else:
                ew = 66.2 + 0.02 * (week - 60)
            ew = min(ew, 68)

            fi_bw_factor = 1.0
        elif breed == "Hy-Line Brown":
            # Slightly higher body weight, similar production
            prod = 0
            if week < 18:
                prod = 0
            elif week <= 25:
                prod = 2.4 * (week - 18) + 8
            elif week <= 32:
                prod = 95 - 0.15 * (week - 25)
            elif week <= 60:
                prod = 93.5 - 0.35 * (week - 32)
            elif week <= 80:
                prod = 84 - 0.4 * (week - 60)
            else:
                prod = 76 - 0.3 * (week - 80)
            prod = max(0, min(97, prod))

            ew = 0
            if week < 18:
                ew = 0
            elif week <= 25:
                ew = 36 + 4.2 * (week - 18)
            elif week <= 40:
                ew = 63.5 + 0.25 * (week - 25)
            elif week <= 60:
                ew = 67.2 + 0.05 * (week - 40)
            else:
                ew = 68.2 + 0.02 * (week - 60)
            ew = min(ew, 70)

            fi_bw_factor = 1.08
        elif breed == "ISA Brown":
            prod = 0
            if week < 18:
                prod = 0
            elif week <= 24:
                prod = 2.6 * (week - 18) + 9
            elif week <= 34:
                prod = 96 - 0.2 * (week - 24)
            elif week <= 60:
                prod = 94 - 0.35 * (week - 34)
            elif week <= 80:
                prod = 85 - 0.4 * (week - 60)
            else:
                prod = 77 - 0.3 * (week - 80)
            prod = max(0, min(97, prod))

            ew = 0
            if week < 18:
                ew = 0
            elif week <= 24:
                ew = 35 + 4.5 * (week - 18)
            elif week <= 40:
                ew = 63 + 0.2 * (week - 24)
            elif week <= 60:
                ew = 66.8 + 0.05 * (week - 40)
            else:
                ew = 67.8 + 0.02 * (week - 60)
            ew = min(ew, 69)

            fi_bw_factor = 1.05
        else:  # Lohmann LSL-Classic
            prod = 0
            if week < 18:
                prod = 0
            elif week <= 24:
                prod = 2.4 * (week - 18) + 10
            elif week <= 32:
                prod = 96 - 0.25 * (week - 24)
            elif week <= 60:
                prod = 93 - 0.3 * (week - 32)
            elif week <= 80:
                prod = 85 - 0.35 * (week - 60)
            else:
                prod = 78 - 0.3 * (week - 80)
            prod = max(0, min(97, prod))

            ew = 0
            if week < 18:
                ew = 0
            elif week <= 24:
                ew = 34 + 4.5 * (week - 18)
            elif week <= 40:
                ew = 61 + 0.2 * (week - 24)
            elif week <= 60:
                ew = 64.2 + 0.05 * (week - 40)
            else:
                ew = 65.2 + 0.02 * (week - 60)
            ew = min(ew, 67)

            fi_bw_factor = 0.95

        prod = round(prod, 1)
        ew = round(ew, 1)

        # Body weight (g) by breed and week — smooth rearing growth curve
        # Targets: wk0=38-40, wk6=430-500, wk18=1280-1500
        bw_fns = {
            "Hy-Line W-36": lambda w: (
                0.352 * w ** 2 + 66.56 * w + 38 if w <= 18
                else 1350 + 15 * (w - 18) - 0.08 * (w - 18) ** 2
            ),
            "Hy-Line Brown": lambda w: (
                0.370 * w ** 2 + 74.45 * w + 40 if w <= 18
                else 1500 + 18 * (w - 18) - 0.10 * (w - 18) ** 2
            ),
            "ISA Brown": lambda w: (
                0.264 * w ** 2 + 71.90 * w + 39 if w <= 18
                else 1420 + 16 * (w - 18) - 0.09 * (w - 18) ** 2
            ),
            "Lohmann LSL-Classic": lambda w: (
                0.296 * w ** 2 + 63.72 * w + 37 if w <= 18
                else 1280 + 14 * (w - 18) - 0.07 * (w - 18) ** 2
            ),
        }
        bw_fn = bw_fns.get(breed, bw_fns["Hy-Line W-36"])
        bw = round(max(38, bw_fn(week)), 1)

        # Feed intake (g/hen/day)
        if week < 18:
            fi = round(8 + 3.5 * week, 1)
        else:
            fi = round((90 + 2.5 * (week - 18) - 0.02 * (week - 18) ** 2) * fi_bw_factor, 1)
            fi = min(fi, 132 if fi_bw_factor <= 1.0 else 145)
            fi = max(fi, 85)

        # Derived metrics
        egg_mass = round(prod / 100 * ew, 1)
        fdz = round((fi * 7 * 12) / (prod / 100 * 7 * ew / 1000) / 1000, 3) if prod > 0 and ew > 0 else 0
        fke = round(fi / max(egg_mass, 0.1) / 10, 3) if egg_mass > 0 else 0
        mortality = round(0.05 * week + random.uniform(0, 2), 2)
        mortality = min(mortality, 10)
        shell_strength = round(max(28, 42 - 0.08 * week + random.uniform(-2, 2)), 1)
        haugh = round(max(60, 92 - 0.2 * week + random.uniform(-3, 3)), 1)

        return [prod, ew, egg_mass, fi, fdz, fke, bw, mortality, shell_strength, haugh]

    breeds = ["Hy-Line W-36", "Hy-Line Brown", "ISA Brown", "Lohmann LSL-Classic"]
    rows = []
    for breed in breeds:
        for week in range(0, 101):  # 0 to 100 weeks
            metrics = layer_curve(breed, week)
            rows.append([breed, week] + metrics)

    filepath = os.path.join(DATA_DIR, "performance_management.csv")
    with open(filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(rows)

    print(f"[OK] Layer Performance: {len(rows)} rows ({len(breeds)} breeds × 101 weeks)")
    return rows


# ============================================================
# 2. NUTRIENT REQUIREMENTS - layer hens
# ============================================================
def generate_nutrient_requirements():
    """Generate layer nutrient requirement specifications.

    Phases: Starter (0-6w), Grower (7-12w), Developer (13-17w),
            Pre-Lay (18-20w), Lay I (21-40w), Lay II (41-60w), Lay III (61w+)
    """
    phases = [
        "Starter 0-6w",
        "Grower 7-12w",
        "Developer 13-17w",
        "Pre-Lay 18-20w",
        "Lay I 21-40w",
        "Lay II 41-60w",
        "Lay III 61w+",
    ]
    breeds = ["Hy-Line W-36", "Hy-Line Brown", "ISA Brown", "Lohmann LSL-Classic"]

    fields = [
        "Breed", "Phase", "ME_kcal_kg", "CP_pct", "Ca_pct", "Avail_P_pct",
        "Na_pct", "Lys_pct", "Met_pct", "M_C_pct", "Thr_pct", "Trp_pct",
        "Val_pct", "Arg_pct", "Ile_pct",
        "SID_Lys_pct", "SID_Met_pct", "SID_M_C_pct", "SID_Thr_pct", "SID_Trp_pct",
        "Choline_mg_kg", "Linoleic_Acid_pct",
    ]

    # Base requirements by phase (Hy-Line W-36, then scaled for others)
    phase_specs = {
        "Starter 0-6w": {
            "ME_kcal_kg": 2900, "CP_pct": 20.0, "Ca_pct": 1.00, "Avail_P_pct": 0.45,
            "Na_pct": 0.18, "Lys_pct": 1.10, "Met_pct": 0.45, "M_C_pct": 0.80,
            "Thr_pct": 0.72, "Trp_pct": 0.20, "Val_pct": 0.78, "Arg_pct": 1.10,
            "Ile_pct": 0.65,
            "SID_Lys_pct": 0.98, "SID_Met_pct": 0.40, "SID_M_C_pct": 0.72,
            "SID_Thr_pct": 0.65, "SID_Trp_pct": 0.18,
            "Choline_mg_kg": 1300, "Linoleic_Acid_pct": 1.0,
        },
        "Grower 7-12w": {
            "ME_kcal_kg": 2850, "CP_pct": 17.0, "Ca_pct": 0.90, "Avail_P_pct": 0.40,
            "Na_pct": 0.17, "Lys_pct": 0.85, "Met_pct": 0.35, "M_C_pct": 0.65,
            "Thr_pct": 0.58, "Trp_pct": 0.17, "Val_pct": 0.62, "Arg_pct": 0.85,
            "Ile_pct": 0.55,
            "SID_Lys_pct": 0.76, "SID_Met_pct": 0.32, "SID_M_C_pct": 0.58,
            "SID_Thr_pct": 0.52, "SID_Trp_pct": 0.15,
            "Choline_mg_kg": 1200, "Linoleic_Acid_pct": 1.0,
        },
        "Developer 13-17w": {
            "ME_kcal_kg": 2800, "CP_pct": 15.5, "Ca_pct": 1.00, "Avail_P_pct": 0.35,
            "Na_pct": 0.16, "Lys_pct": 0.75, "Met_pct": 0.32, "M_C_pct": 0.60,
            "Thr_pct": 0.52, "Trp_pct": 0.15, "Val_pct": 0.55, "Arg_pct": 0.75,
            "Ile_pct": 0.48,
            "SID_Lys_pct": 0.67, "SID_Met_pct": 0.29, "SID_M_C_pct": 0.54,
            "SID_Thr_pct": 0.47, "SID_Trp_pct": 0.14,
            "Choline_mg_kg": 1100, "Linoleic_Acid_pct": 0.9,
        },
        "Pre-Lay 18-20w": {
            "ME_kcal_kg": 2800, "CP_pct": 16.5, "Ca_pct": 2.50, "Avail_P_pct": 0.42,
            "Na_pct": 0.17, "Lys_pct": 0.85, "Met_pct": 0.38, "M_C_pct": 0.68,
            "Thr_pct": 0.58, "Trp_pct": 0.17, "Val_pct": 0.65, "Arg_pct": 0.85,
            "Ile_pct": 0.52,
            "SID_Lys_pct": 0.76, "SID_Met_pct": 0.34, "SID_M_C_pct": 0.61,
            "SID_Thr_pct": 0.52, "SID_Trp_pct": 0.15,
            "Choline_mg_kg": 1200, "Linoleic_Acid_pct": 1.0,
        },
        "Lay I 21-40w": {
            "ME_kcal_kg": 2825, "CP_pct": 17.5, "Ca_pct": 4.00, "Avail_P_pct": 0.40,
            "Na_pct": 0.18, "Lys_pct": 0.85, "Met_pct": 0.40, "M_C_pct": 0.72,
            "Thr_pct": 0.60, "Trp_pct": 0.18, "Val_pct": 0.68, "Arg_pct": 0.88,
            "Ile_pct": 0.55,
            "SID_Lys_pct": 0.76, "SID_Met_pct": 0.36, "SID_M_C_pct": 0.65,
            "SID_Thr_pct": 0.54, "SID_Trp_pct": 0.16,
            "Choline_mg_kg": 1400, "Linoleic_Acid_pct": 1.25,
        },
        "Lay II 41-60w": {
            "ME_kcal_kg": 2825, "CP_pct": 16.5, "Ca_pct": 4.20, "Avail_P_pct": 0.38,
            "Na_pct": 0.17, "Lys_pct": 0.78, "Met_pct": 0.36, "M_C_pct": 0.66,
            "Thr_pct": 0.55, "Trp_pct": 0.17, "Val_pct": 0.62, "Arg_pct": 0.80,
            "Ile_pct": 0.50,
            "SID_Lys_pct": 0.70, "SID_Met_pct": 0.32, "SID_M_C_pct": 0.59,
            "SID_Thr_pct": 0.50, "SID_Trp_pct": 0.15,
            "Choline_mg_kg": 1400, "Linoleic_Acid_pct": 1.25,
        },
        "Lay III 61w+": {
            "ME_kcal_kg": 2825, "CP_pct": 15.5, "Ca_pct": 4.40, "Avail_P_pct": 0.35,
            "Na_pct": 0.16, "Lys_pct": 0.72, "Met_pct": 0.34, "M_C_pct": 0.62,
            "Thr_pct": 0.52, "Trp_pct": 0.16, "Val_pct": 0.58, "Arg_pct": 0.75,
            "Ile_pct": 0.48,
            "SID_Lys_pct": 0.65, "SID_Met_pct": 0.30, "SID_M_C_pct": 0.56,
            "SID_Thr_pct": 0.47, "SID_Trp_pct": 0.14,
            "Choline_mg_kg": 1350, "Linoleic_Acid_pct": 1.25,
        },
    }

    # Breed adjustment factors
    breed_factors = {
        "Hy-Line W-36": {"ME": 1.0, "CP": 1.0, "Ca": 1.0, "Other": 1.0},
        "Hy-Line Brown": {"ME": 1.0, "CP": 1.03, "Ca": 1.02, "Other": 1.02},
        "ISA Brown": {"ME": 1.0, "CP": 1.02, "Ca": 1.01, "Other": 1.01},
        "Lohmann LSL-Classic": {"ME": 1.0, "CP": 0.98, "Ca": 0.98, "Other": 0.98},
    }

    rows = []
    for breed in breeds:
        bf = breed_factors[breed]
        for phase in phases:
            spec = phase_specs[phase]
            row = [breed, phase]
            for field in fields[2:]:
                val = spec.get(field, 0)
                if field in ("ME_kcal_kg",):
                    val = round(val * bf["ME"])
                elif field in ("CP_pct",):
                    val = round(val * bf["CP"], 1)
                elif field in ("Ca_pct",):
                    val = round(val * bf["Ca"], 2)
                else:
                    val = round(val * bf["Other"], 2) if isinstance(val, float) else val
                row.append(val)
            rows.append(row)

    filepath = os.path.join(DATA_DIR, "nutrient_requirements.csv")
    with open(filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(rows)

    print(f"[OK] Layer Nutrient Requirements: {len(rows)} rows ({len(breeds)} breeds × {len(phases)} phases)")

    # Generate vitamin/mineral specs
    vm_fields = [
        "Breed", "Phase",
        "Vitamin_A_IU_kg", "Vitamin_D3_IU_kg", "Vitamin_E_IU_kg",
        "Vitamin_K3_mg_kg", "Vitamin_B1_mg_kg", "Vitamin_B2_mg_kg",
        "Vitamin_B6_mg_kg", "Vitamin_B12_mcg_kg", "Niacin_mg_kg",
        "Pantothenic_Acid_mg_kg", "Folic_Acid_mg_kg", "Biotin_mcg_kg",
        "Fe_mg_kg", "Cu_mg_kg", "Zn_mg_kg", "Mn_mg_kg", "Se_mg_kg", "I_mg_kg",
    ]

    vm_phase_specs = {
        "Starter 0-6w": {
            "Vitamin_A_IU_kg": 10000, "Vitamin_D3_IU_kg": 4000, "Vitamin_E_IU_kg": 30,
            "Vitamin_K3_mg_kg": 2.5, "Vitamin_B1_mg_kg": 2.5, "Vitamin_B2_mg_kg": 6.0,
            "Vitamin_B6_mg_kg": 4.0, "Vitamin_B12_mcg_kg": 20, "Niacin_mg_kg": 50,
            "Pantothenic_Acid_mg_kg": 12, "Folic_Acid_mg_kg": 1.5, "Biotin_mcg_kg": 150,
            "Fe_mg_kg": 80, "Cu_mg_kg": 12, "Zn_mg_kg": 80, "Mn_mg_kg": 80,
            "Se_mg_kg": 0.25, "I_mg_kg": 1.0,
        },
        "Grower 7-12w": {
            "Vitamin_A_IU_kg": 10000, "Vitamin_D3_IU_kg": 4000, "Vitamin_E_IU_kg": 25,
            "Vitamin_K3_mg_kg": 2.0, "Vitamin_B1_mg_kg": 2.0, "Vitamin_B2_mg_kg": 5.0,
            "Vitamin_B6_mg_kg": 3.0, "Vitamin_B12_mcg_kg": 15, "Niacin_mg_kg": 40,
            "Pantothenic_Acid_mg_kg": 10, "Folic_Acid_mg_kg": 1.0, "Biotin_mcg_kg": 100,
            "Fe_mg_kg": 70, "Cu_mg_kg": 10, "Zn_mg_kg": 70, "Mn_mg_kg": 70,
            "Se_mg_kg": 0.20, "I_mg_kg": 1.0,
        },
        "Developer 13-17w": {
            "Vitamin_A_IU_kg": 10000, "Vitamin_D3_IU_kg": 4000, "Vitamin_E_IU_kg": 25,
            "Vitamin_K3_mg_kg": 2.0, "Vitamin_B1_mg_kg": 2.0, "Vitamin_B2_mg_kg": 4.0,
            "Vitamin_B6_mg_kg": 3.0, "Vitamin_B12_mcg_kg": 15, "Niacin_mg_kg": 35,
            "Pantothenic_Acid_mg_kg": 8, "Folic_Acid_mg_kg": 1.0, "Biotin_mcg_kg": 80,
            "Fe_mg_kg": 60, "Cu_mg_kg": 10, "Zn_mg_kg": 60, "Mn_mg_kg": 60,
            "Se_mg_kg": 0.20, "I_mg_kg": 1.0,
        },
        "Pre-Lay 18-20w": {
            "Vitamin_A_IU_kg": 12000, "Vitamin_D3_IU_kg": 4500, "Vitamin_E_IU_kg": 30,
            "Vitamin_K3_mg_kg": 3.0, "Vitamin_B1_mg_kg": 2.5, "Vitamin_B2_mg_kg": 6.0,
            "Vitamin_B6_mg_kg": 4.0, "Vitamin_B12_mcg_kg": 20, "Niacin_mg_kg": 45,
            "Pantothenic_Acid_mg_kg": 12, "Folic_Acid_mg_kg": 1.5, "Biotin_mcg_kg": 120,
            "Fe_mg_kg": 80, "Cu_mg_kg": 15, "Zn_mg_kg": 80, "Mn_mg_kg": 80,
            "Se_mg_kg": 0.25, "I_mg_kg": 1.2,
        },
        "Lay I 21-40w": {
            "Vitamin_A_IU_kg": 12000, "Vitamin_D3_IU_kg": 5000, "Vitamin_E_IU_kg": 35,
            "Vitamin_K3_mg_kg": 3.0, "Vitamin_B1_mg_kg": 3.0, "Vitamin_B2_mg_kg": 8.0,
            "Vitamin_B6_mg_kg": 5.0, "Vitamin_B12_mcg_kg": 25, "Niacin_mg_kg": 55,
            "Pantothenic_Acid_mg_kg": 14, "Folic_Acid_mg_kg": 2.0, "Biotin_mcg_kg": 180,
            "Fe_mg_kg": 80, "Cu_mg_kg": 15, "Zn_mg_kg": 100, "Mn_mg_kg": 100,
            "Se_mg_kg": 0.30, "I_mg_kg": 1.2,
        },
        "Lay II 41-60w": {
            "Vitamin_A_IU_kg": 12000, "Vitamin_D3_IU_kg": 5000, "Vitamin_E_IU_kg": 35,
            "Vitamin_K3_mg_kg": 3.0, "Vitamin_B1_mg_kg": 3.0, "Vitamin_B2_mg_kg": 8.0,
            "Vitamin_B6_mg_kg": 5.0, "Vitamin_B12_mcg_kg": 25, "Niacin_mg_kg": 55,
            "Pantothenic_Acid_mg_kg": 14, "Folic_Acid_mg_kg": 2.0, "Biotin_mcg_kg": 180,
            "Fe_mg_kg": 80, "Cu_mg_kg": 15, "Zn_mg_kg": 100, "Mn_mg_kg": 100,
            "Se_mg_kg": 0.30, "I_mg_kg": 1.2,
        },
        "Lay III 61w+": {
            "Vitamin_A_IU_kg": 12000, "Vitamin_D3_IU_kg": 5500, "Vitamin_E_IU_kg": 40,
            "Vitamin_K3_mg_kg": 3.0, "Vitamin_B1_mg_kg": 3.0, "Vitamin_B2_mg_kg": 8.0,
            "Vitamin_B6_mg_kg": 5.0, "Vitamin_B12_mcg_kg": 25, "Niacin_mg_kg": 55,
            "Pantothenic_Acid_mg_kg": 14, "Folic_Acid_mg_kg": 2.0, "Biotin_mcg_kg": 180,
            "Fe_mg_kg": 80, "Cu_mg_kg": 15, "Zn_mg_kg": 100, "Mn_mg_kg": 100,
            "Se_mg_kg": 0.30, "I_mg_kg": 1.2,
        },
    }

    vm_rows = []
    for breed in breeds:
        for phase in phases:
            row = [breed, phase]
            spec = vm_phase_specs[phase]
            for f in vm_fields[2:]:
                row.append(spec.get(f, 0))
            vm_rows.append(row)

    vm_filepath = os.path.join(DATA_DIR, "nutrient_vitamin_mineral.csv")
    with open(vm_filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(vm_fields)
        w.writerows(vm_rows)

    print(f"[OK] Layer Vitamin & Mineral: {len(vm_rows)} rows")
    return rows


# ============================================================
# 3. EVALUATION QUERIES - 120 layer-specific questions
# ============================================================
def generate_evaluation_queries():
    """Generate 120 layer-specific evaluation queries across 6 categories."""
    queries = {
        "Performance Management Set 1 (Production)": [
            {"id": "LPM-001", "query": "What is the peak hen-day egg production percentage for Hy-Line W-36?", "type": "single-value"},
            {"id": "LPM-002", "query": "What is the average egg weight for Hy-Line Brown at 40 weeks?", "type": "single-value"},
            {"id": "LPM-003", "query": "What is the daily feed intake of ISA Brown at peak production?", "type": "single-value"},
            {"id": "LPM-004", "query": "What is the body weight of Lohmann LSL-Classic at 18 weeks?", "type": "single-value"},
            {"id": "LPM-005", "query": "What is the egg mass per hen per day for Hy-Line W-36 at 30 weeks?", "type": "single-value"},
            {"id": "LPM-006", "query": "Compare the peak egg production between Hy-Line W-36 and ISA Brown.", "type": "comparison"},
            {"id": "LPM-007", "query": "Compare egg weight between Hy-Line Brown and Lohmann LSL-Classic at 50 weeks.", "type": "comparison"},
            {"id": "LPM-008", "query": "How does feed intake change as a hen ages from peak lay to late lay?", "type": "open-ended"},
            {"id": "LPM-009", "query": "Describe the typical egg production curve of a commercial layer.", "type": "open-ended"},
            {"id": "LPM-010", "query": "What factors influence feed intake in laying hens?", "type": "open-ended"},
            {"id": "LPM-011", "query": "What is the feed per dozen eggs for Hy-Line Brown at 30 weeks?", "type": "single-value"},
            {"id": "LPM-012", "query": "What is the feed per kg egg mass for Lohmann LSL at 60 weeks?", "type": "single-value"},
            {"id": "LPM-013", "query": "Compare body weight between Hy-Line W-36 and Hy-Line Brown at 40 weeks.", "type": "comparison"},
            {"id": "LPM-014", "query": "How does egg mass change over the laying cycle?", "type": "open-ended"},
            {"id": "LPM-015", "query": "What is the relationship between feed intake and egg production?", "type": "open-ended"},
            {"id": "LPM-016", "query": "Compare the mortality rates of ISA Brown and Hy-Line W-36.", "type": "comparison"},
            {"id": "LPM-017", "query": "What is the egg shell breaking strength for Hy-Line W-36 at 40 weeks?", "type": "single-value"},
            {"id": "LPM-018", "query": "What is the Haugh unit value for Hy-Line Brown at 30 weeks?", "type": "single-value"},
            {"id": "LPM-019", "query": "Explain the economic importance of feed conversion efficiency in egg production.", "type": "open-ended"},
            {"id": "LPM-020", "query": "Compare the production characteristics of ISA Brown vs Lohmann LSL-Classic.", "type": "comparison"},
        ],
        "Performance Management Set 2 (Egg Quality)": [
            {"id": "LPM-021", "query": "What is the shell breaking strength for ISA Brown at 60 weeks?", "type": "single-value"},
            {"id": "LPM-022", "query": "What is the Haugh unit for Lohmann LSL-Classic at 70 weeks?", "type": "single-value"},
            {"id": "LPM-023", "query": "How does egg shell quality change as hens age?", "type": "open-ended"},
            {"id": "LPM-024", "query": "Compare Haugh unit values between white and brown egg layers.", "type": "comparison"},
            {"id": "LPM-025", "query": "What factors affect egg shell breaking strength?", "type": "open-ended"},
            {"id": "LPM-026", "query": "Describe the relationship between hen age and internal egg quality.", "type": "open-ended"},
            {"id": "LPM-027", "query": "What is the shell strength of Hy-Line W-36 at 80 weeks?", "type": "single-value"},
            {"id": "LPM-028", "query": "Compare shell breaking strength at 30 weeks vs 70 weeks for Hy-Line Brown.", "type": "comparison"},
            {"id": "LPM-029", "query": "What nutritional factors influence egg shell quality?", "type": "open-ended"},
            {"id": "LPM-030", "query": "How does egg weight affect eggshell quality parameters?", "type": "open-ended"},
            {"id": "LPM-031", "query": "What is the albumen height indicator for ISA Brown at peak production?", "type": "single-value"},
            {"id": "LPM-032", "query": "Explain the economic impact of egg quality in commercial layer operations.", "type": "open-ended"},
            {"id": "LPM-033", "query": "Compare egg quality parameters between Hy-Line W-36 and Lohmann LSL.", "type": "comparison"},
            {"id": "LPM-034", "query": "How does nutrition affect Haugh unit values?", "type": "open-ended"},
            {"id": "LPM-035", "query": "What is the relationship between calcium metabolism and shell quality?", "type": "open-ended"},
            {"id": "LPM-036", "query": "Describe the effects of heat stress on egg shell quality.", "type": "open-ended"},
            {"id": "LPM-037", "query": "Compare the Haugh unit of a 35-week-old vs 75-week-old ISA Brown hen.", "type": "comparison"},
            {"id": "LPM-038", "query": "What management practices improve egg shell quality in late lay?", "type": "open-ended"},
            {"id": "LPM-039", "query": "How does egg size influence shell thickness?", "type": "open-ended"},
            {"id": "LPM-040", "query": "What is the role of vitamin D3 in eggshell formation?", "type": "open-ended"},
        ],
        "Nutrient Requirements": [
            {"id": "LNR-001", "query": "What is the calcium requirement for Hy-Line W-36 in Lay I phase?", "type": "single-value"},
            {"id": "LNR-002", "query": "What is the crude protein requirement for ISA Brown in the Starter phase?", "type": "single-value"},
            {"id": "LNR-003", "query": "What is the available phosphorus requirement for Lohmann LSL in Lay II?", "type": "single-value"},
            {"id": "LNR-004", "query": "What is the methionine requirement for Hy-Line Brown in Lay I?", "type": "single-value"},
            {"id": "LNR-005", "query": "What is the SID lysine requirement for Hy-Line W-36 in Starter phase?", "type": "single-value"},
            {"id": "LNR-006", "query": "Compare calcium requirements from Pre-Lay to Lay III in layer diets.", "type": "comparison"},
            {"id": "LNR-007", "query": "How do amino acid requirements change from starter to lay phases?", "type": "open-ended"},
            {"id": "LNR-008", "query": "What is the choline requirement for Hy-Line Brown in Lay I?", "type": "single-value"},
            {"id": "LNR-009", "query": "Compare the calcium and phosphorus ratio across different lay phases.", "type": "comparison"},
            {"id": "LNR-010", "query": "Explain why calcium requirement increases dramatically at the onset of lay.", "type": "open-ended"},
            {"id": "LNR-011", "query": "What is the linoleic acid requirement for Hy-Line W-36 in Lay I?", "type": "single-value"},
            {"id": "LNR-012", "query": "What is the sodium requirement for ISA Brown during Pre-Lay?", "type": "single-value"},
            {"id": "LNR-013", "query": "Compare methionine+cysteine requirements across starter, grower, and lay phases.", "type": "comparison"},
            {"id": "LNR-014", "query": "Describe the importance of amino acid balancing in layer diets.", "type": "open-ended"},
            {"id": "LNR-015", "query": "What is the Vitamin D3 requirement for Hy-Line W-36 in Lay II?", "type": "single-value"},
            {"id": "LNR-016", "query": "How do calcium and phosphorus requirements differ between broiler and layer diets?", "type": "comparison"},
            {"id": "LNR-017", "query": "What is the zinc requirement for Lohmann LSL in the Starter phase?", "type": "single-value"},
            {"id": "LNR-018", "query": "Explain the importance of vitamin and mineral specifications in layer diets.", "type": "open-ended"},
            {"id": "LNR-019", "query": "Compare the tryptophan requirement between Hy-Line W-36 and Hy-Line Brown.", "type": "comparison"},
            {"id": "LNR-020", "query": "How do nutrient requirements differ between pullet rearing and laying phases?", "type": "open-ended"},
        ],
        "Definitions": [
            {"id": "LDEF-001", "query": "What is the definition of Hen-Day Egg Production?", "type": "definition"},
            {"id": "LDEF-002", "query": "Define Haugh Unit.", "type": "definition"},
            {"id": "LDEF-003", "query": "What is the Pre-Lay phase in layer nutrition?", "type": "definition"},
            {"id": "LDEF-004", "query": "Define Egg Mass (g/hen/day).", "type": "definition"},
            {"id": "LDEF-005", "query": "What is egg shell breaking strength?", "type": "definition"},
            {"id": "LDEF-006", "query": "Define the Lighting Program in layer management.", "type": "definition"},
            {"id": "LDEF-007", "query": "What is a Pullet?", "type": "definition"},
            {"id": "LDEF-008", "query": "Define Feed per Dozen Eggs.", "type": "definition"},
            {"id": "LDEF-009", "query": "What is the meaning of Peak Production in layers?", "type": "definition"},
            {"id": "LDEF-010", "query": "Define Forced Molting.", "type": "definition"},
            {"id": "LDEF-011", "query": "What is Egg Shell Quality?", "type": "definition"},
            {"id": "LDEF-012", "query": "Define albumen height.", "type": "definition"},
            {"id": "LDEF-013", "query": "What is a caged layer vs cage-free production?", "type": "definition"},
            {"id": "LDEF-014", "query": "Define the Fatty Liver Hemorrhagic Syndrome in layers.", "type": "definition"},
            {"id": "LDEF-015", "query": "What is Egg Yolk Pigmentation?", "type": "definition"},
            {"id": "LDEF-016", "query": "Define Egg Drop Syndrome.", "type": "definition"},
            {"id": "LDEF-017", "query": "What is the Developer phase in pullet rearing?", "type": "definition"},
            {"id": "LDEF-018", "query": "Define Hen-Housed Egg Production.", "type": "definition"},
            {"id": "LDEF-019", "query": "What is the Roche Yolk Color Fan?", "type": "definition"},
            {"id": "LDEF-020", "query": "Define Sexually Mature in context of pullets.", "type": "definition"},
        ],
        "Feed Ingredient Bank Set 1 (Basics)": [
            {"id": "LFIB-001", "query": "What is the calcium content of Limestone?", "type": "single-value"},
            {"id": "LFIB-002", "query": "What is the crude protein content of Soybean Meal 48%?", "type": "single-value"},
            {"id": "LFIB-003", "query": "What is the metabolizable energy of Corn Grain?", "type": "single-value"},
            {"id": "LFIB-004", "query": "What is the available phosphorus content of Dicalcium Phosphate?", "type": "single-value"},
            {"id": "LFIB-005", "query": "What is the lysine content of Soybean Meal 48%?", "type": "single-value"},
            {"id": "LFIB-006", "query": "Compare calcium sources for layer diets: limestone vs dicalcium phosphate.", "type": "comparison"},
            {"id": "LFIB-007", "query": "Which feed ingredients provide the most available calcium for eggshell formation?", "type": "open-ended"},
            {"id": "LFIB-008", "query": "Compare the energy content of Corn Grain vs Wheat Grain.", "type": "comparison"},
            {"id": "LFIB-009", "query": "What are the main protein sources available for layer diet formulation?", "type": "open-ended"},
            {"id": "LFIB-010", "query": "Describe the role of oyster shell in layer nutrition.", "type": "open-ended"},
            {"id": "LFIB-011", "query": "What is the sodium content of Salt?", "type": "single-value"},
            {"id": "LFIB-012", "query": "What is the methionine content of DL-Methionine supplement?", "type": "single-value"},
            {"id": "LFIB-013", "query": "Compare the amino acid profiles of Soybean Meal and Canola Meal.", "type": "comparison"},
            {"id": "LFIB-014", "query": "Which feed ingredients are good sources of linoleic acid for laying hens?", "type": "open-ended"},
            {"id": "LFIB-015", "query": "Explain the importance of calcium particle size in layer feeds.", "type": "open-ended"},
            {"id": "LFIB-016", "query": "What is the calcium digestibility of Meat and Bone Meal?", "type": "single-value"},
            {"id": "LFIB-017", "query": "Compare the phosphorus digestibility between plant and animal sources.", "type": "comparison"},
            {"id": "LFIB-018", "query": "What feed additives support egg shell quality in late lay?", "type": "open-ended"},
            {"id": "LFIB-019", "query": "Compare the crude fiber content of ingredient sources used in layer feeds.", "type": "comparison"},
            {"id": "LFIB-020", "query": "Describe the role of synthetic amino acids in low-protein layer diets.", "type": "open-ended"},
        ],
        "Feed Ingredient Bank Set 2 (Digestibility)": [
            {"id": "LFIB-021", "query": "What is the protein digestibility of Soybean Meal 48%?", "type": "single-value"},
            {"id": "LFIB-022", "query": "What is the SID lysine value for Corn Grain?", "type": "single-value"},
            {"id": "LFIB-023", "query": "What is the calcium digestibility of Limestone?", "type": "single-value"},
            {"id": "LFIB-024", "query": "Compare protein digestibility between animal and plant protein meals.", "type": "comparison"},
            {"id": "LFIB-025", "query": "How does crude fiber affect energy digestibility in layers?", "type": "open-ended"},
            {"id": "LFIB-026", "query": "What is the phosphorus digestibility of Dicalcium Phosphate?", "type": "single-value"},
            {"id": "LFIB-027", "query": "Compare the SID lysine of Corn Grain and Sorghum Grain.", "type": "comparison"},
            {"id": "LFIB-028", "query": "What is the role of phytase in improving phosphorus digestibility?", "type": "open-ended"},
            {"id": "LFIB-029", "query": "Describe the importance of standardized ileal digestibility in feed formulation.", "type": "open-ended"},
            {"id": "LFIB-030", "query": "What factors affect calcium digestibility in laying hens?", "type": "open-ended"},
            {"id": "LFIB-031", "query": "What is the fat digestibility of Soybean Oil?", "type": "single-value"},
            {"id": "LFIB-032", "query": "Compare SID methionine values across different protein meals.", "type": "comparison"},
            {"id": "LFIB-033", "query": "How does feed particle size affect nutrient digestibility in layers?", "type": "open-ended"},
            {"id": "LFIB-034", "query": "What is the amino acid digestibility of Fish Meal 65%?", "type": "single-value"},
            {"id": "LFIB-035", "query": "Compare the dry matter digestibility of Corn Grain vs Barley Grain.", "type": "comparison"},
            {"id": "LFIB-036", "query": "How do non-starch polysaccharides affect nutrient digestibility?", "type": "open-ended"},
            {"id": "LFIB-037", "query": "What is the protein digestibility of Cottonseed Meal and what limits its use in layer diets?", "type": "single-value"},
            {"id": "LFIB-038", "query": "Describe the interaction between calcium and phosphorus digestibility in layers.", "type": "open-ended"},
            {"id": "LFIB-039", "query": "How does the form of calcium supplement affect its digestibility?", "type": "open-ended"},
            {"id": "LFIB-040", "query": "What exogenous enzymes improve nutrient digestibility in layer feeds?", "type": "open-ended"},
        ],
    }

    filepath = os.path.join(QUERIES_DIR, "evaluation_queries.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)

    total = sum(len(qs) for qs in queries.values())
    print(f"[OK] Layer Evaluation Queries: {total} queries ({len(queries)} categories)")
    return queries


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  NutriCHAT - Layer Data Generation")
    print("=" * 60)

    print("\nGenerating Layer Performance Management...")
    generate_performance()

    print("\nGenerating Layer Nutrient Requirements...")
    generate_nutrient_requirements()

    print("\nGenerating Layer Evaluation Queries...")
    generate_evaluation_queries()

    print()
    print("=" * 60)
    print("  Layer data generation complete!")
    print(f"  Output directory: {DATA_DIR}")
    print("=" * 60)
