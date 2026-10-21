# Supplementary Material — NutriAgent

This document contains supplementary tables and materials referenced in the main paper.

---

## S1. Data tables (Tables S1–S3)

## Table S1. Data schema and completeness

Nominal cells = rows × parameters. Populated cells count non-missing values; the difference is reported rather than hidden.

| Module | File | Rows | Parameters | Nominal cells | Populated | Completeness | Fully empty parameters |
|---|---|---:|---:|---:|---:|---:|---|
| Feed ingredient bank | `corpus/shared/feed_ingredient_bank.csv` | 108 | 38 | 4104 | 2376 | 57.9% | NFE_pct, NE_kcal_kg, Linoleic_pct, Linolenic_pct, Cl_pct, S_pct, Fe_mg_kg, Cu_mg_kg, Zn_mg_kg, Mn_mg_kg, Se_mg_kg, I_mg_kg, Vit_A_IU_kg, Vit_D3_IU_kg, Vit_E_mg_kg, Vit_K3_mg_kg |
| Feed ingredient amino acids | `corpus/shared/feed_ingredient_amino_acids.csv` | 108 | 19 | 2052 | 2052 | 100.0% | — |
| Feed ingredient digestibility | `corpus/shared/feed_ingredient_digestibility.csv` | 108 | 40 | 4320 | 4320 | 100.0% | — |
| Layer nutrient requirements | `corpus/layer/nutrient_requirements.csv` | 103 | 20 | 2060 | 1517 | 73.6% | — |
| Layer vitamin / mineral specifications | `corpus/layer/nutrient_vitamin_mineral.csv` | 30 | 18 | 540 | 540 | 100.0% | — |
| Layer production benchmarks | `corpus/layer/performance_management.csv` | 1131 | 12 | 13572 | 5798 | 42.7% | Egg_Mass_g_per_d, Feed_per_Dozen_kg, Feed_per_kg_Egg_kg |
| Terminology definitions | `corpus/shared/definitions.csv` | 556 | — | — | — | — | — |

**Layer nutrient requirement parameters (20):** metabolizable energy; crude protein; calcium; available phosphorus; sodium; total lysine, methionine, methionine–cysteine, threonine, tryptophan, valine, arginine, isoleucine; SID coefficients for lysine, methionine, methionine–cysteine, threonine, tryptophan; choline; linoleic acid.

**Layer production parameters (12):** hen-day production; egg weight; egg mass per hen per day; daily feed intake; feed per dozen eggs; feed per kg egg mass; body weight; mortality; shell breaking strength; Haugh unit; cumulative egg count; daily water intake.

**Vitamin/mineral parameters (18):** vitamins A, D3, E, K3, B1, B2, B6, B12, niacin, pantothenic acid, folic acid, biotin; Fe, Cu, Zn, Mn, Se, I.

## Table S2. Phase crosswalk (original breeder labels → seven reference phases)

Every original label is mapped explicitly. `mapping_type` is one of exact, within, boundary, semantic, composite, or ambiguous; composite and ambiguous labels are not forced into a single phase.

| Original label | Reference phase | Mapping type | Breeds (nutrition) | Note |
|---|---|---|---|---|
| D1 6-12w | Developer 13-17w | semantic | Nongda 6 | D1 of a 4-phase scheme; age overlaps Grower |
| D2 13-16w | Developer 13-17w | within | Nongda 6 | D2 of a 4-phase scheme |
| Developer (13-16w) | Developer 13-17w | within | Hy-Line Brown; Hy-Line Pink; Hy-Line W-36 | — |
| Developer 11-16w | Developer 13-17w | boundary | Hisex Brown; Lohmann Pink | — |
| Developer 13-16w | Developer 13-17w | within | Beinong 1; Beinong 2; Nongda 3 | — |
| Developer 13-17w | Developer 13-17w | exact | ISA Brown | — |
| Developer 7-10w | Developer 13-17w | semantic | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong 1 v3.0 | age lies in Grower window |
| Developer 9-16w | Developer 13-17w | boundary | Lohmann Grey | — |
| Finisher 11-14w | Developer 13-17w | semantic | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong 1 v3.0 | finisher label precedes Pre-Lay 15w-5% |
| G 4-6w | Grower 7-12w | semantic | Nongda 6 | labelled G but 4-6w lies in Starter window |
| Grower (7-12w) | Grower 7-12w | exact | Hy-Line Brown; Hy-Line Pink; Hy-Line W-36 | — |
| Grower 3-6w | Grower 7-12w | semantic | Jingfen 6; Jinghong 1 v3.0 | age lies in Starter window |
| Grower 4-6w | Grower 7-12w | semantic | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939 | age lies in Starter window |
| Grower 4-8w | Grower 7-12w | boundary | Lohmann Grey | — |
| Grower 5-10w | Grower 7-12w | boundary | Lohmann Pink | — |
| Grower 6-10w | Grower 7-12w | boundary | Hisex Brown | — |
| Grower 6-12w | Grower 7-12w | boundary | Beinong 1; Beinong 2; Nongda 3 | — |
| Grower 7-12w | Grower 7-12w | exact | ISA Brown | — |
| Lay I 21-40w | Lay I 21-40w | exact | ISA Brown | — |
| Lay II 41-60w | Lay II 41-60w | exact | ISA Brown | — |
| Lay III 61w+ | Lay III 61w+ | exact | ISA Brown | — |
| Layer | unmapped | ambiguous | — | vitamin table: laying phase not specified |
| Layer I (5%-90%) | Lay I 21-40w | semantic | Dawu Jinfeng; Jingbai 939 | physiological-stage label, not age-based |
| Layer I (5%-peak+4w) | Lay I 21-40w | semantic | Jingfen 6; Jinghong 1 v3.0 | physiological-stage label |
| Layer I 19-50w | Lay I 21-40w | boundary | Lohmann Pink | age spans Lay I and Lay II |
| Layer II (90%-80%) | Lay II 41-60w | semantic | Dawu Jinfeng; Jingbai 939 | physiological-stage label |
| Layer II (peak+4w-90%) | Lay II 41-60w | semantic | Jinghong 1 v3.0 | physiological-stage label |
| Layer II (peak-90%) | Lay II 41-60w | semantic | Jingfen 6 | physiological-stage label |
| Layer II 51-70w | Lay II 41-60w | boundary | Lohmann Pink | age spans Lay II and Lay III |
| Layer III (80%-cull) | Lay III 61w+ | semantic | Dawu Jinfeng; Jingbai 939 | physiological-stage label |
| Layer III (90%-85%) | Lay III 61w+ | semantic | Jingfen 6; Jinghong 1 v3.0 | physiological-stage label |
| Layer III 71-100w | Lay III 61w+ | within | Lohmann Pink | — |
| Layer IV (85%-cull) | Lay III 61w+ | semantic | Jingfen 6; Jinghong 1 v3.0 | breeder-specific 4th laying phase |
| PL 17w-5% | Pre-Lay 18-20w | boundary | Nongda 6 | PL = pre-lay |
| PP <83% | Lay III 61w+ | semantic | Nongda 6 | post-peak production threshold |
| Peak 5%-peak | Lay I 21-40w | semantic | Nongda 3 | peak lies inside Lay I |
| Pk1 5%-88% | Lay I 21-40w | semantic | Nongda 6 | peak phase 1 |
| Pk2 88%-83% | Lay II 41-60w | semantic | Nongda 6 | post-peak phase 2 |
| Post-Peak <85% | unmapped | ambiguous | Beinong 2 | post-peak may span Lay II and Lay III |
| Post-Peak <=85% | unmapped | ambiguous | Nongda 3 | post-peak may span Lay II and Lay III |
| Pre-Lay (17w-5%) | Pre-Lay 18-20w | boundary | Hy-Line Brown; Hy-Line Pink; Hy-Line W-36 | — |
| Pre-Lay 15w-5% | Pre-Lay 18-20w | boundary | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong 1 v3.0 | — |
| Pre-Lay 17w-2% | Pre-Lay 18-20w | boundary | Hisex Brown | — |
| Pre-Lay 17w-5% | Pre-Lay 18-20w | boundary | Lohmann Pink; Nongda 3 | — |
| Pre-Lay 17w-peak | Pre-Lay 18-20w | composite | Beinong 2 | spans pre-lay to peak |
| Pre-Lay 18-20w | Pre-Lay 18-20w | exact | ISA Brown | — |
| Pre-Lay 18w-5% | Pre-Lay 18-20w | boundary | Lohmann Grey | — |
| Rearing | unmapped | composite | — | vitamin table: rearing covers 0-18w |
| Rearing 0-18w | unmapped | composite | — | covers Starter-Grower-Developer-PreLay |
| S 0-3w | Starter 0-6w | within | Nongda 6 | 3-phase Chinese scheme; S = starter |
| Starter 0-2w | Starter 0-6w | within | Jingfen 6; Jinghong 1 v3.0 | — |
| Starter 0-3w | Starter 0-6w | within | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939 | — |
| Starter 0-4w | Starter 0-6w | within | Lohmann Pink | — |
| Starter 0-5w | Starter 0-6w | within | Beinong 1; Beinong 2; Hisex Brown; Nongda 3 | — |
| Starter 0-6w | Starter 0-6w | exact | ISA Brown | — |
| Starter 1 (0-3w) | Starter 0-6w | within | Hy-Line Brown; Hy-Line Pink; Hy-Line W-36 | starter split into 1/2 |
| Starter 1-3w | Starter 0-6w | within | Lohmann Grey | — |
| Starter 2 (4-6w) | Starter 0-6w | within | Hy-Line Brown; Hy-Line Pink; Hy-Line W-36 | starter split into 1/2 |
| Starter-Grower | unmapped | composite | — | covers Starter and Grower |

## Table S3. Per-breed provenance summary

Full machine-readable table with URLs, versions, access dates, and licenses: `corpus/provenance.csv` (fields are recorded where available; unresolved entries carry a status flag). `needs_primary_source` marks Chinese domestic rows that were compiled through jbzyw.com; `needs_version_and_url` marks breeder guides whose exact version still has to be recorded; `needs_license_check` marks public feed tables whose redistribution terms are unresolved.

| Dataset | Scope | Source label | Source type | Status |
|---|---|---|---|---|
| feed_ingredient_bank.csv | all entries | INRAE-CIRAD-AFZ feed tables (feedtables.com) | public_feed_table | needs_license_check |
| feed_ingredient_amino_acids.csv | all entries | INRAE-CIRAD-AFZ feed tables (feedtables.com) | public_feed_table | needs_license_check |
| feed_ingredient_digestibility.csv | all entries | INRAE-CIRAD-AFZ feed tables (feedtables.com) | public_feed_table | needs_license_check |
| definitions.csv | all entries | other-Sourced | unspecified | needs_author_input |
| nutrient_requirements.csv | Beinong 1 | Beinong 1 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Beinong 2 | Beinong 2 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Dawu Fen 1 | Dawu Fen 1 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Dawu He | Dawu He Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Dawu Jinfeng | Dawu Jinfeng Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Hisex Brown | Hisex Brown Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Hy-Line Brown | Hy-Line Brown Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Hy-Line Pink | Hy-Line Pink Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Hy-Line W-36 | Hy-Line W-36 Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | ISA Brown | other-Sourced | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Jingbai 939 | Jingbai 939 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Jingfen 6 | Jingfen 6 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Jinghong 1 v3.0 | Jinghong 1 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Lohmann Grey | Lohmann Grey Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Lohmann Pink | Lohmann Pink Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_requirements.csv | Nongda 3 | Nongda 3 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_requirements.csv | Nongda 6 | Nongda 6 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Beinong 2 | Beinong 2 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Dawu Jinfeng | Dawu Jinfeng Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Hy-Line Brown | Hy-Line Brown Official Manual (vitamin reference) | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | Hy-Line Pink | Hy-Line Pink Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | Hy-Line W-36 | Hy-Line W-36 Official Manual (vitamin reference) | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | ISA Brown | ISA Brown Official Manual (vitamin reference) | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | Jingbai 939 | Jingbai 939 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Jingfen 6 | Jingfen 6 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Jinghong 1 v3.0 | Jinghong 1 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Lohmann Grey | Lohmann Grey Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | Lohmann Pink | Lohmann Pink Official Manual | breeder_management_guide | needs_version_and_url |
| nutrient_vitamin_mineral.csv | Nongda 3 | Nongda 3 Official Manual | aggregator_mirror | needs_primary_source |
| nutrient_vitamin_mineral.csv | Nongda 6 | Nongda 6 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Beinong 1 | Beinong 1 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Beinong 2 | Beinong 2 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Dawu Fen 1 | Dawu Fen 1 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Dawu He | Dawu He Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Dawu Jinfeng | Dawu Jinfeng Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Hy-Line Brown | Hy-Line Brown Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | Hy-Line Pink | Hy-Line Pink Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | Hy-Line W-36 | Hy-Line W-36 Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | ISA Brown | ISA Brown Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | Jingbai 939 | Jingbai 939 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Jingfen 6 | Jingfen 6 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Jinghong 1 v3.0 | Jinghong 1 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Lohmann Grey | Lohmann Grey Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | Lohmann Pink | Lohmann Pink Official Manual | breeder_management_guide | needs_version_and_url |
| performance_management.csv | Nongda 3 | Nongda 3 Official Manual | aggregator_mirror | needs_primary_source |
| performance_management.csv | Nongda 6 | Nongda 6 Official Manual | aggregator_mirror | needs_primary_source |

---

## S2. System Prompt Templates

### S2.1 ReAct Agent System Prompt

The ReAct agent uses a species-aware system prompt that dynamically inserts breed-specific metadata:

```
You are NutriAgent, a domain-specific AI assistant for {species_name} nutrition. You have
access to expert-designed tools for accurate nutritional information.

Current species: {species_name}
Breeds available: {breeds}
Production phases: {phases}
Key metrics: {metrics}

CRITICAL RULES:
1. ALWAYS use the appropriate tool to retrieve nutritional data rather
   than relying on your own knowledge
2. For numeric queries, retrieve precise values from the tools
3. Provide specific numbers with appropriate units
4. If you need multiple pieces of information, use tools one at a time
5. Keep responses concise and under {max_tokens} tokens when possible
6. Synthesize tool outputs into clear, actionable answers

Available tools:
- feed_ingredient_bank: Get nutritional composition data for feed
  ingredients (CP, ME, amino acids, minerals, digestibility)
- performance_management: {perf_description}
- nutrient_requirements: {nr_description}
- definitions: Get definitions of poultry nutrition terms and concepts

Answer the user's poultry nutrition question using these tools as needed.
```

### S2.2 Router Agent Prompt

```
You are a query router for NutriAgent, a poultry nutrition AI system.
Classify the user's query to determine which specialist agent(s) should
handle it.

Available specialist agents:

1. feed: Questions about feed ingredient nutritional composition,
   digestibility, and raw material properties.
2. nutrition: Questions about nutrient requirements, diet specifications,
   vitamin/mineral levels, and feeding phases.
3. performance: Questions about production performance metrics: body
   weight, ADG, FCR, egg production, egg quality.
4. definitions: Questions about poultry nutrition terminology and concept
   definitions.

Query: {query}

Output ONLY a JSON object with these fields:
- "intent": one of "feed", "nutrition", "performance", "definitions",
  or "multi"
- "target_agents": list of agent names to invoke
- "requires_cross_validation": true only if multiple agents are needed
  AND their answers may conflict
```

### S2.3 Synthesis Agent Prompt

```
You are a senior poultry nutrition expert reviewing answers from multiple
specialist agents. Your job is to cross-validate, resolve conflicts, and
produce a single coherent final answer.

Original question: {query}

Specialist responses:
{specialist_outputs}

{rag_context}

{cross_validate_warnings}

Instructions:
1. Synthesize the information from all specialists into one coherent answer.
2. If there are contradictions between specialists, note the discrepancy
   and explain which value is best supported.
3. If supplementary information is provided, incorporate it where relevant.
4. The final answer should be comprehensive, accurate, and directly address
   the user's question.
5. Cite the source of each key number (e.g., "[from Performance tool]"
   or "[from Nutrient tool]").
6. Keep the same concise style as the original responses.

FINAL ANSWER:
```

### S2.4 EvaluatorLLM Prompt (Comparative, n > 1)

> **Rubric version note.** This is the submitted evaluator rubric (v1), retained unchanged because it is the prompt used for the automated scores. Its correctness anchor includes a citation clause. The primary expert used rubric v2 (S12), which removes the citation clause from correctness and scores provenance as a separate column. Automated and expert scores are therefore not generated under identical rubrics; the manuscript reports them as separate instruments.

```
You are an expert evaluator of poultry nutrition responses. Evaluate {n}
responses to the following question using the detailed rubrics below.

QUESTION: {query}

RESPONSES:
{responses}

Rate each response on three metrics using a 5-point scale with the
following rubrics:

**Correctness** — Factual accuracy and relevance to the query.
  5 = All facts accurate, directly answers the query, cites/grounds
      authoritative data correctly
  4 = Mostly accurate with minor imprecision or slightly incomplete
  3 = Partially correct but has noticeable factual errors or missing
      key information
  2 = Several factual errors or largely off-topic
  1 = Completely incorrect, hallucinated information, or irrelevant

**Precision** — Numerical accuracy. Set to null ONLY for definition/
  terminology queries.
  5 = Exact point estimate matching reference value; or narrow,
      tightly-grounded range
  4 = Point estimate close to reference; or moderately precise range
  3 = Estimate directionally correct but noticeably off; or overly
      wide range
  2 = Vague or significantly inaccurate numeric answer
  1 = No numeric answer when quantitative response is expected, or
      completely wrong value

**Scientific Depth** — Depth of domain knowledge, context, and
  explanatory quality.
  5 = Demonstrates thorough understanding, provides mechanistic
      explanation and practical context
  4 = Good domain knowledge with relevant context, minor depth missing
  3 = Adequate but surface-level; lacks mechanism or broader context
  2 = Superficial; minimal domain-specific insight beyond generic knowledge
  1 = No scientific content or factually misleading explanation

Respond with ONLY a JSON object containing a "scores" array.

IMPORTANT:
- The "scores" array must contain ALL {n} responses (R1 to R{n}).
- If precision is not applicable (definition/terminology only), set it
  to null.
- Compare each response against the others (best=5, slightly worse=4, etc.).
- No text before or after the JSON object.
```

### S2.5 EvaluatorLLM Prompt (Absolute, n = 1)

Used in ablation experiments where each variant is scored independently. It uses rubric v1
(the S2.4 anchors, including the citation clause); the expert rubric v2 is in S12.

```
[Same rubrics as S2.4]

IMPORTANT: Apply the rubric strictly. A score of 5 requires ALL criteria
to be fully met. Most well-formed responses should score 3-4; reserve 5
for truly exceptional answers and 1-2 for clearly deficient ones.

Score based on the rubric above, not relative to other responses.
```

---

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

The full 195-query candidate pool is in `queries/layer/evaluation_queries_pool195.json`. The curated set is fixed before Rev.1 scoring and is not an independent held-out benchmark.

---

## S4. Comparison with Existing Agricultural Decision-Support Systems

**Table S4.** Capability comparison with representative domain-specific agent systems. ✓ = reported in the cited description; ✗ = not reported (not necessarily absent).

| System | Domain | Multi-agent | Structured tool access | External corpus | Faithfulness metric | Bilingual | Real-time adaptability |
|--------|--------|:-----------:|:----------------------:|:---------------:|:-------------------:|:---------:|:----------------------:|
| ChemCrow (Bran et al., 2024) | Chemistry | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Biomni (Huang et al., 2025a) | Biomedicine | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| BioMaster (Su et al., 2025) | Bioinformatics | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| CottonBot (Kandamali et al., 2025) | Cotton farming | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
| Smart-greenhouse agents (Pardo-Pina et al., 2026) | Greenhouse management | ✓ | ✓ | ✓ | ✗ | ✗ | ✓ |
| NutriCHAT (Mandiga et al., 2026) | Poultry nutrition (broiler) | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **NutriAgent (this work)** | **Poultry nutrition (layer)** | **✓** | **✓** | **✓** | **✓** | **✓** | **✗** |

---

---

## S5. Per-query EvaluatorLLM results (Rev.1 NutriAgent)

Per-query MiMo-V2.5-Pro absolute scores for NutriAgent on the frozen Rev.1 model set (single run). The primary expert scored all 378 responses (Table 9); this table is the automated-score record and is not the primary expert table.

**Table S5.** Per-query automated scores for NutriAgent (DeepSeek-V4-Flash, multi-agent, validation on). C = correctness, P = precision, D = scientific depth; — = not scored. SelfCheckGPT-NLI and tolerance are reported in aggregate elsewhere, not per query here.

| ID | Category | Type | C | P | D |
|---|---|---|---:|---:|---:|
| C-DEF-001 | Definitions | definition | 5 | — | 5 |
| C-DEF-002 | Definitions | definition | 5 | — | 5 |
| C-DEF-003 | Definitions | definition | 5 | — | 5 |
| C-DEF-004 | Definitions | single-value | 5 | 5 | 4 |
| C-DEF-005 | Definitions | definition | 5 | — | 5 |
| C-DEF-006 | Definitions | open-ended | 5 | — | 5 |
| C-EC-001 | Edge Cases | single-value | 5 | — | 4 |
| C-EC-002 | Edge Cases | single-value | 5 | 5 | 4 |
| C-EC-003 | Edge Cases | single-value | 5 | 5 | 4 |
| C-EC-004 | Edge Cases | single-value | 5 | 5 | 4 |
| C-EC-005 | Edge Cases | comparison | 5 | 5 | 4 |
| C-FIB-001 | Feed Ingredient Bank | single-value | 5 | 5 | 4 |
| C-FIB-002 | Feed Ingredient Bank | single-value | 5 | 5 | 5 |
| C-FIB-003 | Feed Ingredient Bank | single-value | 5 | 5 | 5 |
| C-FIB-004 | Feed Ingredient Bank | comparison | 5 | 5 | 4 |
| C-FIB-005 | Feed Ingredient Bank | comparison | 5 | 5 | 4 |
| C-FIB-006 | Feed Ingredient Bank | open-ended | 5 | 5 | 4 |
| C-FIB-007 | Feed Ingredient Bank | open-ended | 4 | 4 | 5 |
| C-FIB-008 | Feed Ingredient Bank | definition | 5 | — | 5 |
| C-FIB-009 | Feed Ingredient Bank | single-value | 5 | 5 | 4 |
| C-FIB-010 | Feed Ingredient Bank | comparison | 4 | 4 | 5 |
| C-NR-001 | Nutrient Requirements | single-value | 5 | 5 | 5 |
| C-NR-002 | Nutrient Requirements | single-value | 4 | 5 | 3 |
| C-NR-003 | Nutrient Requirements | single-value | 5 | 5 | 4 |
| C-NR-004 | Nutrient Requirements | comparison | 5 | 5 | 5 |
| C-NR-005 | Nutrient Requirements | comparison | 5 | 5 | 4 |
| C-NR-006 | Nutrient Requirements | open-ended | 5 | 5 | 5 |
| C-NR-007 | Nutrient Requirements | single-value | 5 | 5 | 4 |
| C-NR-008 | Nutrient Requirements | single-value | 3 | 3 | 3 |
| C-NR-009 | Nutrient Requirements | definition | 4 | — | 4 |
| C-NR-010 | Nutrient Requirements | single-value | 5 | 4 | 5 |
| C-NR-011 | Nutrient Requirements | comparison | 5 | 5 | 5 |
| C-NR-012 | Nutrient Requirements | single-value | 5 | 5 | 5 |
| C-PM-001 | Performance Management | single-value | 5 | 5 | 5 |
| C-PM-002 | Performance Management | single-value | 5 | 5 | 5 |
| C-PM-003 | Performance Management | comparison | 5 | 5 | 5 |
| C-PM-004 | Performance Management | comparison | 5 | 5 | 5 |
| C-PM-005 | Performance Management | open-ended | 4 | 1 | 2 |
| C-PM-006 | Performance Management | open-ended | 5 | 5 | 4 |
| C-PM-007 | Performance Management | single-value | 5 | 5 | 3 |
| C-PM-008 | Performance Management | definition | 5 | — | 5 |
| C-PM-009 | Performance Management | single-value | 5 | 5 | 4 |
| C-PM-010 | Performance Management | comparison | 5 | 5 | 4 |
| C-PM-011 | Performance Management | single-value | 5 | 5 | 4 |
| C-XD-001 | Cross-Domain | multi-hop | 3 | 3 | 3 |
| C-XD-002 | Cross-Domain | multi-hop | 5 | 5 | 5 |
| C-XD-003 | Cross-Domain | constraint | 5 | 5 | 5 |
| C-XD-004 | Cross-Domain | constraint | 3 | 5 | 4 |
| C-XD-005 | Cross-Domain | counterfactual | 5 | 5 | 5 |
| C-XD-006 | Cross-Domain | counterfactual | 4 | 5 | 4 |
| C-XD-007 | Cross-Domain | multi-hop | 5 | 5 | 4 |
| C-XD-008 | Cross-Domain | open-ended | 3 | 3 | 3 |
| C-XD-009 | Cross-Domain | multi-hop | 5 | 5 | 3 |
| C-XD-010 | Cross-Domain | constraint | 5 | 5 | 4 |

## S6. SelfCheckGPT-NLI N sensitivity

Twenty queries (NutriAgent, frozen Rev.1 model set), one sample-generation pass per
query, scores sliced at N = 5/10/20:

| N | Mean | SD | n |
|---|---:|---:|---:|
| 5 | 0.163 | 0.214 | 20 |
| 10 | 0.153 | 0.209 | 20 |
| 20 | 0.149 | 0.212 | 20 |

Pearson correlations: N=5 vs 10 = 0.977; 5 vs 20 = 0.963; 10 vs 20 = 0.995.
The rank ordering is stable, so N=5 is adequate for relative comparisons; the
absolute mean decreases slightly with N (0.163 → 0.149), so absolute scores are
N-dependent. This is a 20-query, single-system sensitivity check, not a
calibration of the metric against human labels.

## S7. Claim-aware faithfulness audit

Rule-based audit of the E1 multi-agent responses (validation on/off). A claim is
`direct` when its entity and attribute appear in the query's tool observations and a value
is within 5%; `attribute` drops the entity requirement; `any_number` is the old permissive
criterion.

| Variant | Claims | Direct | Attribute | Any number | Unsupported |
|---|---:|---:|---:|---:|---:|
| validation on | 101 | 10.9% | 9.9% | 13.9% | 65.3% |
| validation off | 96 | 16.7% | 6.2% | 13.5% | 63.5% |

Caveat: the extractor finds about two claims per response and does not fully parse
observation units, so these are strict lower bounds under this parser, not a human-validated
rate. The submitted 0.444 any-number score is not claim-level support.

### S7b. Consistency-checker rule coverage (E3)

A 42-pair synthetic test set was constructed to cover the rebuilt entity/attribute/unit/basis
checks: 16 conflict pairs, 12 consistent or unit-converted pairs, and 14 distractors (e.g.,
crude protein in an ingredient vs a dietary requirement; cage density vs calcium). The
validator is a rule-coverage test, not a field precision estimate.

| Category | n | Correct | Accuracy |
|---|---:|---:|---:|
| Conflict | 16 | 16 | 100% |
| Consistent / unit-converted | 12 | 12 | 100% |
| Distractor | 14 | 14 | 100% |
| **Total** | **42** | **42** | **100%** |

Precision, recall, and F1 are 1.00 on this set. The test is deliberately balanced and
synthetic; it shows that the implemented rules handle the intended cases and the legacy
false-positive patterns, not that the checker is accurate on unrestricted expert text.
Implementation and cases: `docs/paper/audit/e3_validator_eval.{json,md}` and
`tests/test_validation.py`.

## S8. RAG retrieval depth

PoultryDB hit@k on 44 queries with annotated target documents (one acceptable document per
query, not an exhaustive relevance judgment):

| Metric | Value |
|---|---:|
| hit@1 | 27.3% |
| hit@3 | 54.5% |
| hit@5 | 63.6% |
| MRR | 0.411 |

By type: definitions 71.4%/100% (hit@1/@5); single-value 20%/53.3%; comparison 10%/50%;
multi-hop 0%/66.7%; constraint 0%/0% (n=2); counterfactual 100%/100% (n=2). The reported runs use k=1; k=5 would
improve recall but was not used.

## S9. Model versions and run manifest

The frozen model set is Table 3 in the main text and `config/models.lock.yaml`; the per-run manifest (hardware, package versions, file hashes, model IDs) is written by `scripts/paper/run_manifest.py` and deposited with the code.

## S10. Error coding (single-coder, descriptive)

This section replaces the earlier empty placeholder. It is a **single-coder descriptive audit**, not the planned two-coder E14 with Cohen's kappa. The numeric part uses the tolerance analysis; the non-numeric part uses the primary expert's notes for all NutriAgent responses scored correctness ≤3.

**Numeric errors (E14).** Of 36 queries with ground truth, 32/36 (88.9%) are within ±5% and 30/36 (83.3%) within ±2%. The four failures are:

| Query | Expected | Nearest parsed | Issue |
|---|---:|---:|---|
| C-FIB-005 | 11.6 | 8.5 | wrong comparison value |
| C-FIB-010 | 2260 | 48 | unit/scale mismatch |
| C-XD-001 | 0.27 | 0.25 | borderline multi-hop arithmetic |
| C-XD-006 | 1.45 (decrease) | 5.125 | reported contribution instead of change |

**Non-numeric error categories (NutriAgent, C ≤3; n = 9).**

| Category | n | Query IDs | Description |
|---|---:|---|---|
| Value/source substitution | 4 | C-EC-002, C-FIB-006, C-NR-010, C-NR-011 | familiar/approximate value substituted for the tool/reference value; out-of-corpus breed treated as a related breed |
| Unit/scale/source mismatch | 1 | C-FIB-010 | ME reported in MJ/kg rather than the bank's kcal/kg, with an approximate source label |
| Arithmetic | 1 | C-NR-008 | 0.15 + 0.15 computed as 0.375% |
| Retrieval/entity mismatch | 1 | C-FIB-007 | retrieved maize gluten feed instead of maize; caveat stated |
| Refusal/incomplete synthesis | 2 | C-PM-005, C-XD-008 | refused a multi-point body-weight question despite available data; omitted balancing steps |

The nine cases are 17% of the 54 NutriAgent responses. Categories are not mutually exclusive at the level of a full taxonomy, and the coding is single-coder; we do not report a kappa. The descriptive counts address the reviewer's request for error causes without overclaiming a validated taxonomy.

## S11. Additional factorial contrasts

**Table S11a.** E1 architecture factorial (n = 54). Same backbone and output budget.

| Variant | Correctness | Precision | Depth |
|---|---:|---:|---:|
| Standalone LLM | 4.63±0.78 | 4.44±0.84 | 4.15±0.81 |
| Single ReAct + tools | 4.31±1.36 | 4.41±1.37 | 3.81±1.30 |
| Single ReAct + tools + RAG | 4.54±1.14 | 4.51±1.20 | 4.13±1.17 |
| Single ReAct + tools + RAG + synthesis | 4.48±1.13 | 4.26±1.41 | 3.94±1.27 |
| Multi-Agent (validation off) | 4.74±0.65 | 4.64±0.86 | 4.35±0.73 |
| Multi-Agent (validation on) | 4.83±0.42 | 4.72±0.77 | 4.17±0.77 |

**Table S11b.** E2 synthesis factorial (n = 54). Inputs and output budget held fixed.

| Variant | Correctness | Precision | Depth |
|---|---:|---:|---:|
| Concatenation | 4.28±1.32 | 4.41±1.20 | 3.69±1.21 |
| Validation + concatenation | 4.11±1.30 | 4.14±1.37 | 3.74±1.18 |
| Synthesis (shuffled warnings) | 4.87±0.44 | 4.84±0.64 | 4.37±0.78 |
| Synthesis (validation off) | 4.91±0.35 | 4.78±0.84 | 4.35±0.68 |
| Synthesis (correct warnings) | 4.91±0.29 | 4.83±0.44 | 4.35±0.59 |
| Query-only synthesis | 4.85±0.49 | 4.83±0.49 | 4.44±0.66 |

Per-query scores: `docs/paper/audit/e1_rescored.json` and `e2_rescored.json` (E2 concatenation/shuffled/correct are in the E2 report cache). The E2 result does not support an integration or validation benefit: validation-off and correct warnings are identical, shuffled is 0.04 lower, and query-only synthesis matches full synthesis.

## S12. Scoring rubric v2

Correctness no longer requires a citation; provenance is scored as a separate column.

| Score | Correctness | Precision (numeric; N/A for definitions) | Scientific depth |
|---|---|---|---|
| 5 | All facts accurate | Exact point estimate | Thorough mechanistic understanding with practical context |
| 4 | Mostly accurate, minor imprecision | Close estimate | Good domain knowledge |
| 3 | Partially correct, noticeable errors | Directionally correct but noticeably off | Adequate but surface-level |
| 2 | Several factual errors | Vague or significantly inaccurate | Superficial |
| 1 | Completely incorrect or hallucinated | No numeric answer when one is expected | No scientific content |

**Provenance (separate column, 0–2).** 0 = no source attribution; 1 = some key numbers
cite a tool/source; 2 = every key number is attributed to a named tool or source. It is not
folded into correctness; the submitted rubric's "5 = accurate with direct citation"
conflated the two constructs.

## S13. Prompt/control matrix

| Component | Standalone LLM | Single ReAct | Multi-agent | E2 synthesis conditions |
|---|---|---|---|---|
| System prompt | generic QA | generic ReAct + tool descriptions | router + four specialist prompts + synthesis | specialist prompts fixed; synthesis prompt varies by condition |
| Tools | none | all four | specialist-specific subset | specialist outputs fixed; no new tools |
| RAG | off | optional | optional (on in the reported run) | held at the reported setting |
| Output budget | 512 tokens | 512 | 512 per call | 512 per call |
| Validation | none | none | off/on | off / shuffled / correct / query-only |

Prompt text is in Supplementary S2; the matrix documents which components are shared and
which are intentionally varied. The standalone condition is not given the specialist
prompts, so prompt content is not identical across conditions by design.

## S14. Attribution of adopted vs new components

| Component | Source / precedent | Use in NutriAgent | New in this work? |
|---|---|---|---|
| ReAct tool loop | Yao et al. (2023); NutriCHAT (Mandiga et al., 2026) | specialist and router reasoning | No (adopted) |
| Four domain tools | NutriCHAT (feed, nutrient, performance, definitions) | same four domains, layer-hen corpus | No (adopted; corpus extended) |
| Retrieval-augmented context | Lewis et al. (2020); NutriCHAT | supplementary PoultryDB context | No (adopted) |
| Specialist routing | multi-agent/role decomposition literature | router activates a subset of four specialists | Yes (implementation + factorial test) |
| Entity/attribute/unit-aware consistency checker | rule-based validation literature | cross-specialist contradiction warnings | Yes |
| Bilingual layer-hen corpus (17 breeds, Chinese strains) | public breeder guides, jbzyw.com, feed tables | data layer | Yes (assembly + provenance) |
| E1/E2 factorial controls | ablation methodology | six-condition architecture and synthesis grids | Yes |
| Blinded expert re-score + provenance column | evaluation methodology | 378-response primary sheet, 120-response intra-rater repeat, 120-response independent check | Yes |

## S15. Expert-score reliability and primary means

**Table S15.** Primary-expert means (378 responses; 54 queries). C = correctness, P = precision (numeric queries, n=38), D = scientific depth; Overall = (mean C + mean P + mean D)/3. Because P is missing for 16 queries, this Overall is not the paired per-response overall in Table 10.

| Method | C | P | D | Overall | n (C/P/D) |
|---|---:|---:|---:|---:|---:|
| NutriAgent | 4.46 | 4.47 | 4.07 | 4.34 | 54/38/54 |
| DeepSeek-V4-Pro | 4.26 | 3.97 | 3.93 | 4.05 | 54/38/54 |
| DeepSeek-V4-Flash | 4.06 | 3.74 | 4.33 | 4.04 | 54/38/54 |
| Qwen3.8-Flash | 3.96 | 3.79 | 4.28 | 4.01 | 54/38/54 |
| GLM-4.5-Air | 3.74 | 3.63 | 3.28 | 3.55 | 54/38/54 |
| Qwen3-8B | 3.13 | 2.87 | 3.13 | 3.04 | 54/38/54 |
| MiniMax-M2.5 | 2.80 | 2.53 | 2.56 | 2.63 | 54/38/54 |

## S16. Reliability tables

**Table S16.** Reliability on the 120-response subset. ICC(2,1), quadratic weighted κ, Spearman ρ, and Bland–Altman mean difference (95% limits). The independent rater vs primary is the inter-rater estimate; the primary repeat sheet is an intra-rater (same-expert repeat/copy) check and is not used as an independent rater.

| Pair / metric | n | ICC(2,1) | weighted κ | Spearman ρ | BA mean (95% limits) |
|---|---:|---:|---:|---:|---|
| Independent rater vs primary — correctness | 120 | 0.847 | 0.846 | 0.862 | −0.27 (−1.45, +0.92) |
| Independent rater vs primary — precision | 80 | 0.876 | 0.874 | 0.913 | −0.11 (−1.36, +1.14) |
| Independent rater vs primary — depth | 120 | 0.760 | 0.758 | 0.725 | +0.21 (−1.06, +1.48) |
| Primary repeat sheet (intra-rater) — correctness | 120 | 0.995 | 0.995 | 0.994 | −0.02 (−0.27, +0.23) |
| Primary repeat sheet (intra-rater) — precision | 80 | 0.996 | 0.996 | 0.996 | −0.01 (−0.23, +0.21) |
| Primary repeat sheet (intra-rater) — depth | 120 | 0.932 | 0.931 | 0.914 | +0.08 (−0.57, +0.73) |

The primary repeat sheet is 98% identical to the primary on correctness and has a note-text median similarity of 0.70 (38/109 ≥0.80); it is a same-expert repeat/copy pass, so the high ICC reflects intra-rater consistency rather than independent agreement. The independent rater's 120-response subset does not reproduce the full top rank (overall: DeepSeek-V4-Flash 4.28, DeepSeek-V4-Pro 4.14, NutriAgent 4.12); it is a reliability check, not a ranking replication. Raw normalized scores are in `expert_scores_primary.csv`, `expert_scores_second.csv`, and `expert_scores_third.csv`.

**Sensitivity to query clarifications.** Excluding C-XD-005, C-XD-006, and one of the near-duplicate C-PM-006/C-XD-007 pair leaves 51 queries. NutriAgent's correctness is 4.45 and DeepSeek-V4-Pro's is 4.22 (paired difference +0.23; Wilcoxon p = 0.115); MiniMax-M2.5 remains lowest (correctness 2.90; overall 2.76) and NutriAgent remains highest. The main ranking and the non-significant correctness advantage over DeepSeek-V4-Pro are unchanged.

## S17. Full claim-calibration matrix

**Table S17.** Replication status of the submitted component and evaluation claims under the Rev.1 model set. "Not supported" means the Rev.1 evidence does not reproduce the direction or magnitude; "withdrawn" means the condition did not execute as described. The Rev.1 expert main comparison is reported in Table 9; this table summarizes the factorial, ablation, retrieval, and audit evidence.

| Submitted claim | Rev.1 evidence | Status |
|---|---|---|
| NutriAgent 4.42 vs 3.80 (+0.62), strongest baseline DeepSeek-V4-Flash | Rev.1 expert (Table 9): NutriAgent 4.34; DeepSeek-V4-Pro 4.05 (strongest baseline); DeepSeek-V4-Flash 4.04; Qwen3.8-Flash 4.01; GLM 3.55; Qwen3-8B 3.04; MiniMax 2.63. ΔC vs DeepSeek-V4-Pro +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146). | **Not replicated: gap 0.28; correctness advantage not significant** |
| Synthesis / cross-validation is the dominant driver (+24.2% C, −29.7% inconsistency) | E2: validation-off 4.91 = correct warnings 4.91; shuffled 4.87; query-only 4.85; concatenation 4.28. The extra call, not validation or specialist content, is associated with the increase. | **Not supported** |
| Multi-agent improves over single agent by +5.3% C / −48.3% inconsistency | The no-ReAct row was a duplicate full-pipeline run and is withdrawn. E1: tools-only 4.31 < standalone 4.63; RAG 4.54; multi-agent 4.74/4.83; validation adds no reliable gain. | **Withdrawn** |
| Each specialist contributes (Performance −0.20, Nutrition −0.09, Feed −0.04) | D2 Rev.1 same-pass (n=54): Full 4.44; w/o Feed 4.67 (+0.22); w/o Definitions 4.57 (+0.13); w/o Performance 4.39 (−0.06); w/o Nutrition 4.37 (−0.07). No removal hurts. D2 is architectural removal; the shared corpus remains. | **Not replicated; no positive contribution** |
| Feed data are necessary for judged correctness | E7 hard removal (20 Feed/Cross queries): full 4.40 vs hard removal 4.70 correctness (+0.30), precision +0.07, depth 0.0; single run. | **Not supported** |
| LLM router has the highest correctness (4.80 vs 4.69/4.61; keyword at 97.7%) | D3 Rev.1 (n=54): LLM 4.63 > Broadcast 4.59 > Keyword 4.48; the submitted ordering is not replicated. | **Not replicated; LLM highest** |
| Routing strategy has no correctness effect (spread ≤0.05) | D3 Rev.1 (n=54): LLM 4.63 > Broadcast 4.59 (−0.04) > Keyword 4.48 (−0.15). | **Not supported; LLM router highest** |
| RAG improves correctness (+0.08) and precision (+0.10) | D4 complete case (n=54): +RAG 4.52 vs no-RAG 4.52; C 0.00, P +0.04, D −0.22 (no-RAG D n=46). Proxy ITT (16 E6 misses = failure 1): 3.50 vs 4.52; Δ −1.02 (95% CI −1.52 to −0.52; p < 0.001); S19. | **Not replicated; complete-case null; proxy ITT negative** |
| DeepSeek-V4-Flash is the best backbone (4.85 vs 4.74/4.69/4.44/4.11) | D6 Rev.1 (n=54): DS-V4-Pro 4.67 > DS-V4-Flash 4.61 > Qwen3.8-27B 4.50 > Qwen3.8-Flash 4.43 > Qwen3-8B 3.81. Top-two gap 0.06; DS-V4-Flash has higher depth (4.04 vs 3.87). | **Not replicated; Qwen3-8B lowest holds** |
| Hallucination reduced by 70%; 56% of numbers are parametric | SelfCheckGPT-NLI is a cross-sample inconsistency score, not a factual-error rate. Claim-aware audit: direct entity+attribute support 10.9–16.7% (parser lower bound), not 0.444 provenance. | **Reframed** |
| Evaluator agreement ρ = 0.83 / 0.67 / 0.37 | Recomputed against the Rev.1 primary expert: ρ = 0.55 (C), 0.71 (P), 0.34 (D); the judge is more lenient, and the earlier ρ = 0.038 for precision is withdrawn. | **Corrected** |
| Single-run scores are reproducible at temperature 0.0 | E9: 10 queries × 3 runs, mean pairwise similarity 0.371, exact match 0/10. | **Not supported** |
| Chinese queries have lower correctness | E11 auto scores: Chinese 4.92 vs English 4.69 (n=12/42; CIs overlap); the cross-lingual issue is inconsistency, not correctness. | **Not supported** |
| k = 1 retrieval is sufficient | E6: hit@1 27.3%, hit@3 54.5%, hit@5 63.6%, MRR 0.411; k=1 misses ~73% of annotated targets. | **Not supported** |

The replication matrix is the main message of the revision: the submitted paper over-attributed quality gains to individual components. Under the Rev.1 controls, the robust finding is narrower: the full synthesis pass is associated with higher judged scores, tool access alone is insufficient, and validation, routing, RAG-within-multi-agent, and most specialist removals are null. The main comparison is now reported with intervals (Tables 9–10); the remaining open items are the human-labeled faithfulness subset (E4) and the full non-numeric error coding (E14), not the expert main comparison.

## S18. Model-set transition

The submitted model set included endpoints that are no longer available. Rev.1 uses one frozen current set; absolute scores are not comparable across versions.

| Role | Submitted | Rev.1 | Availability note |
|---|---|---|---|
| NutriAgent backbone | DeepSeek-V4-Flash | DeepSeek-V4-Flash | current endpoint |
| Strong baseline | DeepSeek-V4-Pro | DeepSeek-V4-Pro | current endpoint/version |
| Strong baseline | DeepSeek-V4-Flash | DeepSeek-V4-Flash | current endpoint/version |
| Qwen baseline | Qwen3.5-Flash | Qwen3.8-Flash | Qwen3.5 endpoint retired |
| GLM baseline | GLM-4.5-Air | GLM-4.5-Air | current endpoint |
| Small baseline | Qwen3-8B | Qwen3-8B | current endpoint |
| Small baseline | MiniMax-M2.5 | MiniMax-M2.5 | current provider |

| Method | Submitted overall | Rev.1 overall | Direction |
|---|---:|---:|---|
| NutriAgent | 4.42 | 4.34 | −0.08 |
| DeepSeek-V4-Pro | 3.77 | 4.05 | +0.28 |
| DeepSeek-V4-Flash | 3.80 | 4.04 | +0.24 |
| GLM-4.5-Air | 3.59 | 3.55 | −0.04 |
| Qwen (3.5 → 3.8) | 3.44 | 4.01 | +0.57 |
| Qwen3-8B | 3.11 | 3.04 | −0.07 |
| MiniMax-M2.5 | 3.71 | 2.63 | −1.08 |

The strongest submitted baseline improved from 3.80 to 4.05; the NutriAgent point estimate moved by −0.08. Thus much of the smaller margin reflects stronger current baselines, not only a change in NutriAgent. The submitted and Rev.1 scores also use different expert/rubric passes, so the table is descriptive and is not used for causal attribution.

## S19. D4 RAG ITT sensitivity (proxy failures)

The Rev.1 D4 rescore includes all 54 correctness scores but does not preserve a retrieval-failure flag; the four submitted-run exclusions cannot be reconstructed exactly. As a conservative, clearly labeled proxy, the 16 E6 hit@5 misses are scored as system failures (1; sensitivity 0) in the +RAG condition. This is not an exact reconstruction of the submitted four-query exclusion and is not used as the primary D4 estimate.

| Metric | Analysis | n | +RAG | no-RAG | Δ | 95% CI | Wilcoxon p |
|---|---|---:|---:|---:|---:|---|---:|
| Correctness | ITT, failure = 1 | 54 | 3.500 | 4.519 | −1.019 | −1.519 to −0.519 | 0.0008 |
| Correctness | ITT, failure = 0 | 54 | 3.204 | 4.519 | −1.315 | −1.944 to −0.704 | 0.0005 |
| Correctness | complete case | 54 | 4.519 | 4.519 | 0.000 | −0.204 to +0.185 | 0.9857 |
| Precision | ITT, failure = 1 | 45 | 3.156 | 4.333 | −1.178 | −1.778 to −0.600 | 0.0008 |
| Precision | complete case | 45 | 4.356 | 4.333 | +0.022 | −0.244 to +0.289 | 0.8240 |
| Depth | ITT, failure = 1 | 46 | 2.957 | 3.957 | −1.000 | −1.413 to −0.609 | 0.0001 |
| Depth | complete case | 46 | 3.804 | 3.957 | −0.152 | −0.391 to +0.087 | 0.2598 |

The proxy ITT does not support a RAG correctness or precision benefit; the direction is neutral-to-negative. Because the failure set is a proxy, this is a sensitivity analysis, not an exact ITT effect.

## Closing note

The submitted manuscript did not clearly separate adopted components from Rev.1
contributions. This table is the attribution record; Table 8 in the main text compares the
design dimensions, and Table 7 records which submitted claims replicate.

---

*End of Supplementary Material*
