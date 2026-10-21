"""中国品种批量导入（营养+维矿）"""
import sys; sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data

# ========== 京红1号3.0 营养+维矿 ==========
B = "Jinghong 1 v3.0"; S = "Jinghong 1 Official Manual"

nut_rows = []
phases_r = ["Starter 0-2w","Grower 3-6w","Developer 7-10w","Finisher 11-14w","Pre-Lay 15w-5%"]
ME_r  = [2910, 2900, 2838, 2812, 2800]
CP_r  = [20.0, 19.0, 17.0, 15.5, 16.5]
Ca_r  = [1.0, 1.0, 0.9, 0.8, 2.55]
AvP_r = [0.45, 0.43, 0.42, 0.40, 0.45]
Na_r  = [0.18, 0.18, 0.18, 0.18, 0.18]
LA_r  = [1.0, 1.0, 1.0, 1.0, 1.0]

Lys  = [1.10,1.00,0.95,0.72,0.85]
Met  = [0.46,0.45,0.42,0.35,0.43]
MC   = [0.84,0.81,0.76,0.65,0.77]
Thr  = [0.75,0.68,0.65,0.49,0.58]
Trp  = [0.22,0.20,0.19,0.14,0.15]
Arg  = [1.12,1.02,0.97,0.73,0.44]
Ile  = [0.75,0.68,0.65,0.49,0.28]
Val  = [0.79,0.72,0.68,0.52,0.55]
SLys = [1.00,0.90,0.88,0.65,0.75]
SMet = [0.44,0.43,0.40,0.33,0.41]
SMC  = [0.78,0.76,0.69,0.58,0.70]
SThr = [0.64,0.59,0.56,0.42,0.50]
STrp = [0.18,0.16,0.15,0.12,0.12]

for i in range(5):
    r = {"Breed":B,"Phase":phases_r[i],"ME_kcal_kg":str(ME_r[i]),
         "CP_pct":str(CP_r[i]),"Ca_pct":str(Ca_r[i]),
         "Avail_P_pct":str(AvP_r[i]),"Na_pct":str(Na_r[i]),
         "Linoleic_Acid_pct":str(LA_r[i]),
         "Lys_pct":str(Lys[i]),"SID_Lys_pct":str(SLys[i]),
         "Met_pct":str(Met[i]),"SID_Met_pct":str(SMet[i]),
         "M_C_pct":str(MC[i]),"SID_M_C_pct":str(SMC[i]),
         "Thr_pct":str(Thr[i]),"SID_Thr_pct":str(SThr[i]),
         "Trp_pct":str(Trp[i]),"SID_Trp_pct":str(STrp[i]),
         "Val_pct":str(Val[i]),"Arg_pct":str(Arg[i]),
         "Ile_pct":str(Ile[i]),"source":S}
    nut_rows.append(r)

# 产蛋4阶段
phases_l = ["Layer I (5%-peak+4w)","Layer II (peak+4w-90%)",
            "Layer III (90%-85%)","Layer IV (85%-cull)"]
ME_l  = [2700, 2680, 2660, 2640]
CP_l  = [17.2, 15.8, 15.2, 14.9]
Ca_l  = [3.91, 3.74, 3.96, 4.22]
AvP_l = [0.41, 0.38, 0.32, 0.29]
Na_l  = [0.17, 0.16, 0.16, 0.16]

for i in range(4):
    r = {"Breed":B,"Phase":phases_l[i],"ME_kcal_kg":str(ME_l[i]),
         "CP_pct":str(CP_l[i]),"Ca_pct":str(Ca_l[i]),
         "Avail_P_pct":str(AvP_l[i]),"Na_pct":str(Na_l[i]),
         "source":S}
    nut_rows.append(r)

write_breed_data(B, "layer", "nutrient", nut_rows, replace=False)

# 维矿
vit_rows = [
    {"Breed":B,"Phase":"Rearing 0-18w",
     "Vitamin_A_IU_kg":"9900","Vitamin_D3_IU_kg":"3500",
     "Vitamin_E_IU_kg":"25","Vitamin_K3_mg_kg":"3",
     "Vitamin_B1_mg_kg":"2.2","Vitamin_B2_mg_kg":"5.5",
     "Vitamin_B6_mg_kg":"3.5","Vitamin_B12_mcg_kg":"27",
     "Niacin_mg_kg":"50","Pantothenic_Acid_mg_kg":"15",
     "Folic_Acid_mg_kg":"1.5","Biotin_mcg_kg":"175",
     "Fe_mg_kg":"60","Cu_mg_kg":"10","Zn_mg_kg":"80",
     "Mn_mg_kg":"90","Se_mg_kg":"0.3","I_mg_kg":"0.6",
     "source":S},
    {"Breed":B,"Phase":"Layer",
     "Vitamin_A_IU_kg":"8000","Vitamin_D3_IU_kg":"3500",
     "Vitamin_E_IU_kg":"24","Vitamin_K3_mg_kg":"2.5",
     "Vitamin_B1_mg_kg":"4","Vitamin_B2_mg_kg":"5.5",
     "Vitamin_B6_mg_kg":"4","Vitamin_B12_mcg_kg":"20",
     "Niacin_mg_kg":"40","Pantothenic_Acid_mg_kg":"9",
     "Folic_Acid_mg_kg":"1","Biotin_mcg_kg":"125",
     "Fe_mg_kg":"55","Cu_mg_kg":"9","Zn_mg_kg":"60",
     "Mn_mg_kg":"80","Se_mg_kg":"0.3","I_mg_kg":"0.6",
     "source":S},
]
write_breed_data(B, "layer", "vitamin", vit_rows, replace=False)
print("Jinghong 1 nutr+vit done")

# ========== 京白939 营养+维矿 ==========
B2 = "Jingbai 939"; S2 = "Jingbai 939 Official Manual"

# 数据来自四、日粮营养需求标准（5阶段育雏+3阶段产蛋）+五、维矿
nut2 = []
p2r = ["Starter 0-3w","Grower 4-6w","Developer 7-10w","Finisher 11-14w","Pre-Lay 15w-5%"]
ME2r  = [2925, 2875, 2825, 2775, 2725]
CP2r  = [20.0, 19.0, 17.0, 15.5, 16.0]
Ca2r  = [1.0, 1.0, 0.9, 0.8, 2.25]
AvP2r = [0.45, 0.43, 0.42, 0.40, 0.45]
Na2r  = [0.18, 0.18, 0.18, 0.18, 0.18]
L2  = [1.10,1.00,0.96,0.75,0.80]; M2 = [0.47,0.45,0.42,0.36,0.37]
MC2 = [0.84,0.81,0.76,0.67,0.68]; T2 = [0.76,0.68,0.66,0.51,0.60]
Tr2 = [0.22,0.20,0.19,0.15,0.18]
SL2 = [1.00,0.90,0.89,0.68,0.71]; SM2 = [0.44,0.43,0.40,0.33,0.35]
SMC2= [0.78,0.76,0.69,0.60,0.62]; ST2 = [0.65,0.59,0.56,0.44,0.51]
STr2= [0.19,0.16,0.16,0.12,0.14]

for i in range(5):
    r = {"Breed":B2,"Phase":p2r[i],"ME_kcal_kg":str(ME2r[i]),
         "CP_pct":str(CP2r[i]),"Ca_pct":str(Ca2r[i]),
         "Avail_P_pct":str(AvP2r[i]),"Na_pct":str(Na2r[i]),
         "Lys_pct":str(L2[i]),"SID_Lys_pct":str(SL2[i]),
         "Met_pct":str(M2[i]),"SID_Met_pct":str(SM2[i]),
         "M_C_pct":str(MC2[i]),"SID_M_C_pct":str(SMC2[i]),
         "Thr_pct":str(T2[i]),"SID_Thr_pct":str(ST2[i]),
         "Trp_pct":str(Tr2[i]),"SID_Trp_pct":str(STr2[i]),
         "source":S2}
    nut2.append(r)

p2l = ["Layer I (5%-90%)","Layer II (90%-80%)","Layer III (80%-cull)"]
ME2l  = [2685, 2662, 2635]
CP2l  = [16.0, 15.5, 15.0]
Ca2l  = [3.80, 4.00, 4.20]
AvP2l = [0.42, 0.40, 0.34]
for i in range(3):
    r = {"Breed":B2,"Phase":p2l[i],"ME_kcal_kg":str(ME2l[i]),
         "CP_pct":str(CP2l[i]),"Ca_pct":str(Ca2l[i]),
         "Avail_P_pct":str(AvP2l[i]),"source":S2}
    nut2.append(r)
write_breed_data(B2, "layer", "nutrient", nut2, replace=False)

# 京白939维矿
vit2 = [
    {"Breed":B2,"Phase":"Rearing",
     "Vitamin_A_IU_kg":"10000","Vitamin_D3_IU_kg":"3300",
     "Vitamin_E_IU_kg":"35","Vitamin_K3_mg_kg":"3",
     "Vitamin_B1_mg_kg":"2.2","Vitamin_B2_mg_kg":"6.5",
     "Vitamin_B6_mg_kg":"4.5","Vitamin_B12_mcg_kg":"23",
     "Niacin_mg_kg":"40","Pantothenic_Acid_mg_kg":"12",
     "Folic_Acid_mg_kg":"1.2","Biotin_mcg_kg":"150",
     "Fe_mg_kg":"30","Cu_mg_kg":"15","Zn_mg_kg":"85",
     "Mn_mg_kg":"90","Se_mg_kg":"0.3","I_mg_kg":"1.5",
     "source":S2},
    {"Breed":B2,"Phase":"Layer",
     "Vitamin_A_IU_kg":"8000","Vitamin_D3_IU_kg":"3300",
     "Vitamin_E_IU_kg":"25","Vitamin_K3_mg_kg":"2.5",
     "Vitamin_B1_mg_kg":"2.5","Vitamin_B2_mg_kg":"6.0",
     "Vitamin_B6_mg_kg":"4","Vitamin_B12_mcg_kg":"23",
     "Niacin_mg_kg":"35","Pantothenic_Acid_mg_kg":"10",
     "Folic_Acid_mg_kg":"1.6","Biotin_mcg_kg":"150",
     "Fe_mg_kg":"40","Cu_mg_kg":"8","Zn_mg_kg":"80",
     "Mn_mg_kg":"90","Se_mg_kg":"0.3","I_mg_kg":"1.2",
     "source":S2},
]
write_breed_data(B2, "layer", "vitamin", vit2, replace=False)
print("Jingbai 939 nutr+vit done")

# ========== 京粉6号 营养+维矿 ==========
B3 = "Jingfen 6"; S3 = "Jingfen 6 Official Manual"

nut3 = []
p3r = ["Starter 0-2w","Grower 3-6w","Developer 7-10w","Finisher 11-14w","Pre-Lay 15w-5%"]
ME3r  = [2910, 2900, 2828, 2805, 2780]
CP3r  = [20.0, 19.0, 17.0, 15.5, 16.2]
Ca3r  = [1.05, 1.05, 0.9, 0.8, 2.55]
AvP3r = [0.46, 0.45, 0.43, 0.42, 0.50]
L3  = [1.10,1.00,0.96,0.75,0.84]; M3 = [0.46,0.45,0.42,0.36,0.44]
MC3 = [0.84,0.81,0.76,0.67,0.76]; T3 = [0.75,0.73,0.68,0.55,0.62]
SL3 = [1.00,0.90,0.89,0.68,0.74]; SM3 = [0.44,0.43,0.40,0.33,0.42]
SMC3= [0.78,0.76,0.69,0.60,0.69]; ST3 = [0.64,0.62,0.57,0.47,0.54]

for i in range(5):
    r = {"Breed":B3,"Phase":p3r[i],"ME_kcal_kg":str(ME3r[i]),
         "CP_pct":str(CP3r[i]),"Ca_pct":str(Ca3r[i]),
         "Avail_P_pct":str(AvP3r[i]),
         "Lys_pct":str(L3[i]),"SID_Lys_pct":str(SL3[i]),
         "Met_pct":str(M3[i]),"SID_Met_pct":str(SM3[i]),
         "M_C_pct":str(MC3[i]),"SID_M_C_pct":str(SMC3[i]),
         "Thr_pct":str(T3[i]),"SID_Thr_pct":str(ST3[i]),
         "source":S3}
    nut3.append(r)

p3l = ["Layer I (5%-peak+4w)","Layer II (peak-90%)",
       "Layer III (90%-85%)","Layer IV (85%-cull)"]
ME3l  = [2725, 2710, 2695, 2680]
CP3l  = [17.2, 16.2, 15.6, 15.0]
Ca3l  = [3.92, 3.76, 3.92, 3.95]
AvP3l = [0.45, 0.37, 0.33, 0.31]
for i in range(4):
    r = {"Breed":B3,"Phase":p3l[i],"ME_kcal_kg":str(ME3l[i]),
         "CP_pct":str(CP3l[i]),"Ca_pct":str(Ca3l[i]),
         "Avail_P_pct":str(AvP3l[i]),"source":S3}
    nut3.append(r)
write_breed_data(B3, "layer", "nutrient", nut3, replace=False)

# 京粉6号维矿（附件7）
vit3 = [
    {"Breed":B3,"Phase":"Rearing 0-18w",
     "Vitamin_A_IU_kg":"9900","Vitamin_D3_IU_kg":"3500",
     "Vitamin_E_IU_kg":"25","Vitamin_K3_mg_kg":"3",
     "Vitamin_B1_mg_kg":"2.2","Vitamin_B2_mg_kg":"5.5",
     "Vitamin_B6_mg_kg":"3.5","Vitamin_B12_mcg_kg":"27",
     "Niacin_mg_kg":"50","Pantothenic_Acid_mg_kg":"15",
     "Folic_Acid_mg_kg":"1.5","Biotin_mcg_kg":"175",
     "Fe_mg_kg":"60","Cu_mg_kg":"10","Zn_mg_kg":"80",
     "Mn_mg_kg":"90","Se_mg_kg":"0.3","I_mg_kg":"0.6",
     "source":S3},
    {"Breed":B3,"Phase":"Layer",
     "Vitamin_A_IU_kg":"8000","Vitamin_D3_IU_kg":"3500",
     "Vitamin_E_IU_kg":"24","Vitamin_K3_mg_kg":"2.5",
     "Vitamin_B1_mg_kg":"4","Vitamin_B2_mg_kg":"5.5",
     "Vitamin_B6_mg_kg":"4","Vitamin_B12_mcg_kg":"20",
     "Niacin_mg_kg":"40","Pantothenic_Acid_mg_kg":"9",
     "Folic_Acid_mg_kg":"1.25","Biotin_mcg_kg":"150",
     "Fe_mg_kg":"60","Cu_mg_kg":"9","Zn_mg_kg":"70",
     "Mn_mg_kg":"85","Se_mg_kg":"0.3","I_mg_kg":"0.6",
     "source":S3},
]
write_breed_data(B3, "layer", "vitamin", vit3, replace=False)
print("Jingfen 6 nutr+vit done")

print("\nAll Chinese breed nutrient/vitamin imports done")
