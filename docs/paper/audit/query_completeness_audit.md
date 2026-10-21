# Query completeness audit — 54 curated queries (2026-10-21)

Scope: the 54-query set used for E18 / the expert scoring package, across six categories
(Feed Ingredient Bank, Nutrient Requirements, Performance Management, Definitions,
Cross-Domain, Edge Cases). Method: read every query, check text length/terminators/
duplicates, compare the expert CSV against the source JSON, and look up the referenced
corpus rows for expected values.

## 1. Text-level result

- 54 unique IDs; no empty query; no truncated sentence.
- All 54 end with `?`, `？`, or `。`; 42 English, 12 Chinese.
- Shortest query 12 characters (C-FIB-009), longest 198 (C-XD-001).
- The `query` column in the 378-row and 120-row expert sheets is identical to the source
  JSON for all rows (0 mismatches).
- **48/54 are fully self-contained.** Six need a clarification (below); no query was
  rewritten, because the generated responses must remain aligned with the prompt.

## 2. Queries needing a clarification

| ID | Issue | Resolution |
|---|---|---|
| C-XD-005 | Original formula says only "60% maize"; to compute the SBM increase, the other 40% must be SBM48. | `query_note`: remaining 40% is SBM48; expected answer +4.33 pp. |
| C-XD-006 | "CP contribution change" can mean the new contribution (11.70%) or new minus original (−1.45 pp). | `query_note`: report the change; expected −1.45 pp. |
| C-FIB-004 | ME unit/source not stated; truth uses feed-bank kcal/kg. | `query_note`: use feed-bank ME in kcal/kg; reference gives both values. |
| C-FIB-005 | CP source not stated; truth uses feed-bank values. | `query_note`: use feed-bank CP in %. |
| C-FIB-010 | ME unit/source not stated; truth uses kcal/kg. | `query_note`: use feed-bank ME in kcal/kg; MJ/kg conversions accepted. |
| C-EC-005 | ME unit/source not stated; limestone is a mineral with ME=0. | `query_note`: report both ME values; limestone = 0. |

These six are marked in the `query_note` column of both expert workbooks and in
`04_查询真值表.xlsx`.

## 3. Truth/reference corrections

The following were **metadata/truth errors**, not query-text errors. They were corrected in
`queries/layer/evaluation_queries_curated.json` and in the expert truth table.

| ID | Old metadata | Corrected | Why |
|---|---|---|---|
| C-XD-005 | expected 0.04 | **4.33 percentage points** | 0.04 is the fraction, not the percentage-point increase; SBM 40% → 44.33%. |
| C-XD-006 | expected 11.7% | **1.45 percentage-point decrease** | 11.70% is the new contribution, not the change (13.15 → 11.70). |
| C-FIB-004 | expected 3090 only | both values + direction | Maize 3090; soft wheat 2860; maize +230 kcal/kg. |
| C-FIB-005 | expected 11.6 only | both values + direction | SBM48 52.6%; canola 41.0%; SBM +11.6 pp. |
| C-FIB-010 | expected 2260 only | both values + direction | SBM48 2260; rapeseed meal 1450; SBM +810 kcal/kg. |
| C-NR-004 | expected 4.44 only | both phases + direction | Lay I 4.04%; Lay III 4.44%; Lay III +0.40 pp. |
| C-NR-005 | expected 4.04 only | both breeds + direction | ISA 4.04%; Dawu 3.90%; ISA +0.14 pp. |
| C-NR-011 | expected 4.20 only | both phases + direction | Lay I 3.90%; Lay III 4.20%; +0.30 pp. |
| C-PM-003 | expected 95.7 only | both breeds + direction | ISA 95.5%; Hy-Line 95.7%; Hy-Line +0.2 pp. |
| C-PM-004 | expected 113 only | both breeds + direction | ISA 112; Hy-Line 113; Hy-Line +1 g/d. |
| C-PM-010 | expected 95.7 only | both breeds + direction | Jingfen 6 95.5%; Hy-Line 95.7%; +0.2 pp. |
| C-PM-011 | expected 95.5 only | both outputs | Hen-day 95.5%; egg weight 55.0 g. |
| C-PM-005 | no reference | three weights | Week 5 370 g; week 10 894.5 g; week 15 1307.5 g. |
| C-FIB-006 | no reference | example set | Any three plant proteins >30% CP; e.g. SBM48 52.6, canola 41.0, rapeseed 38.1. |
| C-FIB-007 | no reference | both digestibilities | Maize Lys SID 90%, SBM48 88%; absolute SID Lys 1.89 vs 22.26 g/kg. |
| C-NR-006 | no reference | phase series | Developer 1.01%; Pre-Lay 2.52%; Lay I 4.04%; Lay II 4.24%; Lay III 4.44%. |
| C-XD-001 / 003 / 004 / 009 | value only | value + yes/no | Added "does/does not meet" to expected behavior. |
| C-EC-005 | behavior only | both ME values | Fish meal 3180; limestone 0; fish meal higher. |

In total, **21 query records** were updated (2 expected values + 19 expected-behavior
entries). The query text itself was left unchanged to preserve the response/prompt
correspondence; the clarification is delivered through `query_note` and
`expected_behavior`.

## 4. Non-blocking observations

- **C-PM-006 and C-XD-007 are near-duplicates**: both ask for daily Ca intake for ISA Brown
  at week 30 with 112 g/day and 4.04% Ca. They are retained as a Performance vs
  Cross-Domain pair, but the overlap should be noted in the query-set description.
- **Open-ended queries** (C-FIB-006/007, C-NR-006, C-XD-008) have no single scalar truth;
  the truth table now gives reference facts or constraints, and the rubric should be used.
- **C-EC-004** deliberately accepts two behaviors (provide the value or flag the column
  name); it remains an edge case, not a factual query with one answer.

## 5. Verification after the fix

- Source JSON: 54 queries, 36 with expected values, 25 with expected behavior.
- Expert package: 378 primary + 120 second rows; 54/54 query coverage; no model-identity
  map copied; `query_note` present only for the six flagged IDs.
- E14 re-run with corrected metadata: 32/36 correct at ±5% (88.9%), 83.3% at ±2%;
  failures are C-FIB-005, C-FIB-010, C-XD-001, C-XD-006. C-XD-005 now passes (4.34 vs
  4.33).

## 6. Artifacts

- `queries/layer/evaluation_queries_curated.json` — corrected metadata.
- `scripts/paper/fix_query_truth.py` — 21-entry correction record.
- `scripts/paper/build_expert_package.py` — package builder with `query_note`.
- Desktop package: `NutriAgent_专家评分_20261021` (xlsx/docx/CSV/JSON).
