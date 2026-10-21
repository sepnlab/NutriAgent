# Rev.1 expert-score analysis

Primary: 378 responses; second: 120; third: 120.

## Primary model means (378 responses)

| Method | C | 95% CI | P | 95% CI | D | 95% CI | Overall | 95% CI | Provenance | n (C/P/D) |
|---|---:|---|---:|---|---:|---|---:|---|---:|---:|
| NutriAgent | 4.46 | 4.18–4.70 | 4.47 | 4.11–4.79 | 4.07 | 3.89–4.26 | 4.34 | 4.10–4.54 | 1.667 | 54/38/54 |
| DeepSeek-V4-Pro | 4.26 | 4.04–4.48 | 3.97 | 3.68–4.26 | 3.93 | 3.69–4.17 | 4.05 | 3.87–4.23 | 0.13 | 54/38/54 |
| DeepSeek-V4-Flash | 4.06 | 3.80–4.32 | 3.74 | 3.40–4.05 | 4.33 | 4.15–4.52 | 4.04 | 3.84–4.24 | 0.241 | 54/38/54 |
| Qwen3.8-Flash | 3.96 | 3.70–4.22 | 3.79 | 3.45–4.13 | 4.28 | 4.11–4.44 | 4.01 | 3.80–4.22 | 0.296 | 54/38/54 |
| GLM-4.5-Air | 3.74 | 3.41–4.06 | 3.63 | 3.24–4.00 | 3.28 | 3.11–3.44 | 3.55 | 3.28–3.80 | 0.0 | 54/38/54 |
| Qwen3-8B | 3.13 | 2.76–3.52 | 2.87 | 2.40–3.34 | 3.13 | 2.93–3.33 | 3.04 | 2.72–3.36 | 0.0 | 54/38/54 |
| MiniMax-M2.5 | 2.80 | 2.43–3.17 | 2.53 | 2.10–2.97 | 2.56 | 2.24–2.87 | 2.63 | 2.29–2.96 | 0.056 | 54/38/54 |

## Paired comparisons vs NutriAgent

| Baseline | ΔC [95% CI] | p (Holm) | d_z | ΔP | ΔD | ΔO |
|---|---:|---:|---:|---:|---:|---:|
| DeepSeek-V4-Pro | +0.20 [-0.09, +0.50] | 0.1459 | +0.18 | +0.50 | +0.15 | +0.20 |
| DeepSeek-V4-Flash | +0.41 [+0.09, +0.70] | 0.0264 | +0.36 | +0.74 | -0.26 | +0.20 |
| Qwen3.8-Flash | +0.50 [+0.17, +0.81] | 0.0140 | +0.41 | +0.68 | -0.20 | +0.26 |
| GLM-4.5-Air | +0.72 [+0.35, +1.11] | 0.0034 | +0.50 | +0.84 | +0.80 | +0.76 |
| Qwen3-8B | +1.33 [+0.94, +1.74] | 0.0000 | +0.87 | +1.60 | +0.94 | +1.21 |
| MiniMax-M2.5 | +1.67 [+1.24, +2.09] | 0.0000 | +1.04 | +1.95 | +1.52 | +1.65 |

## Second/third subset means (120 responses)

| Method | C2 | C3 | P2 | P3 | D2 | D3 |
|---|---:|---:|---:|---:|---:|---:|
| NutriAgent | 4.44 | 4.50 | 4.50 | 4.30 | 3.81 | 3.56 |
| DeepSeek-V4-Pro | 4.39 | 4.61 | 4.00 | 4.09 | 3.78 | 3.72 |
| DeepSeek-V4-Flash | 4.10 | 4.40 | 4.00 | 4.15 | 4.40 | 4.30 |
| Qwen3.8-Flash | 3.90 | 4.19 | 3.50 | 3.64 | 4.05 | 4.00 |
| GLM-4.5-Air | 3.65 | 4.18 | 3.60 | 3.90 | 3.41 | 3.06 |
| Qwen3-8B | 3.18 | 3.27 | 3.50 | 3.62 | 3.27 | 3.27 |
| MiniMax-M2.5 | 2.82 | 3.00 | 2.71 | 2.79 | 2.59 | 2.53 |

## Inter-rater agreement

| Pair | Metric | n | ICC(2,1) | weighted κ | Spearman ρ | BA mean (LoA) | exact | MAD |
|---|---|---:|---:|---:|---:|---|---:|---:|
| Repeat sheet vs Third (120) | correctness | 120 | 0.858 | 0.857 | 0.871 | -0.25 (-1.39, +0.89) | 0.68 | 0.35 |
| Repeat sheet vs Third (120) | precision | 80 | 0.879 | 0.878 | 0.916 | -0.10 (-1.33, +1.13) | 0.74 | 0.30 |
| Repeat sheet vs Third (120) | scientific_depth | 120 | 0.806 | 0.805 | 0.768 | +0.12 (-1.00, +1.25) | 0.66 | 0.34 |
| Repeat sheet vs Third (120) | provenance | 120 | 0.926 | 0.932 | 0.889 | +0.03 (-0.47, +0.54) | 0.93 | 0.07 |
| Primary vs repeat sheet (120, intra-rater) | correctness | 120 | 0.995 | 0.995 | 0.994 | -0.02 (-0.27, +0.23) | 0.98 | 0.02 |
| Primary vs repeat sheet (120, intra-rater) | precision | 80 | 0.996 | 0.996 | 0.996 | -0.01 (-0.23, +0.21) | 0.99 | 0.01 |
| Primary vs repeat sheet (120, intra-rater) | scientific_depth | 120 | 0.932 | 0.931 | 0.914 | +0.08 (-0.57, +0.73) | 0.88 | 0.12 |
| Primary vs repeat sheet (120, intra-rater) | provenance | 120 | 0.972 | 1.000 | 0.954 | -0.03 (-0.33, +0.28) | 0.97 | 0.03 |
| Primary vs Third (120) | correctness | 120 | 0.847 | 0.846 | 0.862 | -0.27 (-1.45, +0.92) | 0.67 | 0.37 |
| Primary vs Third (120) | precision | 80 | 0.876 | 0.874 | 0.913 | -0.11 (-1.36, +1.14) | 0.72 | 0.31 |
| Primary vs Third (120) | scientific_depth | 120 | 0.760 | 0.758 | 0.725 | +0.21 (-1.06, +1.48) | 0.64 | 0.39 |
| Primary vs Third (120) | provenance | 120 | 0.916 | 0.928 | 0.865 | +0.01 (-0.53, +0.55) | 0.93 | 0.07 |

## Data-integrity note

- The primary repeat 120-response sheet is a same-expert repeat/copy pass (user-confirmed; 118/120 exact correctness, 79/80 precision, 106/120 depth; ICC 0.995/0.996/0.932; notes median similarity 0.70, 38/109 ≥0.80). It is reported as intra-rater consistency, not independent inter-rater.
- The independent third rater vs primary gives ICC 0.847/0.876/0.760; weighted kappa 0.846/0.874/0.758; notes median similarity 0.30. The 120 subset does not reproduce the full top rank (third-rater overall: DeepSeek-V4-Flash 4.28, DeepSeek-V4-Pro 4.14, NutriAgent 4.12).
- The primary 378-response table (Table 9) remains the main analysis; the subset is a reliability check, not a ranking replication.
