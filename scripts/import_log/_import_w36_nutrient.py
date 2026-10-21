"""海兰W36 → 营养数据（育雏育成5阶段）"""
import sys, re
sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

B = "Hy-Line W-36"
S = "Hy-Line W-36 Official Manual"

def mid(r):
    parts = re.split(r'[~–-]', str(r).replace(' ', '').replace(',',''))
    if len(parts) == 2:
        try: return round((float(parts[0]) + float(parts[1])) / 2, 1)
        except: pass
    try: return float(r.replace(',',''))
    except: return 0

# 育雏育成期：5阶段 × 营养指标
# 数据列顺序：开食料1, 开食料2, 育雏料, 育成料, 产前料
# 营养指标行：ME(kcal), CP%, Ca%, AvailP%, Na%, Cl%, 亚油酸%, 胆碱mg/kg
# AA指标：SID/Total 对

rearing = {
    "phase": ["Starter 1 (0-3w)", "Starter 2 (4-6w)", "Grower (7-12w)",
              "Developer (13-16w)", "Pre-Lay (17w-5%)"],
    "ME":     [3032, 3032, 3008, 2965, 2999],
    "CP":     [20.0, 18.25, 17.5, 16.0, 16.5],
    "Ca":     [1.05, 1.00, 0.95, 0.90, 2.50],
    "AvailP": [0.48, 0.47, 0.45, 0.40, 0.43],
    "Na":     [0.18, 0.17, 0.17, 0.18, 0.18],
    "Cl":     [0.18, 0.17, 0.17, 0.18, 0.18],
    "LA":     [1.20, 1.20, 1.20, 1.20, 1.20],
    "Choline":[2000, 2000, 1800, 1500, 1500],
    # (SID, Total) pairs
    "Lys":    [(1.05,1.15), (0.98,1.07), (0.90,0.96), (0.76,0.83), (0.78,0.85)],
    "Met":    [(0.47,0.51), (0.44,0.47), (0.40,0.44), (0.36,0.38), (0.38,0.41)],
    "MC":     [(0.74,0.83), (0.74,0.83), (0.67,0.75), (0.59,0.67), (0.66,0.74)],
    "Thr":    [(0.69,0.82), (0.66,0.77), (0.60,0.70), (0.52,0.62), (0.55,0.64)],
    "Trp":    [(0.18,0.21), (0.18,0.21), (0.17,0.20), (0.15,0.18), (0.16,0.20)],
    "Arg":    [(1.12,1.21), (1.05,1.13), (0.94,1.01), (0.81,0.87), (0.83,0.90)],
    "Ile":    [(0.74,0.79), (0.71,0.76), (0.65,0.70), (0.57,0.61), (0.62,0.67)],
    "Val":    [(0.76,0.83), (0.73,0.80), (0.69,0.76), (0.61,0.67), (0.66,0.73)],
}

rows = []
for i in range(5):
    r = {"Breed":B, "Phase":rearing["phase"][i],
         "ME_kcal_kg":str(rearing["ME"][i]),
         "CP_pct":str(rearing["CP"][i]),
         "Ca_pct":str(rearing["Ca"][i]),
         "Avail_P_pct":str(rearing["AvailP"][i]),
         "Na_pct":str(rearing["Na"][i]),
         "Linoleic_Acid_pct":str(rearing["LA"][i]),
         "Choline_mg_kg":str(rearing["Choline"][i]),
         "source":S}
    # 氨基酸（注意列名映射）
    aa_map = {"Lys":"Lys","Met":"Met","MC":"M_C","Thr":"Thr","Trp":"Trp"}
    for aa, csv_aa in aa_map.items():
        sid, total = rearing[aa][i]
        r[f"{csv_aa}_pct"] = str(total)
        r[f"SID_{csv_aa}_pct"] = str(sid)
    # Arg, Ile, Val: 只有 Total，无 SID 列
    for aa in ["Arg","Ile","Val"]:
        sid, total = rearing[aa][i]
        r[f"{aa}_pct"] = str(total)
    rows.append(r)

write_breed_data(B, "layer", "nutrient", rows, replace=True)
print("W36 营养数据导入完成 ✅")
