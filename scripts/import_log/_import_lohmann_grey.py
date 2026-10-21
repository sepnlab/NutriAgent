"""罗曼灰 → Lohmann Grey"""
import sys; sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

B = "Lohmann Grey"
S = "Lohmann Grey Official Manual"

# 1-19周体重 + 耗料（来自表5块）
bw_data = [75,127,190,271,355,452,558,658,758,853,935,1009,1072,1130,1183,
           1230,1280,1333,1394]
fi_data = [10,17,23,29,35,39,43,47,51,55,59,62,65,68,71,74,77,80,84]

rows = []
for w in range(1, 20):
    rows.append({"Breed":B,"Week":str(w),"HenDay_Prod_Pct":"0",
        "FI_g_per_d":str(fi_data[w-1]),
        "BW_g":str(bw_data[w-1]),"source":S})
write_breed_data(B, "layer", "performance", rows, replace=False)

# 育雏营养4阶段
nut_rows = []
phases_r = ["Starter 1-3w","Grower 4-8w","Developer 9-16w","Pre-Lay 18w-5%"]
ME_r  = [2900, 2775, 2775, 2775]
CP_r  = [20.0, 18.5, 14.5, 17.5]
Ca_r  = [1.05, 1.00, 0.90, 2.00]
AvP_r = [0.48, 0.45, 0.37, 0.45]
Na_r  = [0.18, 0.17, 0.16, 0.16]
LA_r  = [2.0, 1.4, 1.0, 1.0]
Lys_r = [(0.98,1.20),(0.82,1.00),(0.53,0.65),(0.70,0.85)]
Met_r = [(0.39,0.48),(0.33,0.40),(0.28,0.34),(0.29,0.36)]
MC_r  = [(0.68,0.83),(0.57,0.70),(0.50,0.60),(0.56,0.68)]
Thr_r = [(0.65,0.80),(0.57,0.70),(0.40,0.50),(0.49,0.60)]
Trp_r = [(0.19,0.23),(0.17,0.21),(0.13,0.16),(0.16,0.20)]
Ile_r = [(0.68,0.83),(0.62,0.75),(0.50,0.60),(0.61,0.74)]
Val_r = [(0.76,0.89),(0.64,0.75),(0.46,0.53),(0.55,0.64)]

for i in range(4):
    r = {"Breed":B,"Phase":phases_r[i],"ME_kcal_kg":str(ME_r[i]),
         "CP_pct":str(CP_r[i]),"Ca_pct":str(Ca_r[i]),
         "Avail_P_pct":str(AvP_r[i]),"Na_pct":str(Na_r[i]),
         "Linoleic_Acid_pct":str(LA_r[i]),"source":S}
    for aa, data in [("Lys",Lys_r),("Met",Met_r),("MC",MC_r),
                     ("Thr",Thr_r),("Trp",Trp_r)]:
        sid, total = data[i]; cn = "M_C" if aa=="MC" else aa
        r[f"{cn}_pct"]=str(total); r[f"SID_{cn}_pct"]=str(sid)
    for aa, data in [("Ile",Ile_r),("Val",Val_r)]:
        sid,total = data[i]; r[f"{aa}_pct"]=str(total)
    nut_rows.append(r)
write_breed_data(B, "layer", "nutrient", nut_rows, replace=False)

# 维矿（罗曼灰标准）
vit_rows = [
    {"Breed":B,"Phase":"Starter-Grower",
     "Vitamin_A_IU_kg":"12000","Vitamin_D3_IU_kg":"2000",
     "Vitamin_E_IU_kg":"25","Vitamin_K3_mg_kg":"3",
     "Vitamin_B1_mg_kg":"1","Vitamin_B2_mg_kg":"6",
     "Vitamin_B6_mg_kg":"3","Vitamin_B12_mcg_kg":"20",
     "Niacin_mg_kg":"30","Pantothenic_Acid_mg_kg":"8",
     "Folic_Acid_mg_kg":"1","Biotin_mcg_kg":"50",
     "Fe_mg_kg":"25","Cu_mg_kg":"5","Zn_mg_kg":"60",
     "Mn_mg_kg":"100","Se_mg_kg":"0.2","I_mg_kg":"0.5",
     "source":S},
    {"Breed":B,"Phase":"Layer",
     "Vitamin_A_IU_kg":"10000","Vitamin_D3_IU_kg":"2500",
     "Vitamin_E_IU_kg":"22","Vitamin_K3_mg_kg":"3",
     "Vitamin_B1_mg_kg":"1","Vitamin_B2_mg_kg":"4",
     "Vitamin_B6_mg_kg":"3","Vitamin_B12_mcg_kg":"25",
     "Niacin_mg_kg":"30","Pantothenic_Acid_mg_kg":"10",
     "Folic_Acid_mg_kg":"0.5","Biotin_mcg_kg":"50",
     "Fe_mg_kg":"25","Cu_mg_kg":"5","Zn_mg_kg":"60",
     "Mn_mg_kg":"100","Se_mg_kg":"0.2","I_mg_kg":"0.5",
     "source":S},
]
write_breed_data(B, "layer", "vitamin", vit_rows, replace=False)
print("Lohmann Grey done")
