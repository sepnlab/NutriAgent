"""海赛克斯褐 → Hisex Brown（营养指南型）"""
import sys; sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

B = "Hisex Brown"
S = "Hisex Brown Official Manual"

# 育雏育成4阶段
nut_rows = []
phases = ["Starter 0-5w", "Grower 6-10w", "Developer 11-16w", "Pre-Lay 17w-2%"]
ME   = [2962, 2862, 2725, 2725]
CP   = [20.5, 19.0, 16.4, 16.8]
Ca   = [1.08, 1.00, 1.10, 2.30]
AvP  = [0.48, 0.48, 0.45, 0.48]
Na   = [0.20, 0.19, 0.18, 0.18]
Lys  = [1.16, 0.98, 0.77, 0.81]
Met  = [0.52, 0.45, 0.37, 0.40]
MC   = [0.93, 0.86, 0.68, 0.66]
Thr  = [0.80, 0.66, 0.54, 0.58]
Trp  = [0.21, 0.20, 0.18, 0.18]
Val  = [0.99, 0.84, 0.65, 0.69]
Ile  = [0.89, 0.76, 0.59, 0.62]
Arg  = [1.08, 0.92, 0.76, 0.81]
SLys = [1.00, 0.85, 0.66, 0.71]
SMet = [0.48, 0.41, 0.34, 0.38]
SMC  = [0.84, 0.74, 0.61, 0.59]
SThr = [0.69, 0.59, 0.46, 0.49]
STrp = [0.19, 0.17, 0.15, 0.16]

for i in range(4):
    r = {"Breed":B,"Phase":phases[i],
         "ME_kcal_kg":str(ME[i]),"CP_pct":str(CP[i]),
         "Ca_pct":str(Ca[i]),"Avail_P_pct":str(AvP[i]),
         "Na_pct":str(Na[i]),
         "Lys_pct":str(Lys[i]),"SID_Lys_pct":str(SLys[i]),
         "Met_pct":str(Met[i]),"SID_Met_pct":str(SMet[i]),
         "M_C_pct":str(MC[i]),"SID_M_C_pct":str(SMC[i]),
         "Thr_pct":str(Thr[i]),"SID_Thr_pct":str(SThr[i]),
         "Trp_pct":str(Trp[i]),"SID_Trp_pct":str(STrp[i]),
         "Val_pct":str(Val[i]),"Arg_pct":str(Arg[i]),
         "Ile_pct":str(Ile[i]),"source":S}
    nut_rows.append(r)
write_breed_data(B, "layer", "nutrient", nut_rows, replace=False)
print("Hisex Brown done")
