# Agreement and paired-difference report (recomputed)

> **SUPERSEDED (submitted-run scores).** These correlations were computed against the
> submitted 54-query expert scores and are retained as an audit trail. The final Rev.1
> agreement against the completed 378-response primary-expert scores is ρ = 0.55
> (correctness), 0.71 (precision), and 0.34 (depth), reported in
> `docs/paper/audit/expert_analysis.json` and the manuscript. The precision value below
> (0.038) is not the Rev.1 estimate.

> Source: `logs\comp_layer_20260612_183548`  
> Bootstrap: 10000 resamples, seed=42

## 1. EvaluatorLLM–expert agreement

| Scope | Metric | n | Spearman ρ | 95% CI | Within 1 point |
|---|---|---:|---:|---|---:|
| nutriagent | correctness | 54 | 0.575 | [0.246, 0.807] | 0.926 |
| nutriagent | precision | 34 | 0.038 | [-0.272, 0.419] | 0.794 |
| nutriagent | scientific_depth | 54 | 0.529 | [0.274, 0.734] | 0.926 |
| pooled | correctness | 378 | 0.478 | [0.388, 0.564] | — |
| pooled | precision | 237 | 0.156 | [0.027, 0.285] | — |
| pooled | scientific_depth | 378 | 0.516 | [0.435, 0.591] | — |

> The submitted values (0.83 / 0.67 / 0.37) are not reproduced by the deposited scores.

## 2. Paired expert differences (NutriAgent − baseline)

| Baseline | Metric | n | Δ mean | 95% CI | d_z | Wilcoxon p | Holm p |
|---|---|---:|---:|---|---:|---:|---:|
| aliyun/Qwen3-8B | correctness | 54 | 1.1296 | [0.7593, 1.5185] | 0.784 | 1e-05 | 6e-05 |
| aliyun/Qwen3-8B | precision | 37 | 1.4865 | [0.973, 2.0] | 0.904 | 7e-05 | 0.00042 |
| aliyun/Qwen3-8B | scientific_depth | 54 | 1.2037 | [0.9259, 1.4444] | 1.206 | 0.0 | 0.0 |
| siliconflow/GLM-4.5-Air | correctness | 54 | 0.7593 | [0.4074, 1.1296] | 0.553 | 0.00048 | 0.0024 |
| siliconflow/GLM-4.5-Air | precision | 38 | 1.0789 | [0.5789, 1.5526] | 0.674 | 0.00093 | 0.00372 |
| siliconflow/GLM-4.5-Air | scientific_depth | 54 | 1.037 | [0.7778, 1.2963] | 1.068 | 0.0 | 0.0 |
| aliyun/Qwen3.5-Flash | correctness | 54 | 0.7222 | [0.3519, 1.0926] | 0.514 | 0.00098 | 0.00392 |
| aliyun/Qwen3.5-Flash | precision | 36 | 1.3333 | [0.7778, 1.8889] | 0.773 | 0.00035 | 0.00175 |
| aliyun/Qwen3.5-Flash | scientific_depth | 54 | 0.3704 | [0.0926, 0.6296] | 0.352 | 0.01203 | 0.01203 |
| deepseek/DeepSeek-V4-Pro | correctness | 54 | 0.4074 | [0.0926, 0.7222] | 0.334 | 0.01997 | 0.01997 |
| deepseek/DeepSeek-V4-Pro | precision | 38 | 0.7368 | [0.2895, 1.1579] | 0.523 | 0.00518 | 0.01554 |
| deepseek/DeepSeek-V4-Pro | scientific_depth | 54 | 0.6111 | [0.3704, 0.8333] | 0.696 | 4e-05 | 0.00012 |
| deepseek/DeepSeek-V4-Flash | correctness | 54 | 0.4444 | [0.1296, 0.7593] | 0.368 | 0.00896 | 0.01792 |
| deepseek/DeepSeek-V4-Flash | precision | 39 | 0.7436 | [0.2821, 1.1795] | 0.508 | 0.00704 | 0.01554 |
| deepseek/DeepSeek-V4-Flash | scientific_depth | 54 | 0.5185 | [0.2778, 0.7407] | 0.586 | 7e-05 | 0.00014 |
| siliconflow/MiniMax-M2.5 | correctness | 54 | 0.4815 | [0.1481, 0.8148] | 0.388 | 0.00583 | 0.01749 |
| siliconflow/MiniMax-M2.5 | precision | 36 | 0.8611 | [0.3333, 1.3611] | 0.548 | 0.00625 | 0.01554 |
| siliconflow/MiniMax-M2.5 | scientific_depth | 54 | 0.6852 | [0.4074, 0.9444] | 0.681 | 2e-05 | 8e-05 |
