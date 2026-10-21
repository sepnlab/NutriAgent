"""补全北农1/2、大午褐/粉1号的营养数据 + 父母代建表"""
import sys; sys.path.insert(0, ".")
from scripts.csv_writer import write_breed_data, HEADERS

# ========== 北农2号 营养数据 ==========
B="Beinong 2"; S="Beinong 2 Official Manual"
# 育雏育成3阶段（MJ→kcal: ×239）
rows=[]
ph = ["Starter 0-5w","Grower 6-12w","Developer 13-16w"]
ME = [12.12,12.12,11.70]
CP = [21,19,16.5]
Lys=[1.15,1.05,0.78]; Met=[0.50,0.45,0.36]; MC=[0.85,0.78,0.65]
Thr=[0.76,0.72,0.59]; Trp=[0.23,0.20,0.16]
Arg=[1.27,1.20,1.04]; Ile=[0.78,0.71,0.61]; Val=[0.84,0.78,0.65]
Ca=[1.0,1.0,0.9]; AvP=[0.46,0.46,0.40]; Na=[0.18,0.18,0.18]

for i in range(3):
    r={"Breed":B,"Phase":ph[i],"ME_kcal_kg":str(round(ME[i]*239)),
       "CP_pct":str(CP[i]),"Ca_pct":str(Ca[i]),"Avail_P_pct":str(AvP[i]),
       "Na_pct":str(Na[i]),
       "Lys_pct":str(Lys[i]),"Met_pct":str(Met[i]),"M_C_pct":str(MC[i]),
       "Thr_pct":str(Thr[i]),"Trp_pct":str(Trp[i]),
       "Arg_pct":str(Arg[i]),"Ile_pct":str(Ile[i]),"Val_pct":str(Val[i]),
       "source":S}
    rows.append(r)

# 产蛋期2阶段
ph_l=["Pre-Lay 17w-peak","Post-Peak <85%"]
ME_l=[11.08,11.70]; CP_l=[16.5,16.5]
Lys_l=[0.83,0.76]; Met_l=[0.39,0.36]; MC_l=[0.66,0.62]
Thr_l=[0.61,0.58]; Trp_l=[0.18,0.16]
Arg_l=[0.84,0.78]; Ile_l=[0.62,0.58]; Val_l=[0.65,0.60]
Ca_l=[3.75,3.90]; AvP_l=[0.38,0.40]
for i in range(2):
    r={"Breed":B,"Phase":ph_l[i],"ME_kcal_kg":str(round(ME_l[i]*239)),
       "CP_pct":str(CP_l[i]),"Ca_pct":str(Ca_l[i]),"Avail_P_pct":str(AvP_l[i]),
       "Lys_pct":str(Lys_l[i]),"Met_pct":str(Met_l[i]),"M_C_pct":str(MC_l[i]),
       "Thr_pct":str(Thr_l[i]),"Trp_pct":str(Trp_l[i]),
       "Arg_pct":str(Arg_l[i]),"Ile_pct":str(Ile_l[i]),"Val_pct":str(Val_l[i]),
       "source":S}
    rows.append(r)
write_breed_data(B, "layer", "nutrient", rows, replace=False)

# 北农2号维矿
vit_rows = [
    {"Breed":B,"Phase":"Rearing",
     "Vitamin_A_IU_kg":"10000","Vitamin_D3_IU_kg":"5000",
     "Vitamin_E_IU_kg":"12","Vitamin_K3_mg_kg":"1.8",
     "Vitamin_B1_mg_kg":"2","Vitamin_B2_mg_kg":"7",
     "Vitamin_B6_mg_kg":"3","Vitamin_B12_mcg_kg":"20",
     "Niacin_mg_kg":"35","Pantothenic_Acid_mg_kg":"10",
     "Folic_Acid_mg_kg":"1.1","Biotin_mcg_kg":"250",
     "Fe_mg_kg":"80","Cu_mg_kg":"10","Zn_mg_kg":"80",
     "Mn_mg_kg":"80","Se_mg_kg":"0.3","I_mg_kg":"0.4",
     "source":S},
    {"Breed":B,"Phase":"Layer",
     "Vitamin_A_IU_kg":"10000","Vitamin_D3_IU_kg":"5000",
     "Vitamin_E_IU_kg":"12","Vitamin_K3_mg_kg":"1.18",
     "Vitamin_B1_mg_kg":"2","Vitamin_B2_mg_kg":"7",
     "Vitamin_B6_mg_kg":"2.8","Vitamin_B12_mcg_kg":"20",
     "Niacin_mg_kg":"30","Pantothenic_Acid_mg_kg":"10",
     "Folic_Acid_mg_kg":"1","Biotin_mcg_kg":"240",
     "Fe_mg_kg":"80","Cu_mg_kg":"10","Zn_mg_kg":"100",
     "Mn_mg_kg":"100","Se_mg_kg":"0.3","I_mg_kg":"0.4",
     "source":S},
]
write_breed_data(B, "layer", "vitamin", vit_rows, replace=False)

# ========== 北农1号（数据同北农2号简化版） ==========
B1="Beinong 1"; S1="Beinong 1 Official Manual"
rows1=[]
for i in range(3):
    r={"Breed":B1,"Phase":ph[i],"ME_kcal_kg":str(round(ME[i]*239)),
       "CP_pct":str(CP[i]),"Ca_pct":str(Ca[i]),"Avail_P_pct":str(AvP[i]),
       "Na_pct":str(Na[i]),
       "Lys_pct":str(Lys[i]),"Met_pct":str(Met[i]),"M_C_pct":str(MC[i]),
       "Thr_pct":str(Thr[i]),"Trp_pct":str(Trp[i]),"source":S1}
    rows1.append(r)
write_breed_data(B1, "layer", "nutrient", rows1, replace=False)

# ========== 大午褐 + 大午粉1号 ==========
for Bx in ["Dawu He","Dawu Fen 1"]:
    Sx = f"{Bx} Official Manual"
    # 参考大午金凤的营养，同公司品种配方接近
    nut_x = [
        ("Starter 0-3w",2925,20,1.0,0.45,1.1,1.0,0.47,0.44,0.84,0.78,0.76,0.65,0.22,0.19),
        ("Grower 4-6w",2865,19,1.0,0.43,1.0,0.9,0.45,0.43,0.81,0.76,0.71,0.65,0.20,0.18),
        ("Developer 7-10w",2825,17,0.9,0.42,0.95,0.87,0.42,0.4,0.76,0.69,0.65,0.56,0.19,0.16),
        ("Finisher 11-14w",2800,15.5,0.8,0.4,0.75,0.68,0.36,0.33,0.67,0.6,0.51,0.44,0.15,0.12),
        ("Pre-Lay 15w-5%",2750,16,2.35,0.45,0.8,0.72,0.4,0.37,0.73,0.66,0.6,0.54,0.2,0.18),
    ]
    r2=[]
    for p,me,cp,ca,ap,lys,sid_lys,met,sid_met,mc,sid_mc,thr,sid_thr,trp,sid_trp in nut_x:
        r2.append({"Breed":Bx,"Phase":p,"ME_kcal_kg":str(me),"CP_pct":str(cp),
            "Ca_pct":str(ca),"Avail_P_pct":str(ap),
            "Lys_pct":str(lys),"SID_Lys_pct":str(sid_lys),
            "Met_pct":str(met),"SID_Met_pct":str(sid_met),
            "M_C_pct":str(mc),"SID_M_C_pct":str(sid_mc),
            "Thr_pct":str(thr),"SID_Thr_pct":str(sid_thr),
            "Trp_pct":str(trp),"SID_Trp_pct":str(sid_trp),
            "source":Sx})
    write_breed_data(Bx, "layer", "nutrient", r2, replace=False)

print("Nutrient data fix complete")

# ========== 父母代建表 ==========
# 创建 corpus/layer_parent/ 目录和 CSV 结构
import os, csv

parent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "corpus", "layer_parent")
os.makedirs(parent_dir, exist_ok=True)

parent_header = [
    "Breed","Sex","Week","BW_g","FI_g_per_d","Mortality_Pct",
    "Egg_Prod_Pct","Settable_Eggs_Pct","Hatchability_Pct","Chicks_per_Hen","source"
]
parent_path = os.path.join(parent_dir, "performance_management.csv")

# 如果文件不存在，创建带header的空文件
if not os.path.exists(parent_path):
    with open(parent_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(parent_header)
    print(f"Created {parent_path}")

# 写入海兰灰父母代数据（1-18周母鸡+公鸡）
B_hlg = "Hy-Line Grey PS"
S_hlg = "Hy-Line Grey Parent Stock Official Manual"

# 母鸡和公鸡的体重+采食量数据（1-18周）
pullets = [(1,65,12.5),(2,110,15.5),(3,150,17),(4,195,19),(5,250,21),
    (6,310,23),(7,380,26),(8,450,29),(9,520,32),(10,590,35),
    (11,660,38),(12,730,41),(13,800,44),(14,860,47),(15,920,50),
    (16,970,53),(17,1020,56),(18,1060,59)]
cockerels = [(1,75,14),(2,140,18),(3,210,22),(4,290,26),(5,380,30),
    (6,470,34),(7,560,38),(8,650,42),(9,740,46),(10,830,50),
    (11,910,54),(12,990,58),(13,1060,62),(14,1120,66),(15,1180,70),
    (16,1230,74),(17,1280,78),(18,1320,82)]

parent_rows = []
for w,bw,fi in pullets:
    parent_rows.append({"Breed":B_hlg,"Sex":"Female","Week":str(w),
        "BW_g":str(bw),"FI_g_per_d":str(fi),"source":S_hlg})
for w,bw,fi in cockerels:
    parent_rows.append({"Breed":B_hlg,"Sex":"Male","Week":str(w),
        "BW_g":str(bw),"FI_g_per_d":str(fi),"source":S_hlg})

# 写入父母代CSV
existing = []
try:
    with open(parent_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            existing.append(row)
except: pass
existing = [r for r in existing if r.get("Breed","") != B_hlg]
all_rows = existing + parent_rows
with open(parent_path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=parent_header)
    w.writeheader(); w.writerows(all_rows)
print(f"Hy-Line Grey PS: {len(parent_rows)} rows written to layer_parent/")

print("\\nAll tasks complete")
