## S3. Evaluation Query Sets

### S3.1 Curated Evaluation Set (54 queries)

> Auto-generated from `queries/layer/evaluation_queries_curated.json` by `scripts/paper/build_supplementary_s3.py`. Do not edit by hand.

- Total: **54** queries (42 English / 12 Chinese)
- Query types: {'single-value': 21, 'comparison': 10, 'open-ended': 7, 'definition': 7, 'multi-hop': 4, 'constraint': 3, 'counterfactual': 2}
- Numeric ground truth: **36**; expected-behaviour annotations: **25**

**Feed Ingredient Bank (10 queries)**

- C-FIB-001: What is the crude protein content of maize? [single-value, EN; unit=%; target=feed_ingredient_bank:Maize]
- C-FIB-002: What is the calcium content of limestone? [single-value, EN; unit=%; target=feed_ingredient_bank:Limestone]
- C-FIB-003: What is the metabolizable energy of soybean meal 48% in kcal/kg? [single-value, EN; unit=kcal/kg; target=feed_ingredient_bank:Soybean meal, oil < 5%, 48% protein + oil]
- C-FIB-004: Which has higher metabolizable energy, maize or soft wheat? State both values. [comparison, EN; unit=kcal/kg; target=feed_ingredient_bank:Maize, feed_ingredient_bank:Wheat, soft]
- C-FIB-005: Compare the crude protein of soybean meal 48% and canola meal. Which is higher and by how much? [comparison, EN; unit=%; target=feed_ingredient_bank:Soybean meal, oil < 5%, 48% protein + oil, feed_ingredient_bank:Canola meal, oil < 5%]
- C-FIB-006: List three plant protein sources from the feed ingredient bank with crude protein above 30%. Cite exact CP values. [open-ended, EN; unit=%]
- C-FIB-007: Compare the SID lysine digestibility of maize and soybean meal 48%. What does this imply for formulation? [open-ended, EN; unit=%; target=feed_ingredient_digestibility:Maize, feed_ingredient_digestibility:Soybean meal, oil < 5%, 48% protein + oil]
- C-FIB-008: Define metabolizable energy (ME). How does it differ from gross energy? [definition, EN; target=definitions:metabolizable energy]
- C-FIB-009: 玉米的粗蛋白含量是多少？ [single-value, ZH; unit=%; target=feed_ingredient_bank:Maize]
- C-FIB-010: 豆粕48和菜粕的代谢能各是多少？哪个更高？ [comparison, ZH; unit=kcal/kg; target=feed_ingredient_bank:Soybean meal, oil < 5%, 48% protein + oil, feed_ingredient_bank:Rapeseed meal, oil < 5%]

**Nutrient Requirements (12 queries)**

- C-NR-001: What is the calcium requirement for Isa Brown in Lay I? [single-value, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I]
- C-NR-002: What is the SID methionine requirement for Isa Brown in Lay I? [single-value, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I]
- C-NR-003: What is the crude protein requirement for Jinghong 1 in Layer I? [single-value, EN; unit=%; target=nutrient_requirements:Jinghong 1 v3.0/Layer I]
- C-NR-004: Compare calcium requirement: Isa Brown Lay I vs Lay III. Which is higher? [comparison, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I, nutrient_requirements:ISA Brown/Lay III]
- C-NR-005: Compare calcium requirement: Isa Brown vs Dawu Jinfeng, both in Lay I. Which is higher? [comparison, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I, nutrient_requirements:Dawu Jinfeng/Lay I]
- C-NR-006: How does the calcium requirement for Isa Brown change from Developer through Lay III? State the Ca% for each phase. [open-ended, EN; unit=%; target=nutrient_requirements:ISA Brown]
- C-NR-007: A feed ingredient has total lysine of 0.85% and SID lysine digestibility of 88%. What is the SID lysine content (in %)? [single-value, EN; unit=%]
- C-NR-008: A diet has 0.45% total phosphorus and 0.30% phytate phosphorus. If phytase improves phytate P release by 50%, what is the effective available phosphorus? [single-value, EN; unit=%]
- C-NR-009: Define SID (Standardized Ileal Digestible) amino acids. Why is it preferred over total amino acids? [definition, EN; target=definitions:standardized ileal digestibility]
- C-NR-010: 大午金凤在产蛋I期的钙需要量是多少？ [single-value, ZH; unit=%; target=nutrient_requirements:Dawu Jinfeng/Lay I]
- C-NR-011: 大午金凤从产蛋I期到产蛋III期，钙需要量怎么变化？ [comparison, ZH; unit=%; target=nutrient_requirements:Dawu Jinfeng]
- C-NR-012: 大午金凤在产蛋I期的SID蛋氨酸需要量是多少？ [single-value, ZH; unit=%; target=nutrient_requirements:Dawu Jinfeng/Lay I]

**Performance Management (11 queries)**

- C-PM-001: What is the hen-day production for Isa Brown at week 30? [single-value, EN; unit=%; target=performance_management:ISA Brown/week 30]
- C-PM-002: What is the egg weight for Hy-Line Brown at week 30? [single-value, EN; unit=g; target=performance_management:Hy-Line Brown/week 30]
- C-PM-003: Compare hen-day production: Isa Brown week 30 vs Hy-Line Brown week 30. Which is higher? [comparison, EN; unit=%; target=performance_management:ISA Brown/week 30, performance_management:Hy-Line Brown/week 30]
- C-PM-004: Compare daily feed intake: Isa Brown week 30 vs Hy-Line Brown week 30. [comparison, EN; unit=g/d; target=performance_management:ISA Brown/week 30, performance_management:Hy-Line Brown/week 30]
- C-PM-005: Track the body weight of Isa Brown pullets at week 5, 10, and 15. What is the weight at each point? [open-ended, EN; unit=g; target=performance_management:ISA Brown/weeks 5,10,15]
- C-PM-006: Isa Brown at week 30: feed intake 112 g/day, Ca requirement 4.04%. Estimate daily calcium intake in mg/hen/day. Is it sufficient for eggshell (~4000 mg/day)? [open-ended, EN; unit=mg/hen/day; target=performance_management:ISA Brown/week 30, nutrient_requirements:ISA Brown/Lay I]
- C-PM-007: Isa Brown at week 30: hen-day production 95.5%, average egg weight 61.5g. Calculate egg mass in g/hen/day. [single-value, EN; unit=g/hen/day; target=performance_management:ISA Brown/week 30]
- C-PM-008: Define hen-day egg production. How is it calculated? [definition, EN; target=definitions:hen-day egg production]
- C-PM-009: 京粉6号在第30周的产蛋率是多少？ [single-value, ZH; unit=%; target=performance_management:Jingfen 6/week 30]
- C-PM-010: 京粉6号和海兰褐在第30周的产蛋率各是多少？哪个更高？ [comparison, ZH; unit=%; target=performance_management:Jingfen 6/week 30, performance_management:Hy-Line Brown/week 30]
- C-PM-011: 京粉6号第30周的产蛋率和蛋重各是多少？ [single-value, ZH; unit=% / g; target=performance_management:Jingfen 6/week 30]

**Definitions (6 queries)**

- C-DEF-001: Define metabolizable energy (ME). How does it differ from digestible energy (DE)? [definition, EN; target=definitions:metabolizable energy, definitions:digestible energy]
- C-DEF-002: Define available phosphorus. Why is it different from total phosphorus? [definition, EN; target=definitions:available phosphorus, definitions:total phosphorus]
- C-DEF-003: What is feed conversion ratio (FCR)? How is it calculated? [definition, EN; target=definitions:feed conversion ratio]
- C-DEF-004: A feed sample has 2.5% nitrogen. Using N×6.25, what is the crude protein percentage? [single-value, EN; unit=%]
- C-DEF-005: 什么是代谢能？它和消化能有什么区别？ [definition, ZH; target=definitions:metabolizable energy, definitions:digestible energy]
- C-DEF-006: 蛋鸡饲料配方为什么优先用代谢能而不是消化能？ [open-ended, ZH; target=definitions:metabolizable energy, definitions:digestible energy]

**Cross-Domain (10 queries)**

- C-XD-001: A Lay I diet uses 60% maize (total lysine=0.247%, SID=90%) and 25% SBM48 (total lysine=0.620%, SID=88%). Calculate the SID lysine contribution. Does it meet the ISA Brown layers requirement (0.77%)? [multi-hop, EN; unit=%]
- C-XD-002: Ca requirement for ISA Brown layers is 4.04%. Limestone has 35% Ca. What % of limestone is needed in the diet? [multi-hop, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I, feed_ingredient_bank:Limestone]
- C-XD-003: Can limestone at 9% inclusion meet the Ca requirement of 4.04% for ISA Brown layers? Calculate the Ca contribution. [constraint, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I, feed_ingredient_bank:Limestone]
- C-XD-004: A Lay I diet: 55% maize + 30% SBM48. Using SID lysine values, calculate total SID lysine. Does it meet 0.77%? [constraint, EN; unit=%]
- C-XD-005: Maize CP drops from 8.8% to 5.0% (severe drought). Original formula: 60% maize. By how many percentage points must SBM48 (CP=52.6%) increase to maintain total CP? [counterfactual, EN; unit=percentage points; target=feed_ingredient_bank:Maize]
- C-XD-006: SBM price doubles. Replace 50% of SBM with canola meal. Original: 25% SBM (CP=52.6%). New: 12.5% SBM + 12.5% canola (CP=41.0%). Calculate the CP contribution change. [counterfactual, EN; unit=percentage points (decrease); target=feed_ingredient_bank:Soybean meal, oil < 5%, 48% protein + oil, feed_ingredient_bank:Canola meal, oil < 5%]
- C-XD-007: ISA Brown at week 30: feed intake 112 g/day, Ca requirement 4.04%. Estimate daily Ca intake (mg/hen/day). Sufficient for eggshell? [multi-hop, EN; unit=mg/hen/day; target=nutrient_requirements:ISA Brown/Lay I, performance_management:ISA Brown/week 30]
- C-XD-008: A nutritionist has maize, SBM48, limestone, and dicalcium phosphate. Explain how to balance Ca and P in a layer diet. What constraints must be satisfied? [open-ended, EN]
- C-XD-009: 一个产蛋I期配方用60%玉米（总赖氨酸0.247%，SID消化率90%）和25%豆粕48（总赖氨酸0.620%，SID消化率88%）。这两样原料的SID赖氨酸加起来是多少？能不能满足大午金凤蛋鸡的需要量（0.76%）？ [multi-hop, ZH; unit=%; target=nutrient_requirements:Dawu Jinfeng/Lay I]
- C-XD-010: 石灰石含钙35%，大午金凤蛋鸡的钙需要量是3.90%。配方里要加多少石灰石才能满足？ [constraint, ZH; unit=%; target=nutrient_requirements:Dawu Jinfeng/Lay I, feed_ingredient_bank:Limestone]

**Edge Cases (5 queries)**

- C-EC-001: What is the crude protein content of unicorn feed? [single-value, EN]
- C-EC-002: What is the calcium requirement for Lohmann Tinted in Lay I? [single-value, EN; unit=%]
- C-EC-003: What is the body weight of ISA Brown broilers at day 35? [single-value, EN; unit=g]
- C-EC-004: What is the methionine requirement for ISA Brown in Lay I? [single-value, EN; unit=%; target=nutrient_requirements:ISA Brown/Lay I]
- C-EC-005: Compare the metabolizable energy of fish meal and limestone. [comparison, EN; unit=kcal/kg; target=feed_ingredient_bank:Fish meal, protein 65%, feed_ingredient_bank:Limestone]
