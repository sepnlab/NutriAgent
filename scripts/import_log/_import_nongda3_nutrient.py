"""农大3号 → Nongda 3 营养+维生素数据"""
import sys
sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

B = "Nongda 3"
S = "Nongda 3 Official Manual"

# ── 营养数据（6阶段） ──
# 代谢能在手册中为 MJ/kg，转换为 kcal/kg (1 MJ = 239 kcal)
# 阶段名使用手册原文
phases = ["Starter 0-5w", "Grower 6-12w", "Developer 13-16w",
          "Pre-Lay 17w-5%", "Peak 5%-peak", "Post-Peak <=85%"]

ME  = [12.12*239, 12.12*239, 11.70*239, 11.29*239, 11.08*239, 11.08*239]  # MJ→kcal
CP  = [21.0, 19.0, 16.5, 17.0, 16.5, 15.5]
Ca  = [1.00, 1.00, 0.90, 2.00, 3.75, 3.90]
AvP = [0.46, 0.46, 0.40, 0.36, 0.38, 0.40]
Na  = [0.18, 0.18, 0.18, 0.18, 0.18, 0.18]
LA  = [1.2, 1.2, 1.2, 1.2, 1.5, 1.3]  # 亚油酸
Chol= [500, 500, 400, 400, 400, 400]  # 胆碱 mg/kg

Lys = [1.15, 1.05, 0.78, 0.85, 0.83, 0.76]
Met = [0.50, 0.45, 0.36, 0.39, 0.39, 0.36]
MC  = [0.85, 0.78, 0.65, 0.66, 0.66, 0.62]
Thr = [0.76, 0.72, 0.59, 0.63, 0.61, 0.58]
Trp = [0.23, 0.20, 0.19, 0.20, 0.18, 0.16]
Arg = [1.27, 1.20, 1.04, 1.05, 0.84, 0.78]
Ile = [0.78, 0.71, 0.61, 0.62, 0.62, 0.58]
Val = [0.84, 0.78, 0.65, 0.68, 0.65, 0.60]

# 注意：农大3号手册给出的是总氨基酸，无SID数据
rows = []
for i in range(6):
    r = {"Breed":B, "Phase":phases[i],
         "ME_kcal_kg":str(round(ME[i])),
         "CP_pct":str(CP[i]),
         "Ca_pct":str(Ca[i]),
         "Avail_P_pct":str(AvP[i]),
         "Na_pct":str(Na[i]),
         "Lys_pct":str(Lys[i]),
         "Met_pct":str(Met[i]),
         "M_C_pct":str(MC[i]),
         "Thr_pct":str(Thr[i]),
         "Trp_pct":str(Trp[i]),
         "Arg_pct":str(Arg[i]),
         "Ile_pct":str(Ile[i]),
         "Val_pct":str(Val[i]),
         "Linoleic_Acid_pct":str(LA[i]),
         "Choline_mg_kg":str(Chol[i]),
         "source":S}
    rows.append(r)

write_breed_data(B, "layer", "nutrient", rows, replace=True)

# ── 维生素/微量元素（6阶段，取中值） ──
# 数据来自手册表9
vit_rows = []
vit_phases = phases  # 同6阶段
VA  = [15000, 12000, 10000, 10000, 10000, 10000]
VD3 = [5000, 4500, 4000, 5000, 5000, 5000]
VE  = [30, 20, 12, 12, 12, 12]
VK  = [2.0, 2.0, 1.5, 1.8, 1.8, 1.8]
VB1 = [2.0, 2.0, 1.8, 2.0, 2.0, 2.0]
VB2 = [8.0, 8.0, 6.0, 7.0, 7.0, 7.0]
VB6 = [3.0, 3.0, 2.4, 2.8, 2.8, 2.8]
VB12= [0.02, 0.02, 0.02, 0.02, 0.02, 0.02]  # mg/kg → 需转 mcg/kg
Niac= [35, 35, 25, 30, 30, 30]
PAA = [10, 10, 9, 10, 10, 10]
Fol = [1.1, 1.1, 0.8, 1.0, 1.0, 1.0]
Bio = [0.25, 0.25, 0.20, 0.24, 0.24, 0.24]  # mg/kg → mcg/kg
Fe  = [100, 100, 80, 80, 80, 80]
Cu  = [10, 10, 8, 10, 10, 10]
Zn  = [100, 100, 80, 100, 100, 100]
Mn  = [100, 100, 80, 100, 100, 100]
Se  = [0.30, 0.30, 0.30, 0.30, 0.30, 0.30]
I   = [0.40, 0.40, 0.35, 0.40, 0.40, 0.40]

for i in range(6):
    r = {"Breed":B, "Phase":vit_phases[i],
         "Vitamin_A_IU_kg":str(VA[i]),
         "Vitamin_D3_IU_kg":str(VD3[i]),
         "Vitamin_E_IU_kg":str(VE[i]),
         "Vitamin_K3_mg_kg":str(VK[i]),
         "Vitamin_B1_mg_kg":str(VB1[i]),
         "Vitamin_B2_mg_kg":str(VB2[i]),
         "Vitamin_B6_mg_kg":str(VB6[i]),
         "Vitamin_B12_mcg_kg":str(VB12[i] * 1000),  # mg → mcg
         "Niacin_mg_kg":str(Niac[i]),
         "Pantothenic_Acid_mg_kg":str(PAA[i]),
         "Folic_Acid_mg_kg":str(Fol[i]),
         "Biotin_mcg_kg":str(Bio[i] * 1000),  # mg → mcg
         "Fe_mg_kg":str(Fe[i]),
         "Cu_mg_kg":str(Cu[i]),
         "Zn_mg_kg":str(Zn[i]),
         "Mn_mg_kg":str(Mn[i]),
         "Se_mg_kg":str(Se[i]),
         "I_mg_kg":str(I[i]),
         "source":S}
    vit_rows.append(r)

write_breed_data(B, "layer", "vitamin", vit_rows, replace=True)

print("Nongda 3 营养+维生素导入完成")
