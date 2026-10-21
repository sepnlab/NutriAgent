## Table S1. Data schema and completeness

Nominal cells = rows × parameters. Populated cells count non-missing values; the difference is reported rather than hidden.

| Module | File | Rows | Parameters | Nominal cells | Populated | Completeness | Fully empty parameters |
|---|---|---:|---:|---:|---:|---:|---|
| Feed ingredient bank | `corpus/shared/feed_ingredient_bank.csv` | 108 | 38 | 4104 | 2376 | 57.9% | NFE_pct, NE_kcal_kg, Linoleic_pct, Linolenic_pct, Cl_pct, S_pct, Fe_mg_kg, Cu_mg_kg, … |
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
| Developer 7-10w | Developer 13-17w | semantic | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong… | age lies in Grower window |
| Developer 9-16w | Developer 13-17w | boundary | Lohmann Grey | — |
| Finisher 11-14w | Developer 13-17w | semantic | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong… | finisher label precedes Pre-Lay 15w-5% |
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
| Pre-Lay 15w-5% | Pre-Lay 18-20w | boundary | Dawu Fen 1; Dawu He; Dawu Jinfeng; Jingbai 939; Jingfen 6; Jinghong… | — |
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

Full machine-readable table with URLs, versions, access dates, and licenses: `corpus/provenance.csv`. `needs_primary_source` marks Chinese domestic rows that were compiled through jbzyw.com; `needs_version_and_url` marks breeder guides whose exact version still has to be recorded.

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
