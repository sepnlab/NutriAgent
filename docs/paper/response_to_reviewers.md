# Response to Reviewers — NutriAgent (AGRCOM-D-26-00673)

> **Status**: tracker (working package). The submission letter is `response_letter.md`.
> Reviewer comments are preserved in `docs/paper/review_round1/extracted/reviews.txt`.
> Status definitions: `DONE` = new evidence/text with a location; `PARTIAL` = addressed
> with an explicit remaining limitation; `LIMITATION` = not done, stated as a boundary;
> `AUTHOR_INPUT` = author/repository detail still needed.

## Status summary

- DONE: **57**
- PARTIAL: **19**
- LIMITATION: **1**
- AUTHOR_INPUT: **1**
- Total: **78** (R1 = 5, R2 = 42, R3 = 18, R4 = 13)

The letter does not claim all comments are fully satisfied; it states that all are
addressed and identifies the remaining limitations.

## Comment-response tracker

| ID | Concern (short) | Type | Severity | Action | Status | Location / note |
|---|---|---|---|---|---|---|
| R1.1 | Cross-validation claim exceeds implemented rules | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E3 42-pair rule coverage (S7b); E2 automated pattern; no expert E2 subset |
| R1.2 | Fig. 2 stages 1/2/4 (no stage 3) | presentation | minor | ACCEPT_FIGURE | **DONE** | Fig. 2 Stages 1–3; labels moved clear of boxes |
| R1.3 | Fig. 2 "Cross-Validation + Integration" overstates | presentation | minor | ACCEPT_FIGURE/TEXT | **DONE** | Fig. 2 label: consistency checks + integration |
| R1.4 | Baseline confounds architecture with data/tools | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E1 six-condition architecture factorial; §2.4/§3.6.1 |
| R1.5 | D5 does not isolate cross-validation | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E2 six-condition synthesis factorial; expert E2 subset not run |
| R2.1 | Synthesis gain attributed to cross-validation | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E2 automated pattern; expert E2 subset not run |
| R2.2 | Ca:P rule nutritionally unsafe for layers | evidence | major | ACCEPT_TEXT/ANALYSIS | **DONE** | Ca:P opt-in; E3 42-pair rule coverage; §2.2.4/S7b |
| R2.3 | CP ingredient vs requirement compared | evidence | major | ACCEPT_TEXT | **DONE** | CP-vs-requirement comparison removed |
| R2.4 | Standalone baselines lack tools/RAG | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E1 controls; tools-only 4.31 vs standalone 4.63 |
| R2.5 | Correctness rubric rewards citation | statistical | major | ACCEPT_TEXT/ANALYSIS | **DONE** | Rubric v2; expert provenance column; evaluator rubric v1 disclosed (S2.4) |
| R2.6 | Query pool provenance/selection bias | methodological | major | ACCEPT_TEXT + AUTHOR_INPUT | **DONE** | §2.3.1: team-compiled pool, purposeful selection, fixed before Rev.1; not held out (R4.5) |
| R2.7 | Bilingual language–breed confound | evidence | major | SOFTEN_CLAIM + PARTIAL | **DONE** | §3.5 exploratory; E11 CIs overlap |
| R2.8 | Chinese query breed counts inconsistent | data | major | ACCEPT_TEXT | **DONE** | S3 regenerated from curated JSON; 42 EN / 12 ZH |
| R2.9 | Flesch applied to Chinese? | statistical | major | ACCEPT_TEXT | **DONE** | Flesch English-only (n=42) |
| R2.10 | Single primary expert; subset second rater | statistical | major | ACCEPT_ANALYSIS | **DONE** | Primary 378; repeat 120 intra-rater; independent 120 ICC 0.847/0.876/0.760; kappa/BA reported |
| R2.11 | No paired uncertainty/effect sizes | statistical | major | ACCEPT_ANALYSIS | **DONE** | Table 10: paired bootstrap, d_z, Wilcoxon, Holm |
| R2.12 | Two judge protocols; weak precision agreement | statistical | major | ACCEPT_TEXT/ANALYSIS | **DONE** | MiMo absolute scoring; rho 0.55/0.71/0.34 |
| R2.13 | SelfCheckGPT not a factual-error rate | interpretation | major | ACCEPT_TEXT | **DONE** | Renamed SelfCheckGPT-NLI inconsistency throughout |
| R2.14 | NLI model identity/implementation unclear | methodological | major | ACCEPT_TEXT | **PARTIAL** | Exact HF ID + local pin; upstream revision not recorded |
| R2.15 | Numeric faithfulness ignores entity/unit | methodological | major | ACCEPT_ANALYSIS | **PARTIAL** | E4 rule-based audit (10.9–16.7%); human labels pending |
| R2.16 | Semantic faithfulness validation missing | methodological | major | ACCEPT_ANALYSIS | **PARTIAL** | E4 parser audit + caveat; human-labeled validation pending |
| R2.17 | 56% numeric claims = parametric knowledge | interpretation | major | ACCEPT_TEXT | **DONE** | Derived/unit values distinguished; S7 |
| R2.18 | Tolerance definition asymmetric | statistical | major | ACCEPT_ANALYSIS | **DONE** | Relative-error equation; E14 32/36 at ±5% |
| R2.19 | 20-parameter schema inconsistent; Ca missing | data | major | ACCEPT_TEXT | **DONE** | 20-field schema with units/basis; §2.1.2/Table S1 |
| R2.20 | Data provenance for Chinese breeds | data | major | ACCEPT_TEXT + AUTHOR_INPUT | **PARTIAL** | provenance.csv + Table S3; 27 primary-source/19 version-URL/3 license/1 author-input flagged |
| R2.21 | Phase remapping undocumented | data | major | ACCEPT_TEXT | **DONE** | Table S2 + phase_crosswalk.csv |
| R2.22 | "Data points" mixes units | data | major | ACCEPT_TEXT | **DONE** | Records/parameters/cells separated; §2.1 |
| R2.23 | Entity resolution fragile | methodological | major | PARTIAL | **PARTIAL** | Alias table; E15 misspelling 37.5%, Chinese 0% stated |
| R2.24 | k=1 rationale vs "breadth" | methodological | major | ACCEPT_TEXT | **PARTIAL** | §2.2.5 + E6 hit@k; system-level k-sensitivity not run |
| R2.25 | no-ReAct result weakens ReAct narrative | evidence | **blocking** | ACCEPT_EXPERIMENT + CORRECTION | **DONE** | Dispatch defect documented; no-ReAct row withdrawn; E1 true single-pass |
| R2.26 | D2 removal leaks information | evidence | major | ACCEPT_EXPERIMENT | **PARTIAL** | D2 architectural-removal caveat; E7 hard removal (n=20) |
| R2.27 | D4 excludes retrieval failures | evidence | major | ACCEPT_ANALYSIS | **PARTIAL** | D4 proxy ITT in S19; exact four-query flag not recoverable |
| R2.28 | Error causes not tested | interpretation | major | PARTIAL | **PARTIAL** | E14 numeric + single-coder descriptive S10; two-coder kappa not done |
| R2.29 | Categorical absence claims | citation | major | ACCEPT_TEXT | **DONE** | Absence claims bounded; CottonBot/greenhouse added |
| R2.30 | USDA source wrong for eggs | citation | major | ACCEPT_TEXT | **DONE** | Yang (2021) for egg-production share |
| R2.31 | Balaguer percent vs percentage points | citation | major | ACCEPT_TEXT | **DONE** | Percentage points wording corrected |
| R2.32 | Nutritionist shortage unsourced | citation | major | ACCEPT_TEXT | **DONE** | Workforce claim labeled contextual |
| R2.33 | Model IDs/determinism/repeated runs | reproducibility | major | ACCEPT_TEXT | **DONE** | Table 3 + models.lock; E9 repeat-run variability |
| R2.34 | Cost/latency details incomplete | reproducibility | major | ACCEPT_ANALYSIS | **PARTIAL** | Submitted-run cost only; no Rev.1 cost or latency distribution |
| R2.35 | Formulation recommendation overclaim | interpretation | major | ACCEPT_TEXT | **DONE** | Formulation caveat in Limitations |
| R2.36 | Cross-breed benchmark comparison | interpretation | major | ACCEPT_TEXT | **DONE** | Guide-specific targets; §2.1.3 |
| R2.37 | Seven vs six baselines; 4 vs 7 types | data | major | ACCEPT_TEXT | **DONE** | Six baselines + single-agent control; seven query types |
| R2.38 | General design principle overstated | interpretation | major | SOFTEN_CLAIM | **DONE** | Design principle reframed as hypothesis |
| R2.39 | SID definition; Stein is pigs | citation | minor | ACCEPT_TEXT | **DONE** | SID definition; Stein removed |
| R2.40 | "Species-independent" imprecise | interpretation | minor | ACCEPT_TEXT | **DONE** | “Shared across layer breeds”; Fig. 1 |
| R2.41 | Suggested citations | citation | minor | ADD_CITATION | **DONE** | Three suggested DOIs verified + CottonBot/greenhouse; duplicate AgroLLM removed |
| R2.42 | 60+ line-level edits | presentation | minor | ACCEPT_TEXT | **DONE** | Line edits applied; this build |
| R3.1 | Novelty vs NutriCHAT unclear | citation/positioning | major | ACCEPT_TEXT | **DONE** | S14 attribution table; Table 8 |
| R3.2 | Adopted vs new components unclear | citation/positioning | major | ACCEPT_TEXT | **DONE** | S14 adopted vs new components |
| R3.3 | Related work on multi-agent mechanisms | citation | major | ACCEPT_TEXT | **PARTIAL** | Related-work paragraph + CottonBot/greenhouse; no comprehensive survey |
| R3.4 | D5 does not isolate validation | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E2 factorial; integration claim withdrawn |
| R3.5 | D1 no-ReAct undermines ReAct | evidence | **blocking** | ACCEPT_EXPERIMENT + CORRECTION | **DONE** | E1/E2; dispatch defect corrected |
| R3.6 | Rules need technical justification | evidence | major | ACCEPT_TEXT/ANALYSIS | **PARTIAL** | E3 42-pair rule coverage (S7b); field false-positive rate not measured |
| R3.7 | NLI model naming inconsistent | methodological | major | ACCEPT_TEXT | **DONE** | NLI model identity fixed; exact HF ID |
| R3.8 | Expert/judge design; kappa vs rho | statistical | major | ACCEPT_ANALYSIS | **DONE** | ICC/kappa/BA reported; not full dual scoring |
| R3.9 | N=5 claim unsupported | statistical | major | ACCEPT_ANALYSIS | **DONE** | E5 N=5/10/20; absolute scores N-dependent |
| R3.10 | D4 excludes failures | evidence | major | ACCEPT_ANALYSIS | **PARTIAL** | D4 proxy ITT S19; complete-case null |
| R3.11 | Cost comparison confounded; NutriCHAT model wrong | evidence | major | ACCEPT_TEXT | **DONE** | NutriCHAT GPT-4o generated; Claude evaluator; Table 8 |
| R3.12 | Chinese breed provenance | data | major | ACCEPT_TEXT + AUTHOR_INPUT | **PARTIAL** | provenance.csv + Table S3; unresolved fields flagged |
| R3.13 | D1 controls not documented | evidence | major | ACCEPT_TEXT | **DONE** | E1 controls; Table 2/3/S11a |
| R3.14 | D2 does not measure domain importance | evidence | major | ACCEPT_EXPERIMENT | **PARTIAL** | D2 + E7; caveat stated |
| R3.15 | Query provenance/selection procedure | methodological | major | ACCEPT_TEXT + AUTHOR_INPUT | **DONE** | §2.3.1: pool authorship/timing, purposeful selection, not held out |
| R3.16 | Faithfulness metric validation | methodological | major | ACCEPT_ANALYSIS | **PARTIAL** | E4 parser audit; human labels pending |
| R3.17 | Prompt control contradictory | methodological | major | ACCEPT_TEXT | **DONE** | S13 prompt matrix; S2 prompts |
| R3.18 | Figures 4–8 overlap | presentation | minor | ACCEPT_FIGURE | **DONE** | Fig. 6/7 regenerated; Fig. 2 labels cleared |
| R4.1 | "Hallucination" too strong | interpretation | major | ACCEPT_TEXT | **DONE** | Renamed; numeric limitation emphasized |
| R4.2 | Numeric faithfulness under-emphasized | interpretation | major | ACCEPT_ANALYSIS | **PARTIAL** | §3.4 reweighted; human labels pending |
| R4.3 | Architecture vs data/tool confound | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E1 architecture factorial |
| R4.4 | D5 does not isolate validation | evidence | major | ACCEPT_EXPERIMENT | **DONE** | E2 synthesis factorial |
| R4.5 | Independent held-out benchmark | evidence | major | PARTIAL | **LIMITATION** | No external held-out set; 195 pool not used as such |
| R4.6 | Statistical comparison | statistical | major | ACCEPT_ANALYSIS | **DONE** | Table 10 paired inference; bulk/per-item caveat |
| R4.7 | EvaluatorLLM ablation caution | statistical | major | PARTIAL | **DONE** | Judge within-dimension only; expert primary |
| R4.8 | no-ReAct result deserves discussion | evidence | **blocking** | ACCEPT_EXPERIMENT + CORRECTION | **DONE** | Dispatch defect; row withdrawn |
| R4.9 | Bilingual interpretation | interpretation | major | SOFTEN_CLAIM | **DONE** | Bilingual exploratory; E11 |
| R4.10 | Reproducibility package | data/code | major | ACCEPT_TEXT | **AUTHOR_INPUT** | Repository assembled; public push pending |
| R4.11 | Chinese data provenance | data | major | ACCEPT_TEXT + AUTHOR_INPUT | **PARTIAL** | provenance.csv + Table S3; unresolved fields flagged |
| R4.12 | Design principle → hypothesis | interpretation | minor | SOFTEN_CLAIM | **DONE** | Design principle reframed as hypothesis |
| R4.13 | Manuscript too long | presentation | minor | ACCEPT_TEXT | **PARTIAL** | Details moved to S2/S13; further trimming deferred |
