# Response to Reviewers — AGRCOM-D-26-00673

**Manuscript**: NutriAgent: a controlled evaluation of specialist routing for layer-hen nutrition question answering
**Journal**: Agriculture Communications
**Decision**: Major revision
**Reviewers**: 4 (78 comments: R1 = 5, R2 = 42, R3 = 18, R4 = 13)

> Status: final response letter. Expert scoring is complete (primary 378 responses; an
> independent 120-response rater; a repeat 120-response sheet from the primary expert is
> reported as intra-rater consistency, not independent inter-rater). E4 still has human
> labels pending; E10 was not used; E14 covers the numeric subset plus a single-coder
> descriptive non-numeric audit (S10); a two-coder kappa is not claimed. All D2–D6
> correctness cells are n=54; precision/depth cells with n<54 are labeled. Page anchors
> below are for the Rev.1 PDF with line numbers. The only author-side open item is the
> public repository push.

## Manuscript location guide

| Item | Page |
|---|---|
| Section 3.2, main expert comparison | 14 |
| Section 3.3, query-type/domain breakdown | 16 |
| Section 3.4, faithfulness and inconsistency | 20 |
| Section 3.5, bilingual and cost | 21 |
| Section 3.6.1, component ablation | 21, 26, 29 |
| Table 8, NutriAgent vs NutriCHAT | 28 |
| Table 9, expert main comparison | 29 |
| Table 10, paired comparisons | 29 |
| Table 11, by query type | 30 |
| Fig. 5, main expert comparison | 16 |
| Fig. 8, query-type/domain breakdown | 18 |
| Fig. 9, domain radar | 19 |
| Fig. 10, bilingual comparison | 22 |
| Conclusion | 30 |
| Limitations | 30 |
| Data and code availability | 31 |

The PDF has continuous line numbers; the page map is also in
`docs/paper/audit/manuscript_page_map.md`.

## Status summary

| Status | Meaning | Count |
|---|---|---:|
| DONE | new evidence/text with a manuscript location | 57 |
| PARTIAL | addressed, with an explicit remaining limitation | 19 |
| LIMITATION | not done; stated as a boundary | 1 |
| AUTHOR_INPUT | repository/author detail still needed | 1 |

All 78 comments are addressed; the letter does not claim that every requested analysis was completed.

## General response

We thank the editor and the four reviewers for a detailed and unusually
constructive set of comments. The revision narrows the claims to what the
evidence supports: the reviewers identified places where the submitted
manuscript described behavior the code did not implement, and several
conclusions that the original design could not support. We have therefore
recalibrated the contribution rather than defending the original framing.

The revision makes four structural changes. Table 7 in the manuscript is a
compact claim-calibration summary; the full matrix is Table S17. We summarize
the main changes below.

1. **Factorial controls replace the confounded D1/D5 comparisons.** The original
   "pipeline architecture" contrast compared a multi-agent pipeline against a
   condition that was supposed to be a no-ReAct single agent, and the original
   "synthesis" contrast changed concatenation, validation, and an extra LLM call
   at once. Neither can attribute the observed difference. We added a
   six-condition architecture factorial (E1: standalone, tools-only, tools+RAG,
   tools+RAG+synthesis, multi-agent with validation off/on) and a six-condition
   synthesis factorial (E2: concatenation, validation+concatenation, synthesis
   with validation off/shuffled/correct, query-only synthesis). All conditions
   share the same backbone and output budget.

2. **The consistency-checking layer was rebuilt.** The submitted regex-based
   checks could read "crude protein … 8.8" as phosphorus and "cage 6" as calcium,
   and the Ca:P rule is not appropriate as a universal layer-hen constraint. The
   new validator compares entity, attribute, unit, and basis, uses a curated
   ingredient alias table, and treats Ca:P as an opt-in check. We report its
   precision/recall on a labeled overlap set rather than asserting that it
   "validates" specialist outputs.

3. **The evaluation record was corrected.** The submitted Methods named
   MiMo-V2.5-Pro as the judge, but the deposited configurations used
   DeepSeek-V4-Pro with absolute scoring; the reported agreement statistics
   (ρ = 0.83/0.67/0.37) are not reproducible from the deposited scores. Rev.1
   re-scores all responses with MiMo-V2.5-Pro and reports agreement against the
   completed expert scores: ρ = 0.55 (correctness), 0.71 (precision), 0.34
   (depth); the judge is more lenient on all metrics, and the earlier ρ = 0.038
   for precision is withdrawn.
   The main comparison is now complete: the primary expert scored all 378
   responses, and the Rev.1 result is NutriAgent 4.34 vs 4.05 for the strongest
   baseline (DeepSeek-V4-Pro); the correctness difference is +0.20 (95% CI −0.09
   to +0.50; Holm p = 0.146), and the precision difference is +0.50 (unadjusted
   p = 0.037; p = 0.256 after correction across all dimension tests). The
   advantage is therefore descriptive and precision-oriented rather than a
   corrected-significance gain. The submitted 4.42/3.80 numbers are retained
   only as historical comparison.

4. **Data, query, and model descriptions now match the deposited artifacts.**
   The 20-parameter requirement schema is listed explicitly with units; the 108
   ingredient records, 103 requirement rows, 1,131 performance rows, 556
   definitions, and 2,144 PoultryDB documents replace the mixed "~14,800 data
   points" total; 59 phase labels (55 nutrition + 4 vitamin-only) are mapped
   with a stated mapping type, with 53 mapped to seven reference phases and 6
   marked unmapped; per-breed provenance distinguishes breeder guides, the
   jbzyw.com aggregator, and public feed tables, with unresolved source fields
   flagged. The model set is frozen in Table 3 and
   `config/models.lock.yaml`, with provider, exact model ID, access date,
   thinking mode, and pricing date.

## Conclusion-level changes

We were asked to identify changes that affect the paper's conclusions. Five
changes are substantive; all are documented in
`docs/paper/audit/conclusion_changes.md`.

1. **The claim that synthesis / cross-validation is the dominant driver is
   withdrawn.** E1 shows that the extra synthesis call without decomposition
   (4.48 correctness) is not better than RAG alone (4.54), while the multi-agent
   pipeline reaches 4.74 (validation off) and 4.83 (validation on). The synthesis
   factorial (E2) is the direct test; the submitted 24.2% / −29.7% attribution is
   not used.

2. **The claim that the multi-agent pipeline improves correctness by 5.3% and
   reduces inconsistency by 48.3% is withdrawn.** The no-ReAct row was produced
   by the full pipeline because a case-sensitive dispatch check silently fell
   through; the condition never executed. Rev.1 implements a true single-pass
   tool-call condition. Tools-only scores below the standalone LLM (4.31 vs
   4.63); RAG recovers most of the gap (4.54); decomposition raises correctness
   (4.74/4.83); validation adds a small correctness/precision gain (+0.09/+0.08)
   at a depth cost (−0.18). These differences are small and are not
   significance-tested in the automated-judge analysis.

3. **"Hallucination reduced by 70%" and "56% of numbers come from parametric
   knowledge" are reframed.** SelfCheckGPT-NLI measures cross-sample
   inconsistency, not factual error; the metric is renamed accordingly, and the
   56% figure is withdrawn because the any-number ±5% match ignores entity and
   unit. A claim-aware audit (E4) is reported with its parser caveat; the guarded
   synthesis condition (E3b) is not completed.

4. **The evaluator-agreement claim is corrected.** Against the completed Rev.1
   expert scores, the Spearman correlations are 0.55 (correctness), 0.71
   (precision), and 0.34 (depth); the judge is more lenient on all metrics. The
   earlier ρ = 0.038 for precision is withdrawn; dimension-level correlations are
   removed because the expert did not score ablation variants.

5. **The "design principle" is replaced by a testable hypothesis.** The abstract
   and conclusion now state that, in retrieval-dominated nutrition QA, grounding
   and integration matter more than the number of specialists, and that
   consistency checking is worth its cost only when specialist outputs overlap
   on the same entity and attribute. This is conditional on the task, data
   coverage, and judge; it is not a general principle.

## Implementation corrections stated explicitly

We prefer to state these plainly rather than bury them in Methods.

| Issue | What the submitted version said | What the code did | Rev.1 action |
|---|---|---|---|
| No-ReAct condition | A no-ReAct multi-agent variant was evaluated | `mode == "no_react"` never matched; the variant ran the full pipeline | True `single_pass` path; submitted row withdrawn; E1 reports the six conditions |
| Evaluator identity | MiMo-V2.5-Pro, comparative scoring | DeepSeek-V4-Pro, absolute scoring | MiMo-V2.5-Pro absolute scoring; DeepSeek-V4-Pro as robustness judge; recomputed agreement |
| Agreement statistics | ρ = 0.83 / 0.67 / 0.37 | Not reproducible from deposited scores | Recomputed against Rev.1 expert: 0.55 (C), 0.71 (P), 0.34 (D); judge more lenient; dimension-level correlations removed |
| Consistency checks | Regex Ca:P and Ca/CP overlap rules | False positives on CP and cage numbers; Ca:P unsafe as a universal rule | Entity/attribute/unit/basis-aware validator; Ca:P opt-in; precision/recall reported |
| RAG depth | k = 1 | k = 2 in the deposited run | `Config.RAG_K`; retrieval hit@k reported; exact k-sensitivity incomplete; D4 proxy ITT in S19 |
| Router flag | Cross-validation flag gated synthesis | Flag was ignored | `validation_mode = auto/always/off`; flag now gates the checker |
| Token accounting | Router and synthesis tokens included | They were omitted | Full component accounting; cost table recomputed |
| Data counts | ~14,800 data points; 80 ingredients | Mixed units; 108 ingredient records | Separate records/parameters/cells; exact schema and completeness in Table S1 |

## Point-by-point responses

The full 78-item tracker is in `docs/paper/response_to_reviewers.md`; the
responses below follow the reviewer numbering. Each response states the action,
the location, and the evidence. Items that depend on a run still in progress are
marked.

### Reviewer 1

**R1.1 — Cross-validation claim exceeds the implemented rules.**
Accepted. The submitted text described consistency checks that the code did not
perform as described (regex Ca:P and Ca/CP overlap; see the implementation table).
Rev.1 rebuilds the checker around entity/attribute/unit/basis claims, handles both
attribute-first and value-first order, uses a 5% threshold, and maps commodity
short names and phase labels. On a 42-pair labeled set (16 conflicts, 12
consistent/unit-converted, 14 distractors) it reaches 16/16, 12/12, 14/14; this is
a synthetic rule-coverage test, not field precision. The synthesis section no
longer claims that cross-validation is the dominant driver: E1 shows the extra
synthesis call alone is not sufficient (4.48 vs 4.54 for RAG), and E2 shows that
validation-off (4.91), correct warnings (4.91), shuffled warnings (4.87), and
query-only synthesis (4.85) are numerically indistinguishable in the automated
scores (no significance test was run). The integration/validation mechanism is
therefore **not** supported by the Rev.1 automated evidence; no expert scoring of
the E2 conditions was performed, so this remains an automated-judge result rather
than an expert-confirmed one.

**R1.2 — Fig. 2 stages 1/2/4 without a stage 3.**
Accepted. The caption and panel labels now use Stage 1 (routing), Stage 2
(specialist execution), Stage 3 (consistency checking + integration). The figure
is regenerated from the current pipeline.

**R1.3 — Fig. 2 "Cross-Validation + Integration" overstates the synthesis step.**
Accepted. The label is now "Consistency checks + integration"; the text states
that the checker emits warnings and that the synthesis LLM integrates the
outputs. No claim of full validation remains.

**R1.4 — Baseline confounds architecture with data/tool access.**
Accepted. E1 adds the missing controls: standalone LLM, tools-only single ReAct,
tools+RAG, tools+RAG+synthesis, and multi-agent with validation off/on, all on the
same backbone and output budget. The baseline paragraphs in §2.4 and §3.6.1 now
distinguish "no tools" from "tools but no decomposition" and from "decomposition".
Results: tools-only 4.31 < RAG 4.54 < standalone 4.63 < multi-agent 4.74/4.83
(correctness; n = 54).

**R1.5 — D5 does not isolate cross-validation.**
Accepted. The D5 rows are removed. E2 varies six conditions that hold the
specialist outputs and output budget fixed (n = 54 each): concatenation 4.28;
validation + concatenation 4.11; synthesis with shuffled warnings 4.87; synthesis
with validation off 4.91; synthesis with correct warnings 4.91; query-only
synthesis 4.85. Correct vs shuffled warnings differ by +0.04, and query-only
synthesis — with no specialist outputs to integrate — is within 0.06 of full
synthesis. The submitted 24.2% / −29.7% figures are withdrawn. E2 does **not**
support an integration or validation benefit; the extra synthesis pass, or a judge
preference for its prose, is the more parsimonious explanation. No expert scoring
of the E2 conditions was performed; a human-scored E2 subset is stated as future
work, and no positive integration claim is made. Results are in Table 6 and §3.6.1.

### Reviewer 2

R2.1–R2.42 are tracked individually in `docs/paper/response_to_reviewers.md`.
The major methodological items are answered individually below; the remaining line
edits are grouped afterward.

**R2.1 — Synthesis gain attributed to cross-validation.**
Accepted. The submitted D5 changed concatenation, validation, and an extra LLM call
together, so it could not attribute the gain. E2 holds the specialist outputs and output
budget fixed (n = 54 each): concatenation 4.28; validation + concatenation 4.11; synthesis
with shuffled warnings 4.87; synthesis with validation off 4.91; correct warnings 4.91;
query-only synthesis 4.85. Correct vs shuffled differs by +0.04, and query-only — with no
specialist outputs to integrate — is within 0.06 of full synthesis. The 24.2% / −29.7%
attribution and the "cross-validation is dominant" claim are withdrawn; the extra synthesis
pass, or a judge preference for its prose, is the more parsimonious explanation. No expert
scoring of the E2 conditions was performed; a human-scored E2 subset is future work
(Table 6, §3.6.1).

**R2.2 — Ca:P rule unsafe for layers.**
Accepted. The Ca:P rule is removed from the default path and documented as opt-in, with a
species/phase and phosphorus-basis caveat. The rebuilt checker compares entity, attribute,
unit, and basis; on a 42-pair labeled set it detects 16/16 conflicts, keeps 12/12
consistent/unit-converted pairs, and stays silent on 14/14 distractors (§2.2.4,
Supplementary S7b; `tests/test_validation.py`).

**R2.3 — CP of an ingredient compared with a requirement.**
Accepted. The CP-vs-requirement comparison is removed. The checker compares only claims
that share entity, attribute, and basis; a feed CP value cannot be grouped with a
requirement CP value for a different entity. The legacy false positives ("CP … 8.8" read as
phosphorus; "cage 6" read as calcium) are regression tests.

**R2.4 — Baselines confound architecture with data/tool access.**
Accepted. E1 adds the missing controls: standalone, tools-only, tools+RAG,
tools+RAG+synthesis, and multi-agent validation off/on, on one backbone and output budget.
Tools-only scores 4.31, below the standalone LLM (4.63); RAG recovers to 4.54;
multi-agent reaches 4.74/4.83. The old D1/D5 rows are withdrawn.

**R2.5 — Correctness rubric rewards citation.**
Accepted. Rubric v2 separates correctness (all facts accurate) from provenance (0 = no
attribution, 1 = some key numbers, 2 = every key number attributed), scored as an
independent column; the "5 = accurate with direct citation" anchor is removed
(Supplementary S12; expert sheets carry `provenance_(0-2_or_NA)`). The primary expert has
now scored all 378 responses with the separated rubric; the submitted scores are not mixed
with it.

**R2.6 — Query provenance and selection bias.**
Accepted in part. §2.3.1 now states that the 195-query pool was compiled by the study team
from four existing query sets (120 English, 28 Chinese, 30 English advanced, and
17 Chinese advanced), and that the 54-query set was selected by purposeful
stratified selection across seven query types and six domains and fixed before
Rev.1 scoring. Two domain experts on the study team independently reviewed the
54 queries before Rev.1. Because selection was criterion-based rather than
random, no random seed is reported; we do not describe it as a random sample.
The source sets were assembled during system development and were not held out;
the developers had access to them, so some queries may have informed prompt and tool development. The final set was fixed before
Rev.1 scoring but is not an independent held-out benchmark. Supplementary S3
contains the 54-query set generated from the curated JSON; the 195-query pool is
in the repository. External independent query validation was not obtained.

**R2.7 — Bilingual language–breed confound.**
Accepted. §2.3.1 now states that the 12 Chinese queries include Hy-Line Brown and
feed/definition questions, not only domestic breeds; §3.5 labels the comparison
exploratory. E11 auto scores show Chinese 4.92 vs English 4.69 correctness (n=12/42; CIs
overlap), so we do not claim a Chinese correctness deficit; the cross-lingual concern is
the inconsistency score. Language and breed remain confounded.

**R2.8 — Chinese query breed counts inconsistent.**
Accepted. The counts are corrected: the 12 Chinese queries target Jingfen 6 (3) and Dawu
Jinfeng (5), plus one Hy-Line Brown and feed/definition questions. The S3 table is
regenerated from the query JSON; the stale "Jinghong 1" count is removed.

**R2.9 — Flesch applied to Chinese text.**
Accepted. Flesch Reading Ease is computed only for English responses (n=42); Chinese
responses are excluded because textstat has no validated Chinese variant. The manuscript
states this and does not compare readability across languages.

**R2.10 — Single primary expert; second rater only a subset.**
Accepted with a limitation. The primary expert scored all 378 responses on one blinded
sheet (Model_A–G, randomized within query). A repeat 120-response sheet from the primary
gives intra-rater ICC(2,1) = 0.995 (correctness), 0.996 (precision), and 0.932 (depth);
weighted κ = 0.995/0.996/0.931; Bland–Altman mean differences −0.02/−0.01/+0.08. Because
this is a same-expert repeat/copy pass, it measures consistency, not independent
reliability. An independent third rater gives ICC(2,1) = 0.847 (correctness), 0.876
(precision), 0.760 (depth); quadratic weighted κ = 0.846/0.874/0.758; Spearman ρ =
0.862/0.913/0.725; Bland–Altman mean differences −0.27/−0.11/+0.21. On the 120-response
subset, the independent rater's overall means place DeepSeek-V4-Flash (4.28) and
DeepSeek-V4-Pro (4.14) close to NutriAgent (4.12); the subset is not powered to reproduce
the full ranking. We report this subset as the reliability check and do not claim full
dual scoring of all 378 responses.

**R2.11 — No paired uncertainty or effect sizes.**
Accepted. Paired bootstrap CIs (10,000 resamples), Cohen's d_z, Wilcoxon signed-rank tests,
and Holm correction are now reported in Table 10. Against the strongest baseline
(DeepSeek-V4-Pro), ΔC = +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146), so the correctness
advantage is not significant; precision is +0.50 (unadjusted p = 0.037; p = 0.256 after
correction across all dimension tests), and the paired per-response overall is +0.20
(p = 0.062). Correctness differences from DeepSeek-V4-Flash, Qwen3.8-Flash, GLM-4.5-Air,
Qwen3-8B, and MiniMax-M2.5 remain significant after Holm correction. The submitted
significance claims are withdrawn; Table 3 is the model-version table, and Table 10 is the
statistical table.

**R2.12 — Two judge protocols and agreement recomputed.**
Accepted. The submitted Methods named MiMo-V2.5-Pro but the deposited configurations used
DeepSeek-V4-Pro with absolute scoring. Rev.1 uses MiMo-V2.5-Pro absolute scoring for all
responses and reports agreement against the completed expert scores: ρ = 0.55
(correctness), 0.71 (precision), 0.34 (depth); the judge is more lenient. The earlier
ρ = 0.038 for precision is withdrawn, so precision agreement is no longer described as
weak. Dimension-level correlations are removed because the expert did not score ablation
variants. We also found that bulk and per-item scoring differ in absolute level by 0.4–0.8
points (D2 Full 4.44 in the new bulk pass vs 4.04 per-item; the original pass was 4.81) while
the ordering is consistent; all comparisons are therefore within the same scoring mode,
and cross-mode absolute values are not pooled.

**R2.25 — The no-ReAct row undermines the ReAct narrative.**
Accepted, and the row is withdrawn. The submitted "Multi-Agent (no ReAct)" condition never
executed: a case-sensitive dispatch check fell through to the full pipeline. Rev.1
implements a true single-pass tool-call condition. In E1, tools-only scores 4.31, below
the standalone LLM (4.63); the multi-agent pipeline reaches 4.74/4.83. We no longer claim
that iterative ReAct reasoning is necessary; the data show that tool access alone is not
enough, and that decomposition plus a synthesis pass is associated with higher scores,
although E2 does not isolate whether specialist content or the extra pass drives it. The
dispatch defect and the withdrawal are stated in §3.6.1 and Table 7.

**R2.26 — D2 removal does not measure domain importance; information leak.**
Partially accepted. D2 removes the specialist and its tool, but the shared PoultryDB can
still surface public feed documents. We therefore call D2 an architectural-removal test,
not a hard data-removal test. E7 is the stricter test: on 20 Feed/Cross-Domain queries,
deleting the Feed specialist and filtering Feed Ingredient Bank documents out of RAG gives
4.70 correctness vs 4.40 for the full pipeline (+0.30), with precision +0.07 and depth
unchanged. Hard data removal did **not** reduce judged quality, which is a
judge-sensitivity negative result; it does not show that feed data can be removed in
deployment. Both limitations are stated in §3.6.1 and Table 7.

**R2.27 — D4 excludes retrieval failures.**
Accepted with a transparent proxy. The Rev.1 re-score includes all 54 correctness scores but did not retain a retrieval-failure flag; the four submitted-run exclusions cannot be reconstructed exactly. We therefore report a conservative proxy ITT in which the 16 E6 hit@5 misses are scored as system failures (1; 0-score sensitivity): +RAG 3.50 vs no-RAG 4.52 correctness (Δ −1.02; 95% CI −1.52 to −0.52; p < 0.001); precision Δ −1.18; depth Δ −1.00. Complete-case is null (+0.00 C, +0.02 P). This is explicitly labeled a proxy, not an exact four-query reconstruction (S19). Retrieval hit@k remains: hit@1 27.3%, hit@3 54.5%, hit@5 63.6%, MRR 0.411. We do not claim a RAG benefit.

**R2.28 — Error causes are asserted, not tested.**
Partially accepted. E14 is a numeric error audit on the 36 queries with ground truth:
32/36 correct at ±5% (88.9%), 4 wrong values, 0 without a numeric answer; ±2% is 83.3%.
The four failures are C-FIB-005 (11.6 vs 8.5), C-FIB-010 (2260 vs 48), C-XD-001 (0.27 vs
0.25), and C-XD-006 (1.45 decrease vs 5.125). A single-coder descriptive non-numeric table
is in Supplementary S10 (five categories, 9/54 low-score responses); a two-coder kappa is
**not completed**, and we state that scope rather than claiming a tested causal account.

**R2.33 — Model IDs, determinism, repeated runs.**
Accepted. Exact providers, model IDs, access dates, thinking modes, and token limits are in
Table 3 and `config/models.lock.yaml`. Temperature 0.0 reduces but does not eliminate
variability: E9 (10 queries × 3 runs, cache off) gives mean pairwise similarity 0.371
(range 0.106–0.870) and exact-match rate 0. All reported scores are single-run and are
labeled as such; small differences are not interpreted as effects.

**R2.34 — Cost and latency details.**
Accepted in part. The submitted USD 0.000723/query figure did not include router and
synthesis tokens, and no Rev.1 cost estimate was computed. Table 3 records model settings
and the pricing date; `config/pricing.yaml` records per-token prices. The cost figure is
reported as a submitted-run property, not as a Rev.1 measurement or an architectural
efficiency claim; latency distributions across repeated runs were not collected.

**R2.35 — Formulation recommendation overclaim.**
Accepted. The manuscript now states that the system provides informational retrieval and
structured calculations, not a complete ration formulation or a prospective feeding
recommendation; the formulation claim and its limitation are in the Limitations.

**R2.36 — Cross-breed benchmark comparison.**
Accepted. §2.1.3 now describes production benchmarks as breed- and guide-specific targets,
not as a like-for-like cross-breed ranking. Cross-breed comparisons are presented as
descriptive and are not used to rank breeds.

**R2.20 — Data provenance for Chinese breeds.**
Accepted in part. Breed-level sources are in `corpus/provenance.csv`, and Table S3
summarizes the source type and status. The file records the document/version and
distinguishes the Chinese industry source from international breeder guides. Of the
50 rows, 27 still need a primary source (mostly Chinese aggregator entries), 19 need
a version and URL, 3 need a license check, and 1 needs author input; these are
flagged in the status column rather than presented as resolved. Where a Chinese value
could not be matched to a primary technical document, it is labeled as
industry-compiled rather than as a breeder specification.

**R2.21 — Phase remapping undocumented.**
Accepted. The phase crosswalk is reported in Table S2 and `phase_crosswalk.csv`,
with the source phase, target phase, and the rule used for each breed. The main
text now points to the crosswalk rather than implying that phases are directly
interchangeable.

**R2.22 — “Data points” mixes units.**
Accepted. §2.1 now defines each count: ingredient records, parameters, populated
cells, and vitamin/mineral cells are reported separately, with units and missing
cells distinguished. The aggregate “data points” label is removed.

**R2.23 — Entity resolution is fragile.**
Partially accepted. A curated alias table is added, and E15 (39 perturbations)
gives 100% family-level resolution for exact, commodity-short, and case/whitespace
names, but only 37.5% for misspellings and 0% for Chinese aliases. The feed index
remains English-only and substring-based; we state this as a limitation rather
than claiming robust bilingual entity resolution.

**R2.30 — USDA source is wrong for eggs.**
Accepted. The egg-production share now cites Yang (2021); the USDA report is not
used as the source for that value.

**R2.31 — Balaguer percent vs percentage points.**
Accepted. The text now states "more than six percentage points" for fine-tuning and
"approximately five percentage points further" for RAG in the cumulative setup, and
no longer describes the difference as a percent increase.

**R2.32 — Nutritionist shortage is unsourced.**
Accepted. The workforce claim is removed from the argument or explicitly labeled
as contextual; it is no longer used as quantitative motivation.

**R2.37 — Seven vs six baselines; four vs seven query types.**
Accepted. §1/§2.4 now state six standalone LLM baselines plus one single-agent
architectural control, and seven query types across six knowledge domains. The
stale counts are removed from the abstract and Table 5 notes.

**R2.38 — General design principle overstated.**
Accepted. The “design principle applicable beyond poultry nutrition” sentence is
now framed as a hypothesis for future cross-domain work, not as a demonstrated
general conclusion (Conclusion and Limitations).

**R2.39 — SID definition; Stein is pigs.**
Accepted. SID is defined as standardized ileal digestibility; the Stein reference,
which concerns pigs, is removed from the poultry justification.

**R2.40 — “Species-independent” is imprecise.**
Accepted. The wording is changed to “shared across layer breeds”; the manuscript
no longer claims species independence for the shared ingredient/definition
modules.

**R2.41 — Suggested citations.**
Accepted. All three suggested works were verified by DOI and added: Ruchay et al.
(2027, agentic AI for livestock housing), Tian et al. (2026, foundation models in
precision livestock farming), and Silvestri et al. (2026, digital technologies in
animal housing). CottonBot (Kandamali et al., 2025) and the RAG-grounded greenhouse
architecture (Pardo-Pina et al., 2026) were also verified and added to the
Introduction and Table 1. The duplicate AgroLLM preprint was removed: the
peer-reviewed AgriEngineering version (Ravindran et al., 2026) is retained, and the
earlier Samuel et al. (2025) arXiv entry is no longer cited as independent evidence.

- **R2.13 / R2.14 / R2.15 / R2.16 / R2.17 / R2.18 (metrics).** SelfCheckGPT-NLI
  is renamed and interpreted as cross-sample inconsistency; the exact NLI model
  is `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` (the local snapshot is pinned in
  `config/models.lock.yaml`, with file hashes in the run manifest; the upstream
  repository revision is not recorded, which we state as a limitation); numeric
  faithfulness is described as a permissive
  any-number match, not provenance; the rule-based claim-aware audit (E4) is
  reported with its parser caveat, and the human-labeled subset is still pending.
  The tolerance implementation now matches the relative-error definition
  (`|p−g|/|g| ≤ τ`); E14 gives 32/36 correct at ±5% (88.9%), 83.3% at ±2%, with
  4 wrong values and no missing numeric answers. The old interval rule agrees on
  every case in this set.
- **R2.19–R2.24 (data and query description).** The 20-parameter schema, 108
  ingredient records, completeness, phase crosswalk, provenance, and entity
  resolution are reported in §2.1/§2.3 and Tables S1–S3; retrieval hit@k is
  reported (E6); the exact k-sensitivity is not completed, while the D4 proxy ITT is
  reported in R2.27 and S19.
  A 39-case perturbation test (E15) found 100% family-level resolution for exact,
  commodity short, and case/whitespace names, but only 37.5% family-correct for
  misspellings and 0% for Chinese aliases; the feed index is English-only, so
  Chinese inputs depend on the model translating the ingredient name before the
  tool call. We state this as a limitation rather than claiming robust bilingual
  entity resolution.
- **R2.29–R2.42 (positioning and line edits).** Categorical absence claims are
  softened; USDA is replaced by Yang (2021); Balaguer's 5% is corrected to
  percentage points; the workforce claim is sourced/softened; model IDs and
  determinism are corrected. A 10-query × 3-run check at temperature 0.0 gives mean
  pairwise similarity 0.371 (range 0.106–0.870) and exact-match rate 0, so all
  scores are labeled single-run and small differences are not overinterpreted
  (E9, §2.3.5). Cost details, formulation caveats, baseline counts, and
  SID/species-independent wording are corrected. The 60+ line edits are applied in
  the revised manuscript; page anchors are in the location guide at the top, and
  the PDF carries continuous line numbers.

### Reviewer 3

**R3.1 / R3.2 — Novelty vs NutriCHAT; adopted vs new components.**
Accepted. Supplementary S14 is a new attribution table that separates adopted components
(ReAct loop, four tools, RAG) from Rev.1 contributions (specialist routing, entity-aware
consistency checker, bilingual layer-hen corpus, E1/E2 factorial controls, blinded
re-score). Table 8 compares the design dimensions; the manuscript no longer presents
adopted components as novel.

**R3.3 — Related work on multi-agent mechanisms.**
Accepted in part. The related-work section now discusses specialist routing, validation,
and failure modes; we did not attempt a comprehensive survey of every multi-agent
framework. The N=5 choice is supported by E5 (next item). Retrieval hit@k (E6) still shows
k=1 misses most annotated targets; the D4 proxy ITT is reported in R3.10 and S19. We state
these as limitations rather than claiming an exact ITT or a complete k-sensitivity.

**R3.4 / R3.5 — D5 and D1 do not isolate the mechanism.**
Accepted. E2 holds inputs and output budget fixed and shows validation-off = correct
warnings = 4.91, shuffled 4.87, query-only 4.85, concatenation 4.28; the integration claim
is withdrawn. E1 provides the true single-pass and tools/RAG controls; the submitted
no-ReAct row was a dispatch defect and is withdrawn.

**R3.6 / R3.7 — Rules need justification; NLI model identity.**
Accepted. The checker now compares entity, attribute, unit, and basis, handles both word
orders, and uses a 5% threshold; the Ca:P rule is opt-in. E3's 42-pair test detects 16/16
conflicts and stays silent on 26 consistent/distractor pairs (rule-coverage caveat in S7b).
The NLI model is exactly `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`; the local snapshot is pinned in `config/models.lock.yaml`, file hashes are recorded by `run_manifest.py`, and the upstream revision is not recorded (stated as a limitation).

**R3.8 — Expert design; kappa vs rho.**
Completed. The primary expert scored 378 responses. A repeat 120-response sheet from the
primary gives intra-rater ICC(2,1) = 0.995/0.996/0.932 (correctness/precision/depth);
weighted κ = 0.995/0.996/0.931; it is a same-expert repeat/copy pass and is not used as an
independent rater. The independent third rater gives ICC(2,1) = 0.847 (correctness), 0.876
(precision), 0.760 (depth); quadratic weighted κ = 0.846/0.874/0.758; Spearman ρ =
0.862/0.913/0.725; Bland–Altman mean differences −0.27/−0.11/+0.21. We report both κ and ρ,
do not claim full dual scoring of all 378 responses, and have withdrawn the unverifiable
submitted rho values (R2.10).

**R3.9 — N=5 stabilization claim.**
Accepted. The unsupported stabilization wording is removed. E5 (20 queries) gives means
0.163/0.153/0.149 at N=5/10/20 with Pearson 0.977/0.963/0.995: N=5 is adequate for relative
comparisons, but absolute scores are N-dependent (Supplementary S6).

**R3.10 — D4 excludes retrieval failures.**
Accepted with a transparent proxy. The Rev.1 re-score has all 54 correctness scores but no retained failure flag; the four submitted-run exclusions cannot be reconstructed. Using the 16 E6 hit@5 misses as a conservative failure proxy (score 1), +RAG is 3.50 vs no-RAG 4.52 (Δ −1.02; 95% CI −1.52 to −0.52; p < 0.001); complete-case is null (4.52 vs 4.52). The proxy is labeled as such and is not an exact four-query ITT (S19). E6 hit@1 27.3%, hit@3 54.5%, hit@5 63.6% (MRR 0.411) still quantifies the retrieval miss rate.

**R3.11 — Cost comparison confounded; NutriCHAT model wrong.**
Accepted. NutriCHAT uses GPT-4o for generation and Claude Sonnet 4.5 as its evaluator; the
cost paragraph and Table 8 are corrected. The USD 0.0007 vs USD 0.0124 figures are explicitly
not treated as architectural efficiency.

**R3.12 — Chinese breed provenance.**
Accepted in part. `corpus/provenance.csv` and Table S3 separate breeder guides, the
jbzyw.com aggregator, and public feed tables; Chinese domestic rows obtained through the
aggregator are labeled as such. Of the 50 provenance rows, 27 still need a primary source,
19 need a version and URL, 3 need a license check, and 1 needs author input; these are
flagged in the status column, and the manuscript states this gap rather than presenting
every row as fully resolved.

**R3.13 — D1 controls not documented.**
Accepted. E1's six conditions are documented in Table 2, Table 3, and Supplementary S11a;
the output budget and backbone are held fixed.

**R3.14 — D2 does not measure domain importance; information leak.**
Partially accepted. D2 removes the specialist and its tool, but the shared PoultryDB can
still surface public feed documents; it is an architectural-removal test, not a strict
data-removal test. E7 is the stricter test: on 20 Feed/Cross-Domain queries, deleting the
Feed specialist and filtering Feed documents out of RAG gives 4.70 correctness vs 4.40 for
the full pipeline (+0.30). Data removal also does not reduce judged quality. Both D2 and
E7 are stated in §3.6.1 and Table 7.

**R3.15 — Query provenance and selection procedure.**
Accepted. §2.3.1 now states that the 195-query pool was compiled by the study team
from four existing query sets and that the 54-query set was selected by purposeful
stratified selection across seven query types and six domains, fixed before Rev.1
scoring. Two domain experts on the study team independently reviewed the set
before Rev.1. Because selection was criterion-based rather than random, no random
seed is reported; we do not claim a random sample. External independent query
validation was not obtained and is stated as a limitation.

**R3.16 — Faithfulness validation.**
Partially accepted. E4 is a rule-based claim-aware audit (direct entity+attribute support
10.9–16.7%, parser lower bound), not a human-labeled validation; the human-labeled subset
has not been completed. The manuscript states this explicitly.

**R3.17 — Prompt/tool control.**
Accepted. Supplementary S13 is a prompt/control matrix and Table 3 records the frozen
model settings; together they document which components are shared and which are
intentionally varied. Prompt text is in S2.

**R3.18 — Figures 4–8 overlap.**
Accepted. Figure 11 was replaced with the Rev.1 contrast figure; Fig. 5, 8, 9, and 10 were
regenerated from the primary expert scores; Fig. 6 and 7 were regenerated with
non-overlapping annotations and are labeled as submitted-run automated panels
(readability and cost). The Fig. 2 stage labels were also moved clear of the specialist
boxes. No panels were merged because they answer different questions.

### Reviewer 4

**R4.1 / R4.2 — Hallucination naming; numeric faithfulness under-emphasized.**
Accepted. SelfCheckGPT-NLI is renamed and interpreted as cross-sample inconsistency. The
0.444 numeric-faithfulness score is now a limitation: a strict claim-aware audit finds
direct support for only 10.9–16.7% of extracted claims (E4, parser lower bound). The human
labels for that audit are **not completed**; we do not report them as done.

**R4.3 / R4.4 / R4.8 — Architecture confound; D5; no-ReAct.**
Accepted. E1/E2 replace the confounded comparisons; the no-ReAct dispatch defect is
documented and the row is withdrawn. The submitted +5.3%/−48.3% claim is not used.

**R4.5 — Independent held-out benchmark.**
Accepted as a limitation. We did not obtain a query set authored outside the project; the
195-query pool will be available in the repository but was created by the same team and is
**not** used as a held-out benchmark. We do not claim external validity.

**R4.6 / R4.7 — Statistical comparison; EvaluatorLLM caution.**
Accepted. Table 10 now reports paired bootstrap CIs, d_z, Wilcoxon, and Holm correction for
the completed expert scores. Against DeepSeek-V4-Pro, ΔC = +0.20 (95% CI −0.09 to +0.50;
Holm p = 0.146), so the correctness advantage is not significant; precision is +0.50
(unadjusted p = 0.037; p = 0.256 after Holm correction across all dimension tests), and
the paired per-response overall is +0.20 (p = 0.062). The automated judge is used only for
within-dimension contrasts; bulk and per-item scoring differ by 0.4–0.8 points (D2 Full
4.44 new pass vs 4.04 per-item; original pass 4.81), so only within-mode/pass comparisons
are interpreted. E9 shows mean repeat-run similarity 0.371 and exact match 0/10, so small
differences are not interpreted as effects.

**R4.9 / R4.11 / R4.12 / R4.13 — Bilingual, Chinese provenance, design principle, length.**
Accepted in part. The bilingual analysis is exploratory (E11: Chinese 4.92 vs English 4.69
correctness, CIs overlap; inconsistency is the cross-lingual issue). Provenance is in
`corpus/provenance.csv` and Table S3, with unresolved fields (27 primary-source, 19
version/URL, 3 license, 1 author-input) flagged as a limitation. The design principle is
replaced by a testable hypothesis. Implementation details are in Supplementary S2/S13; the
main text was shortened where possible, but further trimming is deferred until the final
figure/table consolidation.

**R4.10 — Reproducibility package.**
Completed. The public release is available at https://github.com/sepnlab/NutriAgent
(commit `1d5795dc`). It contains the code, configuration, prompts, 54/195 query sets,
de-identified expert scores, audit files, and reproduction commands. API keys, raw expert
workbooks, and name/label maps are excluded. The layer-hen corpus is not redistributed
because some source terms (notably Chinese domestic-breed data compiled through jbzyw.com)
do not clearly permit redistribution; provenance and extraction are documented in Table S3.
A Zenodo DOI is optional and will be added only if an archive is created.

## Closing

We hope the revision addresses the reviewers' concerns. The expert scoring is complete:
the primary expert scored all 378 responses, and the Rev.1 main comparison is NutriAgent
4.34 vs 4.05 for the strongest baseline (DeepSeek-V4-Pro), with a correctness difference
of +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146); the precision difference is +0.50
(unadjusted p = 0.037; p = 0.256 after correction across all dimension tests). An
independent 120-response rater shows moderate-to-good score reliability (ICC 0.85 correctness, 0.88 precision,
0.76 depth), but the top rank is not stable in that subset; a repeat 120-response sheet
from the primary expert gives intra-rater ICC(2,1) = 0.995/0.996/0.932 and is reported as
same-expert consistency, not independent reliability. Remaining limitations are the human-labeled faithfulness
subset, the absence of an external held-out query set, the unresolved provenance fields,
and the reduced scope of E14. The code, blinded sheets, completed scores, audit artifacts,
and per-query scores are available in the repository (https://github.com/sepnlab/NutriAgent,
commit `1d5795dc`); the archive DOI will be added at acceptance.
