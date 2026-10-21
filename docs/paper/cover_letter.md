**Cover Letter — Agriculture Communications**

**Manuscript ID:** AGRCOM-D-26-00673
**Title:** NutriAgent: a controlled evaluation of specialist routing for layer-hen nutrition question answering
**Decision:** Major revision

Dear Editor,

We thank you and the four reviewers for the detailed and constructive reports. We are submitting a revised manuscript that responds to all 78 comments. The revision narrows the claims to what the evidence supports: the reviews identified places where the submitted text described behavior the code did not implement, and several conclusions that the original design could not support. We have recalibrated the contribution and state the changes plainly.

**What changed**

1. **Factorial controls replace the confounded D1/D5 comparisons.** We added a six-condition architecture factorial (standalone, tools-only, tools+RAG, tools+RAG+synthesis, multi-agent with validation off/on) and a six-condition synthesis factorial (concatenation, validation+concatenation, synthesis with validation off/shuffled/correct, query-only synthesis), all on one frozen model set and output budget.

2. **The consistency-checking layer was rebuilt and tested.** The submitted regex checks could read "crude protein … 8.8" as phosphorus and "cage 6" as calcium. The new validator compares entity, attribute, unit, and basis, handles both attribute-first and value-first order, uses a 5% threshold, and maps commodity short names and phase labels. A 42-pair labeled test now passes 16/16 conflicts, 12/12 consistent/unit-converted pairs, and 14/14 distractors; this is a rule-coverage test, not a field precision estimate.

3. **The evaluation record was corrected.** The submitted Methods named MiMo-V2.5-Pro, but the deposited configurations used DeepSeek-V4-Pro with absolute scoring; the reported agreement statistics (ρ = 0.83/0.67/0.37) are not reproducible. Rev.1 re-scores with MiMo-V2.5-Pro and reports agreement against the completed expert scores (ρ = 0.55 correctness, 0.71 precision, 0.34 depth); the earlier ρ = 0.038 for precision is withdrawn. The main comparison is complete: the primary expert scored all 378 blinded responses, and NutriAgent's overall score is 4.34 vs 4.05 for the strongest baseline (DeepSeek-V4-Pro); the correctness difference is +0.20 (95% CI −0.09 to +0.50; Holm p = 0.146), and the precision difference is +0.50 (unadjusted p = 0.037; Holm p = 0.256 across all dimension tests). The advantage is therefore descriptive and precision-oriented, not a corrected-significance gain. An independent 120-response rater shows moderate-to-good score reliability (ICC 0.85 correctness, 0.88 precision, 0.76 depth), but the top rank is not stable in that subset; a repeat 120-response sheet from the primary expert gives intra-rater ICC(2,1) = 0.995/0.996/0.932 and is reported as same-expert consistency, not independent reliability.

4. **Data, query, and model descriptions now match the deposited artifacts.** The exact 20-parameter schema, 108 ingredient records, 103 requirement rows, 1,131 performance rows, 556 definitions, and 2,144 PoultryDB documents replace the mixed "~14,800 data points" total; 59 phase labels (55 nutrition + 4 vitamin-only) are mapped with a mapping type, with 53 mapped to seven reference phases and 6 marked unmapped; per-breed provenance separates breeder guides, the jbzyw.com aggregator, and public feed tables, with unresolved source fields flagged. Model IDs, providers, access dates, thinking modes, and pricing dates are frozen in Table 3.

**Conclusion-level changes**

We were asked to identify changes that affect the paper's conclusions. The revision withdraws or reframes six claims:

- **Synthesis/cross-validation as the dominant driver is withdrawn.** In the synthesis factorial, validation-off and correct-warnings both score 4.91, shuffled 4.87, query-only synthesis 4.85, and concatenation 4.28. The extra synthesis call, not the specialist content or validation, is associated with the score increase; a judge preference for polished prose is a plausible alternative. The submitted 24.2%/29.7% attribution is not used.
- **The multi-agent +5.3%/−48.3% claim is withdrawn.** The no-ReAct condition never executed because of a case-sensitive dispatch defect; the row is removed. In the architecture factorial, tools-only scores below the standalone LLM, RAG recovers most of the correctness gap, and decomposition raises correctness; validation shows no measurable gain once the extra synthesis pass is controlled.
- **"Hallucination reduced by 70%" and "56% parametric" are reframed.** SelfCheckGPT-NLI measures cross-sample inconsistency, not factual error; the metric is renamed. A rule-based claim-aware audit finds direct entity+attribute support for only 10.9–16.7% of extracted claims, with a parser caveat; the 0.444 any-number score is not claim-level provenance.
- **The evaluator-agreement claim is corrected** to ρ = 0.55 (correctness), 0.71 (precision), and 0.34 (depth) against the completed Rev.1 expert scores. The judge scores more leniently on all metrics; precision agreement is substantial, and the earlier ρ = 0.038 is withdrawn.
- **The main-comparison margin is narrower than submitted.** The submitted 4.42 vs 3.80 (+0.62, strongest baseline DeepSeek-V4-Flash) is not replicated. The Rev.1 expert scores are NutriAgent 4.34, DeepSeek-V4-Pro 4.05, DeepSeek-V4-Flash 4.04, and Qwen3.8-Flash 4.01; the column-mean gap is 0.28, the correctness advantage over DeepSeek-V4-Pro is not significant after Holm correction (+0.20; 95% CI −0.09 to +0.50; p = 0.146), and the precision difference is +0.50 (unadjusted p = 0.037; p = 0.256 after correction across all dimensions). MiniMax-M2.5, not Qwen3-8B, is the lowest baseline.
- **The "design principle" is replaced by a testable hypothesis**: in retrieval-dominated nutrition QA, grounding and integration matter more than the number of specialists, and consistency checking is worth its cost only when specialist outputs overlap on the same entity and attribute.

We also report that single-run scores are not reproducible (mean repeat-run similarity 0.371, exact match 0/10), so small differences are not interpreted as effects.

**Fit with Agriculture Communications**

The manuscript addresses the journal's interest in AI-enabled agricultural decision support, digital poultry production, and reproducible evaluation of domain-specific language systems. It combines a structured layer-hen nutrition corpus, a specialist-routed architecture, bilingual evaluation, and a transparent component analysis. We believe the revision is more useful to readers because it separates what the architecture does from what the judge rewards, and identifies a descriptive precision advantage on structured queries while stating that it does not survive family-wise correction.

**Declarations**

- All authors have approved the revised submission and agree to its submission to Agriculture Communications.
- The work is not under consideration elsewhere.
- The manuscript is original; all sources are cited.
- The authors declare no competing interests.
- No animal experiments were conducted; all data are from public sources.
- Code, blinded sheets, audit artifacts, and per-query scores are available at https://github.com/sepnlab/NutriAgent (commit `1d5795dc`). The layer-hen corpus is not redistributed because some source terms do not clearly permit it; provenance and extraction are documented in Table S3. A Zenodo DOI is optional and will be added only if an archive is created.

Thank you for your time and consideration.

Yours sincerely,

Hai Lin (Corresponding Author)
Chairman, Livestock Environmental Hygiene Branch
Chinese Association of Animal Science and Veterinary Medicine
College of Animal Science and Technology, Shandong Agricultural University
