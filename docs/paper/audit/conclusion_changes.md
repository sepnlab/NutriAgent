# Conclusion-level changes in Rev.1

> Living document. Last updated 2026-10-20.
> Status labels: **OVERTURNED** (the original conclusion is not supported and is
> replaced), **WEAKENED** (direction may hold but the claim is reduced), **CORRECTED**
> (factual/definition error fixed), **PENDING** (depends on an experiment still running).
> This file is the audit trail for the response letter; the manuscript text is the
> authoritative version.

> **Final-status note (2026-10-21; Rev.1 build).** This file records the audit trail from the working phase. Several sections below are historical and were superseded by the completed runs. Final values used in the manuscript and response letter: E18 primary expert NutriAgent 4.34 vs DeepSeek-V4-Pro 4.05 (ΔC +0.20, Holm p = 0.146; ΔP +0.50, unadjusted p = 0.037, Holm across all dimensions p = 0.256); D2 same-pass n=54 Full 4.44, without Feed 4.67, without Definitions 4.57, without Performance 4.39, without Nutrition 4.37; D3 LLM 4.63, Broadcast 4.59, Keyword 4.48; D4 +RAG 4.52 vs no-RAG 4.52 (proxy ITT 3.50 vs 4.52); D6 Pro 4.67, Flash 4.61, 27B 4.50, Qwen3.8-Flash 4.43, Qwen3-8B 3.81; evaluator agreement ρ = 0.55 (C), 0.71 (P), 0.34 (D); E3 42/42 rule coverage; E4 is a rule-based audit only; no expert scoring of E2 was performed. The manuscript and response letter are authoritative where this file differs.


## 1. Synthesis / cross-validation was the dominant driver — OVERTURNED

- **Original claim**: the Synthesis Agent is the largest contributor (+24.2% correctness,
  −29.7% inconsistency); cross-validation between specialists matters more than
  decomposition.
- **Why it fails**: the submitted D5 changed concatenation → synthesis, validation, and an
  extra LLM call at once, so it cannot attribute the gain to consistency checking. The
  "no-ReAct" condition was also a duplicate of the full pipeline (dispatch bug).
- **Rev.1 evidence**: E1 architecture factorial (n = 54, re-scored): standalone 4.63,
  tools-only 4.31, RAG 4.54, synthesis-only 4.48, multi-agent validation-off 4.74,
  validation-on 4.83. The extra synthesis call **without decomposition** is not better than
  RAG alone; decomposition plus tools is what raises correctness; validation adds a small
  gain (+0.09 C / +0.08 P) at a depth cost (−0.18 D).
- **Replacement**: a modest, testable claim — decomposition and grounding improve
  correctness; consistency checking may add a small correctness/precision gain but is not
  the primary driver. E2 (six-condition synthesis factorial) is complete; it does not support an integration/validation benefit.

## 2. Multi-agent beats single-agent by +5.3% correctness / −48.3% inconsistency — OVERTURNED

- **Original claim**: multi-agent improves over a single ReAct agent by 5.3% correctness
  and 48.3% inconsistency reduction.
- **Why it fails**: the single-agent condition in the submitted run was not a
  single-pass tool call; the "no-ReAct" row was produced by the full pipeline because a
  case-sensitive dispatch check silently fell through.
- **Rev.1 evidence**: E1 now has a true single-pass condition and five other controls.
  Tools-only is *below* the standalone LLM (4.31 vs 4.63); RAG recovers most of the gap;
  the multi-agent pipeline is highest (4.74/4.83) but the contrast is smaller and
  depth-sensitive.
- **Replacement**: report the factorial table (Table 7), withdraw the no-ReAct row, and do
  not quote the 5.3%/48.3% figures.

## 3. "Hallucination reduced by 70%" / 3.1× Chinese gap — WEAKENED + CORRECTED

- **Original claim**: hallucination reduced by 70.0%; Chinese queries have a 3.1× higher
  hallucination rate; numeric faithfulness shows 56% of numbers come from parametric
  knowledge.
- **Why it fails**: SelfCheckGPT-NLI measures cross-sample inconsistency, not factual
  error; the any-number ±5% match ignores entity and unit; the 56% figure therefore
  includes derived values and unit conversions.
- **Rev.1**: metric renamed to "SelfCheckGPT-NLI inconsistency score" throughout; the 70%
  difference is retained as an observed score difference, not as a factual-error
  reduction; the 56% parametric claim is withdrawn; a claim-aware audit (E4) and
  entity/attribute/unit-aware validator (E3) are pending. The Chinese gap is reported as
  exploratory with language/breed confounding.

## 4. Evaluator agreement ρ = 0.83 / 0.67 / 0.37 — CORRECTED

- **Original claim**: strong agreement between EvaluatorLLM and the expert.
- **Rev.1 recomputation** from the deposited scores: ρ = 0.575 (95% CI 0.25–0.81),
  0.529 (0.27–0.73), 0.038 (−0.27–0.42) for correctness, depth, and precision. Precision
  agreement is negligible; dimension-level correlations were removed because the expert
  did not score ablation variants.
- **Consequence**: the automated judge is used for within-dimension relative contrasts,
  not as a substitute for expert scores; the main comparison is being re-scored by the
  primary expert (E18).

## 5. Data scale and schema — CORRECTED

- **Original**: "~14,800 data points", "80 unique ingredients", "20 parameters" without
  the exact list, "55 phase labels", "17 breeds" with Chinese data described as official
  management guides.
- **Rev.1**: 108 ingredient records (38 composition + 19 amino acid + 40 digestibility
  parameters), 103 requirement rows × 20 parameters (73.6% populated), 1,131 performance
  rows × 12 parameters (42.7%), 556 definitions, 2,144 PoultryDB documents; 59 phase labels
  mapped to 7 reference phases; per-breed provenance table separates breeder guides,
  jbzyw.com aggregator, and public feed tables. The mixed "data point" total is withdrawn.

## 6. Query set composition — CORRECTED

- **Original**: 42 English international-breed queries + 12 Chinese domestic-breed queries.
- **Rev.1**: 42 English + 12 Chinese; the Chinese set includes one international strain
  (Hy-Line Brown) and feed/definition questions, not only domestic breeds; the
  breed-targeted Chinese queries are Jingfen 6 and Dawu Jinfeng. Language and breed are
  confounded; the bilingual analysis is exploratory.

## 7. Baseline count and model set — CORRECTED + PENDING

- **Original**: "seven standalone LLM baselines"; Qwen3.5-Flash, SiliconFlow MiniMax,
  DeepSeek official endpoint.
- **Rev.1**: six standalone baselines plus a single-agent architectural baseline; the
  frozen Rev.1 set is Table 6 (SiliconFlow DeepSeek-V4-Flash, Qwen3-8B, GLM-4.5-Air,
  Qwen3.8-Flash, Tencent MiniMax-M2.5, DeepSeek-V4-Pro). The main comparison is being
  re-run and re-scored (E18); no submitted-model score is mixed with Rev.1.

## 8. Cost / efficiency — WEAKENED

- **Original**: $0.0007/query and a 5–6× token-cost ratio vs a single-agent design.
- **Rev.1**: full-component accounting (router + specialists + synthesis); the token-cost
  ratio was not token-matched and is withdrawn. Costs are reported with provider/date/FX;
  no architecture-level efficiency claim.

## 9. Design principle — OVERTURNED

- **Original**: "synthesis-stage cross-validation contributes more to factual reliability
  than decomposition" as a general design principle.
- **Rev.1**: replaced by a testable hypothesis; the abstract and conclusion state that the
  result is conditional on the task and the judge, not a general principle.

## 10. Main comparison numbers — PENDING (E18)

- **Original**: 4.42/5.0 vs 3.80 for the strongest baseline, expert-scored.
- **Rev.1**: the main comparison was re-run on the frozen model set (7 methods × 54 = 378
  responses). The blinded expert sheet is exported; the primary expert's re-score is complete (4.34 vs 4.05). The submitted numbers are retained only as historical comparison and are
  not mixed with Rev.1.

---

## 11. E2: the synthesis gain is a second-pass/style effect, not integration — CONFIRMED (E2 complete)

- **E2 results** (all n = 54): concatenation 4.28; validation + concatenation
  **4.11**; synthesis with shuffled warnings 4.87; synthesis with validation off
  **4.91**; **query-only synthesis 4.85**; synthesis with correct warnings **4.91**.
  Correct and validation-off are identical at 4.91, shuffled is 4.87, and query-only
  (no specialist outputs) is 4.85 — the validation content has no measurable effect,
  and the extra synthesis pass, not integration, is associated with the score increase.
  Validation + concatenation is *lower* than concatenation (4.11 vs 4.28).
- **Why this matters**: query-only synthesis has no specialist outputs to integrate, yet
  it scores as high as the full synthesis conditions and much higher than concatenation.
  The score increase is therefore associated with the extra synthesis LLM call, not with
  cross-specialist content or validation. An alternative explanation is that the judge
  rewards polished, structured prose (a style effect) rather than grounding.
- **Consequence**: we cannot claim that integration or consistency checking improves
  quality from E2. The manuscript must present E2 as **not supporting** the integration
  mechanism, and no expert scoring of the E2 conditions was performed; this is stated as future work, and no positive integration claim is made.
- **Status**: CONFIRMED at n=54; this remains an automated-judge result.

---

## 12. D2 specialist contribution is not replicated — NEW, PENDING

- **Rev.1 D2** (`logs/ablation_specialist_layer_20261020_200015/`): Full 4.81 (n=53);
  without Feed 4.85 (n=54); without Nutrition 4.86 (n=44); without Performance 4.70
  (n=54); without Definitions 4.80 (n=54).
- **Why it matters**: the submitted D2 reported Performance −0.20, Nutrition −0.09,
  Feed −0.04. Rev.1 reproduces only the Performance drop (−0.11); removing Feed or
  Nutrition does not reduce judged correctness (the point estimates are slightly
  higher, within judge noise), and removing Definitions is negligible.
- **Interpretation**: the specialist ablation does not establish that each specialist
  contributes; the system appears redundant across Feed/Nutrition/Definitions for these
  queries, or the judge is insensitive to the difference. The manuscript must not claim
  a clean specialist-contribution ordering; report the Rev.1 table with CIs and note the
  null results.
- **Status**: PENDING re-score of the n<54 variants; D3/D4/D6 Rev.1 results pending.

---

## 13. The consistency validator itself had three order/tolerance/alias defects — CORRECTED

- **E3** on a 42-pair labeled set initially gave **recall 0.00**: the validator never
  flagged a conflict, including 35% vs 38% Ca.
- **Root causes**: (i) claim extraction only handled attribute-before-value
  ("calcium 35%"), not the value-before-attribute order ("35% calcium") that the
  submitted 38%-Ca failure used; (ii) the default relative tolerance was 10%, so a
  7.9% difference never triggered; (iii) the entity lexicon had long feed-table names
  but not commodity-level short names ("soybean meal", "wheat", "fish meal") or phase
  labels ("Lay I").
- **Fixes**: reversed extraction patterns, 5% tolerance, commodity-family aliases,
  phase short labels; 24 validation tests. E3 now: 16/16 conflicts, 12/12 consistent,
  14/14 distractors (precision/recall/F1 = 1.00).
- **Caveat**: the 42-pair set is synthetic and partly derived from the same lexicon;
  1.00 is a rule-coverage/regression result, not field precision. Expert/literature
  labeled claims remain part of E4.

---

## 14. Single-run scores are not reproducible — NEW

- **E9** (10 queries × 3 runs, temperature 0.0, cache disabled): mean pairwise text
  similarity **0.371** (min 0.106, max 0.870), exact-match rate **0.0**, mean latency
  14.0 s.
- **Why it matters**: the pipeline is non-deterministic despite temperature 0.0, because
  provider sampling, routing, tool-call order, and synthesis inputs vary. Single-run
  scores therefore carry substantial run-to-run variance.
- **Consequence**: small differences (e.g., validation-on vs off +0.09 C; correct vs
  shuffled +0.04) are within run noise and must not be interpreted as effects. Only
  large contrasts (e.g., concatenation 4.28 vs synthesis 4.91) survive this caveat, and
  even those should be averaged over repeats in future work. The paper should state that
  all scores are single-run and add repeat-averaged evaluation as a limitation.

---

## 15. Feed-tool entity resolution is English-only and misspelling-fragile — NEW

- **E15** (39 perturbation cases): exact canonical, commodity short names, and
  case/whitespace variants resolve 100% at the family level; **misspellings resolve
  62.5% but are family-correct only 37.5%** (`wheatt` → wheat bran; `corn meal` →
  corn gluten feed); **Chinese aliases resolve 0%**; ambiguous families are 80%
  family-correct.
- **Why it matters**: the feed tool uses a case-insensitive substring index and
  silently returns the first matching row. Chinese ingredient names therefore depend
  entirely on the LLM translating them to English before the tool call; the tool itself
  cannot resolve them. Bilingual results are partly a translation result, not an
  entity-resolution result.
- **Consequence**: the paper must not claim robust bilingual entity resolution. State
  the English-only index, the wrong-match rate for misspellings, and the translation
  dependency in §2.1.1, §3.5, and Limitations. The alias table used by the consistency
  checker does not fix the feed tool.

---

## 16. D3 routing advantage is not replicated — NEW

- **Rev.1 D3** (`logs/ablation_router_layer_20261020_211353/`): LLM Router 4.63
  (n=54), Keyword Router 4.64 (n=44), Broadcast 4.68 (n=44); spread ≤0.05. LLM Router
  has the highest precision (4.56 vs 4.39/4.31); Broadcast has the highest depth
  (4.23).
- **Submitted claim**: LLM Router 4.80 > Keyword 4.69 > Broadcast 4.61, with the
  keyword router at "97.7%" of LLM-router correctness. Not replicated.
- **Consequence**: routing is a null result on correctness. Retain the LLM router for
  precision, not because it improves correctness; do not quote 4.80/4.69/4.61 or 97.7%.
  Two Rev.1 cells are n=44, so the comparison is preliminary until re-scored.

---

## 17. D4 RAG precision benefit is not replicated — NEW, PARTIAL

- **Rev.1 D4** (`logs/ablation_rag_layer_20261020_213245/`): +RAG 4.70 correctness
  (n=44), no-RAG 4.56 (n=34); +0.14 correctness, but precision **−0.13** (4.49 vs 4.62)
  and depth +0.18.
- **Submitted claim**: RAG +0.08 correctness and +0.10 precision. Not replicated; the
  precision direction reverses.
- **Consequence**: RAG may improve coverage while adding numerical noise, consistent with
  a fallback role. Both cells are n<54, so the direction is provisional; re-score to
  n=54 and complete E6 (k-sensitivity, ITT) before claiming a RAG benefit. Do not quote
  +0.08/+0.10.

---

## 18. RAG k=1 retrieval recall is low — NEW

- **E6** on 44 queries with annotated target documents: hit@1 **27.3%**, hit@3 54.5%,
  hit@5 **63.6%**, MRR 0.411. Definitions 71.4% hit@1 / 100% hit@5; single-value 20% /
  53.3%; comparison 10% / 50%; multi-hop 0% / 66.7%.
- **Why it matters**: k=1 misses about 73% of annotated targets. The submitted rationale
  for a narrow single passage is not supported, and the deposited run actually used k=2
  while the manuscript said k=1. The frozen Rev.1 value is k=1, so the reported RAG
  condition is conservative; k=5 would improve recall but was not used.
- **Caveat**: target_doc is one acceptable document per query, not an exhaustive
  relevance judgment; 44/54 queries have targets. Report as a retrieval diagnostic, not
  as a complete recall estimate.

---

## 19. The 0.444 numeric-faithfulness score is not claim-level support — NEW, PARTIAL

- **E4 rule-based audit** on the E1 multi-agent responses (validation on/off): 101/96
  numeric claims extracted; **direct support 10.9% / 16.7%** (entity + attribute + value
  within 5%); attribute-only 9.9% / 6.2%; any-number 13.9% / 13.5%; unsupported
  **65.3% / 63.5%**.
- **Why it matters**: the submitted 0.444 any-number score is far above the strict
  claim-level support. It cannot be described as the fraction of claims traceable to tool
  data, and the "56% parametric" interpretation is not supported.
- **Caveat**: the rule-based extractor finds only ~2 claims per response and does not fully
  parse observation units; 10.9–16.7% is a strict lower bound under this parser, not a
  human-validated rate. E4's human-labeled subset is still needed.
- **Consequence**: report 0.444 only as a permissive any-number indicator; use the
  claim-aware audit as the primary grounding evidence with the parser caveat.

---

## 20. D6 backbone ranking is not replicated — NEW, PARTIAL

- **Rev.1 D6** (`logs/ablation_llm_backbone_layer_20261020_214559/`): DeepSeek-V4-Pro
  4.79 (n=43), Qwen3.8-Flash 4.76 (n=33), DeepSeek-V4-Flash 4.66 (n=44), Qwen3.8-27B
  4.64 (n=44), Qwen3-8B 4.00 (n=34).
- **Submitted claim**: DeepSeek-V4-Flash 4.85 > DeepSeek-V4-Pro 4.74 > Qwen3.6-Plus
  4.69 > Qwen3.5-Flash 4.44 > Qwen3-8B 4.11. Not replicated; the top two swap and the
  middle of the ranking changes.
- **Robust part**: Qwen3-8B is clearly weakest (−0.66 correctness, −1.17 depth vs
  DeepSeek-V4-Flash), so backbone capability still matters and the architecture does not
  compensate for a weak backbone's depth deficit.
- **Consequence**: do not quote the submitted backbone ordering; report the Rev.1 table
  with n<54 caveat and re-score before fine ranking. The "DeepSeek-V4-Flash is best"
  claim is not supported.

---

## 21. The submitted second-expert post-hoc correlations are withdrawn — CORRECTED

- **Submitted claim**: a 60-response subset (≈16% of 378) was independently scored and
  showed ρ = 0.81/0.74/0.69, 88% within one point, MAD 0.31.
- **Why it is withdrawn**: the raw second-rater scores were not retained in the deposited
  materials, so the correlations cannot be reproduced. The manuscript no longer presents
  them as evidence.
- **Replacement**: a 120-response second-rater subset covering all 54 queries has been
  sampled and blinded (`expert_eval_second_rater.csv`); ICC(2,1), quadratic weighted kappa,
  and Bland–Altman will be computed when the scores return. Until then, we state that
  inter-rater reliability is not yet established.

---

## 22. E7 hard removal of Feed data does not reduce judged quality — NEW, PARTIAL

- **E7** (20 Feed/Cross-Domain queries, single run): full pipeline 4.40 correctness /
  4.40 precision / 3.70 depth; **hard removal** (delete Feed specialist + filter Feed
  Ingredient Bank documents out of RAG) 4.70 / 4.47 / 3.70. Hard removal is **+0.30
  correctness**, +0.07 precision, 0 depth.
- **Why it matters**: D2 removes the specialist/tool but leaves the shared corpus; E7
  removes the data itself and still does not degrade judged quality. This is a negative
  result for the claim that Feed data are necessary for judged correctness, and it is
  consistent with E2's finding that the judge rewards answer form/polish.
- **Caveat**: n=20, single run, MiMo judge; no expert labels. The result does not prove the
  data are unnecessary for real users, only that the automated judge does not penalize
  their absence. Report it as a judge-sensitivity finding, not as evidence that feed data
  can be removed in deployment.

---

## 23. Tolerance accuracy is updated on Rev.1 responses — CORRECTED, PARTIAL

- **Submitted**: 75.0% at ±2%, 80.6% at ±5% (archived responses).
- **Rev.1**: 83.3% at ±2%, 88.9% at ±5% (32/36 numeric queries; four wrong values,
  none without a numeric answer). The relative-error and submitted interval rules agree
  on every case in this set (E14).
- **Four failures**: C-FIB-005 (expected 11.6, nearest 8.5), C-FIB-010 (2260 vs 48),
  C-XD-001 (0.27 vs 0.25), C-XD-006 (expected decrease 1.45 pp, nearest 5.125). The last
  is a reported-contribution/change mismatch; we do not claim a full unit-error taxonomy.
- **Truth correction**: C-XD-005 was mis-keyed as 0.04; the intended value is 4.33 pp
  (response 4.34 passes). C-XD-006's expected value is a 1.45 pp decrease, not the new
  contribution 11.70%; the response reports 5.125 as nearest, so it fails.
- **Status**: numeric part done; non-numeric error coding (the full E14) remains pending.

---

## 24. Evaluator absolute scores depend on scoring mode — NEW, METHODOLOGICAL

- **D2 Full**: bulk 4.81 (n=53) vs per-item 4.04 (n=54).
- **D2 w/o Nutrition**: bulk 4.86 (n=44) vs per-item 3.98 (n=54).
- **Ordering is consistent**: Full ≈ w/o Nutrition in both modes (bulk +0.05, per-item
  −0.06), so the D2 null result survives. The absolute level shifts by about 0.8 points.
- **Consequence**: absolute scores are not comparable across scoring modes. Report only
  within-mode, within-dimension contrasts; the E1/E2 tables are bulk-mode and the D2
  per-item values are a sensitivity check, not pooled. This is a concrete limitation of
  the "absolute scoring" protocol and must be stated in §2.3.2/§3.6.1.

---

## 25. D4 RAG correctness/precision gain is not replicated at n=54 — OVERTURN

- **+RAG**: 4.52 correctness (n=54), 4.37 precision (n=46), 3.74 depth (n=54).
- **no-RAG**: 4.52 correctness (n=54), 4.33 precision (n=45), 3.96 depth (n=46).
- **Δ**: C **0.00**, P +0.04, D −0.22. The earlier +0.14 C / −0.13 P (n=44/34) is not
  replicated; the submitted +0.08 C / +0.10 P is also not replicated.
- **Consequence**: D4 changes from "provisional positive" to a **null result on
  correctness and precision**. There is no evidence of a precision cost; the depth
  difference favors no-RAG but is incomplete. RAG may still help coverage/recall, but the
  judged-quality claim is withdrawn.

---

## 26. D6 backbone ordering at n=54: DeepSeek-V4-Pro narrowly leads — UPDATE

- **n=54 re-score**: DeepSeek-V4-Pro 4.67, DeepSeek-V4-Flash 4.61, Qwen3.8-27B 4.50,
  Qwen3.8-Flash 4.43, Qwen3-8B 3.81 (C; P n=45–46, D n=54 except Qwen3-8B D n=46).
- **Top two swap** relative to the submitted order (DS-V4-Flash > DS-V4-Pro), but the gap
  is only **0.06**, and DS-V4-Flash has higher depth (4.04 vs 3.87). The top-two ordering
  is not robust; Qwen3-8B's −0.80 C / −1.11 D deficit is.
- **Status**: supersedes #20's n<54 values; Table 5/7 and §3.6.1 updated.

---

## 27. D3 routing is not a null result at n=54 — UPDATE

- **n=54**: LLM Router 4.63, Broadcast 4.59 (−0.04), Keyword 4.48 (−0.15); precision
  4.56/4.47/4.26; depth 3.96/4.00/3.76.
- The earlier n=44 read (LLM 4.63, Keyword 4.64, Broadcast 4.68; spread ≤0.05) is **not
  replicated**. The complete data show a Keyword deficit, not a Broadcast advantage.
- **Consequence**: the LLM router is highest; Broadcast is within 0.04; Keyword is 0.15
  lower. Single-run, no significance test, so we do not claim a routing gain — but the
  "routing is irrelevant" statement is withdrawn.

---

## 28. D2 same-pass re-score: no positive specialist contribution — OVERTURN

- **All five in one pass (n=54 C)**: Full 4.44; w/o Feed 4.67 (+0.22), w/o Definitions
  4.57 (+0.13), w/o Performance 4.39 (−0.06), w/o Nutrition 4.37 (−0.07).
- **No removal lowers correctness materially**; removing Feed or Definitions is followed
  by a higher score. The submitted ordering (Performance −0.20, Nutrition −0.09, Feed
  −0.04) and the earlier separate-pass read (Full 4.81, w/o Nutrition 4.86) are both not
  replicated.
- **Scoring-pass drift**: the same Full condition scores 4.81 in the original pass and
  4.44 in the new pass (Δ 0.37). Only same-pass comparisons are valid; D2 is now fully
  same-pass.
- **Consequence**: withdraw "only Performance matters"; there is no evidence that any
  specialist is necessary for judged correctness. This is consistent with redundancy or a
  judge preference for the simpler answers produced after removal, not evidence that
  specialists can be removed in deployment.

---

## 29. Main comparison: gap shrinks from 0.62 to 0.28; correctness advantage over the strongest baseline is not significant — OVERTURN

- **Primary expert (378 responses)**: NutriAgent 4.34; DeepSeek-V4-Pro 4.05;
  DeepSeek-V4-Flash 4.04; Qwen3.8-Flash 4.01; GLM-4.5-Air 3.55; Qwen3-8B 3.04;
  MiniMax-M2.5 2.63.
- **Paired vs strongest baseline (DeepSeek-V4-Pro)**: ΔC +0.20 (95% CI −0.09 to +0.50;
  Holm p = 0.146), ΔP +0.50 (p = 0.037), ΔD +0.15 (p = 0.238), ΔO +0.20 (p = 0.062).
- **Consequence**: the submitted 4.42 vs 3.80 (+0.62; strongest baseline DeepSeek-V4-Flash)
  is withdrawn. NutriAgent remains the point-estimate leader, but the advantage is
  precision-led and not a significant correctness or overall gain. MiniMax-M2.5, not
  Qwen3-8B, is the lowest baseline; depth is lower than DeepSeek-V4-Flash (4.07 vs 4.33).

---

## 30. Primary repeat sheet is intra-rater, not independent — RESOLVED

- **Primary vs repeat sheet (120 shared rows)**: correctness 118/120 exact, precision
  79/80, depth 106/120, provenance 117/120; ICC(2,1) = 0.995/0.996/0.932; 11 note strings
  are identical, and the note-text median similarity is 0.70 (38/109 ≥0.80).
- **User confirmation**: the repeat sheet was completed by the same expert / copied from
  the primary, not an independent second rater.
- **Relabelled as intra-rater consistency** (test–retest/repeat pass): ICC 0.995/0.996/0.932,
  weighted κ 0.995/0.996/0.931, Bland–Altman −0.02/−0.01/+0.08. It is not used as an
  independent inter-rater estimate.
- **Independent check**: third rater vs primary: ICC(2,1) = 0.847/0.876/0.760; weighted
  κ = 0.846/0.874/0.758; Spearman ρ = 0.862/0.913/0.725. The 120 subset does not reproduce
  the full top rank (third-rater overall: DeepSeek-V4-Flash 4.28, DeepSeek-V4-Pro 4.14,
  NutriAgent 4.12).

---

## 31. Precision agreement is substantial, not negligible — CORRECTED

- Against the completed Rev.1 primary expert: Spearman ρ = 0.55 (correctness; 95% CI
  0.27–0.77), 0.71 (precision; 0.51–0.84), 0.34 (depth; 0.06–0.59); within-one-point
  90.7%/94.7%/98.1%.
- The judge is more lenient on all three metrics (C 4.74 vs 4.46; P 4.71 vs 4.47; D 4.30
  vs 4.07).
- **The earlier ρ = 0.575/0.529/0.038 (precision negligible) is withdrawn.** Precision
  agreement is substantial, so the automated judge can support precision contrasts; the
  expert scores remain the main comparison and the judge is still used only for
  within-dimension ablation contrasts.

---

## 32. D4 RAG ITT sensitivity is neutral-to-negative — CORRECTED

- The Rev.1 D4 re-score has all 54 correctness scores but did not retain a
  retrieval-failure flag; the four submitted-run exclusions cannot be reconstructed
  exactly.
- Conservative proxy ITT: 16 E6 hit@5 misses scored as failures (1; 0 sensitivity).
  Correctness +RAG 3.50 vs no-RAG 4.52 (Δ −1.02; 95% CI −1.52 to −0.52; p < 0.001);
  precision Δ −1.18; depth Δ −1.00. Complete-case is null (+0.00 C, +0.02 P).
- **Consequence**: the manuscript no longer reports only a complete-case null; it states
  that a proxy ITT is negative and labels the proxy explicitly. This is not an exact
  four-query ITT reconstruction.

---

## What the manuscript must say (short version)

- The architecture factorial, not the old D1/D5 rows, is the evidence for component
  attribution (Table 7).
- The synthesis/cross-validation claim is now a hypothesis with a small, conditional
  effect; E2 is the direct test.
- SelfCheckGPT-NLI is an inconsistency score, not a hallucination rate.
- The evaluator agrees moderately, and precision agreement is negligible.
- The data and query descriptions are the corrected counts in §2.1/§2.3 and Tables S1–S3.
- The main comparison awaits E18 expert scores; do not quote 4.42/3.80 as Rev.1 until then.
