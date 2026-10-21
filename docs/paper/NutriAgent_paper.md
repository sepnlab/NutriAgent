# NutriAgent: a controlled evaluation of specialist routing for layer-hen nutrition question answering

Geqi Yanᵃ, Dapeng Liᵇ, Hao Liᶜ, Hongchao Jiaoᵃ, Hai Linᵃ,*

ᵃ Key Laboratory of Efficient Utilization of Non-Grain Feed Resources (Co-Construction by Ministry and Province), Ministry of Agriculture and Rural Affairs, Shandong Provincial Key Laboratory of Animal Nutrition and Efficient Feeding, Department of Animal Science, Shandong Agricultural University, Tai'an, 271017, Shandong, China

ᵇ Poultry Institute, Shandong Academy of Agricultural Sciences, Jinan, 250100, Shandong, China

ᶜ College of Water Resources and Intelligence Engineering, China Agricultural University, Beijing, 100083, China

---

## Highlights

- Specialist-routed layer-hen QA covers 17 breeds with bilingual queries.
- A controlled factorial evaluation uses 54 queries and 378 expert scores.
- NutriAgent scores 4.34 vs 4.05; its precision advantage is nominal.
- Retrieval and validation add no measurable correctness gain.
- Numeric grounding is limited; audits and reproduction files are released.

---

## Abstract

Layer-hen nutrition advisory requires breed-, phase-, and ingredient-specific numerical answers, yet general-purpose LLMs can produce plausible values that are not traceable to a reference. We present NutriAgent, a specialist-routed multi-agent system that assigns four nutrition domains to isolated tool-using specialists and integrates their outputs through a synthesis stage. The system covers 17 layer breeds, including 10 Chinese domestic strains, and supports English and Chinese queries. We evaluate it on 54 purposefully selected queries with a primary expert (378 responses), an independent 120-response reliability rater, and controlled factorial and ablation experiments. NutriAgent achieved the numerically highest overall score (4.34 vs 4.05 for the strongest baseline, DeepSeek-V4-Pro) and nominally higher numeric precision (4.47 vs 3.97; +0.50, unadjusted p = 0.037, which does not survive a family-wise correction across all dimensions). Correctness was comparable rather than superior (4.46 vs 4.26; +0.20, 95% CI −0.09 to +0.50; p = 0.146), and performance was strongest on single-value, comparison, multi-hop, constraint, and definition queries but weaker on open-ended synthesis (C 3.29). Controlled comparisons separate the contributions of tool access, retrieval, specialist routing, and synthesis; the most consistent descriptive advantage is precision on structured queries, whereas retrieval augmentation and validation show no measurable correctness gain once the extra synthesis pass is controlled. The automated judge agrees moderately with the expert on correctness (ρ = 0.55) and depth (ρ = 0.34) and better on precision (ρ = 0.71), while scoring more leniently. We report the boundaries explicitly: one primary expert, 54 queries, a changed current model set, and incomplete human-labeled faithfulness validation.

**Keywords:** Layer hen nutrition, Multi-agent systems, Large language models, Self-consistency evaluation, Cross-lingual evaluation, Chinese domestic breeds

---

## 1. Introduction

Layer hen production is a major sector of the global poultry industry, with distinct nutritional requirements that differ fundamentally from those of broilers. While broiler nutrition focuses on maximizing growth rate and feed efficiency over a short production cycle (typically 42–56 days), layer nutrition must sustain prolonged egg production over 80–100 weeks, requiring precise management of calcium metabolism for eggshell formation, phase-specific amino acid ratios for sustained egg mass output, and careful energy balance to prevent excess fat deposition that compromises laying persistency (Bain et al., 2016; Jiang et al., 2025). These complexities demand specialized expertise: a poultry nutritionist must simultaneously consider breed-specific genetic potential, production phase, environmental conditions, and feed ingredient availability when formulating diets or diagnosing production issues (Pesti and Choct, 2023; Medras and Al-Khalaifah, 2026).

Access to qualified nutritionists who can provide timely, expert guidance to layer operations is limited in many production regions; this is contextual motivation rather than a quantified workforce finding, because we did not identify a study that measures the shortage. The application of artificial intelligence to poultry nutrition decision support offers a promising avenue for bridging this expertise gap, enabling producers to access authoritative nutritional data and structured reasoning without requiring continuous expert consultation (Abdel-Wareth and Ahmed, 2026; Berckmans, 2017; Martinez et al., 2024).

Recent advances in large language models (LLMs) have opened new possibilities for agricultural decision support (Ravindran et al., 2026; Tian et al., 2026; Tzachor et al., 2023; Zhu et al., 2025). However, general-purpose LLMs suffer from hallucination, output uncertainty, and lack of access to authoritative domain data (Ji et al., 2023) — limitations that are particularly costly in nutrition advisory where inaccurate information can lead to significant economic losses (Gong and Li, 2025; Huang et al., 2025b). LLM-based agents that combine structured reasoning with domain-specific tool access address these limitations by grounding responses in curated data sources rather than relying on potentially unreliable training data (Ke et al., 2026; Mialon et al., 2023). Agentic architectures are now being proposed for livestock housing and management as well as for nutrition advisory (Ruchay et al., 2027; Silvestri et al., 2026), but their evaluation remains fragmented across domains.

The ReAct framework (Yao et al., 2023) introduced the paradigm of interleaving reasoning traces with task-specific actions, enabling iterative tool use and observation-driven planning. Subsequent orchestration software — notably the LangChain framework (LangChain, 2026) — and tool augmentation approaches such as Toolformer (Schick et al., 2023) and ToolkenGPT (Hao et al., 2023) have lowered the barrier to tool integration, catalyzing a wave of domain-specific agent systems across chemistry, biomedicine, and poultry nutrition. Table 1 summarizes the representative systems and their architectural characteristics.

**Table 1.** Representative domain-specific LLM agent systems.

| System | Domain | Architecture | Core Contribution |
|---------|--------|-------------|------------------|
| ReAct (Yao et al., 2023) | General | Reasoning + Acting | Interleaved reasoning and tool use paradigm |
| ChemCrow (Bran et al., 2024) | Chemistry | Single-agent ReAct + 18 tools | Tool augmentation significantly outperforms standalone LLM |
| ChemAgent (Tang et al., 2025) | Chemistry | ReAct + self-updating memory | Reusable sub-task knowledge for chemical reasoning |
| Biomni (Huang et al., 2025a) | Biomedicine | Single-agent action discovery | 188% accuracy gain via tool orchestration |
| BioMaster (Su et al., 2025) | Bioinformatics | Multi-agent role-based | Role-based decomposition for complex workflows |
| CottonBot (Kandamali et al., 2025) | Cotton farming | LLM-RAG + agentic tools | Field-specific irrigation advice |
| Smart-greenhouse agents (Pardo-Pina et al., 2026) | Greenhouse management | Multi-agent RAG service | Telemetry analytics and decision support |
| NutriCHAT (Mandiga et al., 2026) | Poultry nutrition | Single-agent ReAct + RAG | First poultry nutrition agent (83.87% improvement) |

Across these systems, a common architectural insight emerges: decomposing complex domain tasks into specialized sub-tasks handled by focused agents with constrained tool access improves both accuracy and reliability.

In agriculture, however, LLM adoption has primarily taken the form of retrieval-augmented generation approaches. Balaguer et al. (2024) reported that fine-tuning raised domain-specific accuracy by more than six percentage points, with RAG adding approximately five percentage points further in a cumulative setup, and Ravindran et al. (2026) demonstrated LLM-based knowledge transfer for agricultural practitioners, while a review by Gong and Li (2025) concluded that hallucination, output uncertainty, and weak data provenance remain the primary barriers to agricultural LLM deployment — exactly the challenges that tool-augmented agent architectures are designed to mitigate. Recent agricultural systems have begun to combine retrieval with agentic tool use, including CottonBot for field-specific cotton irrigation advice (Kandamali et al., 2025) and a RAG-grounded greenhouse service architecture (Pardo-Pina et al., 2026), but specialist-routed multi-agent designs with structured nutrition tools remain less studied.

In the poultry nutrition domain, Mandiga et al. (2026) presented NutriCHAT, a hybrid ReAct-RAG agent for broiler nutrition that couples GPT-4o with four curated data modules covering Ross and Cobb broiler lines. Evaluated on 120 English queries by two poultry nutrition experts, NutriCHAT achieved 83.87% improvement over standalone GPT-4o and a 61.90% reduction in inconsistency score. However, the system is restricted to broiler species and English queries, uses a single-agent architecture that couples domain classification with tool selection in one reasoning chain, and does not verify whether response claims are grounded in tool-retrieved data. These limitations leave several open questions: Can agent architectures support the broader species diversity of commercial poultry production? Does decomposing queries into domain-specific sub-tasks improve accuracy over monolithic agent designs? How do such systems perform across languages, particularly for Chinese-language queries serving one of the world's largest poultry production regions?

Despite NutriCHAT's contributions, several specific gaps remain in poultry nutrition AI systems. The most fundamental is species coverage: existing systems target broiler nutrition, leaving layer hen nutrition — with its distinct parameters such as hen-day egg production, eggshell quality metrics, and phase-specific calcium requirements — largely unaddressed. The gap is compounded by the lack of support for Chinese domestic layer breeds (Jingfen, Nongda, Dawu series), which have limited publicly available nutritional specifications compared to international commercial strains. The economic significance of this gap is substantial: China produces more than 40% of the world's eggs (Yang, 2021), and much of this production relies on domestic layer strains whose nutritional specifications are not codified in the digital advisory systems we surveyed.

At the architectural level, current poultry nutrition agents use a single reasoning chain for all knowledge domains, coupling intent classification, tool selection, and response generation. The monolithic design creates opportunities for error propagation when queries span multiple domains or when the agent must select among competing tools, as upstream misjudgments in intent recognition or tool filtering cascade through downstream retrieval and generation steps. The context window competition problem — where adding more tool descriptions degrades the model's ability to select the correct tool (Qin et al., 2024) — is particularly acute in nutrition advisory because the four knowledge domains (feed ingredient composition, nutritional requirements, production performance, and terminology) have structurally different query patterns. A decomposition-based architecture addresses this by isolating each domain into a dedicated agent with a focused tool set and system prompt.

General-purpose multi-agent frameworks — including debate-based (Du et al., 2023), conversation-based (Wu et al., 2023), role-based (Park et al., 2023), mixture-of-agents (Wang et al., 2024), and orchestration frameworks — have explored task decomposition in open-ended reasoning contexts. These frameworks have been less studied in domain-specific agricultural applications with structured data tool access, and their effectiveness for retrieval-dominated rather than reasoning-dominated tasks remains largely unexplored.

Evaluation methodology also presents gaps. SelfCheckGPT (Manakul et al., 2023) provides a zero-resource cross-sample inconsistency detection method that has become a standard metric for assessing factual reliability in generative systems. Faithfulness evaluation — whether generated responses are supported by retrieved evidence — has been studied in RAG contexts (Honovich et al., 2022), but agent-based systems introduce an additional challenge: the evidence is not a static retrieval result but a dynamic tool observation that depends on the agent's action sequence. To our knowledge, no poultry nutrition system in the literature we surveyed assesses this dimension of response quality.

Cross-lingual evaluation is particularly challenging in domain-specific contexts because poultry nutrition terminology may not have direct Chinese translations. The poultry nutrition evaluations we identified are English-only, leaving cross-lingual applicability underexplored despite the significant Chinese-speaking poultry production community.

This work makes four contributions. First, it provides a layer-hen nutrition resource covering 17 breeds — including 10 Chinese domestic strains — with breed-level provenance and bilingual queries, extending a domain previously dominated by broiler systems. Second, it presents a precision-focused specialist-routed architecture with isolated tool access and a separate synthesis stage, designed for numerical layer-hen questions rather than open-domain chat. Third, it provides a controlled evaluation that separates tool access, retrieval, specialist routing, synthesis, validation, backbone, and query type, using expert scoring for the main comparison and automated scoring only for within-dimension ablations; this identifies precision on structured queries as the most consistent descriptive advantage and shows where the architecture does not add measurable quality. Fourth, it releases the query sets, prompts, de-identified scores, audit artifacts, and reproduction commands, with reliability checks (independent rater ICC 0.85/0.88/0.76; same-expert repeat ICC 0.995/0.996/0.932) that make the boundaries auditable. NutriAgent is therefore not a new domain ontology; it is a layer-hen extension plus a controlled test of specialist routing.

---

## 2. Materials and Methods

### 2.1 Domain-Specific Data Modules

NutriAgent provides access to poultry nutrition data through four specialized retrieval modules, each addressing a distinct information need: what nutrients each ingredient contains (Ingredient Composition), what each breed requires at each production phase (Nutritional Specifications), how breeds perform over the laying cycle (Production Benchmarks), and terminological definitions (Terminology). Data are sourced from breed-specific management guides (Hy-Line, ISA, Lohmann), Chinese domestic breed documentation compiled through the industry resource platform jbzyw.com, and public feed composition databases (feedtables.com, feedipedia.org). Table S3 summarizes the source type and resolution status for each dataset; the machine-readable `corpus/provenance.csv` records the document title, version or date, URL or archived copy, extraction date, and license where available, and flags entries that still need a primary source or version. Chinese domestic data obtained through the aggregator are labeled as such rather than described as official management guides.

The modules are organized into a two-tier data architecture (Fig. 1): resources shared across layer breeds (ingredient composition and terminology; energy and amino-acid digestibility values remain species-specific) and breed-specific resources (nutritional specifications and production benchmarks). This separation enables breed extensibility — new breeds can be supported by supplying corresponding data files and a handler class (Section 2.1.5) without modifying the retrieval or agent logic.

![Fig. 1](assert/fig1_data_architecture.png)

**Fig. 1.** Data module architecture and ingestion pipeline. External sources feed four specialized modules organized into two tiers: shared across layer breeds (green) and breed-specific (blue). Each module's internal structure is shown — the Ingredient Composition module comprises three datasets (chemical composition, amino acid profiles, digestibility coefficients), Nutritional Specifications splits into requirement data and supplementary vitamin/mineral entries, and Production Benchmarks organizes 12 parameters into three functional categories. All modules feed into the PoultryDB vector index (2,144 documents), which supports both structured tool-based retrieval and semantic vector search. Abbreviations: params = parameters; docs = PoultryDB documents; entries = CSV data rows; EAA = essential amino acids; NEAA = non-essential amino acids; AA = amino acids; SID = standardized ileal digestibility; FI = daily feed intake; BW = body weight; wt = weight; str = strength; cumul = cumulative.

#### 2.1.1 Feed Ingredient Composition

The ingredient composition module provides nutritional data for 108 entries with 108 unique ingredient names, organized into three complementary datasets spanning 97 nominal parameters. Across the three datasets, 8,748 of 10,476 nominal ingredient–parameter cells (83.5%) are populated; the general-composition table alone has 16 entirely empty parameters (Table S1). The primary data source is the INRAE-CIRAD-AFZ (2026) feed table; the CVB feed table (CVB, 2023) is used as a secondary reference for selected ingredients. The entries span cereal grains and their by-products, protein meals, animal by-products, oil and fat sources, mineral supplements, and novel feedstuffs including insect meals.

**General chemical composition (38 parameters).** This dataset covers proximate analysis (6), carbohydrates (3), fiber fractions (5), energy values (4), fatty acids (2), minerals (14), and vitamins (4). Only 2,376 of 4,104 cells (57.9%) are populated; 16 parameters are entirely empty in the current release, including NFE, NE, fatty acids, Cl, S, and all six trace minerals (Table S1).

**Amino acid profiles (19 parameters).** This dataset provides complete amino acid composition for each of the 108 entries, covering all nutritionally relevant amino acids: essential amino acids (lysine, methionine, threonine, tryptophan, arginine, valine, isoleucine, leucine, histidine, phenylalanine) and non-essential amino acids (tyrosine, cysteine, methionine-cysteine, glycine, serine, proline, alanine, aspartic acid, glutamic acid). Values are expressed as percentages of the ingredient on an as-fed basis.

**Digestibility coefficients (40 parameters).** For precision formulation, this dataset provides both total amino acid concentrations (g/kg) and standardized ileal digestibility (SID) coefficients for 20 amino acids per ingredient, including combined forms (methionine-cysteine, phenylalanine-tyrosine) that are nutritionally relevant for requirement matching. SID is the ileal digestibility of an amino acid corrected for basal endogenous amino-acid losses (Lemme et al., 2004); it is the preferred amino-acid system for poultry formulation. Together, the total concentration and SID coefficient for each amino acid enable the system to compute digestible amino acid content for precision formulation queries.

The inclusion of locally available feed ingredients commonly used in Chinese poultry production (e.g., distillers dried grains with solubles from rice, cottonseed meal, rapeseed meal varieties) alongside internationally common feed ingredients (maize, soybean meal, wheat, barley) reflects the practical needs of formulators working with regional raw materials. This regional ingredient coverage ensures that queries about feedstuffs common in Chinese production systems return composition data rather than fallback estimates.

Query processing uses case-insensitive substring matching against the ingredient name index. If no match is found, the query is progressively truncated to its first word or first four characters for a broader substring search. When all matching attempts fail, the system lists available ingredients rather than returning a guessed value. This is a known limitation: on a 39-case perturbation set, exact canonical, commodity short, and case/whitespace names resolved 100% at the family level, but misspellings were family-correct only 37.5% (e.g., "wheatt" returned wheat bran; "corn meal" returned corn gluten feed) and Chinese aliases resolved 0%. The feed index is English-only, so Chinese ingredient names depend on the LLM translating them before the tool call. A curated alias table (`corpus/shared/ingredient_alias.csv`) is used by the consistency checker, but the feed tool itself still uses the substring index (Section 4).

#### 2.1.2 Nutritional Specifications

The nutritional specifications module provides breed-specific and phase-specific requirement data sourced from breeder management guides and industry resource platforms. International commercial strain data (Hy-Line, ISA, Lohmann) are drawn from each breeder's published management guides (Hy-Line International, 2026a, 2026b; ISA, 2026; Lohmann, 2026). Chinese domestic breed specifications are sourced from jbzyw.com, a poultry industry resource aggregation platform that compiles breed management parameters from published breeding company documentation and technical reports.

For layers, specifications encompass 17 breeds spanning two categories: (1) international commercial strains — Hy-Line W-36, Hy-Line Brown, Hy-Line Pink, ISA Brown, Lohmann Grey, Lohmann Pink, Hisex Brown; and (2) Chinese domestic commercial strains — Jingfen 6, Jinghong 1 v3.0, Jingbai 939, Dawu Jinfeng, Dawu He, Dawu Fen 1, Nongda 3, Nongda 6, Beinong 1, Beinong 2. The corpus retains the original breeder phase labels rather than forcing a common seven-phase scheme: 55 distinct nutrition labels occur across the 17 breeds (3–9 per breed; Chinese domestic strains typically have 3–5, international strains 5–9), and four additional labels occur only in the vitamin/mineral table (59 labels in total). A crosswalk to seven reference phases (Starter 0–6 w, Grower 7–12 w, Developer 13–17 w, Pre-Lay 18–20 w, Lay I 21–40 w, Lay II 41–60 w, Lay III 61 w+) is provided in Table S2, with an explicit mapping type for every label (exact, within, boundary, semantic, composite, or ambiguous); 53 labels map to one of the seven phases and 6 are marked unmapped. Ambiguous and composite labels are not coerced into a single phase.

Each entry includes 20 numeric parameters: metabolizable energy (kcal/kg); crude protein, calcium, available phosphorus, and sodium (% of diet); total lysine, methionine, methionine–cysteine, threonine, tryptophan, valine, arginine, and isoleucine (%); SID coefficients for lysine, methionine, methionine–cysteine, threonine, and tryptophan (%); choline (mg/kg); and linoleic acid (%) (Table S1). Units are carried in the field names, and values retain the basis used by the source document (diet percentages as published); no dry-matter or unit conversion is applied at ingestion. Available phosphorus is used throughout; total phosphorus is not part of the 20-field requirement schema. Supplementary vitamin and mineral specifications (18 parameters: vitamins A, D3, E, K3, B1, B2, B6, B12, niacin, pantothenic acid, folic acid, biotin, and trace minerals Fe, Cu, Zn, Mn, Se, I) are maintained in a separate dataset covering 13 of the 17 breeds, as these data are published in supplementary sections of the breed management guides and are not uniformly documented across all breeds.

The broad breed coverage — particularly the inclusion of Chinese domestic layer strains — is a deliberate design choice. While international breed guidelines are well-documented, Chinese domestic breeds have limited publicly available nutritional specifications, and their inclusion addresses a practical need in regional poultry production. The module contains 103 breed–phase rows × 20 parameters = 2,060 nominal cells, of which 1,517 (73.6%) are populated, plus 30 vitamin/mineral rows × 18 parameters = 540 cells (100% populated).

#### 2.1.3 Production Benchmarks

The production benchmarks module provides weekly layer performance tracking data across the full production cycle. Data extend up to week 100 for 16 breeds, with 12 parameters per record organized into three categories: production metrics (hen-day egg production, egg weight, egg mass per hen per day, cumulative egg count), feed efficiency indicators (daily feed intake, feed per dozen eggs, feed per kg egg mass), and quality and health measures (body weight, mortality percentage, shell breaking strength, Haugh unit, daily water intake). Coverage varies by breed (19–100 weeks). The layer dataset comprises 1,131 weekly records; 5,798 of 13,572 nominal cells (42.7%) are populated, and three parameters (egg mass per hen per day, feed per dozen eggs, feed per kg egg mass) are empty in the current release (Table S1).

This module supports queries that track production trends over time (e.g., "How does feed intake change from week 20 to week 60 for ISA Brown?"), compare breed-specific target benchmarks, and identify deviations from expected breed-specific targets. These are guide-specific targets rather than controlled head-to-head observations; the weekly granularity enables detection of production dips or health events that coarser summary statistics would obscure.

#### 2.1.4 Terminology Reference

The terminology module provides a glossary of 556 poultry nutrition terms and concepts, compiled from nutrient-requirements references (e.g., National Research Council, 1994) and industry guidelines, covering topics from feed ingredients and digestive physiology to feed processing, environmental management, health and disease, egg production, meat quality, metabolism, vitamins, minerals, additives, anti-nutritional factors, nutritional disorders, and food safety. Because poultry nutrition terminology varies across sources — for example, abbreviations such as 'FCR' coexist with full forms like 'feed conversion ratio' — the module supports three matching strategies: exact match for precise term lookup, partial substring match for abbreviated or incomplete queries, and fuzzy word-level match that scores candidate terms by the number of overlapping words with the query.

#### 2.1.5 Breed Extensibility

To support adding new breeds or species without modifying core logic, NutriAgent employs a strategy pattern that encapsulates breed-specific differences into handler classes. Because breed differences extend beyond data values to include column naming conventions, age representations (weekly for layers, daily for broilers), and tool description language, a code-level strategy pattern was chosen over static configuration to encapsulate these behavioral variations. Each handler defines four categories of information: (1) metadata used in system prompts (display name, available breeds, production phases, key metrics); (2) CSV column naming conventions; (3) age representation; and (4) tool description templates that adjust the LLM's understanding of available data based on the active breed group. All four data modules adapt their behavior through this interface. Extension to a new breed requires (a) a handler subclass implementing the four property categories, (b) breed-specific CSV data files, and (c) registration in the handler factory — with no changes to tool implementations or agent logic.

**Knowledge base summary.** Across the four modules, the knowledge base contains:

- Feed ingredient composition: 108 records × 97 nominal parameters = 10,476 cells (8,748 populated)
- Nutritional specifications: 103 breed–phase rows × 20 parameters = 2,060 cells (1,517 populated), plus 30 × 18 = 540 vitamin/mineral cells (all populated)
- Production benchmarks: 1,131 weekly records × 12 parameters = 13,572 nominal cells (5,798 populated)
- Terminology: 556 definitions

We report records, nominal cells, populated cells, and definitions separately; the single "data point" total used in the submitted version (≈14,800) mixed these units and is withdrawn. This knowledge base supports two complementary retrieval modes. Structured tool-based retrieval serves queries with known parameters (e.g., 'calcium content of limestone'), where specialist agents query specific data fields directly. Semantic retrieval via vector search over the 2,144-document PoultryDB handles open-ended queries where relevant information cannot be predetermined by parameter names alone.

---

### 2.2 Specialist-Routed Pipeline

NutriAgent decomposes poultry nutrition question answering into a three-stage specialist-routed pipeline (Fig. 2): Stage 1, query classification (Router); Stage 2, domain-specific tool-augmented reasoning (Specialists); and Stage 3, consistency checking and answer integration (Synthesis). This architecture draws on the multi-agent paradigm (Hong et al., 2024; Guo et al., 2024), contrasting with single-agent designs where one LLM handles all domains and tool access. All pipeline components share a single base model (DeepSeek-V4-Flash (DeepSeek, 2026a)) with temperature 0.0 and thinking disabled, reducing sampling variability; we do not claim deterministic outputs, and a repeat-run check is reported in Section 2.3.5.

#### 2.2.1 Design Rationale

Poultry nutrition queries exhibit strong domain structure: a question about feed ingredient composition rarely requires knowledge of production benchmarks, and vice versa. Motivated by this observation, we adopt a decomposition-based architecture in which each query is routed to one or more domain specialists, each responsible for a single knowledge area.

The value of multi-agent architectures in domain-specific contexts lies in tool isolation and focused reasoning. When an agent has access to many tools, context window competition between tool descriptions can degrade tool selection accuracy (Qin et al., 2024), a phenomenon observed across tool-augmented LLM systems. By isolating tool access per specialist, NutriAgent avoids this competition — each reasoning agent sees only the tools relevant to its domain, while the synthesis stage re-integrates specialist outputs. Decomposition also enables each specialist to maintain a focused system prompt tuned to its domain's reasoning patterns, which is more difficult to maintain in a single shared prompt.

The pipeline consists of three stages: (1) a Router that classifies the query and selects target specialists; (2) a set of Specialists that independently retrieve and reason over domain-specific data; and (3) a Synthesis Agent that checks cross-specialist consistency and merges specialist outputs into a final response. A retrieval-augmented generation (RAG) component (Lewis et al., 2020) provides supplementary context from the vector knowledge base, complementing tool-retrieved data with semantically relevant passages.

**Fig. 2** illustrates the complete pipeline architecture.

![Fig. 2](assert/fig2_pipeline_architecture.png)

**Fig. 2.** Specialist-routed pipeline architecture. Stage 1: the Router classifies each query and activates one or more domain specialists (blue), each with isolated access to its own tool (green). Stage 2: activated specialists retrieve domain data and execute tool calls in parallel, following a ReAct reasoning loop until sufficient evidence is gathered. PoultryDB (gray dashed) provides supplementary semantic context to both specialists and the Synthesis Agent via domain-tagged retrieval. Stage 3: the Synthesis Agent performs cross-specialist consistency checks and integrates all responses into a final answer. Color coding: orange = routing, blue = specialists, green = tools, yellow = synthesis, teal = output, gray dashed = vector knowledge base. Abbreviations: LLM = large language model.

#### 2.2.2 Query Classification and Routing

The Router classifies each incoming query along two dimensions: the primary intent domain (feed, nutrition, performance, or terminology) and whether the query requires single-domain or multi-domain processing. The output is a routing decision specifying which specialist(s) to activate and whether cross-validation between specialists is needed.

The primary classification mechanism uses a lightweight LLM call (the same base model, DeepSeek-V4-Flash, at temperature 0.0, maximum output length 200 tokens, thinking disabled). The router prompt includes domain descriptions with representative examples and requests a structured JSON output containing the intent, target agent list, and a cross-validation flag (full prompt in Supplementary S2.2). The flag is set when multiple specialists are activated and their outputs may contain overlapping numerical claims requiring consistency checks (Section 2.2.4); it gates whether consistency checking runs. For multi-faceted queries (e.g., "What is the calcium requirement for Hy-Line Brown during Lay I, and how does limestone's calcium content compare?"), the router activates multiple specialists simultaneously.

A keyword-based fallback activates when the LLM classification fails due to API errors or malformed output. The fallback maintains bilingual keyword sets covering ingredient names, nutritional terms, and production metrics in English and Chinese, and selects targets by keyword frequency scoring. When no keywords match, the query is broadcast to all four specialists as a safety measure.

#### 2.2.3 Domain-Specialist Execution

Each specialist is an independent reasoning agent with two constraints: (1) its system prompt is focused exclusively on its domain, and (2) it has access only to the data module relevant to its specialty. Four specialists are implemented:

- **Feed specialist**: Handles ingredient composition, amino acid profiles, and digestibility queries. Accesses the feed ingredient module.
- **Nutrition specialist**: Handles requirement specifications, vitamin/mineral levels, and phase-based formulation queries. Accesses the nutritional specifications module.
- **Performance specialist**: Handles production benchmarks, growth curves, and egg production queries. Accesses the production benchmarks module.
- **Terminology specialist**: Handles terminology lookups and concept explanations. Accesses the terminology module.

Each specialist is a LangChain ReAct agent (LangChain, 2026; Yao et al., 2023) using DeepSeek-V4-Flash at temperature 0.0. The agent iterates through a Thought–Action–Observation cycle: at each step, the LLM reasons over the query and any prior observations, emits a tool call, receives structured data from the domain-specific tool, and appends the result to its scratchpad. The loop terminates when the agent emits a final answer or reaches seven iterations. Simple queries complete in one to two cycles; multi-step queries (e.g., comparing nutrients across ingredients) proceed through successive tool calls. When multiple specialists are activated, they execute concurrently via ThreadPoolExecutor, with per-specialist timeout of 120 seconds. For the D1 factorial contrast, a single-pass variant makes exactly one tool call and then answers without further iterations (Section 2.4).

#### 2.2.4 Consistency Checking and Synthesis

The Synthesis Agent integrates specialist outputs into a single coherent response through two sub-processes.

**Consistency checking.** When multiple specialists are activated, the system parses numeric claims from their responses into (entity, attribute, value, unit, basis) tuples and compares only claims that share the same entity, attribute, and basis. Values are converted to a common unit (%, g/kg, mg/kg; kcal/kg ↔ MJ/kg) before comparison; a claim pair is flagged when the relative difference exceeds 5%, matching the numeric tolerance. The extractor handles both attribute-before-value ("calcium 35%") and value-before-attribute ("35% calcium") order, maps commodity-level short names to family entities (e.g., "soybean meal" across table variants), and resolves phase labels ("Lay I" for "Lay I 21-40w"). Claims whose entity cannot be resolved are not compared ("no confident match"). On a 42-pair labeled set (16 conflicts, 12 consistent or unit-converted, 14 distractors), precision/recall/F1 are 1.00/1.00/1.00; this is a rule-coverage test on synthetic pairs, not a field precision estimate. The generic Ca:P ratio rule used in the submitted version (1.2:1–5.0:1) was removed: it conflated total, available, and digestible phosphorus and flagged normal layer diets (e.g., Ca 4.0% with available P 0.4% gives 10:1). A Ca:P check is available only as an opt-in policy for structured contexts where the phosphorus basis is explicit; it is disabled in the reported experiments.

**Response generation.** The synthesis prompt presents the original query, all specialist responses (tagged by source domain), consistency notes, and optional supplementary context from the RAG component. The synthesis LLM (DeepSeek-V4-Flash, temperature 0.0) is instructed to integrate the information, resolve any flagged inconsistencies with explicit reasoning, and cite the data source for each key numerical claim. If the synthesis call fails, the system falls back to concatenating specialist responses directly.

#### 2.2.5 Supplementary Retrieval via Vector Knowledge Base

A vector-based retrieval component provides supplementary context that may not be captured by the specialists' targeted tool queries, operating in parallel with the specialist execution pipeline.

**Knowledge base construction (PoultryDB).** The vector index is built by first textualizing each data record into a standalone descriptive sentence. For example, a CSV row containing "Ingredient: Maize; CP: 8.5; ME: 3350" produces the sentence "Maize contains 8.5% crude protein and 3350 kcal/kg metabolizable energy." These sentences are embedded using Qwen3-Embedding-0.6B (1,024 dimensions; Yang et al., 2025), a local GPU-based model that avoids API dependency. The resulting vectors encode semantic relationships among nutrition concepts that are latent in the original tabular format. All vectors are indexed in ChromaDB (Chroma, 2026) using an approximate nearest-neighbor HNSW index (Malkov and Yashunin, 2020). The final PoultryDB comprises 2,144 documents: 324 from the ingredient composition module (108 entries × 3 datasets), 133 from nutritional specifications (including vitamin/mineral data), 1,131 from production benchmarks, and 556 from terminology definitions. An independent PoultryDB instance is constructed for each species (broiler and layer) using the corresponding data files; all experiments in this study use the layer instance.

**Retrieval process.** At query time, the user's question is embedded with the same model, producing a query vector $\mathbf{q}$. The index is searched for the document vector $\mathbf{d}_i$ with minimum cosine distance:

$$
\text{cosine distance}(\mathbf{q}, \mathbf{d}_i) = 1 - \frac{\mathbf{q} \cdot \mathbf{d}_i}{\|\mathbf{q}\| \|\mathbf{d}_i\|}
$$

The system retrieves $k$ documents by default (`Config.RAG_K`); the Rev.1 reported runs use $k = 1$. Because each specialist already performs precise structured retrieval through its dedicated tool, the supplementary RAG context is deliberately narrow: a single high-relevance passage is used rather than multiple candidates that may introduce noise. This choice has a cost: on 44 queries with annotated target documents, retrieval hit@1 is 27.3%, hit@3 54.5%, hit@5 63.6% (MRR 0.411), so $k = 1$ misses most annotated targets. We report this as a limitation of the narrow setting, not as evidence that RAG is unhelpful; $k = 5$ would improve recall but adds context and was not used in the reported runs. The submitted manuscript said $k = 1$ while the deposited run used $k = 2$; the frozen Rev.1 value is $k = 1$, documented in `config/settings.yaml` and the model lock.

A domain-tagging step annotates retrieved documents relative to the domains already covered by the activated specialists. Documents from covered domains are tagged "(same domain)" and documents from uncovered domains "(supplementary)". This is tagging rather than filtering: all retrieved documents are passed to the synthesis prompt, so the synthesis LLM can incorporate genuinely complementary information without duplicating what the specialists already provided.

Search results are cached per (query, k) pair in an LRU cache (capacity 512). Since identical queries may appear across different experimental conditions (e.g., ablation variants), the cache eliminates redundant embedding computations during ablation experiments.

---

### 2.3 Evaluation Framework

We evaluate NutriAgent along three complementary dimensions: response quality (how accurate and informative the answers are), groundedness (whether the answers are supported by retrieved data), and text quality (readability and factual consistency). This multi-dimensional assessment captures both the correctness of the system's outputs and the reliability of its knowledge grounding.

#### 2.3.1 Query Set Design

The evaluation uses a curated set of 54 queries that spans six knowledge domains (Ingredient Composition, Nutrient Requirements, Production Performance, Terminology, Cross-Domain, and Edge Cases) and seven query types (single-value, comparison, open-ended, definition, multi-hop, constraint, counterfactual). Queries are drawn from a bilingual pool: 42 English queries covering international and Chinese strains (Hy-Line, ISA, Lohmann, Jinghong 1, Dawu Jinfeng, Jingfen 6) and 12 Chinese queries spanning Chinese domestic strains (Jingfen 6, Dawu Jinfeng) and one international strain queried in Chinese (Hy-Line Brown), plus Chinese-language feed-composition and terminology questions. All queries with unambiguous numerical ground truth (36 of 54) include expected value annotations for tolerance-based accuracy evaluation; five edge-case queries include expected behavioral specifications (e.g., the system should return a warning when queried about incompatible nutrient combinations).

The 54-query evaluation set was selected by purposeful stratified selection from the 195-query candidate pool (120 English, 28 Chinese, 30 English advanced, and 17 Chinese advanced), ensuring representation of all seven query types and six knowledge domains while prioritizing queries that test distinct system capabilities. The four source sets were compiled by the study team during system development and were not held out: the developers had access to them, so some queries may have informed prompt and tool development. The final 54-query set was fixed before the Rev.1 expert scoring reported here, but it is not an independent held-out benchmark. Two domain experts on the study team independently reviewed the selected queries before Rev.1; external independent query validation was not obtained. Because selection was criterion-based rather than random, no random seed is reported, and we do not describe the set as a random sample. The full 195-query pool and the selection criteria are provided in the repository; the reported results use the 54-query set. The approach is consistent with established practice in LLM evaluation, where purposefully curated, stratified sets provide more diagnostic signal per query than larger, undifferentiated sets (Zheng et al., 2023).

The bilingual design reflects real-world usage patterns where domestic breeds are typically queried in the local language. The correspondence is not strict: the 12 Chinese queries include an international strain (Hy-Line Brown) and several feed/terminology questions, while the English set includes questions about Jinghong 1 and Dawu Jinfeng. Language and breed remain confounded overall, and the bilingual analysis is therefore exploratory (Section 3.5). Cross-lingual evaluation is particularly challenging in domain-specific contexts because poultry nutrition terminology (e.g., "standardized ileal digestibility," "hen-day egg production") may not have direct, universally accepted Chinese translations, and the quality of multilingual LLM processing varies across languages and domains (Lai et al., 2023; Ahuja et al., 2023).

**Fig. 3** shows how the 54-query curated set was selected from the 195-query candidate pool and its composition across three dimensions. Panel (a) presents the query-type distribution across all four candidate pools and the curated set: the curated set was drawn proportionally from the English pool (120 queries), English advanced set (30), Chinese pool (28), and Chinese advanced set (17), with the curated row highlighted. Single-value queries form the largest group (21 of 54, 39%), reflecting the system's primary use case of factual lookup. Panels (b) and (c) show the language split (78% English, 22% Chinese) and domain distribution, with Nutrient Requirements (12 queries) and Cross-Domain (10 queries) receiving proportionally more representation due to their higher complexity and practical relevance.

![Fig. 3](assert/fig3_query_composition.png)

**Fig. 3.** Evaluation query set composition and curated selection. (a) Query-type distribution across four candidate pools and the curated set (highlighted); numbers within bars indicate per-type counts. (b) Language split of the curated set (n=54). (c) Distribution by knowledge domain. The curated set (54 queries) is used in all experiments; the full candidate pool (195 queries) is available for extended evaluation.

#### 2.3.2 Response Quality Assessment

**Scoring rubric.** Responses are scored on three axes using a 1–5 Likert scale with behavioral anchors (Likert, 1932; Chang et al., 2024). **Correctness**: 5 = all facts accurate; 4 = mostly accurate, minor imprecision; 3 = partially correct, noticeable errors; 2 = several factual errors; 1 = completely incorrect or hallucinated. **Provenance** is scored separately: whether numeric claims name a tool or source; it is reported as a supplementary column and is **not** folded into correctness. **Precision**: 5 = exact point estimate; 4 = close estimate; 3 = directionally correct but noticeably off; 2 = vague or significantly inaccurate; 1 = no numeric answer (null for definition queries). **Scientific Depth**: 5 = thorough mechanistic understanding with practical context; 4 = good domain knowledge; 3 = adequate but surface-level; 2 = superficial; 1 = no scientific content. Full rubric with per-level examples is provided in Supplementary S12.

**Expert evaluation (primary).** An independent poultry nutrition expert (20+ years in feed formulation and layer hen management) scored all 378 responses (54 queries × 7 methods) for the Rev.1 comparison. The expert was provided with the scoring rubric, annotated ground-truth values, and example query–response pairs for calibration before scoring. All responses were presented in anonymized form with randomized order within each query group to prevent model identification bias; the label map is held by the corresponding author. Scoring was conducted in a single session.

**EvaluatorLLM (supplementary).** For the large-scale ablation (~1,080 responses), we employ MiMo-V2.5-Pro (Xiaomi MiMo Team, 2026) as the automated evaluator using the evaluator rubric v1 in Supplementary S2.4, which includes a citation clause; the primary expert used rubric v2 (Supplementary S12), which removes the citation clause from correctness and scores provenance separately. The two instruments are therefore reported separately, and automated and expert scores are not pooled. Each response is scored independently against the rubric (absolute scoring) for both the main comparison and the ablations. A comparative mode exists in the implementation — all responses for a query presented together, with the evaluator identifying the strongest response and scoring others relative to it — but it was not used for the reported results, because the two protocols change the evaluation task and can change calibration. Response order randomization (controlled by `shuffle_responses`) mitigates position bias (Gu et al., 2025). Failed evaluations are recorded as null and excluded.

**Rationale for the two-tier evaluation design.** This study employs expert evaluation as the primary scoring method for all comparative results, with EvaluatorLLM used for the ablation analysis where the evaluation volume (~1,080 responses over 20 variant configurations) exceeds practical expert capacity. The approach follows the precedent set by ChemCrow (Bran et al., 2024), which used GPT-4 for ablation studies while reserving expert judgment for primary results. NutriCHAT (Mandiga et al., 2026) used two independent poultry nutrition experts and reported Cohen's κ = 0.60–0.73; we use a single expert with a structured rubric and anonymized randomized presentation to promote scoring consistency. We acknowledge a fundamental limitation of LLM-based evaluation, analogous to the EvaluatorGPT bias documented in ChemCrow: when the evaluator LLM lacks the domain-specific expertise to answer a poultry nutrition query itself, it may lack sufficient knowledge to reliably assess response quality. This limitation is partially mitigated by absolute scoring against a fixed rubric and response order randomization. The automated judge agrees only moderately with the expert (Section 3.2); we therefore use it for within-dimension relative contrasts and treat its absolute scores as secondary.

**Statistical reporting.** We report paired mean differences with 95% bootstrap confidence intervals (10,000 resamples), Cohen's *d_z* (Lakens, 2013), Wilcoxon signed-rank tests, and Holm-corrected p-values across baselines; rank associations use Spearman's ρ (Spearman, 2010), and the powered sample-size reference for the bilingual subset follows Cohen (2013). The analysis code is `scripts/paper/agreement.py`, and the full table is Table 10 and Supplementary S15. The standard deviation reflects cross-query variability within each method, not inter-rater disagreement. Medians and interquartile ranges are reported as an ordinal-scale sensitivity analysis. Because the primary comparison is paired by query, these intervals quantify uncertainty in the between-method differences even with a single primary rater; they do not address inter-rater uncertainty. The submitted significance values are not carried over.

**Inter-rater reliability.** The primary expert scored all 378 responses. A repeat 120-response sheet from the same expert gives intra-rater ICC(2,1) = 0.995 (correctness), 0.996 (precision), and 0.932 (depth); quadratic weighted κ = 0.995/0.996/0.931; Bland–Altman mean differences are −0.02/−0.01/+0.08. Because this is a repeat/copy pass by the same rater, it measures consistency, not independent reliability, and is not used for the inter-rater estimate. An independent third rater gives ICC(2,1) = 0.847 (correctness), 0.876 (precision), and 0.760 (depth); quadratic weighted κ = 0.846/0.874/0.758; Spearman ρ = 0.862/0.913/0.725; Bland–Altman mean differences are −0.27/−0.11/+0.21 (95% limits −1.45/+0.92, −1.36/+1.14, −1.06/+1.48). Scoring consistency was supported by three procedural safeguards: (1) a detailed rubric with behavioral anchors, (2) pre-evaluation calibration with example query–response pairs, and (3) anonymized presentation with randomized order within each query group. We do not carry over the submitted post-hoc correlations (ρ = 0.81/0.74/0.69) because the raw scores were not retained and cannot be verified.

#### 2.3.3 Groundedness Assessment

Groundedness measures whether the system's responses are supported by the data its tools actually retrieved, as opposed to the model's parametric knowledge. This is a critical assessment for domain-specific systems where unsupported claims may be factually incorrect.

**Numeric faithfulness.** To detect whether the model introduces numerical values from its parametric knowledge rather than tool-retrieved data, numerical claims are extracted from the response text using regular expressions targeting both single values (e.g., "4.0%", "3350 kcal/kg") and value ranges (e.g., "20–25%"). Extracted values are checked against the tool observation records — the raw key-value pairs returned by data module queries during the specialist execution phase, preserved in a structured log per query. A value is considered supported if it falls within ±5% of any tool-returned value. The score is the ratio of supported claims to total numerical claims. A score of 1.0 indicates all numbers in the response trace back to tool-retrieved data; lower scores suggest the model may have introduced values from its training data. For range-valued predictions $[L, U]$, the tolerance check applies symmetrically: the predicted range is expanded by 5% before checking containment of the tool-returned value.

**Semantic faithfulness.** For non-numerical claims, Natural Language Inference (NLI) verifies whether each claim is entailed by the tool observations — following RAG faithfulness evaluation approaches that check claim entailment against retrieved evidence (Honovich et al., 2022). Tool outputs are first converted to natural-language evidence sentences (e.g., "CP: 8.5" becomes "The CP is 8.5."). Response text is split into sentence-level claims using regex-based sentence segmentation, with numeric-heavy sentences excluded (already covered by numeric faithfulness). A CrossEncoder NLI model (MoritzLaurer/mDeBERTa-v3-base-mnli-xnli, a multilingual MNLI/XNLI checkpoint; He et al., 2023) computes entailment, contradiction, and neutral probabilities for each (evidence, claim) pair. Claims with entailment probability ≥ 0.7 score 1.0; claims with contradiction probability ≥ 0.7 score 0.0; all other cases score 0.5 (neutral or uncertain). The overall semantic faithfulness score is the mean across all claims.

Both metrics range from 0 to 1, with higher values indicating stronger grounding. The NLI model is shared with the inconsistency-scoring component (Section 2.3.4) to avoid duplicate GPU memory allocation.

**Tolerance-based accuracy.** While numeric faithfulness checks responses against tool outputs, tolerance-based accuracy checks against the independently annotated ground truth — a reference that may not appear in any tool response. This provides an objective accuracy measure for queries with annotated numerical ground truth. Following established practice in visual question answering (Masry et al., 2022), we use the conventional relative-error criterion:

$$\frac{|p-g|}{|g|} \le \tau \quad (g \neq 0)$$

This differs from the interval $g \in [p(1-\tau), p(1+\tau)]$ used in the submitted version, which becomes asymmetric as the error grows. For a range output $[L, U]$, the prediction is counted as correct if the ground-truth point lies within $[L(1-\tau), U(1+\tau)]$ after unit normalization; unit conversions are applied before comparison. We report accuracy at two thresholds ($\tau = 0.02$ and $0.05$). Rev.1 recomputes the metric under this definition (Section 3.4).

#### 2.3.4 Text Quality Assessment

While groundedness (Section 2.3.3) evaluates whether responses are supported by retrieved data, text quality assesses the surface-level readability and the model's factual consistency independent of tool outputs.

**Readability.** To assess whether responses are accessible to practitioners with varying educational backgrounds, we compute Flesch Reading Ease scores (Flesch, 1948) via the textstat package (Textstat, 2026). The score is computed as:

$$\text{FRES} = 206.835 - 1.015 \times \frac{\text{total words}}{\text{total sentences}} - 84.6 \times \frac{\text{total syllables}}{\text{total words}}$$

The score integrates sentence length and syllable density into a 0–100 scale where higher values indicate simpler text. Scores between 90–100 are considered very easy (elementary school level), 60–70 are standard (8th–9th grade), and scores below 50 correspond to college-level reading difficulty — the expected range for technical poultry nutrition content. Flesch Reading Ease is computed only for English responses (n = 42); Chinese responses are excluded because textstat does not provide a validated Chinese variant of the formula.

**Factual consistency.** We assess cross-sample inconsistency with SelfCheckGPT-NLI (Manakul et al., 2023), which compares a primary response against stochastic samples from the same model. For each query, the primary response is generated at temperature 0.0 and segmented into sentences. N = 5 additional responses are sampled at temperature 1.0, and each primary-response sentence is evaluated for contradiction against these samples using a CrossEncoder NLI model (`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`; He et al., 2023). The per-query score is the mean contradiction probability across all sentence–sample pairs, ranging from 0.0 (fully consistent) to 1.0 (fully contradictory). This is a self-consistency score, not a direct factual-error rate: a correct answer can vary across samples, and an incorrect answer can be repeated consistently. We adopt N = 5 for the primary evaluation and report an N-sensitivity analysis at N = 5/10/20 in Supplementary S6. To manage API rate limits during batch sampling, concurrency is adaptively reduced from 20 to 10 to 5 upon encountering server errors.

SelfCheckGPT was chosen over reference-based inconsistency detectors because it requires no external knowledge base — it relies solely on the target model's own stochastic samples — and therefore applies uniformly across all evaluated architectures. The NLI-based approach provides sentence-level granularity, making it possible to identify which response components are most prone to cross-sample inconsistency. We use N = 5 for the primary evaluation; on a 20-query subset, mean scores were 0.163, 0.153, and 0.149 at N = 5/10/20, with Pearson r ≥ 0.96 (Supplementary S6). N = 5 is therefore adequate for relative comparisons, but absolute scores are N-dependent and should not be compared across studies with different N.

#### 2.3.5 Cost and Inference Time Tracking

API costs are tracked per-query using a configurable pricing table derived from published API pricing for each model. For each query, prompt and completion tokens are recorded from all LLM calls in the pipeline — for NutriAgent, this includes the router call, each specialist's ReAct loop (which may involve multiple tool invocations and LLM reasoning steps), the synthesis call, and RAG retrieval/context construction. Token counts for each sub-component are tracked separately to enable fine-grained cost attribution.

Inference time measures wall-clock duration from query submission to final response, including tool execution, vector retrieval, and all LLM calls. Because specialists execute in parallel, adding more specialists does not linearly increase response time — a critical property for practical deployment.

The pricing model follows per-token costing for API-based models where the base LLM is accessed through a commercial API. For local models (e.g., Qwen3-Embedding-0.6B for vector embeddings), inference costs are computed based on estimated computational requirements, though these are negligible compared to API-based generation costs. All costs are reported in US dollars per query at provider list prices on 2026-10-20; Qwen AI Platform prices are converted from CNY at 7.2 CNY/USD. Inference time measurements were conducted on a workstation with an Intel processor and NVIDIA GeForce RTX 3060 GPU (6 GB), which hosted the local embedding and NLI models while LLM API calls were made over a broadband internet connection; full hardware and software versions are recorded in the run manifest (Supplementary S9).

**Repeat-run variability.** Temperature 0.0 reduces but does not eliminate sampling variability. In a 10-query × 3-run check with cache disabled, mean pairwise response similarity was 0.371 (range 0.106–0.870), no query produced identical responses, and the exact-match rate was 0. All scores reported here are from a single run per condition; small differences should be read with this run-to-run variance in mind, and repeat-averaged evaluation is left as future work.

---

### 2.4 Component Contribution Analysis

To isolate the contribution of each architectural component, we conduct the seven original sensitivity dimensions plus two factorial contrasts (E1 architecture and E2 synthesis; Table 2), following established ablation methodology in LLM agent systems (Tang et al., 2025; Bran et al., 2024). Each dimension is evaluated independently using the complete evaluation query set (n = 54), with all other architectural components held at their default configuration unless explicitly stated. The factorial contrasts replace the original D1/D5 attributions: they separate data/tool access, RAG, the extra synthesis call, decomposition, and consistency checking within one grid.

**Table 2.** Component contribution analysis dimensions, variants, and research questions. Specialist removal (D2) is purely architectural — no data is removed from the underlying tools. Language and breed are confounded in D7, so that comparison is exploratory.

| Dimension | Variants | Research Question |
|-----------|----------|-------------------|
| D1: Pipeline Architecture | Single ReAct / Multi-Agent (no tools) / Multi-Agent (single-pass tool call) / Multi-Agent (full) | Does tool access or iterative reasoning drive performance? |
| D2: Specialist Contribution | Full / w/o Feed / w/o Nutrition / w/o Performance / w/o Terminology | Which knowledge domains are most critical? |
| D3: Routing Strategy | LLM Router / Keyword Router / Broadcast (All) | Does routing precision affect end-to-end performance? |
| D4: Retrieval Augmentation | Multi-Agent + RAG / Multi-Agent (no RAG) | Does vector retrieval add value beyond structured tools? |
| D5: Synthesis Strategy | Concatenation / Validation + concatenation / Synthesis (validation off) / Synthesis (shuffled warnings) / Synthesis (correct warnings) / Query-only synthesis | Does integration or consistency checking drive the gain? |
| D6: LLM Backbone | Qwen3-8B / Qwen3.8-Flash / DeepSeek-V4-Flash / Qwen3.8-27B / DeepSeek-V4-Pro | Is the architecture robust across model capabilities? |
| D7: Bilingual | English (n=42) / Chinese (n=12) | Do results transfer to Chinese-language queries? |
| E1: Architecture factorial | Standalone LLM / Single ReAct + tools / Single ReAct + tools + RAG / Single ReAct + tools + RAG + synthesis / Multi-Agent (validation off) / Multi-Agent (validation on) | Which component — data access, RAG, extra synthesis, decomposition, or validation — drives performance? |
| E2: Synthesis factorial | Concatenation / Validation + concatenation / Synthesis (validation off/shuffled/correct) / Query-only synthesis | Does consistency checking add value beyond integration and the extra call? |

NutriAgent is evaluated against a single-agent variant and six standalone LLM baselines spanning four capability tiers: strong (DeepSeek-V4-Pro), mid (DeepSeek-V4-Flash, GLM-4.5-Air, MiniMax-M2.5), weak-mid (Qwen3.8-Flash), and weak (Qwen3-8B). The single-agent baseline uses one ReAct loop with all four tools and the same base LLM, isolating the contribution of the multi-agent architecture. Standalone LLM baselines access the base model without tools, RAG, or agent framework, quantifying the value added by the entire agent infrastructure. All baselines are commercial API models accessed through OpenAI-compatible endpoints (DeepSeek, 2026a, 2026b; MiniMax, 2026; Qwen, 2026b, 2026c; Z.ai, 2026). Standalone baselines use temperature 0.0, thinking disabled, and a maximum output length of 512 tokens. NutriAgent's specialists, router, and synthesis use the domain-specific prompts in Supplementary S2 and the role-specific token limits in Table 3; prompt content is therefore not identical across conditions by design, and Table 3 documents which components are shared. Exact provider, model ID, access date, thinking mode, and pricing date for every model are given in Table 3.

**Table 3.** Model versions and access (2026-10-20). Model aliases can change; the exact IDs, access date, and thinking mode are reported here and frozen in `config/models.lock.yaml`.

| Role | Provider | Model ID | Settings |
|---|---|---|---|
| NutriAgent backbone | SiliconFlow | `deepseek-ai/DeepSeek-V4-Flash` | T=0.0; thinking disabled; max 512 |
| EvaluatorLLM (primary) | Xiaomi | `mimo-v2.5-pro` | T=0.0; thinking enabled; max 8192 |
| EvaluatorLLM (robustness) | DeepSeek | `deepseek-v4-pro` | T=0.0; thinking enabled; max 8192 |
| Baseline: DeepSeek-V4-Flash | SiliconFlow | `deepseek-ai/DeepSeek-V4-Flash` | T=0.0; thinking disabled; max 512 |
| Baseline: DeepSeek-V4-Pro | DeepSeek | `deepseek-v4-pro` | T=0.0; thinking disabled; max 512 |
| Baseline: Qwen3-8B | SiliconFlow | `Qwen/Qwen3-8B` | T=0.0; thinking disabled; max 512 |
| Baseline: Qwen3.8-Flash | Qwen AI Platform | `qwen3.8-flash` | T=0.0; thinking disabled; max 512 |
| Baseline: GLM-4.5-Air | SiliconFlow | `zai-org/GLM-4.5-Air` | T=0.0; thinking disabled; max 512 |
| Baseline: MiniMax-M2.5 | Tencent TokenHub | `minimax-m2.5` | T=0.0; thinking disabled; max 512 |
| NLI model | local | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` | revision pinned in models.lock; file hashes in run manifest; GPU |
| Embedding model | local | `Qwen3-Embedding-0.6B` | 1,024 dimensions; GPU |

The submitted version reported DeepSeek-V4-Flash as accessed through SiliconFlow and MiMo-V2.5-Pro as the evaluator; the deposited run configurations instead show the DeepSeek official endpoint and DeepSeek-V4-Pro. Rev.1 re-ran all conditions on the model set in Table 3, and no score from the submitted model set is mixed with the Rev.1 results. Several submitted endpoints were retired; the current strongest baseline is stronger than the submitted strongest baseline (DeepSeek-V4-Pro 4.05 vs submitted DeepSeek-V4-Flash 3.80), so the smaller Rev.1 margin is partly a baseline-version effect. Supplementary S18 records the transition descriptively; because the submitted and Rev.1 scores use different expert/rubric passes, the table is not used for causal attribution.

---

## 3. Results and Discussion

> **Benchmark note.** Section 3.2 reports the completed Rev.1 expert-scored comparison (primary expert; 378 responses) on the frozen model set (Table 3); Section 3.3 uses the same expert scores. Sections 3.4–3.5 retain submitted-run automated metrics (inconsistency, readability, cost) where explicitly labeled; these were not recomputed for all Rev.1 methods. The factorial evidence (Tables 6 and S11) and the D2–D6 re-runs (Table 5) are on the frozen Rev.1 model set and are the basis for the component conclusions. We do not treat 4.42/3.80 or the submitted expert benchmark numbers as Rev.1 claims.

### 3.1 System Workflow Illustration

Before presenting the quantitative results, we illustrate NutriAgent's end-to-end processing through a concrete example (Fig. 4). The query asks whether limestone at 9% inclusion can meet the calcium requirement for ISA Brown in Lay I (C-XD-003 from the curated evaluation set). This multi-hop query requires the system to: (1) identify the calcium requirement for ISA Brown in Lay I, (2) retrieve the calcium content of limestone, and (3) compute the supplied calcium and judge whether 9% inclusion is sufficient.

![Fig. 4](assert/fig4_sequence_diagram.png)

**Fig. 4.** End-to-end pipeline workflow for query C-XD-003. The Router activates Nutrition and Feed specialists in parallel; each performs domain-specific tool calls within a ReAct loop. The Nutrition specialist retrieves the Lay I calcium requirement (4.04%), the Feed specialist retrieves limestone calcium (35.0%), and the synthesis stage computes 9% × 35.0% = 3.15% and judges it insufficient. The synthesis stage also checks cross-specialist consistency before integrating the results.

In this example, the Nutrition specialist retrieves the Lay I calcium requirement and the Feed specialist retrieves limestone's calcium content; the synthesis stage combines them into the inclusion calculation. The example is illustrative: it shows the information flow, not a measured benefit. The controlled architecture contrast in Table 6 (E1) quantifies the difference between this pipeline and a tool-only or standalone condition; we do not infer an advantage from a single query. The specialists may need multiple tool calls to gather comprehensive data, which the ReAct loop supports.

### 3.2 Overall Performance and Efficiency

**Response quality.** Table 9 reports the Rev.1 expert-scored comparison (54 queries, 378 responses; primary expert). The largest descriptive difference is numeric precision: 4.47 for NutriAgent vs 3.97 for the strongest baseline, DeepSeek-V4-Pro (+0.50; unadjusted p = 0.037; Holm-adjusted across all 24 dimension–baseline tests, p = 0.256), with Qwen3.8-Flash at 3.79 and the remaining baselines below 3.7. The precision contrast is therefore nominal rather than robust to family-wise correction. NutriAgent also has the numerically highest overall score (4.34 vs 4.05 for DeepSeek-V4-Pro), but this difference is not significant (paired per-response overall +0.20, p = 0.062), and correctness is comparable rather than superior (+0.20, 95% CI −0.09 to +0.50; Holm p = 0.146). The gap between the column means in Table 9 is 0.28, not the 0.62 in the submitted benchmark; the paired overall estimator is 0.20 because precision is missing for 16 queries (Table 10 note). Depth is lower than DeepSeek-V4-Flash (4.07 vs 4.33) and Qwen3.8-Flash (4.28); the architecture does not improve explanatory depth. The submitted claim that Qwen3-8B was the lowest baseline is not replicated: MiniMax-M2.5 is lowest (2.63), and Qwen3-8B is second lowest (3.04). Table 10 gives the paired contrasts: correctness differs significantly from DeepSeek-V4-Flash, Qwen3.8-Flash, GLM-4.5-Air, Qwen3-8B, and MiniMax-M2.5 after Holm correction, but not from DeepSeek-V4-Pro. Fig. 5 visualizes the same scores.

**Inter-rater reliability.** A repeat 120-response sheet from the primary expert gives intra-rater ICC(2,1) = 0.995 (correctness), 0.996 (precision), and 0.932 (depth), with weighted κ = 0.995/0.996/0.931 and Bland–Altman mean differences −0.02/−0.01/+0.08. This is a repeat/copy pass by the same rater, so it is not an independent rater and does not enter the inter-rater estimate. An independent third rater's 120 responses give ICC(2,1) = 0.847 (correctness), 0.876 (precision), and 0.760 (depth); quadratic weighted κ = 0.846/0.874/0.758; Spearman ρ = 0.862/0.913/0.725; Bland–Altman mean differences are −0.27/−0.11/+0.21 (95% limits −1.45/+0.92, −1.36/+1.14, −1.06/+1.48). Scores are reliable, but depth is the least reliable dimension, and the 120-response subset does not reproduce the full top rank: the independent rater's overall ordering places DeepSeek-V4-Flash (4.28) and DeepSeek-V4-Pro (4.14) close to NutriAgent (4.12). The primary 378-response analysis remains the basis for Table 9; the full agreement table is in Supplementary S15.

![Fig. 5](assert/fig5_main_comparison.png)

**Fig. 5.** Rev.1 expert benchmark (primary expert, n = 54). (a) Correctness, precision, and scientific depth with 95% bootstrap CIs. (b) Overall score with 95% CI; Overall = (mean C + mean P + mean D)/3. Inconsistency is not shown because it was not re-collected for all seven Rev.1 methods. Values in Table 9.

**Text quality.** In the submitted automated run, NutriAgent's SelfCheckGPT-NLI inconsistency score (0.117) is 70.0% lower than the submitted-run comparator DeepSeek-V4-Flash (0.390) and 65.5% lower than the baseline minimum Qwen3-8B (0.339) (Fig. 6); these are cross-sample consistency scores, not factual-error rates. NutriAgent's Flesch Reading Ease score (43.4) falls in the "difficult" range (30–50), reflecting the formulaic, data-dense style imposed by tool-mediated retrieval: responses enumerate specific parameter values, cite data sources, and include numerical precision that reduces sentence flow. Baseline scores range from 37.5 (GLM-4.5-Air) to 51.2 (DeepSeek-V4-Pro), slightly more readable on average. Whether this readability cost is acceptable depends on the deployment audience; we did not test reader comprehension, and producer-facing use may require supplementary explanations. Fig. 6 maps each method in readability–inconsistency space. Among baselines, more readable text tends to coincide with a higher inconsistency score; NutriAgent achieves a lower inconsistency score while maintaining comparable readability. The remaining inconsistency primarily reflects cross-sample variation in contextual descriptions rather than verified factual errors in core nutritional data.

![Fig. 6](assert/fig6_hallucination_readability.png)

**Fig. 6.** Submitted benchmark. Readability–inconsistency trade-off. Labels show (Flesch RE, inconsistency score) per method. Regression line fitted to baselines only. The axes are descriptive; no quadrant is labeled favorable or unfavorable.

**Cost and latency.** NutriAgent's multi-agent architecture incurs higher per-query cost (\$0.000723) and longer inference time (7.55 s) than standalone baselines in the submitted benchmark. The submitted cost figure did not include router and synthesis tokens, and no Rev.1 cost estimate was computed; the figure is therefore reported as a submitted-benchmark property, not as a Rev.1 measurement. In that benchmark, relative to the cheapest baseline (DeepSeek-V4-Flash: \$0.000054), NutriAgent is approximately 13× more expensive per query. Relative to the strongest submitted baseline (DeepSeek-V4-Flash: overall 3.80), it achieves a 0.62-point higher overall score (16.3% relative on the bounded 1–5 scale) and a 70.0% lower inconsistency score (0.390 to 0.117); the Rev.1 expert comparison supersedes these quality values. This trade-off may matter in applications where formulation accuracy has potential economic consequences, but we do not claim architecture-level cost efficiency.

![Fig. 7](assert/fig7_cost_quality.png)

**Fig. 7.** Submitted benchmark. Cost-quality trade-off. Labels show (Cost/query, Overall Quality) per method. X-axis: cost per query (USD, log scale). Y-axis: overall quality score. Bubble size proportional to quality. Reference lines at $0.0001 and $0.001 cost thresholds, and quality = 4.0 threshold.

**EvaluatorLLM–Expert agreement.** Against the completed primary-expert scores, the automated judge shows moderate-to-good rank agreement: Spearman ρ = 0.55 (95% CI 0.27–0.77; n = 54) for correctness, ρ = 0.34 (95% CI 0.06–0.59; n = 54) for scientific depth, and ρ = 0.71 (95% CI 0.51–0.84; n = 38) for precision. The corresponding within-one-point rates are 90.7%, 98.1%, and 94.7%. The judge is systematically more lenient than the expert on all three metrics (correctness 4.74 vs 4.46; depth 4.30 vs 4.07; precision 4.71 vs 4.47), indicating a calibration offset rather than a ranking failure. Precision agreement is therefore substantial, not negligible; the earlier ρ = 0.038 was computed against the submitted scores and is superseded. We still use the expert scores for the main comparison and the automated judge only for within-dimension ablation contrasts.

**Dimension-level agreement.** Because the expert scored only the 54-query main comparison and not the ablation variants, per-dimension agreement statistics cannot be computed from the deposited data. We therefore do not report dimension-level correlations; the ablation results are based on the automated judge and are interpreted as within-dimension relative contrasts, not as absolute quality estimates.


### 3.3 Performance Across Query Types and Knowledge Domains

Table 11 reports NutriAgent's Rev.1 expert scores by query type. The system is strongest on constraint (C 4.67; P 5.00), single-value (4.57/4.67), multi-hop (4.75/4.75), comparison (4.50/4.11), and definition queries (C 5.00; P N/A). It is weakest on open-ended queries (C 3.29; P 3.00), where DeepSeek-V4-Pro (4.43) and DeepSeek-V4-Flash (3.71) are higher, and on counterfactual depth (3.50 vs 4.67 for DeepSeek-V4-Pro). The advantage over the strongest baselines is therefore concentrated in structured retrieval and comparison, not in open-ended synthesis. The submitted values for counterfactual (5.00) and open-ended (3.86) are not replicated.

By knowledge domain, NutriAgent's expert correctness is highest for Definitions (4.83) and Performance Management (4.64), intermediate for Cross-Domain (4.50), Edge Cases (4.40), and Nutrient Requirements (4.33), and lowest for Feed Ingredient Bank (4.20); expert depth is highest for Feed (4.40) and lowest for Performance (3.82). The domain inconsistency scores in Table 4 are from the submitted automated run (0.062–0.177) and are not a Rev.1 expert measure; they are retained to show the structure-dependence pattern, not to rank Rev.1 systems.

![Fig. 8](assert/fig8_performance_breakdown.png)

**Fig. 8.** Rev.1 primary-expert breakdown (n = 54). (a) Correctness, precision, and scientific depth by query type; precision is plotted over the available numeric responses (P n=38 overall), and definition queries have no precision value, so their precision bars are omitted. (b) The same metrics by knowledge domain. Query-type values are in Table 11; domain values are in the text.

Fig. 9 visualizes the same domain C/D profile as a radar chart; larger area indicates stronger expert scores. The Rev.1 expert values are in Table 11 and the text above.

![Fig. 9](assert/fig9_domain_radar.png)

**Fig. 9.** Rev.1 primary-expert domain profile (C and D normalized to 0–1). Larger area indicates stronger expert scores; no inconsistency dimension is included.

Table 4 summarizes NutriAgent's SelfCheckGPT-NLI inconsistency score by knowledge domain from the submitted run, compared with DeepSeek-V4-Flash. Domain-specific inconsistency analysis reveals patterns obscured by aggregate metrics (Huang et al., 2025b; Maynez et al., 2020); these automated patterns are not a Rev.1 expert measure. The four tool-aligned domains each map to a dedicated specialist; cross-domain and edge-case queries span multiple specialists and are excluded from this per-tool comparison. NutriAgent's submitted-run inconsistency is lower than the comparator in all four domains, with the largest absolute reduction in Terminology (−0.423) and the smallest in Ingredient Composition (−0.176). This is a submitted-run pattern in a cross-sample consistency score; it does not establish a factual-reliability advantage, and the Rev.1 factorial and ablation results do not support one.

**Table 4.** Submitted run (archived model set; inconsistency was not recomputed for all Rev.1 methods). SelfCheckGPT-NLI inconsistency by knowledge domain: NutriAgent vs the submitted-run comparison baseline (DeepSeek-V4-Flash; n = 54).

| Knowledge Domain | n | NutriAgent | DeepSeek-V4-Flash | Δ |
|---|---|---|---|---|
| Nutrient Requirements | 12 | 0.062 | 0.456 | −0.394 |
| Ingredient Composition | 10 | 0.097 | 0.273 | −0.176 |
| Production Performance | 11 | 0.142 | 0.363 | −0.221 |
| Terminology | 6 | 0.177 | 0.600 | −0.423 |

**Error analysis.** Nine of 54 NutriAgent responses (17%) scored correctness ≤3 in the primary expert's sheet, and the notes point to five descriptive failure modes (Supplementary S10). (1) *Value substitution / approximate parametric values* (C-EC-002, C-FIB-006, C-NR-010, C-NR-011): the response gives a familiar breed or ingredient value that differs from the tool value, or treats an out-of-corpus breed as a related one. (2) *Unit/scale/source mismatch* (C-FIB-010): the system reports ME in MJ/kg rather than the bank's kcal/kg and labels an approximate source. (3) *Arithmetic error* (C-NR-008): 0.15 + 0.15 is computed as 0.375%. (4) *Retrieval/entity mismatch* (C-FIB-007): the retrieved feed item is the wrong entity (maize gluten feed instead of maize), although the caveat is stated. (5) *Refusal or incomplete synthesis* (C-PM-005, C-XD-008): the system refuses a multi-point body-weight question despite available data or omits the balancing steps. These categories are descriptive and single-coder (E14; Supplementary S10); they are not a two-coder error taxonomy. SelfCheckGPT does not detect them because it measures cross-sample consistency rather than factual correctness; the claim-aware faithfulness audit (Section 3.4) is the relevant check.

### 3.4 Faithfulness and Inconsistency Patterns (submitted metrics + Rev.1 audits)

Automated faithfulness and inconsistency metrics in this subsection are from the submitted run; they were not recomputed for all Rev.1 methods, and the expert scores do not include these metrics. The Rev.1 audits below (E3/E4/E6/E7/E14) are separate.

**Groundedness.** On 36 factoid queries, the submitted benchmark reported 75.0% accuracy at ±2% and 80.6% at ±5%; the Rev.1 responses give 83.3% and 88.9% (32/36 correct, four wrong values, none without a numeric answer) under the relative-error criterion. The relative-error and submitted interval rules agree on this set (E14; no case changed). Beyond ground-truth agreement, we assess response grounding using two operational metrics (Es et al., 2024): numeric faithfulness (fraction of extracted numbers within ±5% of any tool-returned value) and semantic faithfulness (fraction of non-numerical claims entailed by tool observations, measured via NLI). Numeric faithfulness is 0.444. Because the match ignores entity and unit, this value is not a provenance rate: about 56% of extracted numbers do not match any tool value, but that group includes derived values (ratios, percentages, unit conversions) as well as parametric values. A stricter claim-aware audit (E4) requires the entity and attribute to appear in the tool observations; direct support falls to 10.9–16.7% of extracted claims, with about 65% unsupported under this parser (Supplementary S7). This is a strict lower bound because the extractor finds about two claims per response and units are not fully parsed; human validation remains necessary. Semantic faithfulness is 0.811; evidence sentences omit some entity and unit context, so neutral or uncertain cases may be overcounted.

Low numeric faithfulness does not automatically imply factual errors: of the queries where numeric faithfulness fell below 0.3, the expert rated the majority as correct (correctness ≥ 4), indicating that the LLM's parametric knowledge often provides accurate supplementary values. However, a minority exhibited errors traceable to parametric override — most notably, the synthesis LLM substituting a commonly cited industry figure (38% Ca for limestone) for the tool-retrieved value (35%). This pattern suggests that while parametric supplementation is often benign, it introduces a systematic risk in edge cases where tool data diverges from commonly cited values.

**Inconsistency structure-dependence.** Inconsistency scores across domains (0.062–0.177) follow a pattern tied to data structure rather than query difficulty (Table 4). Nutrient Requirements achieves the lowest inconsistency score (0.062) because its data are organized as a structured matrix (breeds × phases × parameters) — tool returns leave essentially no numerical gaps for the LLM to fill generatively. Ingredient Composition shows a similarly low score (0.097) for the same reason: each ingredient has a fixed parameter set. Production Performance produces a higher score (0.142) because its time-series data (100-week trends) require the synthesis LLM to describe trends between retrieved points — a generative act that introduces variability across SelfCheckGPT samples. Terminology shows the highest score (0.177), likely reflecting the NLI model's sensitivity to paraphrase variation in prose-heavy definition responses rather than factual errors.

**Metric independence.** The faithfulness and inconsistency metrics capture dimensions distinct from expert-evaluated accuracy. SelfCheckGPT measures cross-sample consistency, not factual correctness — a model can produce a correct answer with varying paraphrases (high inconsistency score) or consistently reproduce an incorrect one (low inconsistency score). The Terminology domain illustrates this dissociation: perfect correctness (5.00) coexists with the highest inconsistency score (0.177). Similarly, faithfulness measures whether claims are grounded in tool data, not whether those claims are correct — a response can faithfully cite tool values yet draw wrong conclusions. These metrics therefore complement expert evaluation rather than replicating it.

### 3.5 Cross-Lingual Generalizability and Cost Efficiency (expert + automated checks)

**Cross-lingual generalization (exploratory).** The primary expert scored NutriAgent slightly lower on Chinese (n=12) than English (n=42) precision and depth but not correctness: C 4.42 vs 4.48, P 4.30 vs 4.54, D 4.00 vs 4.10. DeepSeek-V4-Pro shows a larger Chinese gap (C 4.00 vs 4.33), while DeepSeek-V4-Flash is similar (4.08 vs 4.05). Rev.1 automated scores show Chinese 4.92 vs English 4.69 correctness (n=12/42; 95% bootstrap CIs overlap), precision 4.80 vs 4.69, depth 4.42 vs 4.26. Neither source shows a large Chinese correctness deficit; the cross-lingual concern is the submitted-run inconsistency score, not correctness. Three confounding factors limit interpretation (Lai et al., 2023; Ahuja et al., 2023): language and breed are confounded; the Chinese sample is small (n=12), with insufficient power below Cohen's *d* ≈ 0.9 at α = 0.05; and the expert may have difficulty separating breed-specific data from general knowledge for less-documented Chinese breeds.

In the submitted run, the 3.1× increase in the SelfCheckGPT-NLI inconsistency score for Chinese queries is the more pronounced finding. Three compounding factors may explain this increase. First, DeepSeek-V4-Flash processes Chinese domain terminology less reliably than English poultry nutrition terms, creating more variability across SelfCheckGPT samples. Second, Chinese domestic breeds have thinner data coverage — both in absolute data volume and in tool descriptions — compared with well-documented international breeds such as Hy-Line and ISA Brown, leaving more room for the synthesis LLM to generate speculative content when tool data are sparse. Third, the NLI model (MoritzLaurer/mDeBERTa-v3-base-mnli-xnli) is multilingual but was not trained on poultry-nutrition claims; when SelfCheckGPT samples mix Chinese and English technical terms for the same concept, it may register spurious contradictions, inflating the score independently of actual factual errors. These mechanisms are hypotheses rather than demonstrated causes. This limitation is consistent with known challenges in cross-lingual NLI (Conneau et al., 2020; He et al., 2023).

Despite the inconsistency-score gap, NutriAgent produces breed-appropriate nutritional specifications for Chinese domestic breeds — a capability absent from existing English-centric poultry nutrition systems. As noted above, China produces more than 40% of the world's eggs (Yang, 2021), and the tool-mediated architecture enables coverage of breed populations with limited English documentation, even where inconsistency scores remain elevated. Reducing the cross-lingual inconsistency gap — through improved multilingual NLI models and expanded Chinese breed data — is a priority for future development.

![Fig. 10](assert/fig10_bilingual.png)

**Fig. 10.** Primary-expert bilingual comparison (English n=42; Chinese n=12). Bars show correctness, precision, and scientific depth; no inconsistency dimension is included.

**Cost efficiency.** NutriAgent's per-query cost (\$0.0007) reflects the multi-specialist pipeline overhead in the submitted run. The submitted version claimed a 5–6× token-cost ratio versus a single-agent design; that comparison was not token-matched, and we therefore do not report it as an architectural efficiency result. No Rev.1 cost estimate was computed; the submitted figure is not used to compare architectures.

### 3.6 Ablation and Comparison with Prior Systems

The preceding sections examined NutriAgent's end-to-end performance and reliability. We now address the questions underlying these results: which architectural components contribute most to the observed advantage, and how does the system compare with prior work? Each ablation dimension is evaluated independently with its own control condition; absolute scores for the same configuration may differ slightly across dimensions due to independent evaluation runs. Within-dimension relative differences (Δ) are the basis for all conclusions. This component-wise analysis follows the ablation methodology employed in prior agent system studies (Tang et al., 2025; Bran et al., 2024; Wu et al., 2023), adapted to the seven dimensions most relevant to our architecture.

#### 3.6.1 Component Contribution Analysis

Fig. 11 summarizes the key Rev.1 factorial and ablation contrasts: E1 tools-only and multi-agent vs standalone, E2 synthesis vs concatenation, D2 w/o Feed vs Full (+0.22), D3 broadcast vs LLM router (−0.04), D4 +RAG vs no RAG (0.00), and D6 Qwen3-8B vs DS-V4-Flash (−0.80). Exact values and sample sizes are in Tables 5 and 6. The bilingual dimension (D7) is discussed in Section 3.5; the architecture and synthesis attributions are replaced by the factorial contrasts (E1/E2) in Table 6. We use Correctness as the primary metric because it captures the overall quality dimension most relevant to user-facing performance; Precision, Depth, and SelfCheckGPT-NLI inconsistency are reported in Tables 5 and 6. The following subsections present each dimension in detail.

![Fig. 11](assert/fig11_ablation_bar.png)

**Fig. 11.** Key Rev.1 contrasts (correctness change vs control). Bars: E1 tools-only and multi-agent vs standalone; E2 synthesis vs concatenation; D2 w/o Feed vs Full; D3 broadcast vs LLM router; D4 +RAG vs no RAG; D6 Qwen3-8B vs DS-V4-Flash. n.s. = within run variance/not significant; exact values and n are in Tables 5 and 6. D4 is 0.00 on correctness (precision +0.04); D2's +0.22 means removing Feed does not hurt; D3's −0.04 is within noise. D1/D5 are replaced by the E1/E2 factorial contrasts; D7 (cross-language) is discussed in Section 3.5.

**Pipeline architecture (E1).** The factorial contrast (Table 6) separates five components that the original D1 comparison confounded. A tool-only single ReAct agent scores 4.31 correctness — below the standalone LLM (4.63) — so tool access alone does not improve judged quality. Adding RAG raises correctness to 4.54; adding the synthesis call without decomposition gives 4.48; the full multi-agent pipeline gives 4.74 with validation off and 4.83 with validation on. Depth shows a different pattern: validation off 4.35 > validation on 4.17 > standalone 4.15 > RAG 4.13 > synthesis-only 3.94 > tools-only 3.81. The decomposition gain is therefore concentrated in correctness and precision. Validation-on is slightly higher than validation-off (+0.09 C / +0.08 P), but E2's shuffled-warning control shows that the warning content is not responsible (+0.04 vs shuffled), so we do not attribute a reliable gain to validation; the E1 difference may reflect run noise or the additional context. These differences are small relative to judge calibration and are not significance-tested. The submitted D1 row labelled "no ReAct" is withdrawn: the implementation did not execute that condition, and the Rev.1 single-pass condition replaces it.

**Specialist contribution (D2).** All five conditions were re-scored in one pass (n=54 correctness). Full scores 4.44; removing Feed gives 4.67 (+0.22), removing Definitions 4.57 (+0.13), removing Performance 4.39 (−0.06), and removing Nutrition 4.37 (−0.07). No specialist removal lowers correctness materially, and removing Feed or Definitions is followed by a higher score. This does not replicate the submitted ordering (Performance −0.20, Nutrition −0.09, Feed −0.04), nor the earlier separate-pass read (Full 4.81, w/o Nutrition 4.86). The pattern is consistent with substantial redundancy across specialists, or with a judge preference for the simpler answers produced when a specialist is removed; it is not a clean per-specialist contribution. We therefore do not claim that each specialist is necessary. The Definitions specialist is retained for coverage and architectural symmetry, not because D2 demonstrates a measurable gain. D2 removes the specialist and its tool; because the shared PoultryDB can still surface public feed documents, it is an architectural-removal test, not a strict data-removal test; E7's data-removal test also found no degradation (4.70 vs 4.40). Single-run intervals are not computed; all cells are from the same pass and mode.

**Hard data removal (E7).** To test whether D2's architectural removal understates data dependence, E7 deleted the Feed specialist and filtered Feed Ingredient Bank documents out of RAG on 20 Feed/Cross-Domain queries. Correctness did not fall (4.70 vs 4.40), precision was +0.07, and depth was unchanged; the judge does not penalize the absence of feed grounding (n=20, single run). This is a negative result for the claim that feed data are necessary for judged quality, and it is consistent with E2's finding that the judge rewards answer form. It does not show that feed data can be removed in deployment; expert labels are needed to separate judge sensitivity from real information loss.

**Scoring-mode and scoring-pass check.** D2 Full/w/o Nutrition gives 4.04/3.98 under per-item scoring, 4.44/4.37 in the new bulk pass, and 4.81/4.86 in the original pass. Absolute levels shift by about 0.8 between scoring modes and by about 0.37 between passes, while the ordering is consistent. All D2 cells are now from one pass; we compare only within the same pass and mode.

**Routing Strategy (D3).** At n=54, the LLM Router scores 4.63 correctness (P 4.56, D 3.96), Broadcast 4.59 (P 4.47, D 4.00), and Keyword 4.48 (P 4.26, D 3.76). The LLM router is therefore highest, Broadcast is within 0.04, and Keyword is 0.15 lower. The earlier n=44 read (LLM 4.63, Keyword 4.64, Broadcast 4.68; spread ≤0.05) is not replicated: it suggested no routing effect and a small Broadcast advantage, whereas the complete data show a Keyword deficit. Single-run differences of this size are not significance-tested; we do not claim a routing gain, but we also no longer claim that routing is irrelevant. The Keyword fallback is retained for availability, not because it matches the LLM router.

**Retrieval Augmentation (D4).** In the n=54 re-score, +RAG scores 4.52 correctness (n=54) and no-RAG scores 4.52 (n=54): the difference is 0.00. Precision is +0.04 (4.37 vs 4.33; n=46/45) and depth is −0.22 (3.74 vs 3.96; no-RAG n=46). The earlier +0.14 correctness / −0.13 precision trade-off (n=44/34) is not replicated. RAG is therefore a null result on correctness and precision; the depth difference favors no-RAG but is incomplete. The submitted +0.08 correctness / +0.10 precision claim is also not replicated. Because the Rev.1 re-score did not retain a retrieval-failure flag, we report a conservative proxy ITT (16 E6 hit@5 misses scored 1): +RAG 3.50 vs no-RAG 4.52 correctness (Δ −1.02; 95% CI −1.52 to −0.52; p < 0.001), with a 0-score sensitivity and a complete-case null. This is a sensitivity analysis, not an exact reconstruction of the submitted four-query exclusion (Supplementary S19). We do not claim a RAG benefit or a precision cost; the exact k-sensitivity remains incomplete (E6).

**Synthesis strategy (E2).** The submitted D5 comparison changed concatenation, validation, and an extra LLM call at once, so it cannot attribute the gain to consistency checking. E2 holds the specialist outputs and output budget fixed and varies six conditions: concatenation; concatenation plus validation warnings; synthesis with validation off; synthesis with shuffled warnings; synthesis with correct warnings; and query-only synthesis. Results are reported in Table 6. The consistency checker now compares entity, attribute, unit, and basis; the submitted Ca:P rule, which produced false positives, is opt-in and was disabled for the reported runs. The synthesis stage still has two channels: it flags cross-specialist contradictions, and it requires the integration LLM to cite tool-retrieved values rather than substitute parametric knowledge. Fig. 12 illustrates a residual failure of the latter kind; the example predates the entity-aware checker and is retained to show the failure mode.

The synthesis mechanism operates through two channels. First, the consistency checker compares numerical claims from different specialists on the same entity, attribute, unit, and basis — for example, the calcium content of limestone reported by the Feed specialist and the value used by the Nutrition specialist — and emits a warning rather than silently choosing one. Second, grounded integration requires the synthesis LLM to cite tool-retrieved values when constructing its response, reducing the tendency to substitute parametric knowledge for observed data. The first channel addresses inter-specialist inconsistency; the second addresses the intra-response faithfulness problem where pre-training knowledge overrides tool outputs. Whether these channels improve judged quality beyond concatenation is the question E2 is designed to answer, and we do not assume a positive answer.

**E2.** Concatenation scores 4.28 correctness; adding validation warnings to concatenation gives 4.11; synthesis with shuffled warnings gives 4.87; synthesis with validation off gives 4.91; and query-only synthesis gives 4.85. **Validation-off and correct-warnings are identical at 4.91**, shuffled is 4.87, and query-only is 4.85, so neither the warning content nor the specialist outputs explain the increase. The parsimonious reading is that the extra synthesis call — or a judge preference for polished, structured prose — drives the score, not cross-specialist integration or validation. This pattern does **not** support the submitted claim that cross-validation between specialists is the primary quality driver. No expert scoring of the E2 conditions was performed, so the E2 pattern is an automated-judge result and is reported as such; a human-scored E2 subset is future work.

![Fig. 12](assert/fig12_query_response.png)

**Fig. 12.** Query-response examples. Left (C-XD-007): multi-hop calculation with unit conversion and sufficiency judgment. Right (C-XD-003): constraint reasoning with a data inconsistency — the synthesis LLM substitutes a parametric value (38% Ca) for the tool-retrieved value (35%). The example predates the entity-aware checker and is retained to show the residual failure mode; the checker's rule coverage is reported in Supplementary S7b and its entity-resolution limits in §2.1.1.

**Language Model Backbone (D6).** At n=54, DeepSeek-V4-Pro scores 4.67, DeepSeek-V4-Flash 4.61, Qwen3.8-27B 4.50, Qwen3.8-Flash 4.43, and Qwen3-8B 3.81. The submitted ordering (DeepSeek-V4-Flash 4.85 > DeepSeek-V4-Pro 4.74 > Qwen3.6-Plus 4.69 > Qwen3.5-Flash 4.44 > Qwen3-8B 4.11) is not replicated: the top two swap, but the gap is only 0.06, and DeepSeek-V4-Flash has higher depth (4.04 vs 3.87). Qwen3-8B remains clearly weakest (−0.80 correctness and −1.11 depth vs DeepSeek-V4-Flash). The C cells are complete (n=54); precision is n=45–46. We treat the top-two ordering as provisional and the Qwen3-8B deficit as the robust finding.

Qwen3-8B in the multi-agent pipeline reaches 3.81 correctness with depth 2.93, versus 4.67/3.87 for DeepSeek-V4-Pro; the architecture does not compensate for a weak backbone's depth deficit. Tool access can ground factual retrieval, but explanation quality remains constrained by the base model.

Scientific depth is consistently lower than correctness across backbones (e.g., DeepSeek-V4-Pro 3.87 depth vs 4.67 correctness; DeepSeek-V4-Flash 4.04 vs 4.61), and the gap is largest for Qwen3-8B (2.93 vs 3.81). The pipeline improves correctness through grounded retrieval but does not inherently improve domain explanations.

**Summary.** The factorial contrast (Table 6) replaces the submitted D1/D5 attributions: tool access alone scores below the standalone LLM; in the single-agent template, RAG recovers part of the gap (4.54), and the full multi-agent pipeline scores higher (4.74/4.83), but D2 shows that this gain is not attributable to individual specialist content and E2 associates it with the extra synthesis pass rather than validation. Validation itself shows no measurable gain once the extra synthesis pass is controlled. Among the remaining dimensions, the LLM backbone (D6) is the largest: Qwen3-8B drops −0.80 correctness and −1.11 depth versus DeepSeek-V4-Flash, while DeepSeek-V4-Pro gains only +0.06; the exact top-two ordering is not replicated, although all D6 correctness cells are now n=54. The Rev.1 D2 same-pass re-run gives no positive specialist contribution: removing Feed +0.22 and Definitions +0.13, while Nutrition/Performance are −0.07/−0.06, so specialist removal does not support a per-specialist contribution. The Rev.1 D3 n=54 re-run gives LLM Router 4.63 > Broadcast 4.59 > Keyword 4.48; Keyword is 0.15 lower, so routing is not entirely null, although no router beats the LLM router. Within the full multi-agent system, the Rev.1 D4 re-run (n=54) shows no correctness difference (4.52 vs 4.52), precision +0.04, and depth −0.22, so RAG's correctness benefit is a null result in this context; the earlier single-agent RAG gain (E1) does not transfer to the full pipeline. The synthesis-stage attribution is tested separately in E2; query-only synthesis matches full synthesis, so we do not assume that consistency checking is the driver.

**Table 5.** Component contribution analysis. D2–D6 are Rev.1 re-runs on the frozen model set. All correctness cells are n=54; each dimension was scored in its own pass, so absolute levels are not comparable across dimensions, and precision/depth cells with n<54 are marked in the n column (D2: Full 54/46/54, w/o Nutrition 54/46/51, w/o Performance 54/46/53, w/o Feed 54/46/53, w/o Definitions 54/46/52; D3: LLM 54/45/54, Broadcast 54/43/54, Keyword 54/46/54; D4: no RAG 54/45/46, +RAG 54/46/54; D6: Pro 54/46/54, Flash 54/46/54, 27B 54/45/54, Flash-8 54/46/54, Qwen3-8B 54/45/46). ΔC = within-dimension correctness change relative to the dimension's control (—). Inconsistency is not available for D2–D6 (SelfCheck skipped). Bulk and per-item scoring differ in absolute level; the D2 per-item sensitivity check is reported in §3.6.1 and is not pooled into this table.

| Dimension | Variant | Correctness | ΔC | Precision | Depth | Inconsistency |
|-----------|---------|-------------|-----|-----------|-------|---------------|
| **D2: Specialist (Rev.1)** | Full (4 Specialists) | 4.44 | — | 4.39 | 4.00 | N/A |
| | w/o Nutrition | 4.37 | −0.07 | 4.20 | 3.98 | N/A |
| | w/o Performance | 4.39 | −0.06 | 3.98 | 3.72 | N/A |
| | w/o Feed | 4.67 | +0.22 | 4.48 | 3.94 | N/A |
| | w/o Definitions | 4.57 | +0.13 | 4.43 | 3.79 | N/A |
| **D3: Routing (Rev.1)** | LLM Router | 4.63 | — | 4.56 | 3.96 | N/A |
| | Broadcast (All) | 4.59 | −0.04 | 4.47 | 4.00 | N/A |
| | Keyword Router | 4.48 | −0.15 | 4.26 | 3.76 | N/A |
| **D4: RAG (Rev.1)** | Multi-Agent (no RAG) | 4.52 | — | 4.33 | 3.96 | N/A |
| | Multi-Agent + RAG | 4.52 | 0.00 | 4.37 | 3.74 | N/A |
| **D6: LLM Backbone (Rev.1)** | DeepSeek-V4-Flash | 4.61 | — | 4.48 | 4.04 | N/A |
| | DeepSeek-V4-Pro | 4.67 | +0.06 | 4.48 | 3.87 | N/A |
| | Qwen3.8-27B | 4.50 | −0.11 | 4.24 | 3.69 | N/A |
| | Qwen3.8-Flash | 4.43 | −0.18 | 4.17 | 3.80 | N/A |
| | Qwen3-8B | 3.81 | −0.80 | 3.78 | 2.93 | N/A |

**Table 6.** Factorial contrasts on the Rev.1 model set. E1 architecture factorial: six conditions, same backbone and output budget (n = 54). Per-query scores for the synthesis-only and multi-agent conditions are in `docs/paper/audit/e1_rescored.json`; the remaining E1 conditions are in `logs/ablation_architecture_factorial_layer_20261020_181143/responses.json`. E2 per-query scores for validation+concatenation, validation-off, and query-only synthesis are in `docs/paper/audit/e2_rescored.json`; concatenation, shuffled-warning, and correct-warning conditions are in `logs/ablation_synthesis_factorial_layer_20261020_193244/responses.json`.

| Contrast | Variant | Correctness | Precision | Depth | n (C/P/D) |
|---|---|---|---|---|---|
| E1 | Standalone LLM | 4.63±0.78 | 4.44±0.84 | 4.15±0.81 | 54/41/54 |
| E1 | Single ReAct + tools | 4.31±1.36 | 4.41±1.37 | 3.81±1.30 | 54/39/54 |
| E1 | Single ReAct + tools + RAG | 4.54±1.14 | 4.51±1.20 | 4.13±1.17 | 54/43/54 |
| E1 | Single ReAct + tools + RAG + synthesis | 4.48±1.13 | 4.26±1.41 | 3.94±1.27 | 54/46/54 |
| E1 | Multi-Agent (validation off) | 4.74±0.65 | 4.64±0.86 | 4.35±0.73 | 54/45/54 |
| E1 | Multi-Agent (validation on) | 4.83±0.42 | 4.72±0.77 | 4.17±0.77 | 54/43/54 |
| E2 | Concatenation | 4.28±1.32 | 4.41±1.20 | 3.69±1.21 | 54/41/54 |
| E2 | Validation + concatenation | 4.11±1.30 | 4.14±1.37 | 3.74±1.18 | 54/42/54 |
| E2 | Synthesis (shuffled warnings) | 4.87±0.44 | 4.84±0.64 | 4.37±0.78 | 54/44/54 |
| E2 | Synthesis (validation off) | 4.91±0.35 | 4.78±0.84 | 4.35±0.68 | 54/46/54 |
| E2 | Query-only synthesis | 4.85±0.49 | 4.83±0.49 | 4.44±0.66 | 54/46/54 |
| E2 | Synthesis (correct warnings) | 4.91±0.29 | 4.83±0.44 | 4.35±0.59 | 54/42/54 |

E2 rows are complete at n = 54. Validation-off and correct warnings are identical at 4.91, shuffled is 4.87, and query-only synthesis is 4.85 — the E2 pattern does not support an integration/validation benefit; the extra synthesis call (or a judge style effect) is the more parsimonious explanation. No expert scoring of the E2 conditions was performed; a human-scored E2 subset is stated as future work.

**Table 7.** Summary of claim calibration under the Rev.1 model set. Full 14-row matrix in Supplementary S17. "Not supported" means the Rev.1 evidence does not reproduce the direction or magnitude; "withdrawn" means the condition did not execute as described.

| Submitted claim | Rev.1 evidence | Status |
|---|---|---|
| NutriAgent 4.42 vs 3.80 (+0.62); DeepSeek-V4-Flash strongest | Rev.1 expert: 4.34 vs 4.05 (DeepSeek-V4-Pro strongest); ΔC +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146); ΔP +0.50 (unadjusted p = 0.037; Holm across all dimension tests p = 0.256) | **Not replicated; precision-led descriptively, not a corrected-significance gain** |
| Synthesis / cross-validation is the dominant driver (+24.2% C, −29.7% inconsistency) | E2: validation-off 4.91 = correct warnings 4.91; shuffled 4.87; query-only 4.85; concatenation 4.28 | **Not supported; extra synthesis pass, not validation content** |
| Multi-agent beats single agent by +5.3% C / −48.3% inconsistency | No-ReAct row was a duplicate full-pipeline run and is withdrawn; E1 tools-only 4.31 < standalone 4.63; multi-agent 4.74/4.83 | **Withdrawn** |
| Each specialist contributes; Feed data are necessary | D2 removal does not reduce quality; E7 Feed hard removal 4.70 vs full 4.40 (single run) | **Not replicated; no positive specialist effect** |
| RAG improves correctness and precision | D4 complete case: +RAG 4.52 vs no-RAG 4.52; C 0.00, P +0.04. Proxy ITT (16 E6 misses = failure 1): 3.50 vs 4.52; Δ −1.02 (95% CI −1.52 to −0.52; p < 0.001); S19 | **Null complete-case; negative proxy ITT** |
| Hallucination −70%; 56% parametric; evaluator ρ = 0.83/0.67/0.37 | Inconsistency metric renamed; claim-aware support 10.9–16.7%; evaluator ρ = 0.55/0.34/0.71 against Rev.1 expert | **Reframed/corrected** |

#### 3.6.2 Comparison with Prior Systems

NutriCHAT (Mandiga et al., 2026) is the closest comparable system — both target poultry nutrition with four domain-specific tools covering feed composition, nutrient requirements, production performance, and terminology. Direct quality-level comparison is confounded by differences in species, query sets, evaluator identity, and scoring protocols (Table 8). We therefore focus on architectural design differences.

**Table 8.** NutriAgent vs NutriCHAT design comparison. Quality metrics are not directly comparable due to different evaluation methodologies; architectural and procedural differences are the basis for comparison.

| Dimension | NutriAgent | NutriCHAT |
|-----------|-----------|-----------|
| Species | Layer (17 breeds, Chinese domestic included) | Broiler (Ross, Cobb) |
| Language | English + Chinese | English only |
| Agent architecture | Multi-agent (Router + 4 Specialists + Synthesis) | Single-agent (ReAct + RAG) |
| Tool isolation | Per-specialist context window | Shared context window |
| Cross-specialist consistency checking | Synthesis Agent (entity/attribute-aware checks + grounded integration) | None |
| Evaluation | 1 primary expert (378) + independent 120-response rater (ICC 0.85 C); EvaluatorLLM (MiMo-V2.5-Pro) | 2 experts (κ = 0.60–0.73) + EvaluatorLLM (Claude Sonnet 4.5) |
| Faithfulness | Numeric + Semantic metrics (Section 3.4) | Not assessed |
| Queries | 54 curated (7 types) | 120 expert-reviewed (3 types) |
| Cost/Query | $0.0007 (not directly comparable) | $0.0124 |

*Agent architecture.* NutriCHAT routes all four tools through a single ReAct reasoning chain. NutriAgent decomposes the pipeline into four specialist agents with a separate synthesis step that checks cross-specialist consistency before generating the final response. The factorial synthesis contrast (Section 3.6.1, E2) separates integration from consistency checking; we do not attribute the synthesis-stage gain to validation alone.

*Tool isolation.* In NutriCHAT, all tool descriptions share a single context window, creating competition for attention during tool selection (Qin et al., 2024). NutriAgent assigns each specialist its own tool subset, ensuring that reasoning agents see only domain-relevant tools. This isolation eliminates inter-tool competition at the cost of requiring a routing mechanism to direct queries to the appropriate specialist.

*Evaluation and faithfulness.* NutriCHAT employs dual-expert scoring (Cohen's kappa = 0.60–0.73) with EvaluatorLLM (Claude Sonnet 4.5), while NutriAgent uses one primary expert, an independent 120-response reliability check, and an automated judge (MiMo-V2.5-Pro) with response order randomization. NutriAgent additionally introduces faithfulness metrics (Section 3.4) to quantify grounding in tool-retrieved evidence — an assessment not conducted by NutriCHAT. These methodological differences preclude direct quality-level comparison; the architectural and procedural distinctions in Table 8 are the basis for comparison.

*Cost efficiency.* The reported costs are not directly comparable because the systems use different backbone models, providers, pricing dates, and workloads. NutriCHAT uses GPT-4o for its ReAct and response-generation components (Claude Sonnet 4.5 is its EvaluatorLLM), whereas NutriAgent uses DeepSeek-V4-Flash. The \$0.0007 versus \$0.0124 figures therefore reflect model price and experiment design rather than architectural efficiency, and we do not interpret them as evidence that the architecture itself is cheaper.

**Design insights.** The broader landscape of domain-specific agent systems (Table 1) spans single-agent designs (NutriCHAT, ChemCrow, ChemAgent, Biomni) and multi-agent designs (NutriAgent, BioMaster). Within agricultural applications, NutriAgent combines multi-agent orchestration with structured tool access, external corpus retrieval, faithfulness assessment, and bilingual support. These capabilities are individually present in other systems; their combination in a single agricultural QA pipeline is less commonly reported, and we frame it as an observed gap in the literature we surveyed rather than a categorical first (Table S4).

**Table 9.** Rev.1 expert-scored main comparison (54 queries; 378 responses; primary expert). C = correctness, P = precision (numeric queries only; n=38), D = scientific depth; Overall = (mean C + mean P + mean D)/3. CIs are 95% percentile bootstrap intervals (10,000 resamples, query-level). Because P is missing for 16 queries, the difference in these Overall column means (+0.28) is not the same estimator as the paired per-response overall in Table 10 (+0.20); both are reported, and the paired estimator is used for inference.

| Method | Correctness (95% CI) | Precision (95% CI) | Depth (95% CI) | Overall (95% CI) | n (C/P/D) |
|---|---|---|---|---|---|
| NutriAgent | **4.46** (4.19–4.70) | **4.47** (4.11–4.79) | 4.07 (3.89–4.26) | **4.34** (4.10–4.54) | 54/38/54 |
| DeepSeek-V4-Pro | 4.26 (4.04–4.48) | 3.97 (3.68–4.26) | 3.93 (3.69–4.17) | 4.05 (3.87–4.23) | 54/38/54 |
| DeepSeek-V4-Flash | 4.06 (3.80–4.32) | 3.74 (3.40–4.05) | **4.33** (4.15–4.52) | 4.04 (3.84–4.24) | 54/38/54 |
| Qwen3.8-Flash | 3.96 (3.70–4.22) | 3.79 (3.45–4.13) | 4.28 (4.11–4.44) | 4.01 (3.80–4.22) | 54/38/54 |
| GLM-4.5-Air | 3.74 (3.41–4.06) | 3.63 (3.24–4.00) | 3.28 (3.11–3.44) | 3.55 (3.28–3.80) | 54/38/54 |
| Qwen3-8B | 3.13 (2.76–3.52) | 2.87 (2.40–3.34) | 3.13 (2.93–3.33) | 3.04 (2.72–3.36) | 54/38/54 |
| MiniMax-M2.5 | 2.80 (2.43–3.17) | 2.53 (2.10–2.97) | 2.56 (2.24–2.87) | 2.63 (2.29–2.96) | 54/38/54 |

**Table 10.** Paired comparisons against NutriAgent (same 54 queries). Δ = NutriAgent − baseline; CIs are paired bootstrap intervals; p is Wilcoxon signed-rank with Holm correction across the six C comparisons; d_z is the paired effect size. P/D/O contrasts are descriptive (unadjusted). ΔO is the paired per-response overall (each response's mean of available dimensions), not the difference of the three dimension means; the latter is 0.28 for DeepSeek-V4-Pro.

| Baseline | ΔC | 95% CI | p (Holm) | d_z | ΔP | ΔD | ΔO |
|---|---:|---|---:|---:|---:|---:|---:|
| DeepSeek-V4-Pro | +0.20 | −0.09, +0.50 | 0.146 | +0.18 | +0.50 | +0.15 | +0.20 |
| DeepSeek-V4-Flash | +0.41 | +0.09, +0.70 | 0.026 | +0.36 | +0.74 | −0.26 | +0.20 |
| Qwen3.8-Flash | +0.50 | +0.17, +0.81 | 0.014 | +0.41 | +0.68 | −0.20 | +0.26 |
| GLM-4.5-Air | +0.72 | +0.35, +1.11 | 0.003 | +0.50 | +0.84 | +0.80 | +0.76 |
| Qwen3-8B | +1.33 | +0.94, +1.74 | <0.001 | +0.87 | +1.60 | +0.94 | +1.21 |
| MiniMax-M2.5 | +1.67 | +1.24, +2.09 | <0.001 | +1.04 | +1.95 | +1.52 | +1.65 |

**Table 11.** NutriAgent Rev.1 expert scores by query type (n=54; primary expert). Precision is N/A for definition queries and for responses with no numeric answer (P n=38 overall; per-type P denominators are single-value 18, comparison 9, multi-hop 4, constraint 3, counterfactual 2, open-ended 2).

| Query type | n | C | P | D |
|---|---:|---:|---:|---:|
| Single-value | 21 | 4.57 | 4.67 | 4.00 |
| Comparison | 10 | 4.50 | 4.11 | 4.50 |
| Multi-hop | 4 | 4.75 | 4.75 | 4.00 |
| Constraint | 3 | 4.67 | 5.00 | 4.33 |
| Counterfactual | 2 | 4.50 | 4.50 | 3.50 |
| Definition | 7 | 5.00 | N/A | 4.29 |
| Open-ended | 7 | 3.29 | 3.00 | 3.57 |

## 4. Conclusion

We present NutriAgent, a specialist-routed multi-agent architecture for layer hen nutrition question answering that integrates four domain specialists (Feed, Nutrition, Performance, Terminology) with consistency-checked synthesis across 17 breeds including Chinese domestic strains.

The Rev.1 evidence is more conditional than the submitted version. The architecture factorial (Table 6) shows that tool access alone does not improve judged quality over a standalone LLM; in the single-agent template, RAG recovers part of the gap, and the full multi-agent pipeline scores higher, but D2 and E2 show that this gain is not attributable to individual specialist content or validation — the extra synthesis pass is associated with higher scores. Within the full multi-agent system, D4 shows that adding RAG does not improve correctness or precision. These contrasts replace the submitted claims that synthesis/cross-validation was the dominant driver and that the multi-agent pipeline improved correctness by 5.3% while reducing inconsistency by 48.3%; the no-ReAct row was produced by a dispatch defect and is withdrawn. Table 7 summarizes which submitted claims replicate; the surviving positive is narrower: precision on structured queries, not uniform architecture superiority.

The automated judge agrees moderately with the expert on correctness (ρ = 0.55) and depth (ρ = 0.34) and better on precision (ρ = 0.71), while scoring more leniently; the factorial results are within-dimension contrasts; the Rev.1 main comparison (Table 9) places NutriAgent highest overall (4.34 vs 4.05 for DeepSeek-V4-Pro), but the correctness advantage is not significant after Holm correction and the precision advantage does not survive family-wise correction across all dimensions. The bilingual evaluation is exploratory and confounded by breed and data coverage. The self-consistency score is not a factual-error rate, and the numeric-faithfulness metric is permissive; a claim-aware grounding analysis is reported separately.

We frame the design implication as a testable hypothesis rather than a general principle: in retrieval-dominated nutrition QA, grounding and integration matter more than the number of specialists, and consistency checking is worth its cost only when specialist outputs overlap on the same entity and attribute. Future work should test this with deconfounded bilingual data, external held-out queries, and prospective formulation validation.

## Limitations

Several limitations bound the claims. First, the primary comparison uses one poultry nutrition expert; a repeat 120-response sheet from the same expert gives intra-rater ICC(2,1) = 0.995/0.996/0.932 (correctness/precision/depth), but it is a repeat/copy pass and not independent, while an independent 120-response rater gives ICC = 0.85/0.88/0.76 and the 120 subset does not reproduce the full top rank (DeepSeek-V4-Flash 4.28 and DeepSeek-V4-Pro 4.14 vs NutriAgent 4.12); full dual scoring of all 378 responses is not available. Second, the ablation results rely on an automated judge whose agreement with the expert is moderate (ρ = 0.55 for correctness, 0.34 for depth, 0.71 for precision); the judge scores more leniently, and the ablation results are within-dimension contrasts, not absolute quality estimates. Third, we did not obtain an external held-out query set authored by nutritionists outside the project; the 195-query pool will be available in the repository but was not used as an extended set. The 54-query set was reviewed by two team-internal experts, not by an external independent panel, so query-selection bias cannot be fully excluded. Fourth, the numeric faithfulness metric uses a permissive any-number match; a claim-aware audit would be needed for a provenance-level conclusion. Fifth, the self-consistency score is not a factual-error rate. Sixth, the bilingual comparison is confounded by breed and data coverage and is exploratory; the feed tool's entity index is English-only, so Chinese ingredient names depend on the model translating them, and a 39-case test found 0% direct Chinese resolution and a 37.5% family-correct rate for misspellings. Seventh, the model set changed during revision because several provider entry points were retired; all Rev.1 results use one frozen model set (Table 3), and no score from the submitted model set is mixed with Rev.1. Finally, the system provides informational retrieval; we did not validate complete ration formulations prospectively with nutritionists.

## Data and code availability

The curated 54-query set with ground-truth annotations, system and specialist prompts, configuration files, evaluation and figure-generation scripts, and per-query scores will be available at https://github.com/sepnlab/NutriAgent; the sanitized release is prepared and will be public before resubmission. A Zenodo archive DOI is optional and will be added only if an archive is created. Per-query scores are in `docs/paper/audit/e1_rescored.json`, `e2_rescored.json`, `d2_rescored_all.json`, `d3_rescored.json`, `d4_rescored.json`, `d6_rescored.json`, and `e18_rescored.json` (the last covers the NutriCHAT comparator only); the blinded expert sheets are `expert_eval_all.csv` (378 rows) and `expert_eval_second_rater.csv` (120 rows); completed normalized expert scores are `expert_scores_primary.csv`, `expert_scores_second.csv`, and `expert_scores_third.csv`, with the analysis in `expert_analysis.json`/`.md`; the validator, retrieval, repeat-run, and entity-resolution audits are in the same directory. The corpus is derived from public feed tables (INRAE-CIRAD-AFZ, feedtables.com) and breeder/company documentation; Table S3 summarizes the source type and status for each dataset, and `corpus/provenance.csv` records the document title, version, URL, extraction date, and license where available, flagging entries that still need a primary source or version. Chinese domestic-breed specifications compiled through jbzyw.com are redistributed only to the extent permitted by the source; otherwise the table records the source and the extraction procedure.

## Competing interests

The authors declare no competing interests. No animal experiments were conducted; all data are from public sources.

## Funding

This work was financially supported by the National Key Research and Development Program of China (No. 2021YFD1300405) and the Key Research and Development Program of Shandong Province (No. 2024CXPT025).

Supplementary material associated with this article is provided as an independent separate document during submission.

---

## References

Abdel-Wareth, A.A., Ahmed, A.A., 2026. Advancing poultry nutrition: AI innovations for sustainable nutrient requirements of poultry: a review. Agriculture 16(4), 450. https://doi.org/10.3390/agriculture16040450

Ahuja, K., Diddee, H., Hada, R., Ochieng, M., Ramesh, K., Jain, P., Nambi, A., Ganu, T., Segal, S., Ahmed, M., Bali, K., Sitaram, S., 2023. MEGA: multilingual evaluation of generative AI, in: Bouamor, H., Pino, J., Bali, K. (Eds.), Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Singapore, pp. 4232–4267. https://doi.org/10.18653/v1/2023.emnlp-main.258

Bain, M.M., Nys, Y., Dunn, I.C., 2016. Increasing persistency in lay and stabilising egg quality in longer laying cycles. What are the challenges? Br. Poult. Sci. 57, 330–338. https://doi.org/10.1080/00071668.2016.1161727

Balaguer, A., Benara, V., Cunha, R.L. de F., Filho, R. de M.E., Hendry, T., Holstein, D., Marsman, J., Mecklenburg, N., Malvar, S., Nunes, L.O., Padilha, R., Sharp, M., Silva, B., Sharma, S., Aski, V., Chandra, R., 2024. RAG vs fine-tuning: pipelines, tradeoffs, and a case study on agriculture. https://doi.org/10.48550/arXiv.2401.08406

Berckmans, D., 2017. General introduction to precision livestock farming. Anim. Front. 7, 6–11. https://doi.org/10.2527/af.2017.0102

Bran, A.M., Cox, S., Schilter, O., Baldassari, C., White, A.D., Schwaller, P., 2024. Augmenting large language models with chemistry tools. Nat. Mach. Intell. 6, 525–535. https://doi.org/10.1038/s42256-024-00832-8

Chang, Yupeng, Wang, X., Wang, J., Wu, Y., Yang, L., Zhu, K., Chen, H., Yi, X., Wang, C., Wang, Y., Ye, W., Zhang, Y., Chang, Yi, Yu, P.S., Yang, Q., Xie, X., 2024. A survey on evaluation of large language models. ACM Trans. Intell. Syst. Technol. 15. https://doi.org/10.1145/3641289

Chroma, 2026. Chroma — open-source AI application database [WWW Document]. URL https://www.trychroma.com/

Cohen, J., 2013. Statistical power analysis for the behavioral sciences, 2nd ed. Routledge, New York, NY, USA. https://doi.org/10.4324/9780203771587

Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzmán, F., Grave, E., Ott, M., Zettlemoyer, L., Stoyanov, V., 2020. Unsupervised cross-lingual representation learning at scale, in: Jurafsky, D., Chai, J., Schluter, N., Tetreault, J. (Eds.), Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, Online, pp. 8440–8451. https://doi.org/10.18653/v1/2020.acl-main.747

CVB, 2023. CVB feed table: chemical composition and nutritional value of feedstuffs (Official Feed Ingredient Nutrient Reference Table). Centraal Veevoederbureau, Lelystad, Netherlands.

DeepSeek, 2026a. DeepSeek-V4-flash [WWW Document]. URL https://platform.deepseek.com/api-docs/

DeepSeek, 2026b. DeepSeek-V4-pro [WWW Document]. URL https://platform.deepseek.com/api-docs/

Du, Y., Li, S., Torralba, A., Tenenbaum, J.B., Mordatch, I., 2023. Improving factuality and reasoning in language models through multiagent debate. https://doi.org/10.48550/arXiv.2305.14325

Es, S., James, J., Espinosa Anke, L., Schockaert, S., 2024. RAGAs: automated evaluation of retrieval augmented generation, in: Aletras, N., De Clercq, O. (Eds.), Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics: System Demonstrations. Association for Computational Linguistics, St. Julians, Malta, pp. 150–158. https://doi.org/10.18653/v1/2024.eacl-demo.16

Flesch, R., 1948. A new readability yardstick. J. Appl. Psychol. 32, 221–233. https://doi.org/10.1037/h0057532

Gong, R., Li, X., 2025. The application progress and research trends of knowledge graphs and large language models in agriculture. Comput. Electron. Agric. 235, 110396. https://doi.org/10.1016/j.compag.2025.110396

Gu, J., Jiang, X., Shi, Z., Tan, H., Zhai, X., Xu, C., Li, W., Shen, Y., Ma, S., Liu, H., Wang, S., Zhang, K., Wang, Y., Gao, W., Ni, L., Guo, J., 2025. A survey on LLM-as-a-judge. https://doi.org/10.48550/arXiv.2411.15594

Guo, T., Chen, X., Wang, Y., Chang, R., Pei, S., Chawla, N.V., Wiest, O., Zhang, X., 2024. Large language model based multi-agents: a survey of progress and challenges. https://doi.org/10.48550/arXiv.2402.01680

Hao, S., Liu, T., Wang, Z., Hu, Z., 2023. ToolkenGPT: augmenting frozen language models with massive tools via tool embeddings, in: Oh, A., Naumann, T., Globerson, A., Saenko, K., Hardt, M., Levine, S. (Eds.), Advances in Neural Information Processing Systems. Curran Associates, Inc., pp. 45870–45894.

He, P., Gao, J., Chen, W., 2023. DeBERTaV3: improving DeBERTa using ELECTRA-style pre-training with gradient-disentangled embedding sharing. https://doi.org/10.48550/arXiv.2111.09543

Hong, S., Zhuge, M., Chen, J., Zheng, X., Cheng, Y., Wang, J., Zhang, C., Wang, Z., Yau, S., Lin, Z., Zhou, L., Ran, C., Xiao, L., Wu, C., Schmidhuber, J., 2024. MetaGPT: meta programming for a multi-agent collaborative framework, in: Kim, B., Yue, Y., Chaudhuri, S., Fragkiadaki, K., Khan, M., Sun, Y. (Eds.), International Conference on Learning Representations. Presented at the International Conference on Learning Representations, pp. 23247–23275.

Honovich, O., Aharoni, R., Herzig, J., Taitelbaum, H., Kukliansy, D., Cohen, V., Scialom, T., Szpektor, I., Hassidim, A., Matias, Y., 2022. TRUE: Re-evaluating factual consistency evaluation, in: Carpuat, M., de Marneffe, M.-C., Meza Ruiz, I.V. (Eds.), Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies. Presented at the NAACL-HLT 2022, Association for Computational Linguistics, Seattle, United States, pp. 3905–3920. https://doi.org/10.18653/v1/2022.naacl-main.287

Huang, K., Zhang, S., Wang, H., Qu, Y., Lu, Y., Roohani, Y., Li, R., Qiu, L., Li, G., Zhang, J., Yin, D., Marwaha, S., Carter, J.N., Zhou, X., Wheeler, M., Bernstein, J.A., Wang, M., He, P., Zhou, J., Snyder, M., Cong, L., Regev, A., Leskovec, J., 2025a. Biomni: a general-purpose biomedical AI agent. bioRxiv. https://doi.org/10.1101/2025.05.30.656746

Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., Chen, Q., Peng, W., Feng, X., Qin, B., Liu, T., 2025b. A survey on hallucination in large language models: principles, taxonomy, challenges, and open questions. ACM Trans. Inf. Syst. 43, 1–55. https://doi.org/10.1145/3703155

Hy-Line International, 2026a. Hy-line W-36 commercial layers: management guide [WWW Document]. URL https://www.hyline.com/

Hy-Line International, 2026b. Hy-line brown commercial layers: management guide [WWW Document]. URL https://www.hyline.com/

INRAE-CIRAD-AFZ, 2026. Feed tables: chemical composition and nutritional value of feed materials [WWW Document]. URL https://feedtables.com/

INRAE, CIRAD, AFZ, FAO, 2026. Feedipedia — an on-line encyclopedia of animal feeds [WWW Document]. URL https://www.feedipedia.org/

ISA, 2026. ISA brown commercial layers: management guide [WWW Document]. URL https://layinghens.hendrix-genetics.com/en/technical-support/nutrition/

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.J., Madotto, A., Fung, P., 2023. Survey of hallucination in natural language generation. ACM Comput. Surv. 55. https://doi.org/10.1145/3571730

Jiang, Q., Zheng, K., Huang, B., Wang, J., Ban, Z., Zhang, B., 2025. Energy restriction optimizes energy partitioning and remodels intestinal energy metabolism in layer pullets. Poult. Sci. 104(12), 105985. https://doi.org/10.1016/j.psj.2025.105985

Kandamali, D.F., Porter, W.M., Porter, E., McLemore, A., Rains, G.C., 2025. CottonBot: an AI-driven cotton farming assistant and irrigation advisor using LLM-RAG and agentic AI tools. Smart Agric. Technol. 12, 101640. https://doi.org/10.1016/j.atech.2025.101640

Ke, Z., Jiao, F., Ming, Y., Nguyen, X.-P., Xu, A., Long, D.X., Li, M., Qin, C., Wang, P., Savarese, S., Xiong, C., Joty, S., 2026. A survey of frontiers in LLM reasoning: inference scaling, learning to reason, and agentic systems. https://doi.org/10.48550/arXiv.2504.09037

Lai, V.D., Ngo, N., Pouran Ben Veyseh, A., Man, H., Dernoncourt, F., Bui, T., Nguyen, T.H., 2023. ChatGPT beyond english: towards a comprehensive evaluation of large language models in multilingual learning, in: Bouamor, H., Pino, J., Bali, K. (Eds.), Findings of the Association for Computational Linguistics: EMNLP 2023. Association for Computational Linguistics, Singapore, pp. 13171–13189. https://doi.org/10.18653/v1/2023.findings-emnlp.878

Lakens, D., 2013. Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. Front. Psychol. 4, 863. https://doi.org/10.3389/fpsyg.2013.00863

LangChain, 2026. LangChain — framework for LLM applications [WWW Document]. URL https://www.langchain.com/

Lemme, A., Ravindran, V., Bryden, W.L., 2004. Ileal digestibility of amino acids in feed ingredients for broilers. World’s Poult. Sci. J. 60, 423–438. https://doi.org/10.1079/WPS200426

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Kuttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., Kiela, D., 2020. Retrieval-augmented generation for knowledge-intensive NLP tasks, in: Advances in Neural Information Processing Systems. Presented at the NeurIPS 2020, Curran Associates, Inc., pp. 9459–9474.

Likert, R., 1932. A technique for the measurement of attitudes. Arch. Psychol. 22, 1–55. https://doi.org/10.4135/9781412961288.n454

Lohmann, 2026. Lohmann LSL-classic commercial layers: management guide [WWW Document]. URL https://www.lohmann-breeders.com/

Malkov, Y.A., Yashunin, D.A., 2020. Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs. IEEE Trans. Pattern Anal. Mach. Intell. 42, 824–836. https://doi.org/10.1109/TPAMI.2018.2889473

Manakul, P., Liusie, A., Gales, M., 2023. SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models, in: Bouamor, H., Pino, J., Bali, K. (Eds.), Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing. Presented at the EMNLP 2023, Association for Computational Linguistics, Singapore, pp. 9004–9017. https://doi.org/10.18653/v1/2023.emnlp-main.557

Mandiga, A., Yoon, J.H., Kasireddy, B., Olukosi, O.A., Li, G., 2026. NutriCHAT: a reasoning-driven large language model agent with expert-designed tools for knowledge-grounded poultry nutrition assistance. Comput. Electron. Agric. 245, 111564. https://doi.org/10.1016/j.compag.2026.111564

Martinez, D., Ponce-de Leon, C., Coon, C., 2024. Exploring the potential of artificial intelligence in feed formulation to advance poultry health and one-health. Ger. J. Vet. Res. 4, 1–3. https://doi.org/10.51585/gjvr.2024.4.0104

Masry, A., Long, D.X., Tan, J.Q., Joty, S., Hoque, E., 2022. ChartQA: a benchmark for question answering about charts with visual and logical reasoning, in: Muresan, S., Nakov, P., Villavicencio, A. (Eds.), Findings of the Association for Computational Linguistics: ACL 2022. Association for Computational Linguistics, Dublin, Ireland, pp. 2263–2279. https://doi.org/10.18653/v1/2022.findings-acl.177

Maynez, J., Narayan, S., Bohnet, B., McDonald, R., 2020. On faithfulness and factuality in abstractive summarization, in: Jurafsky, D., Chai, J., Schluter, N., Tetreault, J. (Eds.), Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, Online, pp. 1906–1919. https://doi.org/10.18653/v1/2020.acl-main.173

Medras, Z.J., Al-Khalaifah, H., 2026. Mastering feed efficiency for a sustainable operation in poultry industry. Front. Anim. Sci. 7, 1798067. https://doi.org/10.3389/fanim.2026.1798067

Mialon, G., Dessì, R., Lomeli, M., Nalmpantis, C., Pasunuru, R., Raileanu, R., Rozière, B., Schick, T., Dwivedi-Yu, J., Celikyilmaz, A., Grave, E., LeCun, Y., Scialom, T., 2023. Augmented language models: a survey. https://doi.org/10.48550/arXiv.2302.07842

MiniMax, 2026. MiniMax-M2.5 [WWW Document]. URL https://platform.minimaxi.com/docs/api-reference/text-openai-api

National Research Council, 1994. Nutrient requirements of poultry, 9 Revised. ed. National Academies Press, Washington, DC. https://doi.org/10.17226/2114

Pardo-Pina, S., Germer, J., Suay-Cortés, R., Platero-Horcajadas, M., Ferrández-Pastor, F.-J., 2026. An agent-based service architecture for smart greenhouses: telemetry analytics and decision support with RAG-grounded LLM agents. Smart Agric. Technol. 13, 101872. https://doi.org/10.1016/j.atech.2026.101872

Park, J.S., O’Brien, J., Cai, C.J., Morris, M.R., Liang, P., Bernstein, M.S., 2023. Generative agents: interactive simulacra of human behavior, in: Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, UIST ’23. Association for Computing Machinery, New York, NY, USA, pp. 1–22. https://doi.org/10.1145/3586183.3606763

Pesti, G.M., Choct, M., 2023. The future of feed formulation for poultry: toward more sustainable production of meat and eggs. Anim. Nutr. 15, 71–87. https://doi.org/10.1016/j.aninu.2023.02.013

Qin, Y., Liang, S., Ye, Y., Zhu, K., Yan, L., Lu, Y., Lin, Y., Cong, X., Tang, X., Qian, B., Zhao, S., Hong, L., Tian, R., Xie, R., Zhou, J., Gerstein, M., Li, D., Liu, Z., Sun, M., 2024. ToolLLM: facilitating large language models to master 16000+ real-world apis, in: International Conference on Learning Representations.

Qwen, 2026b. Qwen3-8B [WWW Document]. URL https://help.aliyun.com/zh/model-studio/getting-started/models

Qwen, 2026c. Qwen3.8 model family [WWW Document]. URL https://platform.qianwenai.com/

Ravindran, D.J.S., Skarga-Bandurova, I., Sivakumar, V., Awais, M., Mithra, S., 2026. AgroLLM: connecting farmers and agricultural practices through large language models for enhanced knowledge transfer and practical application. AgriEngineering 8, 38. https://doi.org/10.3390/agriengineering8010038

Ruchay, A., Guo, H., Pezzuolo, A., 2027. Agentic AI for livestock housing management: applications, benchmarking, and readiness assessment. Comput. Electron. Agric. 256, 112361. https://doi.org/10.1016/j.compag.2026.112361

Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., Scialom, T., 2023. Toolformer: language models can teach themselves to use tools, in: Advances in Neural Information Processing Systems 36 (NeurIPS 2023). https://doi.org/10.52202/075280-2997

Silvestri, A., Parlato, M.C.M., Ruchay, A., Guo, H., Iussig, G., Pezzuolo, A., 2026. Tech-driven evolution of animal housing: an in-depth analysis of the impact of digital technologies, AI, and GenAI in the era of precision livestock farming. Comput. Electron. Agric. 246, 111602. https://doi.org/10.1016/j.compag.2026.111602

Spearman, C., 2010. The proof and measurement of association between two things. Int. J. Epidemiol. 39, 1137–1150. https://doi.org/10.1093/ije/dyq191

Su, H., Long, W., Zhang, Y., 2025. BioMaster: multi-agent system for automated bioinformatics analysis workflow. bioRxiv. https://doi.org/10.1101/2025.01.23.634608

Tang, X., Hu, T., Ye, M., Shao, Y., Yin, X., Ouyang, S., Zhou, W., Lu, P., Zhang, Z., Zhao, Y., Cohan, A., Gerstein, M., 2025. ChemAgent: self-updating library in large language models improves chemical reasoning. https://doi.org/10.48550/arXiv.2501.06590

Textstat, 2026. Textstat — python text statistics package [WWW Document]. URL https://textstat.readthedocs.io/

Tian, M., Guo, H., Long, C., Zhu, J., Zhao, W., Li, H., Ruchay, A., Pezzuolo, A., Li, B., 2026. How large-scale foundation models benefit precision livestock farming: a survey. Artif. Intell. Agric. 16, 1109–1132. https://doi.org/10.1016/j.aiia.2026.04.013

Tzachor, A., Devare, M., Richards, C., Pypers, P., Ghosh, A., Koo, J., Johal, S., King, B., 2023. Large language models and agricultural extension services. Nat. Food 4, 941–948. https://doi.org/10.1038/s43016-023-00867-x

Wang, Junlin, Wang, Jue, Athiwaratkun, B., Zhang, C., Zou, J., 2024. Mixture-of-agents enhances large language model capabilities. https://doi.org/10.48550/arXiv.2406.04692

Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A.H., White, R.W., Burger, D., Wang, C., 2023. AutoGen: enabling next-gen LLM applications via multi-agent conversation. https://doi.org/10.48550/arXiv.2308.08155

Xiaomi MiMo Team, 2026. MiMo-V2.5-pro [WWW Document]. URL https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro

Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D., Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H., Tang, J., Yang, Jian, Tu, J., Zhang, J., Yang, Jianxin, Yang, Jiaxi, Zhou, Jing, Zhou, Jingren, Lin, J., Dang, K., Bao, K., Yang, K., Yu, L., Deng, L., Li, Mei, Xue, M., Li, Mingze, Zhang, P., Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S., Luo, S., Li, T., Tang, T., Yin, W., Ren, Xingzhang, Wang, X., Zhang, X., Ren, Xuancheng, Fan, Y., Su, Y., Zhang, Yichang, Zhang, Yinger, Wan, Y., Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., Qiu, Z., 2025. Qwen3 technical report [WWW Document]. arXiv.org. URL https://arxiv.org/abs/2505.09388v1

Yang, N., 2021. Egg production in China: current status and outlook. Front. Agric. Sci. Eng. 8, 25–34. https://doi.org/10.15302/J-FASE-2020363

Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., Cao, Y., 2023. ReAct: synergizing reasoning and acting in language models, in: International Conference on Learning Representations (ICLR 2023). https://doi.org/10.48550/arXiv.2210.03629

Z.ai, 2026. GLM-4.5-air [WWW Document]. URL https://docs.bigmodel.cn/cn/guide/develop/openai/introduction

Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E.P., Zhang, H., Gonzalez, J.E., Stoica, I., 2023. Judging LLM-as-a-judge with MT-bench and chatbot arena, in: Advances in Neural Information Processing Systems. Presented at the Annual Conference on Neural Information Processing Systems (NeurIPS), New Orleans, LA, USA.

Zhu, H., Qin, S., Su, M., Lin, C., Li, A., Gao, J., 2025. Harnessing large vision and language models in agriculture: a review. Front. Plant Sci. 16, 1579355. https://doi.org/10.3389/fpls.2025.1579355
