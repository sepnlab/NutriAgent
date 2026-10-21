"""海兰褐 → Hy-Line Brown 营养数据"""
import sys
sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

B = "Hy-Line Brown"
S = "Hy-Line Brown Official Manual"

# 育雏育成期：5阶段（与W36同结构，数值不同）
# 数据：ME(kcal,取中值), CP%, Ca%, AvailP%, Na%, 亚油酸%, 胆碱mg/kg
# AA格式：(SID, Total) 对，范围值取中值
phases = ["Starter 1 (0-3w)", "Starter 2 (4-6w)", "Grower (7-12w)",
          "Developer (13-16w)", "Pre-Lay (17w-5%)"]

ME   = [3000, 2950, 2900, 2850, 2875]
CP   = [20.0, 18.0, 17.0, 15.5, 16.5]
Ca   = [1.05, 1.00, 0.95, 0.90, 2.50]
AvP  = [0.45, 0.44, 0.43, 0.38, 0.42]
Na   = [0.18, 0.18, 0.18, 0.18, 0.18]
LA   = [1.20, 1.20, 1.20, 1.20, 1.20]
Chol = [2000, 1800, 1800, 1500, 1800]

Lys = [(1.07,1.17), (0.92,1.00), (0.82,0.89), (0.60,0.66), (0.72,0.78)]
Met = [(0.48,0.52), (0.42,0.45), (0.39,0.43), (0.28,0.30), (0.35,0.38)]
MC  = [(0.82,0.91), (0.72,0.81), (0.66,0.74), (0.50,0.57), (0.62,0.70)]
Thr = [(0.69,0.82), (0.60,0.70), (0.55,0.64), (0.41,0.49), (0.50,0.58)]
Trp = [(0.19,0.22), (0.17,0.20), (0.17,0.20), (0.13,0.16), (0.16,0.20)]
Arg = [(1.11,1.20), (0.96,1.03), (0.85,0.91), (0.63,0.68), (0.75,0.81)]
Ile = [(0.75,0.80), (0.66,0.71), (0.61,0.66), (0.45,0.48), (0.56,0.61)]
Val = [(0.77,0.84), (0.68,0.75), (0.64,0.70), (0.48,0.53), (0.61,0.67)]

rows = []
for i in range(5):
    r = {"Breed":B, "Phase":phases[i],
         "ME_kcal_kg":str(ME[i]), "CP_pct":str(CP[i]),
         "Ca_pct":str(Ca[i]), "Avail_P_pct":str(AvP[i]),
         "Na_pct":str(Na[i]), "Linoleic_Acid_pct":str(LA[i]),
         "Choline_mg_kg":str(Chol[i]), "source":S}
    # AA: SID + Total
    for aa_name, data in [("Lys",Lys),("Met",Met),("MC",MC),
                           ("Thr",Thr),("Trp",Trp)]:
        sid, total = data[i]
        csv_name = "M_C" if aa_name == "MC" else aa_name
        r[f"{csv_name}_pct"] = str(total)
        r[f"SID_{csv_name}_pct"] = str(sid)
    # Arg, Ile, Val: Total only
    for aa_name, data in [("Arg",Arg),("Ile",Ile),("Val",Val)]:
        sid, total = data[i]
        r[f"{aa_name}_pct"] = str(total)
    rows.append(r)

write_breed_data(B, "layer", "nutrient", rows, replace=True)
print("Brown 营养数据导入完成")
