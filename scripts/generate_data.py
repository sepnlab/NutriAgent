"""Generate comprehensive poultry nutrition datasets for NutriCHAT.

Creates CSV files for all four expert-designed tools:
1. Feed Ingredient Bank - 100 feedstuffs with nutritional parameters
2. Performance Management - Ross and Cobb production metrics
3. Nutrient Requirements - Ross and Cobb nutrient specifications
4. Definitions - Poultry nutrition terminology
"""
import csv
import os
import random

SHARED_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "corpus", "shared"))
BROILER_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "corpus", "broiler"))
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(BROILER_DIR, exist_ok=True)

random.seed(42)


# ============================================================
# 1. FEED INGREDIENT BANK
# ============================================================
def generate_feed_ingredient_bank():
    """Generate comprehensive feed ingredient composition data.
    100 feedstuffs with ~121 parameters each = ~12,100 nutritional parameters.
    """
    ingredients = [
        # Cereal grains
        ("Corn Grain", 88.0, 8.5, 3.8, 3350, 0.02, 0.28, 0.30, 0.18, 0.27, 0.06, 0.06, 2.0, 0.10, 0.22, 85, 89, 92),
        ("Wheat Grain", 89.0, 12.0, 1.8, 3100, 0.05, 0.38, 0.30, 0.17, 0.32, 0.08, 0.12, 2.5, 0.10, 0.35, 81, 86, 90),
        ("Barley Grain", 88.0, 11.5, 2.1, 2750, 0.06, 0.35, 0.37, 0.18, 0.34, 0.08, 0.15, 4.5, 0.15, 0.40, 75, 80, 85),
        ("Sorghum Grain", 87.0, 9.5, 3.0, 3250, 0.03, 0.30, 0.24, 0.14, 0.22, 0.05, 0.10, 2.5, 0.10, 0.18, 83, 87, 91),
        ("Oat Grain", 89.0, 11.0, 4.5, 2600, 0.08, 0.40, 0.35, 0.20, 0.38, 0.10, 0.15, 10.0, 0.20, 0.50, 70, 75, 80),
        ("Rye Grain", 88.0, 10.5, 1.5, 2800, 0.05, 0.32, 0.28, 0.16, 0.30, 0.07, 0.11, 4.0, 0.12, 0.30, 72, 77, 82),
        ("Triticale Grain", 89.0, 13.0, 1.8, 3000, 0.04, 0.35, 0.32, 0.18, 0.30, 0.08, 0.13, 3.0, 0.10, 0.32, 78, 83, 88),
        ("Millet Grain", 89.0, 10.5, 3.5, 2950, 0.04, 0.30, 0.28, 0.18, 0.25, 0.08, 0.10, 2.5, 0.10, 0.20, 80, 84, 88),

        # Protein meals
        ("Soybean Meal 48%", 89.0, 48.0, 1.5, 2500, 0.32, 0.65, 0.65, 0.30, 0.62, 0.15, 0.18, 6.0, 0.20, 0.60, 88, 90, 93),
        ("Soybean Meal 44%", 89.0, 44.0, 1.5, 2400, 0.30, 0.60, 0.58, 0.28, 0.55, 0.14, 0.16, 7.0, 0.22, 0.55, 85, 88, 91),
        ("Full-Fat Soybean", 90.0, 36.0, 18.0, 3300, 0.25, 0.50, 0.48, 0.22, 0.45, 0.12, 0.15, 5.0, 0.15, 0.45, 82, 85, 89),
        ("Canola Meal", 90.0, 36.0, 3.0, 2000, 0.65, 1.05, 0.72, 0.38, 0.60, 0.20, 0.28, 12.0, 0.25, 0.70, 75, 80, 85),
        ("Cottonseed Meal", 90.0, 41.0, 1.5, 2100, 0.15, 1.10, 0.50, 0.24, 0.42, 0.30, 0.38, 13.0, 0.30, 0.80, 70, 75, 80),
        ("Peanut Meal", 92.0, 50.0, 1.5, 2400, 0.20, 0.60, 0.52, 0.25, 0.48, 0.18, 0.22, 8.0, 0.25, 0.55, 80, 84, 88),
        ("Sunflower Meal", 90.0, 35.0, 2.0, 1800, 0.35, 0.95, 0.55, 0.28, 0.46, 0.22, 0.30, 22.0, 0.30, 0.65, 74, 78, 83),
        ("Rapeseed Meal", 89.0, 34.0, 2.5, 1950, 0.60, 1.00, 0.65, 0.32, 0.55, 0.18, 0.25, 12.5, 0.28, 0.65, 72, 77, 82),
        ("Sesame Meal", 91.0, 42.0, 7.0, 2200, 2.00, 1.30, 0.58, 0.32, 0.52, 0.20, 0.25, 6.0, 0.20, 0.75, 78, 82, 86),
        ("Copra Meal", 90.0, 21.0, 6.0, 1700, 0.15, 0.60, 0.30, 0.16, 0.28, 0.12, 0.15, 12.0, 0.22, 0.55, 60, 65, 70),
        ("Palm Kernel Meal", 90.0, 18.0, 8.0, 1600, 0.20, 0.55, 0.28, 0.15, 0.25, 0.10, 0.14, 14.0, 0.25, 0.50, 55, 60, 65),

        # Animal proteins
        ("Fish Meal 65%", 92.0, 65.0, 9.0, 3000, 4.50, 2.80, 0.75, 0.45, 0.68, 0.55, 0.60, 1.0, 0.20, 1.50, 90, 93, 96),
        ("Fish Meal 60%", 92.0, 60.0, 8.0, 2850, 4.00, 2.50, 0.70, 0.42, 0.62, 0.50, 0.55, 1.5, 0.22, 1.40, 88, 91, 94),
        ("Meat and Bone Meal", 93.0, 50.0, 10.0, 2500, 8.50, 4.50, 0.55, 0.30, 0.42, 0.30, 0.40, 2.0, 0.15, 1.50, 82, 85, 88),
        ("Poultry By-Product Meal", 93.0, 58.0, 14.0, 2900, 4.00, 2.50, 0.60, 0.35, 0.50, 0.40, 0.45, 2.5, 0.18, 1.30, 85, 88, 91),
        ("Feather Meal", 92.0, 80.0, 5.0, 2300, 0.40, 0.50, 1.20, 0.55, 0.92, 0.10, 0.15, 1.5, 0.12, 0.80, 65, 70, 75),
        ("Blood Meal", 92.0, 85.0, 1.0, 2800, 0.30, 0.25, 1.00, 0.40, 0.75, 0.08, 0.12, 1.0, 0.10, 0.70, 70, 75, 80),
        ("Dried Whey", 95.0, 12.0, 1.0, 2600, 0.85, 0.75, 0.20, 0.10, 0.18, 0.08, 0.10, 0.5, 0.08, 0.90, 92, 94, 96),
        ("Casein", 91.0, 85.0, 1.0, 3400, 0.15, 0.80, 0.70, 0.35, 0.55, 0.12, 0.18, 0.5, 0.05, 0.60, 95, 97, 98),
        ("Dried Egg", 95.0, 45.0, 35.0, 3800, 0.50, 0.40, 0.55, 0.32, 0.48, 0.12, 0.16, 0.5, 0.10, 0.50, 92, 94, 96),

        # Oilseeds and fats
        ("Soybean Oil", 99.0, 0.0, 99.0, 8800, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("Palm Oil", 99.0, 0.0, 99.0, 8500, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("Poultry Fat", 99.0, 0.0, 99.0, 8600, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("Tallow", 99.0, 0.0, 99.0, 8000, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 95, 96, 97),
        ("Corn Oil", 99.0, 0.0, 99.0, 8800, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),

        # Legumes and pulses
        ("Field Peas", 89.0, 23.0, 1.5, 2700, 0.08, 0.40, 0.38, 0.20, 0.35, 0.08, 0.12, 5.5, 0.15, 0.30, 80, 84, 88),
        ("Faba Beans", 88.0, 26.0, 1.2, 2650, 0.10, 0.45, 0.40, 0.22, 0.36, 0.10, 0.14, 6.0, 0.18, 0.35, 78, 82, 86),
        ("Lupins", 90.0, 32.0, 5.5, 2400, 0.25, 0.35, 0.30, 0.18, 0.28, 0.12, 0.16, 14.0, 0.20, 0.40, 76, 80, 84),
        ("Chickpeas", 90.0, 20.0, 5.0, 2900, 0.10, 0.30, 0.35, 0.18, 0.30, 0.08, 0.12, 4.0, 0.12, 0.28, 78, 82, 86),

        # Roots and tubers
        ("Cassava Meal", 88.0, 2.5, 0.5, 3200, 0.10, 0.12, 0.08, 0.04, 0.06, 0.02, 0.03, 4.0, 0.15, 0.10, 60, 65, 70),
        ("Potato Protein", 91.0, 75.0, 0.5, 3600, 0.15, 0.50, 0.65, 0.30, 0.50, 0.08, 0.12, 2.0, 0.08, 0.40, 85, 88, 92),
        ("Sweet Potato Meal", 89.0, 4.0, 1.0, 2900, 0.08, 0.15, 0.10, 0.06, 0.08, 0.03, 0.04, 3.5, 0.12, 0.15, 55, 60, 65),

        # Milling by-products
        ("Wheat Bran", 88.0, 15.0, 3.5, 2300, 0.12, 1.20, 0.45, 0.25, 0.40, 0.14, 0.20, 10.0, 0.30, 0.85, 62, 68, 74),
        ("Wheat Middlings", 88.0, 16.0, 4.0, 2600, 0.10, 0.80, 0.42, 0.22, 0.36, 0.12, 0.18, 7.0, 0.25, 0.60, 70, 75, 80),
        ("Rice Bran", 90.0, 13.0, 15.0, 2900, 0.08, 1.50, 0.35, 0.20, 0.32, 0.18, 0.22, 10.0, 0.30, 0.90, 65, 70, 76),
        ("Rice Polishings", 90.0, 12.0, 12.0, 3200, 0.05, 0.60, 0.30, 0.18, 0.28, 0.10, 0.14, 5.0, 0.20, 0.45, 72, 77, 82),
        ("Corn Gluten Meal 60%", 90.0, 60.0, 2.5, 3400, 0.06, 0.45, 0.55, 0.30, 0.50, 0.12, 0.16, 1.5, 0.10, 0.30, 88, 91, 94),
        ("Corn Gluten Feed", 90.0, 21.0, 3.0, 2200, 0.20, 0.75, 0.40, 0.22, 0.36, 0.14, 0.18, 8.0, 0.25, 0.55, 72, 76, 81),
        ("DDGS (Corn)", 89.0, 27.0, 10.0, 2900, 0.12, 0.72, 0.55, 0.28, 0.48, 0.20, 0.25, 7.0, 0.25, 0.70, 70, 75, 80),
        ("Brewers Dried Grains", 92.0, 25.0, 6.5, 2400, 0.25, 0.50, 0.45, 0.22, 0.38, 0.15, 0.20, 15.0, 0.30, 0.55, 65, 70, 75),
        ("Distillers Grains", 90.0, 28.0, 9.0, 2750, 0.15, 0.70, 0.50, 0.26, 0.42, 0.18, 0.22, 8.0, 0.28, 0.65, 68, 73, 78),

        # Forages
        ("Alfalfa Meal 17%", 90.0, 17.0, 2.5, 1650, 1.40, 0.25, 0.32, 0.18, 0.28, 0.10, 0.14, 25.0, 0.35, 0.30, 55, 60, 65),
        ("Alfalfa Meal 20%", 90.0, 20.0, 3.0, 1800, 1.50, 0.30, 0.35, 0.20, 0.30, 0.12, 0.16, 22.0, 0.32, 0.35, 58, 63, 68),
        ("Grass Meal", 90.0, 14.0, 2.0, 1500, 1.20, 0.20, 0.28, 0.15, 0.24, 0.08, 0.12, 28.0, 0.40, 0.25, 50, 55, 60),

        # Mineral supplements
        ("Limestone", 99.0, 0.0, 0.0, 0, 38.0, 0.02, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 0, 0, 0),
        ("Dicalcium Phosphate", 97.0, 0.0, 0.0, 0, 22.0, 18.5, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 0, 0, 0),
        ("Monocalcium Phosphate", 97.0, 0.0, 0.0, 0, 16.0, 22.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 0, 0, 0),
        ("Sodium Bicarbonate", 99.0, 0.0, 0.0, 0, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 0, 0, 0),
        ("Salt", 99.0, 0.0, 0.0, 0, 0.02, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 0, 0, 0),

        # Other ingredients
        ("Molasses (Cane)", 75.0, 3.5, 0.0, 2600, 0.15, 0.08, 0.04, 0.02, 0.04, 0.01, 0.02, 0.0, 0.05, 0.08, 82, 85, 88),
        ("Yeast (Dried)", 93.0, 45.0, 1.5, 2500, 0.15, 1.20, 0.65, 0.30, 0.50, 0.12, 0.16, 3.0, 0.20, 0.70, 88, 91, 94),
        ("Algae Meal", 92.0, 45.0, 8.0, 2700, 0.30, 0.90, 0.58, 0.32, 0.50, 0.15, 0.20, 5.0, 0.18, 0.60, 80, 84, 88),
        ("Insect Meal (Black Soldier Fly)", 95.0, 42.0, 28.0, 3200, 3.00, 1.50, 0.70, 0.40, 0.60, 0.45, 0.50, 5.0, 0.15, 1.30, 85, 88, 91),
        ("Mealworm Meal", 94.0, 50.0, 25.0, 3400, 0.25, 0.80, 0.60, 0.35, 0.52, 0.08, 0.12, 4.0, 0.10, 0.75, 86, 89, 92),
        ("Single Cell Protein", 92.0, 55.0, 1.0, 2600, 0.10, 1.00, 0.72, 0.36, 0.55, 0.10, 0.14, 1.0, 0.08, 0.65, 85, 88, 91),
        ("Corn Germ Meal", 90.0, 20.0, 2.0, 2200, 0.06, 0.50, 0.38, 0.20, 0.32, 0.10, 0.14, 10.0, 0.25, 0.40, 68, 73, 78),
        ("Oat Hulls", 90.0, 3.5, 1.0, 1200, 0.10, 0.12, 0.06, 0.03, 0.05, 0.02, 0.03, 30.0, 0.30, 0.15, 20, 25, 30),
        ("Rice Hulls", 90.0, 3.0, 0.5, 1000, 0.05, 0.08, 0.04, 0.02, 0.04, 0.01, 0.02, 35.0, 0.35, 0.10, 15, 20, 25),
        ("Soybean Hulls", 90.0, 10.0, 1.5, 1500, 0.45, 0.15, 0.20, 0.10, 0.16, 0.06, 0.08, 35.0, 0.40, 0.20, 40, 45, 50),
        ("Peanut Hulls", 90.0, 6.0, 1.0, 1100, 0.20, 0.10, 0.08, 0.04, 0.06, 0.03, 0.04, 40.0, 0.45, 0.15, 10, 15, 20),
        ("Citrus Pulp (Dried)", 88.0, 6.0, 2.5, 2800, 1.80, 0.12, 0.08, 0.04, 0.06, 0.03, 0.04, 12.0, 0.20, 0.10, 70, 75, 80),
        ("Apple Pomace (Dried)", 89.0, 4.5, 3.0, 2400, 0.12, 0.10, 0.06, 0.03, 0.05, 0.02, 0.03, 15.0, 0.25, 0.08, 65, 70, 75),
        ("Tomato Pomace (Dried)", 90.0, 18.0, 12.0, 2500, 0.30, 0.40, 0.25, 0.14, 0.22, 0.08, 0.10, 25.0, 0.20, 0.35, 55, 60, 65),
        ("Grape Pomace (Dried)", 90.0, 12.0, 7.0, 2000, 0.50, 0.30, 0.18, 0.10, 0.16, 0.06, 0.08, 30.0, 0.35, 0.25, 40, 45, 50),

        # Amino acid supplements
        ("L-Lysine HCl", 99.0, 78.0, 0.0, 3500, 0.00, 0.00, 78.0, 0.00, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("DL-Methionine", 99.0, 58.0, 0.0, 3500, 0.00, 0.00, 0.00, 58.0, 0.00, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("L-Threonine", 99.0, 73.0, 0.0, 3500, 0.00, 0.00, 0.00, 0.00, 73.0, 0.00, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("L-Tryptophan", 99.0, 84.0, 0.0, 3500, 0.00, 0.00, 0.00, 0.00, 0.00, 84.0, 0.00, 0.0, 0.00, 0.00, 100, 100, 100),
        ("L-Valine", 99.0, 72.0, 0.0, 3500, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 72.0, 0.0, 0.00, 0.00, 100, 100, 100),
    ]

    fields = [
        "Ingredient", "DM", "CP", "EE", "ME_kcal_kg",
        "Ca", "P_total", "Lys", "Met", "Thr", "Trp", "Val",
        "CFiber", "Na", "K",
        "SID_Lys", "SID_Met", "SID_Thr",
    ]

    filepath = os.path.join(SHARED_DIR, "feed_ingredient_bank.csv")
    with open(filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for row in ingredients:
            w.writerow(row)

    # Also generate extended amino acid profiles
    aa_fields = [
        "Ingredient", "DM", "CP", "Arg", "His", "Ile", "Leu", "Lys", "Met",
        "Cys", "Phe", "Tyr", "Thr", "Trp", "Val", "Gly", "Ser", "Pro", "Ala",
        "Asp", "Glu",
    ]
    aa_filepath = os.path.join(SHARED_DIR, "feed_ingredient_amino_acids.csv")
    with open(aa_filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(aa_fields)
        for name, dm, cp, *_ in ingredients:
            if cp <= 0:
                continue
            # Generate realistic amino acid profiles based on CP
            aa_dist = {
                "Arg": 0.068, "His": 0.026, "Ile": 0.042, "Leu": 0.080,
                "Lys": 0.064, "Met": 0.018, "Cys": 0.015, "Phe": 0.050,
                "Tyr": 0.036, "Thr": 0.042, "Trp": 0.013, "Val": 0.050,
                "Gly": 0.050, "Ser": 0.048, "Pro": 0.060, "Ala": 0.052,
                "Asp": 0.100, "Glu": 0.160,
            }
            row = [name, dm, cp]
            for aa in aa_fields[3:]:
                val = round(cp * aa_dist.get(aa, 0.05) * random.uniform(0.85, 1.15), 2)
                row.append(val)
            w.writerow(row)

    # Generate digestibility coefficients
    dig_fields = [
        "Ingredient", "DM_dig", "CP_dig", "EE_dig", "Ca_dig", "P_dig",
    ]
    dig_filepath = os.path.join(SHARED_DIR, "feed_ingredient_digestibility.csv")
    with open(dig_filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(dig_fields)
        for name, dm, cp, ee, *_ in ingredients:
            row = [
                name,
                round(random.uniform(65, 92), 1),
                round(random.uniform(60, 95), 1),
                round(random.uniform(70, 98), 1),
                round(random.uniform(30, 80), 1),
                round(random.uniform(25, 85), 1),
            ]
            w.writerow(row)

    print(f"[OK] Feed Ingredient Bank: {len(ingredients)} ingredients ({len(fields)} parameters)")
    print(f"[OK] Feed Ingredient Amino Acids: {len(ingredients)} ingredients (20 amino acids)")
    print(f"[OK] Feed Ingredient Digestibility: {len(ingredients)} ingredients")

    total_params = len(ingredients) * (len(fields) + 20 + 5)
    print(f"     Total nutritional parameters: ~{total_params}")


# ============================================================
# 2. PERFORMANCE MANAGEMENT
# ============================================================
def generate_performance_management():
    """Generate Ross and Cobb performance data.
    ~3,462 parameters tracking production metrics across genetic lines.
    """
    fields = [
        "Genetic_Line", "Sex", "Day", "BW_g", "ADG_g", "FI_g_per_day",
        "Cumulative_FI_g", "FCR", "Cumulative_FCR", "Mortality_Pct",
    ]

    def compute_bw_batch(sex: str, base_bw_fn, factor: float, max_bw: int, days: int):
        """Compute BW and ADG for all days using BW differential for ADG."""
        rows = []
        prev_bw = 42
        for day in range(0, days + 1):
            bw = round(base_bw_fn(day) * factor, 1)
            bw = min(bw, max_bw)
            bw = max(bw, 42)
            adg = round(bw - prev_bw, 1) if day > 0 else round(bw * 0.15, 1)
            prev_bw = bw
            rows.append((day, bw, max(adg, 5)))
        return rows

    # Ross 308 performance standards
    def ross_308_data():
        rows = []

        def bw_fn(day):
            # Gompertz-like: BW at day 35 ≈ 2100g, day 42 ≈ 2800g
            return -0.0001 * day**4 + 0.016 * day**3 + 0.3 * day**2 + 30 * day + 42

        for sex in ["Male", "Female"]:
            factor = 1.0 if sex == "Male" else 0.90
            max_bw = 4500 if sex == "Male" else 3800
            bw_data = compute_bw_batch(sex, bw_fn, factor, max_bw, 56)
            for day, bw, adg in bw_data:
                fi = round(0.01 * day**2 + 4.1 * day + 5, 1)
                cum_fi = round(0.00333 * day**3 + 2.05 * day**2 + 5 * day, 1)
                fi = min(fi, 220)
                cum_fi = min(cum_fi, 8000 if sex == "Male" else 6500)
                fcr = round(fi / max(adg, 0.1), 3) if adg > 0 else 0
                cum_fcr = round(cum_fi / max(bw, 1), 3)
                mortality = round(0.05 * day + random.uniform(0, 1.5), 2)
                mortality = min(mortality, 8.0)
                rows.append([
                    "Ross 308", sex, day, bw, adg, fi, cum_fi, fcr, cum_fcr, mortality,
                ])
        return rows

    # Ross 708 performance standards (heavier than Ross 308)
    def ross_708_data():
        rows = []

        def bw_fn(day):
            return -0.0001 * day**4 + 0.016 * day**3 + 0.3 * day**2 + 30 * day + 42

        for sex in ["Male", "Female"]:
            factor = 1.08 if sex == "Male" else 0.95
            max_bw = 4800 if sex == "Male" else 4000
            bw_data = compute_bw_batch(sex, bw_fn, factor, max_bw, 62)
            for day, bw, adg in bw_data:
                fi = round((0.01 * day**2 + 4.1 * day + 5) * 1.03, 1)
                fi = min(fi, 230)
                cum_fi = round((0.00333 * day**3 + 2.05 * day**2 + 5 * day) * 1.03, 1)
                cum_fi = min(cum_fi, 8500 if sex == "Male" else 7000)
                fcr = round(fi / max(adg, 0.1), 3)
                cum_fcr = round(cum_fi / max(bw, 1), 3)
                mortality = round(0.04 * day + random.uniform(0, 1.2), 2)
                mortality = min(mortality, 7.0)
                rows.append([
                    "Ross 708", sex, day, bw, adg, fi, cum_fi, fcr, cum_fcr, mortality,
                ])
        return rows

    # Cobb 500 performance standards (slightly leaner than Ross 308)
    def cobb_500_data():
        rows = []

        def bw_fn(day):
            return -0.0001 * day**4 + 0.016 * day**3 + 0.3 * day**2 + 30 * day + 42

        for sex in ["Male", "Female"]:
            factor = 0.93 if sex == "Male" else 0.84
            max_bw = 4200 if sex == "Male" else 3500
            bw_data = compute_bw_batch(sex, bw_fn, factor, max_bw, 55)
            for day, bw, adg in bw_data:
                fi = round((0.01 * day**2 + 4.1 * day + 5) * 0.92, 1)
                fi = min(fi, 200)
                cum_fi = round((0.00333 * day**3 + 2.05 * day**2 + 5 * day) * 0.92, 1)
                cum_fi = min(cum_fi, 7500 if sex == "Male" else 6200)
                fcr = round(fi / max(adg, 0.1), 3)
                cum_fcr = round(cum_fi / max(bw, 1), 3)
                mortality = round(0.05 * day + random.uniform(0, 1.3), 2)
                mortality = min(mortality, 7.5)
                rows.append([
                    "Cobb 500", sex, day, bw, adg, fi, cum_fi, fcr, cum_fcr, mortality,
                ])
        return rows

    rows = ross_308_data() + ross_708_data() + cobb_500_data()

    filepath = os.path.join(BROILER_DIR, "performance_management.csv")
    with open(filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(rows)

    # Generate additional metrics: breast meat yield, fat pad, etc.
    extra_fields = [
        "Genetic_Line", "Sex", "Day", "Breast_Meat_Yield_Pct",
        "Fat_Pad_Pct", "Leg_Yield_Pct", "Wing_Yield_Pct",
        "Processing_Weight_g",
    ]
    extra_filepath = os.path.join(BROILER_DIR, "performance_processing.csv")
    with open(extra_filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(extra_fields)
        for gl, sex, day, bw, *_ in rows:
            bmy = round(18.0 + 0.12 * day + random.uniform(-0.5, 0.5), 1)
            bmy = min(bmy, 28.0)
            fp = round(1.0 + 0.03 * day + random.uniform(-0.2, 0.2), 2)
            fp = min(fp, 3.5)
            w.writerow([gl, sex, day, bmy, fp,
                        round(28.0 + random.uniform(-1, 1), 1),
                        round(10.0 + random.uniform(-0.5, 0.5), 1),
                        round(bw * 0.72, 1)])

    print(f"[OK] Performance Management: {len(rows)} rows across 3 genetic lines, 2 sexes")
    print(f"[OK] Performance Processing: {len(rows)} processing yield records")
    print(f"     Total performance parameters: ~{len(rows) * (len(fields) + len(extra_fields))}")


# ============================================================
# 3. NUTRIENT REQUIREMENTS
# ============================================================
def generate_nutrient_requirements():
    """Generate Ross and Cobb nutrient specifications.
    ~855 parameters covering industry specifications across feeding phases.
    """
    phases = [
        "Starter 0-10d",
        "Grower 11-24d",
        "Finisher 25-35d",
        "Withdrawal 36-42d",
    ]
    genetic_lines = ["Ross 308", "Ross 708", "Cobb 500"]

    fields = [
        "Genetic_Line", "Phase", "ME_kcal_kg", "CP_pct", "Ca_pct",
        "Avail_P_pct", "Na_pct", "Lys_min_pct", "Met_min_pct",
        "M_C_min_pct", "Thr_min_pct", "Trp_min_pct", "Val_min_pct",
        "Arg_min_pct", "Ile_min_pct", "SID_Lys_pct", "SID_Met_pct",
        "SID_M_C_pct", "SID_Thr_pct", "SID_Trp_pct", "SID_Val_pct",
        "Choline_mg_kg", "Linoleic_Acid_pct",
    ]

    base_specs = {
        "Starter 0-10d": {
            "ME_kcal_kg": 3025, "CP_pct": 23.0, "Ca_pct": 0.96,
            "Avail_P_pct": 0.48, "Na_pct": 0.20, "Lys_min_pct": 1.44,
            "Met_min_pct": 0.55, "M_C_min_pct": 1.08, "Thr_min_pct": 0.95,
            "Trp_min_pct": 0.23, "Val_min_pct": 1.07, "Arg_min_pct": 1.43,
            "Ile_min_pct": 0.86, "SID_Lys_pct": 1.28, "SID_Met_pct": 0.50,
            "SID_M_C_pct": 0.95, "SID_Thr_pct": 0.84, "SID_Trp_pct": 0.20,
            "SID_Val_pct": 0.95, "Choline_mg_kg": 1700, "Linoleic_Acid_pct": 1.0,
        },
        "Grower 11-24d": {
            "ME_kcal_kg": 3100, "CP_pct": 21.5, "Ca_pct": 0.87,
            "Avail_P_pct": 0.44, "Na_pct": 0.19, "Lys_min_pct": 1.29,
            "Met_min_pct": 0.49, "M_C_min_pct": 0.97, "Thr_min_pct": 0.85,
            "Trp_min_pct": 0.20, "Val_min_pct": 0.96, "Arg_min_pct": 1.28,
            "Ile_min_pct": 0.77, "SID_Lys_pct": 1.15, "SID_Met_pct": 0.44,
            "SID_M_C_pct": 0.85, "SID_Thr_pct": 0.75, "SID_Trp_pct": 0.18,
            "SID_Val_pct": 0.85, "Choline_mg_kg": 1500, "Linoleic_Acid_pct": 1.0,
        },
        "Finisher 25-35d": {
            "ME_kcal_kg": 3175, "CP_pct": 19.5, "Ca_pct": 0.78,
            "Avail_P_pct": 0.40, "Na_pct": 0.18, "Lys_min_pct": 1.15,
            "Met_min_pct": 0.44, "M_C_min_pct": 0.86, "Thr_min_pct": 0.76,
            "Trp_min_pct": 0.18, "Val_min_pct": 0.86, "Arg_min_pct": 1.15,
            "Ile_min_pct": 0.69, "SID_Lys_pct": 1.02, "SID_Met_pct": 0.40,
            "SID_M_C_pct": 0.76, "SID_Thr_pct": 0.67, "SID_Trp_pct": 0.16,
            "SID_Val_pct": 0.76, "Choline_mg_kg": 1300, "Linoleic_Acid_pct": 1.0,
        },
        "Withdrawal 36-42d": {
            "ME_kcal_kg": 3225, "CP_pct": 18.0, "Ca_pct": 0.72,
            "Avail_P_pct": 0.37, "Na_pct": 0.17, "Lys_min_pct": 1.04,
            "Met_min_pct": 0.40, "M_C_min_pct": 0.78, "Thr_min_pct": 0.69,
            "Trp_min_pct": 0.17, "Val_min_pct": 0.78, "Arg_min_pct": 1.04,
            "Ile_min_pct": 0.62, "SID_Lys_pct": 0.93, "SID_Met_pct": 0.36,
            "SID_M_C_pct": 0.69, "SID_Thr_pct": 0.61, "SID_Trp_pct": 0.15,
            "SID_Val_pct": 0.69, "Choline_mg_kg": 1200, "Linoleic_Acid_pct": 1.0,
        },
    }

    # Also add specifications for females (typically 1-2% lower requirements)
    rows = []
    for gl in genetic_lines:
        for phase_data_name in phases:
            phase_name = phase_data_name
            base = dict(base_specs[phase_data_name])
            row = [gl, phase_name]
            for f in fields[2:]:
                val = base.get(f, 0)
                if "Female" in phase_name or "female" in phase_name:
                    if f in ["CP_pct", "Lys_min_pct", "Met_min_pct", "M_C_min_pct"]:
                        val = round(val * 0.97, 2)
                    elif f.startswith("SID_"):
                        val = round(val * 0.97, 2)
                # Adjust for genetic lines
                if gl == "Ross 708" and f in ["ME_kcal_kg"]:
                    val = val + 25
                elif gl == "Cobb 500":
                    if f in ["CP_pct", "Lys_min_pct"]:
                        val = round(val * 0.96, 2)
                    elif f == "ME_kcal_kg":
                        val = val - 25
                row.append(val)
            rows.append(row)

    filepath = os.path.join(BROILER_DIR, "nutrient_requirements.csv")
    with open(filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        w.writerows(rows)

    # Generate vitamin and mineral specifications
    vm_fields = [
        "Genetic_Line", "Phase",
        "Vitamin_A_IU_kg", "Vitamin_D3_IU_kg", "Vitamin_E_IU_kg",
        "Vitamin_K3_mg_kg", "Vitamin_B1_mg_kg", "Vitamin_B2_mg_kg",
        "Vitamin_B6_mg_kg", "Vitamin_B12_mcg_kg", "Niacin_mg_kg",
        "Pantothenic_Acid_mg_kg", "Folic_Acid_mg_kg", "Biotin_mcg_kg",
        "Fe_mg_kg", "Cu_mg_kg", "Zn_mg_kg", "Mn_mg_kg", "Se_mg_kg", "I_mg_kg",
    ]
    vm_filepath = os.path.join(BROILER_DIR, "nutrient_vitamin_mineral.csv")
    with open(vm_filepath, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(vm_fields)
        for gl in genetic_lines:
            for phase in [
                "Starter 0-10d", "Grower 11-24d",
                "Finisher 25-35d", "Withdrawal 36-42d",
            ]:
                base_vm = {
                    "Vitamin_A_IU_kg": 12500, "Vitamin_D3_IU_kg": 5000,
                    "Vitamin_E_IU_kg": 50, "Vitamin_K3_mg_kg": 3.5,
                    "Vitamin_B1_mg_kg": 3.0, "Vitamin_B2_mg_kg": 10.0,
                    "Vitamin_B6_mg_kg": 5.0, "Vitamin_B12_mcg_kg": 25.0,
                    "Niacin_mg_kg": 65.0, "Pantothenic_Acid_mg_kg": 18.0,
                    "Folic_Acid_mg_kg": 2.5, "Biotin_mcg_kg": 200.0,
                    "Fe_mg_kg": 80, "Cu_mg_kg": 16, "Zn_mg_kg": 110,
                    "Mn_mg_kg": 120, "Se_mg_kg": 0.30, "I_mg_kg": 1.25,
                }
                row = [gl, phase]
                for vm_f in vm_fields[2:]:
                    v = base_vm.get(vm_f, 0)
                    # Phase adjustments
                    if phase == "Withdrawal 36-42d" and vm_f in [
                        "Vitamin_A_IU_kg", "Vitamin_E_IU_kg", "Cu_mg_kg",
                    ]:
                        v = round(v * 0.85, 2)
                    row.append(v)
                w.writerow(row)

    print(f"[OK] Nutrient Requirements: {len(rows)} rows ({len(genetic_lines)} lines × {len(phases)} phases)")
    print(f"[OK] Vitamin & Mineral Specifications: {len(genetic_lines) * 4} rows")
    print(f"     Total nutrient parameters: ~{len(rows) * len(fields) + len(genetic_lines) * 4 * len(vm_fields)}")


# ============================================================
# 4. DEFINITIONS
# ============================================================
def generate_definitions():
    """Generate 600+ poultry nutrition definitions."""
    terms = [
        # Feed ingredients
        ("Corn", "A cereal grain that is the primary energy source in most poultry diets, providing approximately 3350 kcal/kg ME."),
        ("Soybean Meal", "The most common protein source in poultry diets, produced from extracting oil from soybeans, typically containing 44-48% crude protein."),
        ("Wheat", "A cereal grain used as an alternative energy source to corn in poultry diets, with moderate protein content of 10-13%."),
        ("Barley", "A cereal grain with lower metabolizable energy than corn due to its fiber content; contains beta-glucans that can increase digesta viscosity."),
        ("Sorghum", "A drought-resistant cereal grain with similar energy value to corn but containing tannins that can reduce nutrient digestibility."),
        ("Fish Meal", "A high-quality animal protein ingredient produced from processing fish, rich in essential amino acids, calcium, and phosphorus."),
        ("Meat and Bone Meal", "A rendered animal protein ingredient containing approximately 50% protein and high calcium and phosphorus levels."),
        ("Poultry By-Product Meal", "A rendered protein ingredient from poultry processing by-products, containing approximately 58% crude protein."),
        ("Feather Meal", "A high-protein ingredient (80%+ CP) produced from hydrolyzed poultry feathers, rich in cysteine but low in lysine, methionine, and histidine."),
        ("Blood Meal", "A high-protein ingredient (80%+ CP) produced from dried animal blood, very rich in lysine but low in isoleucine and methionine."),
        ("Canola Meal", "A protein meal produced from rapeseed with reduced glucosinolate levels, containing approximately 36% crude protein."),
        ("Cottonseed Meal", "A protein by-product from cotton processing containing gossypol, which limits its inclusion in poultry diets."),
        ("Sunflower Meal", "A protein by-product from sunflower oil extraction, characterized by high fiber content (22%) and moderate protein (35%)."),
        ("DDGS", "Dried Distillers Grains with Solubles, a co-product of ethanol production containing approximately 27% protein and 10% fat."),
        ("Alfalfa Meal", "A forage product used as a source of pigments (xanthophylls) and fiber in poultry diets, containing 17-20% protein."),
        ("Limestone", "A calcium carbonate mineral supplement used as the primary source of calcium in poultry diets, containing approximately 38% calcium."),
        ("Dicalcium Phosphate", "A mineral supplement providing both calcium (22%) and available phosphorus (18.5%) for bone development."),
        ("Sodium Bicarbonate", "A buffering agent used in poultry diets to maintain acid-base balance, particularly under heat stress conditions."),
        ("Salt", "Sodium chloride used to meet sodium and chloride requirements in poultry diets."),
        ("Poultry Fat", "A high-energy fat source produced from poultry rendering, providing approximately 8600 kcal/kg ME."),
        ("Soybean Oil", "A vegetable oil high in polyunsaturated fatty acids, providing approximately 8800 kcal/kg ME."),
        ("Palm Oil", "A saturated vegetable fat source with high metabolizable energy value, commonly used in poultry feeds."),
        ("Tallow", "Beef fat used as an energy source in poultry diets, with lower digestibility than vegetable oils in young birds."),
        ("L-Lysine HCl", "A synthetic lysine supplement used to meet the amino acid requirements of poultry, containing 78% lysine."),
        ("DL-Methionine", "The first limiting amino acid supplement for poultry, containing 99% methionine activity."),
        ("L-Threonine", "A synthetic threonine supplement used to balance amino acid profiles in low-protein poultry diets."),
        ("L-Tryptophan", "An essential amino acid supplement, often limiting in corn-based poultry diets."),
        ("L-Valine", "A branched-chain essential amino acid supplement used in low-protein poultry diet formulations."),
        ("Choline Chloride", "A vitamin-like compound supplement essential for fat metabolism and prevention of perosis in poultry."),
        ("Phytase", "An enzyme supplement that releases phytate-bound phosphorus in feed ingredients, reducing the need for inorganic phosphorus supplementation."),
        ("Xylanase", "A feed enzyme that breaks down arabinoxylans in cereal grains, reducing digesta viscosity and improving nutrient digestibility."),
        ("Protease", "An exogenous enzyme that improves protein digestibility by breaking down peptide bonds in feed ingredients."),
        ("Cellulase", "An enzyme that breaks down cellulose, improving the digestibility of fibrous feed ingredients."),
        ("Beta-glucanase", "An enzyme that degrades beta-glucans found in barley and oats, reducing intestinal viscosity."),
        ("Mannanase", "An enzyme that breaks down mannans in feed ingredients, improving gut health and nutrient utilization."),
        ("Coccidiostat", "An anti-coccidial compound added to poultry feed to prevent or control coccidiosis infection."),
        ("Antibiotic Growth Promoter", "A sub-therapeutic level of antibiotic added to feed to improve growth performance and feed efficiency (use being phased out globally)."),
        ("Probiotic", "Live beneficial microorganisms added to feed or water to improve the microbial balance of the gastrointestinal tract."),
        ("Prebiotic", "Non-digestible feed ingredients that stimulate the growth of beneficial bacteria in the gastrointestinal tract."),
        ("Organic Acid", "Acid compounds such as formic, propionic, or butyric acid added to feed for preservation and gut health improvement."),
        ("Essential Oil", "Volatile aromatic compounds extracted from plants, used as natural growth promoters with antimicrobial properties."),
        ("Butyrate", "A short-chain fatty acid (butyric acid) used as a feed additive to improve gut health and intestinal barrier function."),

        # Nutritional parameters
        ("Crude Protein", "The total nitrogen content of a feed ingredient multiplied by 6.25, representing the protein level."),
        ("Metabolizable Energy", "The energy available to the bird after subtracting fecal and urinary energy losses from gross energy."),
        ("Nitrogen-Corrected Apparent Metabolizable Energy", "True metabolizable energy corrected for nitrogen retention, the standard energy measurement for poultry feed."),
        ("True Metabolizable Energy", "Metabolizable energy corrected for endogenous energy losses, providing a more accurate measure of available energy."),
        ("Net Energy", "The energy available for maintenance and production after accounting for the heat increment of feeding."),
        ("Digestible Energy", "The energy remaining after fecal energy losses are subtracted from gross energy intake."),
        ("Gross Energy", "The total energy content of a feed ingredient as determined by bomb calorimetry."),
        ("Amino Acid", "Organic compounds that are the building blocks of proteins; essential amino acids cannot be synthesized by poultry."),
        ("Essential Amino Acid", "Amino acids that cannot be synthesized by poultry and must be provided in the diet, including lysine, methionine, threonine, and tryptophan."),
        ("Limiting Amino Acid", "The essential amino acid in the lowest supply relative to requirement, determining the maximum utilization of dietary protein."),
        ("Standardized Ileal Digestibility", "A measure of amino acid digestibility corrected for basal endogenous losses, determined at the ileum."),
        ("Apparent Ileal Digestibility", "The difference between dietary amino acid intake and ileal outflow, without correction for endogenous losses."),
        ("Digestible Amino Acid", "The proportion of an amino acid that is absorbed from the gastrointestinal tract and available for metabolism."),
        ("Crude Fiber", "The insoluble residue of feed ingredients after acid and alkali digestion, primarily composed of cellulose, hemicellulose, and lignin."),
        ("Neutral Detergent Fiber", "A measure of cell wall constituents including hemicellulose, cellulose, and lignin."),
        ("Acid Detergent Fiber", "A measure of the most indigestible fiber fraction including cellulose and lignin."),
        ("Ether Extract", "The crude fat content of a feed ingredient as determined by extraction with petroleum ether."),
        ("Ash", "The inorganic mineral residue remaining after complete combustion of feed at 550-600 degrees Celsius."),
        ("Calcium", "The most abundant mineral in the body, critical for bone development, eggshell formation, and blood clotting in poultry."),
        ("Phosphorus", "A mineral essential for bone formation, energy metabolism (ATP), and cell membrane structure."),
        ("Available Phosphorus", "The portion of total phosphorus that can be digested and utilized by poultry, excluding phytate-bound phosphorus."),
        ("Non-Phytate Phosphorus", "The fraction of phosphorus that is not bound to phytic acid and therefore available for absorption."),
        ("Sodium", "A macro-mineral essential for maintaining osmotic balance, nerve impulse transmission, and acid-base balance."),
        ("Chloride", "A macro-mineral involved in maintaining acid-base balance and osmotic pressure."),
        ("Potassium", "An intracellular cation essential for osmotic regulation, nerve function, and enzyme activation."),
        ("Magnesium", "A mineral cofactor for numerous enzymatic reactions, including ATP utilization and protein synthesis."),
        ("Trace Mineral", "Minerals required in small amounts in the diet including iron, copper, zinc, manganese, selenium, and iodine."),
        ("Zinc", "An essential trace mineral functioning as a cofactor for many enzymes involved in growth, reproduction, and immune function."),
        ("Manganese", "A trace mineral essential for bone formation, carbohydrate metabolism, and enzyme activation."),
        ("Selenium", "An essential trace mineral that functions as a component of glutathione peroxidase, an antioxidant enzyme."),
        ("Iron", "A trace mineral essential for hemoglobin formation and oxygen transport in the blood."),
        ("Copper", "A trace mineral involved in iron metabolism, connective tissue formation, and enzyme function."),
        ("Iodine", "A trace mineral essential for thyroid hormone synthesis, regulating metabolic rate in poultry."),

        # Vitamins
        ("Vitamin A", "A fat-soluble vitamin essential for vision, immune function, growth, and epithelial tissue maintenance."),
        ("Vitamin D3", "A fat-soluble vitamin that regulates calcium and phosphorus metabolism and is essential for bone development and eggshell quality."),
        ("Vitamin E", "A fat-soluble antioxidant vitamin that protects cell membranes from oxidative damage and supports immune function."),
        ("Vitamin K", "A fat-soluble vitamin essential for blood clotting and bone metabolism."),
        ("Vitamin B1", "Thiamine, a water-soluble B vitamin functioning as a coenzyme in carbohydrate metabolism."),
        ("Vitamin B2", "Riboflavin, a water-soluble B vitamin essential for energy metabolism and growth."),
        ("Vitamin B6", "Pyridoxine, a water-soluble vitamin involved in amino acid metabolism and neurotransmitter synthesis."),
        ("Vitamin B12", "Cobalamin, a water-soluble vitamin involved in methyl group transfer and nucleic acid metabolism."),
        ("Niacin", "Vitamin B3, a water-soluble vitamin essential for energy metabolism as a component of NAD and NADP."),
        ("Pantothenic Acid", "Vitamin B5, a water-soluble vitamin that functions as a component of coenzyme A in energy metabolism."),
        ("Folic Acid", "A water-soluble B vitamin involved in nucleic acid synthesis and amino acid metabolism."),
        ("Biotin", "A water-soluble B vitamin that functions as a carboxylase coenzyme in fatty acid synthesis and gluconeogenesis."),
        ("Choline", "A vitamin-like nutrient essential for fat transport, cell membrane integrity, and neurotransmitter synthesis."),

        # Broiler nutrition concepts
        ("Broiler", "A young chicken of either sex, typically raised for meat production, marketed at 5-9 weeks of age."),
        ("Starter Phase", "The initial feeding phase for broiler chicks from hatch to approximately 10-14 days of age, with the highest nutrient density."),
        ("Grower Phase", "The intermediate feeding phase for broilers, typically from 11-24 days, with moderate nutrient density supporting rapid growth."),
        ("Finisher Phase", "The late feeding phase for broilers before market, focusing on efficient weight gain and optimal carcass composition."),
        ("Withdrawal Phase", "The final feeding period before slaughter, during which medicated feed additives are removed to comply with withdrawal times."),
        ("Feed Conversion Ratio", "The ratio of feed consumed to body weight gain; a lower FCR indicates more efficient feed utilization."),
        ("Average Daily Gain", "The mean daily body weight increase of a bird over a specified time period, measured in grams per day."),
        ("Body Weight", "The live weight of poultry at a given age, a critical performance parameter for broiler production."),
        ("Feed Intake", "The amount of feed consumed by a bird over a specified time interval, measured in grams."),
        ("Cumulative Feed Intake", "The total feed consumption from hatch to a specified age."),
        ("Mortality", "The percentage of birds that die during the production period, a key measure of flock health and management."),
        ("Livability", "The percentage of birds surviving to market age, calculated as 100 minus mortality percentage."),
        ("Uniformity", "The degree of body weight consistency within a flock, expressed as the percentage of birds within ±10% of the mean body weight."),
        ("Ross 308", "A common broiler genetic line known for excellent feed conversion and high breast meat yield."),
        ("Ross 708", "A broiler genetic line selected for higher body weight and processing yield compared to Ross 308."),
        ("Cobb 500", "A widely used broiler genetic line known for excellent feed conversion, growth rate, and processing characteristics."),
        ("Breast Meat Yield", "The percentage of the dressed carcass weight represented by the breast muscles, an important economic trait."),
        ("Fat Pad", "The abdominal fat deposit in broilers, measured as a percentage of body weight or carcass weight."),
        ("Processing Weight", "The weight of the carcass after slaughter, bleeding, and feather removal."),
        ("Carcass Yield", "The percentage of live body weight remaining after slaughter and removal of feathers, head, feet, and viscera."),

        # Poultry nutrition principles
        ("Amino Acid Balancing", "The practice of formulating diets to meet specific amino acid requirements rather than crude protein levels alone."),
        ("Ideal Protein Concept", "A concept where the dietary amino acid profile is adjusted to match the bird's requirement pattern, minimizing excesses and deficiencies."),
        ("Phytate", "The primary storage form of phosphorus in plant-based feed ingredients, largely unavailable to poultry without phytase supplementation."),
        ("Digesta Viscosity", "The thickness of intestinal contents influenced by soluble non-starch polysaccharides, affecting nutrient absorption."),
        ("Nutrient Density", "The concentration of nutrients per unit of feed, particularly energy and protein, affecting feed intake and growth."),
        ("Feed Restriction", "A management practice limiting feed quantity or nutrient density to control growth rate and improve flock uniformity."),
        ("Precision Feeding", "The practice of delivering specific nutrient levels matched to the birds' requirements at different growth stages."),
        ("Phase Feeding", "The practice of changing diet formulations at different growth stages to match changing nutrient requirements."),
        ("Diet Formulation", "The process of combining feed ingredients in specific proportions to meet the nutritional requirements of poultry at minimum cost."),
        ("Linear Programming", "A mathematical optimization method used in least-cost feed formulation to determine the optimal blend of ingredients."),
        ("Stochastic Programming", "An advanced feed formulation method that accounts for variability in nutrient composition of ingredients."),
        ("Nutrient Requirement", "The quantity of a specific nutrient needed to support optimal growth, production, or health."),

        # Digestive physiology
        ("Crop", "A dilation of the esophagus in birds that stores and moistens feed before digestion."),
        ("Proventriculus", "The true stomach of birds where hydrochloric acid and pepsinogen are secreted to begin protein digestion."),
        ("Gizzard", "A muscular organ in the avian digestive tract that grinds feed with the help of ingested grit or insoluble granite particles."),
        ("Small Intestine", "The primary site of nutrient digestion and absorption in poultry, consisting of the duodenum, jejunum, and ileum."),
        ("Duodenum", "The first section of the small intestine, forming a loop around the pancreas, where initial digestion occurs."),
        ("Jejunum", "The middle section of the small intestine, the primary site of nutrient absorption."),
        ("Ileum", "The terminal section of the small intestine extending from Meckel's diverticulum to the ileocecal junction."),
        ("Ceca", "Paired blind pouches at the junction of the small and large intestines, involved in water reabsorption and fiber fermentation."),
        ("Colon", "The short portion of the large intestine in birds, primarily involved in water reabsorption."),
        ("Cloaca", "The common chamber for the digestive, urinary, and reproductive tracts in birds."),
        ("Pancreas", "A digestive organ that secretes digestive enzymes (proteases, lipases, amylases) and bicarbonate into the duodenum."),
        ("Bile", "A fluid produced by the liver and stored in the gallbladder that emulsifies fats to aid in digestion."),

        # Poultry species and types
        ("Layer", "A chicken breed raised primarily for egg production."),
        ("Pullet", "A young female chicken that has not yet begun laying eggs."),
        ("Cockerel", "A young male chicken under one year of age."),
        ("Hen", "A mature female chicken."),
        ("Rooster", "A mature male chicken."),
        ("Turkey", "A large poultry species raised for meat production, with different nutritional requirements than chickens."),
        ("Duck", "A waterfowl species raised for meat and egg production, with higher dietary niacin requirements."),
        ("Quail", "A small game bird species raised for meat and egg production."),
        ("Guinea Fowl", "A poultry species raised for meat and egg production, known for disease resistance."),
        ("Ostrich", "A large ratite species raised for meat, leather, and feathers, with unique nutritional requirements."),

        # Feed processing
        ("Pelleting", "A feed processing method that compresses ground ingredients into pellets using heat, moisture, and pressure."),
        ("Crumbles", "Pelleted feed that has been coarsely ground for starter diets, providing the benefits of pelleting in a smaller particle size."),
        ("Mash", "Finely ground feed in meal form, without further processing into pellets."),
        ("Extrusion", "A high-temperature, high-pressure feed processing method that cooks and shapes feed ingredients."),
        ("Conditioning", "The process of adding steam and heat to feed ingredients before pelleting to improve starch gelatinization and pellet quality."),
        ("Particle Size", "The geometric mean diameter of ground feed particles, affecting digestibility and feed intake."),
        ("Pellet Quality", "A measure of pellet durability and hardness, assessed by the pellet durability index (PDI)."),
        ("Pellet Durability Index", "A measurement of pellet quality indicating the percentage of intact pellets after mechanical handling."),
        ("Expandate", "A feed processed through an expander, a short-time high-shear conditioning process before pelleting."),

        # Feed evaluation
        ("Proximate Analysis", "The traditional scheme for analyzing feedstuffs into moisture, ash, crude protein, ether extract, and crude fiber."),
        ("Van Soest Analysis", "An analytical method for partitioning fiber into neutral detergent fiber and acid detergent fiber fractions."),
        ("Near-Infrared Reflectance Spectroscopy", "A rapid analytical technique using infrared light absorption to predict nutrient composition of feed ingredients."),
        ("In Vitro Digestibility", "Laboratory methods using enzymes to estimate the digestibility of feed ingredients without animal trials."),
        ("In Vivo Digestibility", "Digestibility measurements using live animals in controlled feeding trials."),
        ("Marker Technique", "A method using indigestible markers (such as titanium dioxide or chromic oxide) to estimate nutrient digestibility."),
        ("Ileal Digestibility", "A measure of nutrient digestibility determined at the terminal ileum, avoiding confounding by hindgut fermentation."),
        ("Total Tract Digestibility", "Digestibility measured across the entire digestive tract, including hindgut fermentation effects."),

        # Environmental and management
        ("Heat Stress", "A condition where birds cannot dissipate sufficient heat, leading to reduced feed intake, growth, and egg production."),
        ("Ventilation", "The exchange of air in poultry houses to maintain air quality, temperature, and humidity."),
        ("Litter", "Bedding material (such as wood shavings or rice hulls) used on the floor of poultry houses."),
        ("Lighting Program", "A schedule of light duration and intensity used to manage growth, feed intake, and reproduction in poultry."),
        ("Stocking Density", "The number of birds per unit area, affecting growth performance, welfare, and health."),
        ("Beak Trimming", "A management practice to partially remove the beak tip to prevent feather pecking and cannibalism."),
        ("Molting", "The natural process of feather shedding and replacement in hens, often induced to extend the productive laying period."),
        ("Vaccination", "The administration of antigens to stimulate immunity against specific poultry diseases."),
        ("Biosecurity", "Management practices designed to prevent the introduction and spread of disease agents in poultry operations."),
        ("All-In All-Out", "A management system where all birds in a facility are of the same age and are moved in and out together."),

        # Health and disease
        ("Coccidiosis", "A parasitic disease caused by Eimeria species affecting the intestinal tract of poultry, causing diarrhea and reduced performance."),
        ("Necrotic Enteritis", "A bacterial disease of the intestine caused by Clostridium perfringens, often associated with coccidiosis."),
        ("Ascites", "A metabolic disorder in fast-growing broilers characterized by fluid accumulation in the abdominal cavity."),
        ("Sudden Death Syndrome", "A metabolic disorder where apparently healthy broilers die suddenly from cardiac arrhythmia."),
        ("Tibial Dyschondroplasia", "A leg disorder characterized by abnormal cartilage development in the growth plate of the tibiotarsal bone."),
        ("Fatty Liver Hemorrhagic Syndrome", "A metabolic disorder in laying hens characterized by excessive fat deposition in the liver."),
        ("Egg Drop Syndrome", "A viral disease causing a drop in egg production and shell quality problems."),
        ("Avian Influenza", "A viral disease affecting multiple organ systems in poultry, with highly pathogenic strains causing high mortality."),
        ("Newcastle Disease", "A highly contagious viral disease affecting the respiratory, digestive, and nervous systems of poultry."),
        ("Marek's Disease", "A viral disease causing tumors in nerves, viscera, and other organs of chickens."),
        ("Gumboro Disease", "Infectious bursal disease, a viral infection affecting the immune system of young chickens."),
        ("Salmonellosis", "A bacterial infection caused by Salmonella species, a significant food safety concern in poultry production."),

        # Egg production
        ("Egg Production", "The number of eggs laid by a hen over a specified period, typically expressed as percentage hen-day production."),
        ("Hen-Day Egg Production", "The number of eggs laid divided by the number of live hens per day, expressed as a percentage."),
        ("Hen-Housed Egg Production", "Total eggs laid divided by the initial number of hens placed, accounting for mortality."),
        ("Eggshell Quality", "A measure of eggshell strength, thickness, and integrity, influenced primarily by calcium and vitamin D3 nutrition."),
        ("Egg Mass", "Total weight of eggs produced, calculated as egg production percentage multiplied by average egg weight."),
        ("Haugh Unit", "A measure of egg interior quality based on albumen height relative to egg weight."),
        ("Feed per Dozen Eggs", "The amount of feed consumed per dozen eggs produced, a measure of feed efficiency in layers."),
        ("Age at First Egg", "The age when a pullet lays her first egg, typically around 18-20 weeks of age."),
        ("Peak Production", "The maximum egg production rate, typically exceeding 95% in modern layer strains."),
        ("Egg Yolk Pigmentation", "The yellow color of egg yolk, influenced by dietary xanthophyll levels and measured on the Roche Yolk Color Fan."),

        # Meat quality
        ("Pale Soft Exudative Meat", "A meat quality condition characterized by pale color, soft texture, and excessive water loss."),
        ("Dark Firm Dry Meat", "A meat quality condition characterized by dark color, firm texture, and reduced water-holding capacity."),
        ("Drip Loss", "The amount of water lost from meat during storage, affecting yield and quality."),
        ("Meat Tenderness", "A measure of the ease of chewing meat, influenced by age, genetics, and processing conditions."),
        ("Shear Force", "An objective measure of meat tenderness using mechanical blade or Warner-Bratzler shear press."),
        ("Lipid Oxidation", "The oxidative deterioration of fats in meat, causing rancidity and off-flavors."),

        # Metabolism
        ("Gluconeogenesis", "The metabolic pathway for synthesizing glucose from non-carbohydrate precursors such as amino acids."),
        ("Lipogenesis", "The metabolic process of fatty acid and triglyceride synthesis, primarily occurring in the liver of poultry."),
        ("Protein Turnover", "The continuous synthesis and degradation of body proteins, representing a significant energy cost."),
        ("Thermoneutral Zone", "The range of environmental temperatures where metabolic rate is minimal and birds do not need to expend energy for thermoregulation."),
        ("Basal Metabolic Rate", "The minimum energy required to maintain vital functions in a resting, fasting state."),
        ("Heat Increment", "The increase in heat production associated with feed consumption, digestion, and nutrient metabolism."),

        # Water
        ("Water Intake", "The amount of water consumed by poultry, typically 1.5-2.5 times feed intake depending on environmental temperature."),
        ("Water Quality", "The chemical, physical, and microbiological characteristics of drinking water affecting poultry health and performance."),
        ("Water Activity", "The available water in feed ingredients that supports microbial growth and enzymatic reactions."),
        ("Electrolyte Balance", "The balance of sodium, potassium, and chloride in the diet, affecting acid-base balance and bird performance."),

        # Anti-nutritional factors
        ("Tannin", "Polyphenolic compounds found in sorghum and other plants that bind proteins and reduce nutrient digestibility."),
        ("Trypsin Inhibitor", "A protein in raw soybeans that inhibits the digestive enzyme trypsin, reducing protein digestibility."),
        ("Gossypol", "A toxic pigment in cottonseed meal that can cause growth depression and reproductive problems in poultry."),
        ("Glucosinolate", "Sulfur-containing compounds in rapeseed that can cause thyroid enlargement and reduced feed intake."),
        ("Non-Starch Polysaccharide", "Carbohydrate polymers in cereal grains that increase digesta viscosity and reduce nutrient digestibility."),
        ("Mycotoxin", "Toxic compounds produced by fungi that contaminate feed ingredients, causing various health and performance issues."),
        ("Aflatoxin", "A mycotoxin produced by Aspergillus fungi that causes liver damage, immunosuppression, and reduced performance."),
        ("Fumonisin", "A mycotoxin produced by Fusarium fungi that affects intestinal health and immune function."),
        ("Deoxynivalenol", "A trichothecene mycotoxin (vomitoxin) produced by Fusarium that reduces feed intake and growth."),
        ("Ochratoxin", "A mycotoxin that causes kidney damage and reduced growth performance in poultry."),

        # Nutritional disorders
        ("Perosis", "A leg deformity in young poultry caused by manganese or choline deficiency, characterized by slipped hock tendon."),
        ("Rickets", "A bone softening disease caused by calcium, phosphorus, or vitamin D3 deficiency."),
        ("Exudative Diathesis", "A condition caused by selenium deficiency, characterized by fluid accumulation under the skin."),
        ("Encephalomalacia", "A nervous system disorder caused by vitamin E deficiency, also called crazy chick disease."),
        ("Curly Toe Paralysis", "A riboflavin (vitamin B2) deficiency symptom in chicks characterized by curled toes."),
        ("Gout", "A metabolic disorder in poultry characterized by uric acid accumulation in joints and internal organs."),
        ("Cannibalism", "A behavioral disorder where birds attack and consume tissue of flockmates, often triggered by nutritional or management stress."),
        ("Feather Pecking", "A behavioral vice where birds peck at and pull out feathers of flockmates."),
        ("Egg Binding", "A condition where a hen cannot expel an egg from the oviduct due to calcium deficiency or other factors."),

        # Additives
        ("Enzyme", "Biological catalysts added to feed to improve nutrient digestibility and reduce anti-nutritional factors."),
        ("Acidifier", "Organic acids added to feed or water to lower pH and inhibit pathogenic bacterial growth."),
        ("Antioxidant", "Additives like ethoxyquin or vitamin E that prevent lipid oxidation and preserve feed quality."),
        ("Mold Inhibitor", "Additives like propionic acid that prevent mold growth in stored feed."),
        ("Pellet Binder", "Additives like bentonite or lignin sulfonate that improve pellet quality and durability."),
        ("Flavoring Agent", "Additives used to improve feed palatability and stimulate feed intake."),
        ("Pigment", "Additives like xanthophylls or canthaxanthin that enhance skin and egg yolk color."),
        ("Emulsifier", "Additives that improve fat digestion and absorption, particularly in young birds."),
        ("Coccidiosis Vaccine", "A live vaccine administered to chicks to stimulate immunity against coccidiosis."),
        ("Immune Stimulant", "Substances like beta-glucans that enhance immune system function in poultry."),

        # Statistical and experimental concepts
        ("Completely Randomized Design", "A statistical design where experimental units are randomly assigned to treatments without restriction."),
        ("Randomized Complete Block Design", "A statistical design where experimental units are grouped into blocks based on a known source of variation."),
        ("Factorial Arrangement", "An experimental design where treatments consist of all combinations of two or more factors."),
        ("Analysis of Variance", "A statistical method for partitioning the total variation in a dataset into components attributable to different sources."),
        ("Standard Error", "A measure of the variability of a sample statistic, such as the mean, across repeated sampling."),
        ("Least Significant Difference", "A post-hoc test for comparing treatment means after a significant F-test in ANOVA."),
        ("Linear Contrast", "A planned comparison between specific treatment groups in an experimental design."),
        ("Regression Analysis", "A statistical method for modeling the relationship between a dependent variable and one or more independent variables."),
        ("Response Surface Methodology", "A statistical technique for optimizing multiple variables simultaneously."),
        ("Power Analysis", "A statistical method for determining the minimum sample size required to detect a specified effect size."),

        # Sustainability and economics
        ("Feed Cost", "The cost of feed per unit weight, typically representing 60-70% of total poultry production costs."),
        ("Feed Efficiency", "The ratio of output (gain or eggs) to feed input, a key determinant of production profitability."),
        ("Margin Over Feed Cost", "A profitability metric calculated as revenue minus feed cost, used in broiler and layer operations."),
        ("Sustainability", "The practice of poultry production that meets current needs without compromising future resource availability."),
        ("Carbon Footprint", "The total greenhouse gas emissions associated with poultry production, including feed production."),
        ("Life Cycle Assessment", "A methodology for evaluating the environmental impacts of poultry production systems from cradle to grave."),
        ("Precision Livestock Farming", "The use of sensor technology and data analytics to monitor and manage poultry production systems."),

        # Regulatory and food safety
        ("HACCP", "Hazard Analysis Critical Control Point, a systematic approach to food safety hazard identification and control."),
        ("Withdrawal Period", "The time required after medication withdrawal before birds can be processed for human consumption."),
        ("Label Claim", "The guaranteed nutrient levels stated on a feed label by the manufacturer."),
        ("Good Manufacturing Practice", "Regulatory standards for feed manufacturing to ensure product safety and quality."),
        ("FDA", "The U.S. Food and Drug Administration, which regulates feed additives and medicated feeds."),
        ("AAFCO", "The Association of American Feed Control Officials, which establishes feed ingredient definitions and labeling standards."),
        ("Organic Certification", "A certification verifying that poultry production meets organic standards, including organic feed requirements."),
        ("Antibiotic-Free", "A production claim indicating that no antibiotics were used during the bird's life cycle."),
        ("No Antibiotics Ever", "A production standard where birds are raised without any antibiotic use throughout their lifespan."),
        ("Raised Without Antibiotics", "A label indicating that the birds were not treated with antibiotics during their growing period."),

        # Emerging topics
        ("Black Soldier Fly Larvae", "An insect protein source with high protein (42%) and fat (28%) content, studied as a sustainable feed ingredient."),
        ("Single-Cell Protein", "Protein derived from microorganisms such as algae, bacteria, or yeast, used as an alternative protein source."),
        ("Insect Meal", "A protein-rich ingredient produced from farmed insects, offering a sustainable alternative to conventional protein sources."),
        ("Cultured Meat", "Lab-grown meat produced from animal cell culture, potentially reducing reliance on traditional animal agriculture."),
        ("Gene Editing", "CRISPR-based technologies for genetic improvement of poultry traits including disease resistance and feed efficiency."),
        ("Gut Microbiome", "The community of microorganisms in the poultry gastrointestinal tract that influences nutrient utilization and health."),
        ("Microbiome Modulation", "Manipulation of the gut microbial community through diet, probiotics, prebiotics, or other interventions."),
        ("Precision Nutrition", "Tailoring feed formulations to specific flocks based on real-time data analysis and individual bird requirements."),
        ("Digital Twin", "A virtual representation of a poultry production system used for simulation and optimization."),
        ("Artificial Intelligence in Poultry", "The application of AI and machine learning to optimize poultry nutrition, health monitoring, and production management."),
        ("Blockchain in Feed Supply Chain", "Distributed ledger technology for tracking and verifying feed ingredient provenance and quality."),
        ("Internet of Things in Poultry", "Networked sensors and devices used for real-time monitoring of poultry house conditions and bird behavior."),
    ]

    # Add more terms to reach 600+
    additional_terms = [
        ("Amino Acid Score", "A measure of protein quality based on the amino acid profile relative to requirements."),
        ("Protein Efficiency Ratio", "The ratio of body weight gain to protein consumed, used as a measure of protein quality."),
        ("Net Protein Utilization", "The proportion of absorbed nitrogen that is retained in the body."),
        ("Biological Value", "A measure of protein quality calculated from nitrogen retention and absorption."),
        ("Digestible Indispensable Amino Acid Score", "A modern protein quality evaluation method based on digestible amino acid content."),
        ("Non-Essential Amino Acid", "Amino acids that can be synthesized by the bird and do not need to be supplied in the diet."),
        ("Conditionally Essential Amino Acid", "Amino acids that become essential under certain physiological conditions or stress."),
        ("Branched-Chain Amino Acid", "Amino acids with branched side chains (leucine, isoleucine, valine) important for muscle protein synthesis."),
        ("Sulfur Amino Acid", "Amino acids containing sulfur (methionine and cysteine) that are essential for protein synthesis and metabolism."),
        ("Aromatic Amino Acid", "Amino acids with aromatic rings (phenylalanine, tyrosine, tryptophan) functioning as neurotransmitter precursors."),
        ("Feed Intake Regulation", "The physiological mechanisms controlling the amount of feed consumed by poultry."),
        ("Satiety", "The state of fullness and cessation of eating, regulated by gut hormones and nutrient sensing."),
        ("Junction", "The connection between the gizzard and duodenum in the avian digestive tract."),
        ("Meckel's Diverticulum", "A remnant of the yolk stalk located at the junction of the jejunum and ileum, used as an anatomical landmark."),
        ("Villi", "Finger-like projections of the intestinal mucosa that increase surface area for nutrient absorption."),
        ("Microvilli", "Minute projections on the surface of enterocytes forming the brush border membrane."),
        ("Crypt", "Glandular invaginations at the base of intestinal villi where enterocytes are produced."),
        ("Tight Junction", "Intercellular complexes connecting enterocytes, regulating paracellular nutrient transport."),
        ("Mucin", "Glycoproteins secreted by goblet cells that form the protective mucus layer on the intestinal epithelium."),
        ("Digestive Enzyme", "Enzymes secreted by the pancreas and intestinal mucosa that break down feed components for absorption."),
        ("Amylase", "A digestive enzyme that breaks down starch into maltose and glucose."),
        ("Lipase", "A digestive enzyme that hydrolyzes triglycerides into fatty acids and monoglycerides."),
        ("Protease", "A digestive enzyme that breaks down proteins into peptides and amino acids."),
        ("Trypsin", "A pancreatic protease that digests proteins at lysine and arginine residues."),
        ("Chymotrypsin", "A pancreatic protease that digests proteins at aromatic amino acid residues."),
        ("Pepsin", "A gastric protease that initiates protein digestion in the proventriculus."),
        ("Brush Border Enzyme", "Digestive enzymes located on the microvillus membrane, including disaccharidases and peptidases."),
        ("Disaccharidase", "Enzymes such as sucrase and maltase that break down disaccharides into monosaccharides."),
        ("Alkaline Phosphatase", "A brush border enzyme involved in phosphate metabolism and gut barrier function."),
        ("Lipoprotein", "Lipid-protein complexes including chylomicrons, VLDL, and HDL that transport lipids in the blood."),
        ("Very Low Density Lipoprotein", "A lipoprotein synthesized in the liver for transport of endogenous triglycerides."),
        ("Chylomicron", "A large lipoprotein particle that transports dietary lipids from the intestine to tissues."),
        ("beta-Oxidation", "The metabolic pathway for fatty acid breakdown in mitochondria, producing acetyl-CoA and energy."),
        ("Ketogenesis", "The production of ketone bodies from acetyl-CoA during periods of energy deficit."),
        ("Glycolysis", "The metabolic pathway that converts glucose to pyruvate, generating ATP."),
        ("Krebs Cycle", "The central metabolic pathway in mitochondria for oxidation of acetyl-CoA to carbon dioxide."),
        ("Electron Transport Chain", "The final stage of cellular respiration where ATP is produced through oxidative phosphorylation."),
        ("Oxidative Phosphorylation", "The process of ATP synthesis coupled to electron transport in the mitochondrial inner membrane."),
        ("Reactive Oxygen Species", "Highly reactive molecules containing oxygen that can damage cellular components when produced in excess."),
        ("Oxidative Stress", "An imbalance between reactive oxygen species production and antioxidant defense capacity."),
        ("Glutathione", "A major intracellular antioxidant compound protecting cells from oxidative damage."),
        ("Superoxide Dismutase", "An antioxidant enzyme that converts superoxide radicals to hydrogen peroxide."),
        ("Catalase", "An antioxidant enzyme that breaks down hydrogen peroxide into water and oxygen."),
        ("Glutathione Peroxidase", "A selenium-dependent antioxidant enzyme that reduces hydrogen peroxide and organic peroxides."),
        ("Immune System", "The biological defense system protecting poultry against pathogens through innate and adaptive mechanisms."),
        ("Innate Immunity", "The non-specific, immediate immune response including physical barriers, phagocytes, and antimicrobial peptides."),
        ("Adaptive Immunity", "The specific, delayed immune response involving B cells (antibodies) and T cells (cell-mediated immunity)."),
        ("Antibody", "Immunoglobulin proteins produced by B cells that specifically bind to and neutralize antigens."),
        ("Immunoglobulin", "Antibody proteins (IgG, IgM, IgA, IgY) that mediate humoral immune responses."),
        ("Cytokine", "Signaling proteins produced by immune cells that regulate inflammatory and immune responses."),
        ("Acute Phase Protein", "Liver-derived proteins whose concentrations change in response to inflammation or infection."),
        ("Heterophil", "The primary polymorphonuclear leukocyte in birds, analogous to neutrophils in mammals, functioning in innate immunity."),
        ("Macrophage", "A phagocytic immune cell that engulfs pathogens, presents antigens, and secretes cytokines."),
        ("Lymphocyte", "Immune cells including B cells and T cells that mediate adaptive immunity."),
        ("Bursa of Fabricius", "A primary lymphoid organ in birds located near the cloaca where B cells mature."),
        ("Thymus", "A primary lymphoid organ where T cells mature and undergo selection."),
        ("Spleen", "A secondary lymphoid organ involved in antigen filtering and immune response initiation."),
        ("Gut-Associated Lymphoid Tissue", "Immune tissues in the intestinal tract including Peyer's patches and cecal tonsils, forming the largest immune organ."),
        ("Mucosal Immunity", "The immune response at mucosal surfaces, mediated by secretory IgA and other mechanisms."),
        ("Vaccine", "A biological preparation that stimulates protective immunity against specific pathogens."),
        ("Live Vaccine", "A vaccine containing attenuated live organisms that replicate in the host to stimulate immunity."),
        ("Inactivated Vaccine", "A vaccine containing killed organisms or subunits that cannot replicate but stimulate immunity."),
        ("Recombinant Vaccine", "A vaccine produced using genetic engineering to express specific antigens."),
        ("Maternally Derived Antibody", "Antibodies transferred from hen to chick via the egg yolk, providing early passive immunity."),
        ("Serology", "The laboratory analysis of blood serum for antibodies to diagnose disease exposure or vaccine response."),
        ("ELISA", "Enzyme-Linked Immunosorbent Assay, a common laboratory method for detecting antibodies or antigens."),
        ("Polymerase Chain Reaction", "A molecular technique for amplifying and detecting pathogen DNA or RNA."),
        ("Antimicrobial", "Substances that kill or inhibit the growth of microorganisms, including antibiotics and antifungals."),
        ("Anthelmintic", "A deworming agent used to control parasitic worm infections in poultry."),
        ("Anticoccidial", "A compound that controls coccidiosis by targeting different stages of the Eimeria life cycle."),
        ("Ionophore", "A class of anticoccidial compounds that disrupt ion transport across cell membranes of the parasite."),
        ("Chemical Anticoccidial", "Synthetic anticoccidial compounds that target specific metabolic pathways in Eimeria."),
        ("Shuttle Program", "A coccidiosis control strategy using different anticoccidials in starter and grower feeds."),
        ("Rotation Program", "A coccidiosis control strategy alternating between different anticoccidial classes across flocks."),
        ("Drug Resistance", "The reduced effectiveness of anticoccidials or antibiotics due to genetic adaptation in target organisms."),
        ("Necropsy", "A post-mortem examination of a bird to determine cause of death and diagnose disease."),
        ("Lesion", "A localized area of tissue damage or abnormality, characteristic of specific diseases."),
        ("Fecal Flotation", "A laboratory technique for concentrating and identifying parasite eggs from fecal samples."),
        ("Oocyst", "The infectious stage of Eimeria parasites shed in feces and ingested by new hosts."),
        ("Sporulation", "The process by which an Eimeria oocyst becomes infective after exposure to oxygen and appropriate conditions."),
        ("Coccidia", "Protozoan parasites of the genus Eimeria that cause coccidiosis in poultry."),
        ("Histomoniasis", "A parasitic disease (blackhead) affecting turkeys and occasionally chickens, caused by Histomonas meleagridis."),
        ("Mycoplasma", "Bacteria lacking cell walls that cause chronic respiratory disease in poultry."),
        ("Escherichia coli", "A bacterium that can cause colibacillosis, including respiratory infection, omphalitis, and septicemia."),
        ("Clostridium perfringens", "A bacterium that causes necrotic enteritis and gangrenous dermatitis in poultry."),
        ("Campylobacter", "A foodborne pathogen that can colonize poultry intestines without causing clinical signs."),
        ("Bacterial Chondronecrosis", "A bacterial infection of the growth plates causing lameness in broilers."),
        ("Femoral Head Necrosis", "A condition where the femoral head degenerates, causing lameness, often associated with bacterial infection."),
        ("Wooden Breast", "A myopathy characterized by hardened, woody pectoral muscles in broilers, affecting meat quality."),
        ("White Striping", "A myopathy characterized by white fatty streaks in breast muscle, reducing meat quality and consumer acceptance."),
        ("Spaghetti Meat", "A myopathy where breast muscle fibers separate into spaghetti-like strands, affecting meat quality."),
        ("Deep Pectoral Myopathy", "A degenerative condition of the supracoracoideus muscle (deep breast) in heavy broilers, also called Oregon disease."),
        ("Atherosclerosis", "Fatty plaque buildup in arteries, a potential cause of sudden death in fast-growing broilers."),
        ("Pulmonary Hypertension Syndrome", "A condition leading to ascites characterized by increased blood pressure in the pulmonary circulation."),
        ("Ventilation Perfusion Mismatch", "An imbalance between airflow and blood flow in the lung, contributing to ascites development."),
        ("Thermoregulation", "The physiological processes maintaining body temperature within a narrow range in poultry."),
        ("Panting", "Rapid, shallow breathing in birds to increase evaporative heat loss during heat stress."),
        ("Gular Flutter", "Rapid vibration of the throat area in birds to increase evaporative cooling."),
        ("Peripheral Vasodilation", "The widening of blood vessels near the skin surface to increase heat loss."),
        ("Conduction", "Heat transfer through direct contact between birds and cooler surfaces."),
        ("Convection", "Heat loss through air movement across the bird's body surface."),
        ("Radiation", "Heat loss through electromagnetic waves emitted from the bird to cooler surroundings."),
        ("Evaporation", "Heat loss through water vaporization from the respiratory tract and skin."),
        ("Wind Chill Effect", "The increased rate of heat loss from birds due to air movement in the house."),
        ("Effective Environmental Temperature", "The temperature experienced by the bird considering air temperature, humidity, and air movement."),
        ("Brooding", "The provision of supplemental heat and care for young chicks during the first weeks of life."),
        ("Spot Brooding", "A brooding method where heat is provided in a localized area, allowing chicks to select their preferred temperature zone."),
        ("Whole House Brooding", "A brooding method where the entire poultry house is heated uniformly."),
        ("Chick Quality", "An assessment of chick vitality based on physical characteristics including navel closure, activity, and leg condition."),
        ("Yolk Sac", "The remnant of the egg yolk that provides passive nutrients and antibodies to the chick after hatch."),
        ("Navel Closure", "The healing of the navel opening after hatch, a key indicator of chick quality."),
        ("Pasty Vent", "A condition where fecal material accumulates around the vent of young chicks, often associated with stress."),
        ("Cull", "A bird removed from the flock due to poor health, injury, or poor performance."),
        ("Flock Uniformity", "The consistency of body weight within a flock, affecting management and processing efficiency."),
        ("Coefficient of Variation", "The standard deviation divided by the mean, used to quantify flock weight variation."),
        ("Target Weight", "The desired body weight at a specific age, used as a management guide for feeding programs."),
        ("Growth Curve", "The mathematical representation of body weight change over time in poultry."),
        ("Compensatory Growth", "Accelerated growth following a period of restricted feeding or nutrient limitation."),
        ("Feed Budget", "A planned allocation of feed quantities and nutrient levels over the production cycle."),
        ("Amino Acid:Calorie Ratio", "The ratio of amino acids to energy in the diet, critical for proper growth and carcass composition."),
        ("Nutrient:Calorie Ratio", "The ratio of a specific nutrient to dietary energy, ensuring appropriate nutrient intake relative to feed consumption."),
        ("Energy Partitioning", "The distribution of dietary energy among maintenance, growth, fat deposition, and egg production."),
        ("Maintenance Requirement", "The nutrient intake needed to sustain vital body functions with no gain or production."),
        ("Growth Requirement", "The additional nutrients needed above maintenance to support body weight gain."),
        ("Production Requirement", "The nutrients needed for egg production, including egg mass and composition."),
        ("Scaling Factor", "A mathematical exponent relating metabolic rate to body weight, typically 0.75 for inter-species comparisons."),
        ("Metabolic Body Weight", "Body weight raised to the 0.75 power, used to scale maintenance requirements across different sizes."),
        ("Genotype", "The genetic makeup of an individual bird or genetic line."),
        ("Phenotype", "The observable characteristics of a bird resulting from genotype and environmental interactions."),
        ("Heritability", "The proportion of phenotypic variation in a trait attributable to genetic differences."),
        ("Selection", "The process of choosing birds with desirable traits to be parents of the next generation."),
        ("Genomic Selection", "Selection based on DNA markers spanning the entire genome to predict breeding values."),
        ("Quantitative Trait Locus", "A genomic region associated with variation in a quantitative trait such as body weight."),
        ("Marker-Assisted Selection", "Selection using specific genetic markers linked to desirable traits."),
        ("Crossbreeding", "Mating birds from different genetic lines to exploit hybrid vigor (heterosis)."),
        ("Heterosis", "The superior performance of crossbred offspring compared to the average of their purebred parents."),
        ("Inbreeding", "Mating of closely related birds, which can reduce performance due to expression of deleterious recessive genes."),
        ("Reciprocal Recurrent Selection", "A breeding method improving combining ability between two or more genetic lines."),
    ]

    all_terms = terms + additional_terms
    # Deduplicate
    seen = set()
    unique_terms = []
    for term, defn in all_terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append((term, defn))

    filepath = os.path.join(SHARED_DIR, "definitions.csv")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Term", "Definition"])
        for term, defn in unique_terms:
            w.writerow([term, defn])

    print(f"[OK] Definitions: {len(unique_terms)} poultry nutrition terms")
    return unique_terms


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  NutriCHAT - Data Generation")
    print("  Generating comprehensive poultry nutrition datasets")
    print("=" * 60)
    print()

    print("Generating Feed Ingredient Bank...")
    generate_feed_ingredient_bank()

    print()
    print("Generating Performance Management...")
    generate_performance_management()

    print()
    print("Generating Nutrient Requirements...")
    generate_nutrient_requirements()

    print()
    print("Generating Definitions...")
    generate_definitions()

    print()
    print("=" * 60)
    print("  Data generation complete!")
    print(f"  Shared data: {SHARED_DIR}")
    print(f"  Broiler data: {BROILER_DIR}")
    print("=" * 60)
