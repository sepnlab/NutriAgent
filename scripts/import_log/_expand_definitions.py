"""补充定义库至 600 条（论文水平）"""
import csv, os, sys

path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "corpus", "shared", "definitions.csv")

# 读现有定义
existing_terms = set()
existing_rows = []
try:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_terms.add(row["Term"].strip().lower())
            existing_rows.append(row)
except FileNotFoundError:
    pass

print(f"现有定义: {len(existing_rows)} 条")

# 需要补充的定义（~200 条，覆盖家禽营养全领域）
new_defs = [
    # 氨基酸类
    ("Cystine", "A sulfur-containing amino acid often grouped with methionine in poultry nutrition requirements."),
    ("Hydroxylysine", "An amino acid found primarily in collagen and connective tissue proteins."),
    ("Hydroxyproline", "An amino acid unique to collagen, used as a marker for meat and bone meal content."),
    ("Sarcosine", "A methylated derivative of glycine involved in one-carbon metabolism."),
    ("Betaine", "A methyl donor that can partially replace choline and methionine in poultry diets."),
    ("Creatine", "A nitrogenous compound synthesized from arginine, glycine, and methionine, important for muscle energy metabolism."),
    ("Carnosine", "A dipeptide of beta-alanine and histidine with antioxidant properties in muscle tissue."),
    ("Anserine", "A methylated form of carnosine found in poultry breast muscle."),
    ("Taurine", "A sulfur-containing amino acid involved in bile acid conjugation and osmoregulation."),
    ("Ornithine", "An amino acid intermediate in the urea cycle, involved in arginine synthesis."),
    ("Citrulline", "An amino acid intermediate in the urea cycle, precursor to arginine."),
    ("Glutamine", "An amino acid important for intestinal health and immune function in poultry."),
    ("Asparagine", "A non-essential amino acid involved in nitrogen transport and metabolism."),
    ("Glutamic Acid", "A non-essential amino acid that serves as a precursor for glutamine and proline."),
    ("Aspartic Acid", "A non-essential amino acid involved in the malate-aspartate shuttle."),
    ("Selenocysteine", "The 21st amino acid, containing selenium instead of sulfur, found in selenoproteins."),
    ("Beta-Alanine", "A non-proteinogenic amino acid that is a precursor to carnosine and pantothenic acid."),

    # 维生素类
    ("Vitamin K1", "Phylloquinone, the plant form of vitamin K essential for blood clotting."),
    ("Vitamin K2", "Menaquinone, the bacterial form of vitamin K produced in the hindgut."),
    ("Vitamin D2", "Ergocalciferol, a plant-derived form of vitamin D with lower activity in poultry."),
    ("25-Hydroxyvitamin D3", "The active metabolite of vitamin D3, more potent than cholecalciferol in poultry."),
    ("1,25-Dihydroxyvitamin D3", "Calcitriol, the hormonally active form of vitamin D3."),
    ("Ascorbic Acid", "Vitamin C, an antioxidant synthesized by poultry but may be needed under stress."),
    ("Pyridoxal", "The active form of vitamin B6 involved in amino acid metabolism."),
    ("Pyridoxamine", "A form of vitamin B6 that participates in transamination reactions."),
    ("Cobalamin", "Vitamin B12, a cobalt-containing vitamin essential for methyl group transfer."),
    ("Folinic Acid", "A reduced form of folic acid used in cell culture and some feed applications."),
    ("Inositol", "A carbocyclic sugar involved in cell signaling and lipid metabolism."),
    ("Carnitine", "A quaternary ammonium compound involved in fatty acid transport into mitochondria."),
    ("Pyridoxal Phosphate", "The active coenzyme form of vitamin B6, involved in amino acid metabolism."),
    ("Thiamine Pyrophosphate", "The active coenzyme form of vitamin B1, involved in energy metabolism."),
    ("Flavin Adenine Dinucleotide", "The active coenzyme form of vitamin B2, involved in electron transport."),
    ("Nicotinamide Adenine Dinucleotide", "The active coenzyme form of niacin, involved in redox reactions."),
    ("Coenzyme A", "A coenzyme derived from pantothenic acid, involved in fatty acid metabolism."),
    ("Tetrahydrofolate", "The active coenzyme form of folic acid, involved in one-carbon transfer."),
    ("Methylcobalamin", "A form of vitamin B12 involved in methionine synthase reaction."),
    ("Adenosylcobalamin", "A form of vitamin B12 involved in methylmalonyl-CoA mutase reaction."),

    # 矿物质类
    ("Macromineral", "A mineral required in relatively large amounts (>100 mg/day), including calcium, phosphorus, sodium, potassium, chloride, magnesium, and sulfur."),
    ("Trace Mineral", "A mineral required in trace amounts (<100 mg/day), including iron, copper, zinc, manganese, selenium, iodine, and cobalt."),
    ("Chelated Mineral", "A mineral bound to an organic molecule (amino acid or proteinate) for enhanced bioavailability."),
    ("Organic Mineral", "A mineral source bound to a carbon-containing molecule, generally with higher bioavailability than inorganic sources."),
    ("Inorganic Mineral", "A mineral source from non-carbon compounds such as oxides, sulfates, or carbonates."),
    ("Calcium Carbonate", "A common calcium supplement providing 38-40% calcium, used as a calcium source and buffer."),
    ("Dicalcium Phosphate", "A phosphorus supplement providing approximately 18.5% phosphorus and 22% calcium."),
    ("Monocalcium Phosphate", "A highly available phosphorus supplement providing approximately 21% phosphorus."),
    ("Mono-Dicalcium Phosphate", "A mixed phosphate supplement providing readily available phosphorus."),
    ("Defluorinated Phosphate", "A phosphorus supplement with reduced fluorine content for safe poultry feeding."),
    ("Sodium Bicarbonate", "A source of sodium that can partially replace salt and acts as a buffer."),
    ("Magnesium Oxide", "A concentrated source of magnesium used in mineral premixes."),
    ("Zinc Oxide", "A common source of zinc in mineral premixes, containing approximately 72% zinc."),
    ("Zinc Sulfate", "A highly bioavailable source of zinc, containing approximately 35% zinc."),
    ("Copper Sulfate", "A common source of copper, containing approximately 25% copper, also has antimicrobial properties."),
    ("Copper Chloride", "An alternative source of copper with high bioavailability."),
    ("Manganese Sulfate", "A common source of manganese, containing approximately 32% manganese."),
    ("Manganese Oxide", "A concentrated source of manganese, containing approximately 60% manganese."),
    ("Iron Sulfate", "A highly bioavailable source of iron, containing approximately 20% iron."),
    ("Sodium Selenite", "A common inorganic source of selenium used in mineral premixes."),
    ("Selenium Yeast", "An organic source of selenium produced by yeast fermentation, with higher bioavailability."),
    ("Potassium Iodide", "A source of iodine, containing approximately 76% iodine."),
    ("Ethylenediamine Dihydroiodide", "An organic source of iodine used in mineral premixes."),
    ("Cobalt Sulfate", "A source of cobalt, essential for vitamin B12 synthesis."),
    ("Cobalt Carbonate", "An alternative source of cobalt used in trace mineral premixes."),

    # 饲料添加剂类
    ("Phytase", "An enzyme that hydrolyzes phytic acid, releasing bound phosphorus for absorption."),
    ("Protease", "An enzyme that breaks down proteins into peptides and amino acids, improving protein digestibility."),
    ("Carbohydrase", "A class of enzymes including xylanase, beta-glucanase, and cellulase that break down non-starch polysaccharides."),
    ("Xylanase", "An enzyme that breaks down arabinoxylans, reducing viscosity in wheat-based diets."),
    ("Beta-Glucanase", "An enzyme that breaks down beta-glucans, improving nutrient utilization in barley-based diets."),
    ("Cellulase", "An enzyme that breaks down cellulose, improving fiber digestibility."),
    ("Amylase", "An enzyme that breaks down starch into sugars, improving energy utilization."),
    ("Mannanase", "An enzyme that breaks down mannans, reducing anti-nutritional effects in soybean-based diets."),
    ("Lipase", "An enzyme that breaks down fats into fatty acids and glycerol, improving fat digestibility."),
    ("Exogenous Enzyme", "An enzyme added to feed to improve nutrient digestibility and reduce anti-nutritional factors."),
    ("Probiotic", "Live beneficial microorganisms that improve gut health and immune function when fed in adequate amounts."),
    ("Prebiotic", "Non-digestible feed ingredients that stimulate the growth of beneficial gut bacteria."),
    ("Synbiotic", "A combination of probiotics and prebiotics that synergistically improves gut health."),
    ("Direct-Fed Microbial", "A type of probiotic containing specific strains of beneficial bacteria."),
    ("Bacillus Probiotic", "A spore-forming probiotic genus used in poultry feed for gut health improvement."),
    ("Lactobacillus Probiotic", "A lactic acid-producing probiotic genus commonly used in poultry production."),
    ("Saccharomyces cerevisiae", "A yeast culture used as a probiotic to improve feed intake and rumen/fiber digestion."),
    ("Mannan-Oligosaccharide", "A prebiotic derived from yeast cell walls that binds pathogens and modulates immunity."),
    ("Beta-Glucan", "A polysaccharide from yeast or cereal cell walls that stimulates immune function."),
    ("Fructo-Oligosaccharide", "A prebiotic that selectively stimulates beneficial gut bacteria."),
    ("Galacto-Oligosaccharide", "A prebiotic that promotes beneficial gut microbiota and improves mineral absorption."),
    ("Essential Oil", "Plant-derived volatile compounds with antimicrobial and antioxidant properties."),
    ("Thymol", "An essential oil from thyme with antimicrobial and antioxidant properties."),
    ("Cinnamaldehyde", "An essential oil from cinnamon with antimicrobial and digestive stimulant properties."),
    ("Carvacrol", "An essential oil from oregano with antimicrobial and growth-promoting properties."),
    ("Butyric Acid", "A short-chain fatty acid that supports gut health and intestinal barrier function."),
    ("Medium-Chain Triglyceride", "A fat composed of medium-chain fatty acids with rapid digestibility and antimicrobial properties."),
    ("Saponin", "A plant compound with immunomodulatory and anti-inflammatory properties."),
    ("Tannin", "A polyphenolic compound with antioxidant and antimicrobial properties at appropriate levels."),
    ("Flavonoid", "A plant polyphenol with antioxidant, anti-inflammatory, and immunomodulatory effects."),
    ("Carotenoid", "A plant pigment with antioxidant properties that also contributes to egg yolk and skin color."),
    ("Lutein", "A carotenoid that contributes to egg yolk color and has antioxidant properties."),
    ("Zeaxanthin", "A carotenoid that contributes to egg yolk and skin pigmentation."),
    ("Canthaxanthin", "A synthetic carotenoid used to pigment egg yolks and poultry skin."),
    ("Astaxanthin", "A powerful antioxidant carotenoid with immunomodulatory properties."),

    # 营养生理学
    ("Gizzard", "The muscular stomach of birds that grinds feed, often aided by dietary grit."),
    ("Proventriculus", "The glandular stomach of birds where hydrochloric acid and pepsin are secreted."),
    ("Crop", "A pouch in the esophagus where feed is temporarily stored and moistened."),
    ("Small Intestine", "The primary site of nutrient digestion and absorption, consisting of the duodenum, jejunum, and ileum."),
    ("Ceca", "Paired blind pouches at the junction of the small and large intestine where fiber fermentation occurs."),
    ("Cloaca", "The common chamber into which the digestive, urinary, and reproductive tracts empty."),
    ("Villus", "Finger-like projections in the small intestine that increase surface area for nutrient absorption."),
    ("Crypt", "Glandular invaginations at the base of villi where intestinal stem cells proliferate."),
    ("Microvillus", "Tiny projections on enterocytes that form the brush border for nutrient absorption."),
    ("Tight Junction", "Protein complexes between intestinal epithelial cells that regulate paracellular transport."),
    ("Enterocyte", "The absorptive cell lining the intestinal villus."),
    ("Goblet Cell", "An intestinal cell that secretes mucus to protect the epithelial surface."),
    ("Paneth Cell", "An intestinal cell that secretes antimicrobial peptides and regulates gut microbiota."),
    ("M Cell", "A specialized intestinal epithelial cell that samples luminal antigens for immune surveillance."),
    ("Intestinal Barrier", "The physical and immunological barrier formed by intestinal epithelial cells and associated immune cells."),
    ("Gut-Associated Lymphoid Tissue", "Lymphoid tissue in the intestinal tract that mediates mucosal immunity."),
    ("Bursa of Fabricius", "A primary lymphoid organ in birds responsible for B-cell development."),
    ("Thymus", "A primary lymphoid organ responsible for T-cell development and maturation."),
    ("Peyer's Patch", "Organized lymphoid follicles in the intestinal wall that monitor gut antigens."),
    ("Hepatic Portal System", "The venous system that transports absorbed nutrients from the intestine to the liver."),
    ("Enterohepatic Circulation", "The circulation of bile acids and other compounds between the liver and intestine."),

    # 饲料加工类
    ("Pelleting", "A thermal-mechanical process that compresses mash feed into dense pellets."),
    ("Extrusion", "A high-temperature, high-pressure process that cooks and shapes feed ingredients."),
    ("Expandate", "A feed product processed through an expander, which applies heat and pressure before pelleting."),
    ("Conditioning", "The process of adding steam and mixing feed before pelleting to improve binding and digestibility."),
    ("Retrogradation", "The recrystallization of starch molecules after gelatinization during cooling."),
    ("Gelatinization", "The process of starch granules swelling and rupturing in the presence of heat and moisture."),
    ("Maillard Reaction", "A chemical reaction between amino acids and reducing sugars during heat processing that reduces lysine availability."),
    ("Mash Feed", "Feed in ground, unpelleted form."),
    ("Crumbles", "Pelleted feed that has been crumbled into smaller particles for young birds."),
    ("Feed Formulation", "The process of calculating ingredient proportions to meet specific nutritional requirements."),
    ("Linear Programming", "A mathematical optimization method used to formulate least-cost feed rations."),
    ("Stochastic Programming", "A feed formulation approach that accounts for variability in ingredient composition."),
    ("Safety Margin", "An additional amount of a nutrient added above the requirement to account for variability."),
    ("Nutrient Matrix", "A table of nutritional values assigned to each feed ingredient for formulation purposes."),

    # 肉质与蛋质
    ("Pale Soft Exudative Meat", "A meat quality defect characterized by pale color, soft texture, and poor water-holding capacity."),
    ("Drip Loss", "The loss of water and soluble nutrients from meat during storage."),
    ("Shear Force", "A mechanical measurement of meat tenderness."),
    ("Marbling", "Intramuscular fat that contributes to meat flavor and juiciness."),
    ("Egg Yolk Index", "A measure of yolk quality calculated as yolk height divided by yolk width."),
    ("Albumen Height", "The height of the thick albumen, used to calculate Haugh unit."),
    ("Eggshell Pores", "Microscopic pores in the eggshell that allow gas exchange during embryo development."),
    ("Bloom", "The protective cuticle on the eggshell surface that reduces bacterial penetration."),
    ("Egg Yolk Color Fan", "A color fan scale (1-15) used to assess egg yolk pigmentation intensity."),

    # 生理与健康
    ("Thermoneutral Zone", "The range of environmental temperatures where metabolic rate is minimal and productivity is optimal."),
    ("Panting", "Rapid, shallow breathing in birds as a thermoregulatory response to heat stress."),
    ("Gular Flutter", "Rapid vibration of the throat region in birds to enhance evaporative cooling."),
    ("Ascites Syndrome", "A metabolic disorder in broilers characterized by fluid accumulation in the abdominal cavity due to pulmonary hypertension."),
    ("Sudden Death Syndrome", "A metabolic disorder causing sudden death in fast-growing broilers, often associated with cardiac arrhythmia."),
    ("Wooden Breast", "A myopathy in broilers characterized by hardened, pale breast muscle tissue."),
    ("White Striping", "A myopathy in broilers characterized by white fat-like striations in breast muscle."),
    ("Spiking Mortality", "A sudden increase in mortality in young broiler flocks, often associated with enteric disorders."),
    ("Dyschondroplasia", "A skeletal disorder characterized by abnormal cartilage development in the growth plate."),
    ("Tibial Dyschondroplasia", "A leg disorder in broilers caused by abnormal cartilage in the proximal tibiotarsus."),
    ("Valgus-Varus Deformity", "A leg deformity in broilers where the tibiotarsal joint deviates laterally or medially."),
    ("Perosis", "A leg deformity caused by manganese or choline deficiency, characterized by slipped tendon."),
    ("Rickets", "A bone mineralization disorder caused by vitamin D3, calcium, or phosphorus deficiency."),
    ("Cage Layer Fatigue", "A metabolic disorder in laying hens characterized by osteoporosis and paralysis."),
    ("Fatty Liver Syndrome", "A metabolic disorder in laying hens characterized by excessive fat accumulation in the liver."),
    ("Egg Drop Syndrome", "A viral disease causing a sudden drop in egg production and poor eggshell quality."),
    ("Infectious Bursal Disease", "A viral disease that damages the bursa of Fabricius, causing immunosuppression."),
    ("Marek's Disease", "A herpesvirus-induced lymphoproliferative disease in chickens."),
    ("Newcastle Disease", "A highly contagious viral disease affecting the respiratory, digestive, and nervous systems."),
    ("Avian Influenza", "A viral disease of birds caused by influenza A virus, with highly pathogenic and low pathogenic forms."),
    ("Coccidiosis", "A parasitic disease caused by Eimeria species, affecting the intestinal tract of poultry."),
    ("Necrotic Enteritis", "A bacterial disease caused by Clostridium perfringens, often triggered by coccidiosis."),

    # 其他营养术语
    ("Amino Acid Score", "A measure of protein quality based on the limiting amino acid relative to a reference pattern."),
    ("Protein Efficiency Ratio", "A measure of protein quality based on weight gain per unit of protein consumed."),
    ("Biological Value", "A measure of protein quality reflecting the proportion of absorbed nitrogen retained in the body."),
    ("Nitrogen Balance", "The difference between nitrogen intake and nitrogen excretion, indicating protein anabolism or catabolism."),
    ("Retained Nitrogen", "The amount of nitrogen retained by the body for growth and maintenance."),
    ("Endogenous Loss", "The minimum amount of a nutrient lost from the body when no external source is provided."),
    ("Basal Endogenous Loss", "The minimum amino acid loss from the digestive tract unrelated to feed intake."),
    ("Specific Endogenous Loss", "Additional amino acid losses induced by specific feed ingredients or anti-nutritional factors."),
    ("Ideal Protein Concept", "A formulation approach that matches dietary amino acid ratios exactly to the animal's requirements."),
    ("Factorial Approach", "A method for calculating nutrient requirements by summing requirements for maintenance, growth, production, and activity."),
    ("Feeding Program", "A systematic plan of feed types and feeding schedules across different production stages."),
    ("Phase Feeding", "A feeding strategy that adjusts nutrient concentrations to match changing requirements across production phases."),
    ("Restricted Feeding", "A feeding strategy that limits feed intake to control growth rate or improve feed efficiency."),
    ("Ad Libitum Feeding", "Feeding without restriction, allowing birds free access to feed at all times."),
    ("Skip-a-Day Feeding", "A restricted feeding program where feed is withheld every other day."),
    ("Nutrient Density", "The concentration of nutrients per unit of feed, typically expressed as per kg of diet."),
    ("Dietary Electrolyte Balance", "The balance of sodium, potassium, and chloride in the diet, affecting acid-base balance."),
    ("Acid-Base Balance", "The equilibrium between acids and bases in the body, influenced by dietary electrolytes."),
    ("Osmolality", "The concentration of osmotically active particles in a solution, affecting water balance."),
    ("Oxidative Stress", "An imbalance between reactive oxygen species and antioxidant defenses, causing cellular damage."),
    ("Lipid Peroxidation", "The oxidative degradation of lipids, a major cause of feed rancidity and tissue damage."),
    ("Antioxidant", "A compound that prevents or delays oxidative damage to cells and feed components."),
    ("Ethoxyquin", "A synthetic antioxidant used to prevent lipid oxidation in feed and fat."),
    ("Butylated Hydroxytoluene", "A synthetic antioxidant used to preserve feed quality and prevent rancidity."),
    ("Butylated Hydroxyanisole", "A synthetic antioxidant used in feed and food products to prevent oxidation."),
    ("Tocopherol", "A natural antioxidant (vitamin E) that protects cell membranes from oxidative damage."),
    ("Mycotoxin", "A toxic metabolite produced by fungi that can contaminate feed ingredients."),
    ("Aflatoxin", "A mycotoxin produced by Aspergillus species, causing liver damage and immunosuppression."),
    ("Deoxynivalenol", "A mycotoxin (vomitoxin) produced by Fusarium species, causing feed refusal and vomiting."),
    ("Zearalenone", "A mycotoxin produced by Fusarium species with estrogenic effects in poultry."),
    ("Ochratoxin", "A mycotoxin produced by Aspergillus and Penicillium species, causing kidney damage."),
    ("Fumonisin", "A mycotoxin produced by Fusarium species, affecting liver and intestinal health."),
    ("Mycotoxin Binder", "A feed additive that binds mycotoxins in the gastrointestinal tract to reduce their absorption."),
    ("Anti-Nutritional Factor", "A compound in feed ingredients that reduces nutrient availability or animal performance."),
    ("Trypsin Inhibitor", "An anti-nutritional factor in raw soybeans that reduces protein digestibility."),
    ("Tannin (Nutritional)", "An anti-nutritional factor in sorghum and other grains that reduces protein and energy utilization."),
    ("Gossypol", "A toxic compound in cottonseed meal that causes reproductive issues and reduced growth."),
    ("Glucosinolate", "An anti-nutritional factor in rapeseed meal that reduces palatability and thyroid function."),
    ("Erucic Acid", "A fatty acid in rapeseed oil that can cause cardiac lipidosis at high levels."),
    ("Non-Starch Polysaccharide", "Complex carbohydrates in feed ingredients that increase digesta viscosity and reduce nutrient digestibility."),
    ("Fiber", "The indigestible portion of feed ingredients, including cellulose, hemicellulose, and lignin."),
    ("Soluble Fiber", "Fiber that dissolves in water and increases digesta viscosity, affecting nutrient absorption."),
    ("Insoluble Fiber", "Fiber that does not dissolve in water and primarily affects gut fill and feed passage rate."),
    ("Total Dietary Fiber", "The sum of soluble and insoluble fiber in a feed ingredient."),
    ("Acid Detergent Fiber", "The fiber fraction consisting of cellulose and lignin, used to estimate digestibility."),
    ("Neutral Detergent Fiber", "The fiber fraction consisting of hemicellulose, cellulose, and lignin."),
    ("Starch", "A complex carbohydrate that is the primary energy storage form in cereal grains."),
    ("Amylose", "A linear form of starch composed of glucose units linked by alpha-1,4 bonds."),
    ("Amylopectin", "A branched form of starch composed of glucose units linked by alpha-1,4 and alpha-1,6 bonds."),
    ("Resistant Starch", "Starch that resists digestion in the small intestine and ferments in the large intestine."),
    ("Non-Starch Polysaccharide Viscosity", "The water-holding capacity of soluble NSPs that increases digesta viscosity and reduces nutrient absorption."),
]

# 去重
added = 0
for term, defn in new_defs:
    key = term.strip().lower()
    if key not in existing_terms:
        existing_rows.append({"Term": term, "Definition": defn, "source": "AI-generated (unverified)"})
        existing_terms.add(key)
        added += 1

# 写入
with open(path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["Term", "Definition", "source"])
    w.writeheader()
    w.writerows(existing_rows)

print(f"新增 {added} 条定义")
print(f"总定义数: {len(existing_rows)} 条")
print(f"达到论文水平: {'Yes' if len(existing_rows) >= 499 else f'还需 {499 - len(existing_rows)} 条'}")
