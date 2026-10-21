# NutriAgent 论文绘图数据汇总

> 所有数据来源：`logs/comp_layer_20260612_183548/report.json`（expert evaluation）+ `logs/ablation_*/`（消融实验）。
> 生成脚本：`docs/paper/generate_figures.py`
> 最后更新：2026-06-20

---

## Fig 4: Ablation ΔC Bar Chart

数据来源：Table 5（EvaluatorLLM evaluation）

| Dimension | ΔC | Direction |
|-----------|-----|-----------|
| D1: Architecture (Single → Multi) | +0.24 | Improvement |
| D2: Specialist (w/o Performance) | −0.20 | Degradation |
| D3: Routing (Broadcast → LLM) | −0.19 | Degradation |
| D4: RAG (no RAG → +RAG) | +0.08 | Improvement |
| D5: Synthesis (no → with) | +0.93 | Improvement |
| D6: LLM Backbone (Qwen3-8B → DS-V4-Flash) | −0.74 | Degradation |

注：D1/D4/D5 的 control 是较弱配置（正Δ=改进），D2/D3/D6 的 control 是较强配置（负Δ=退化）。

---

## Fig 5: Main Comparison (Expert Evaluation, n=54)

数据来源：Table 3 + report.json

| Method | Correctness | Precision | Sci. Depth | Overall | Hallucination |
|--------|------------|-----------|------------|---------|---------------|
| NutriAgent | 4.56 | 4.46 | 4.24 | 4.42 | 0.117 |
| DeepSeek-V4-Pro | 4.15 | 3.52 | 3.63 | 3.77 | 0.372 |
| DeepSeek-V4-Flash | 4.11 | 3.58 | 3.72 | 3.80 | 0.390 |
| MiniMax-M2.5 | 4.07 | 3.49 | 3.56 | 3.71 | 0.340 |
| GLM-4.5-Air | 3.83 | 3.08 | 3.87 | 3.59 | 0.423 |
| Qwen3.5-Flash | 3.80 | 3.32 | 3.20 | 3.44 | 0.347 |
| Qwen3-8B | 3.43 | 2.85 | 3.04 | 3.11 | 0.339 |

---

## Fig 6: Hallucination vs Readability (Bubble Chart)

数据来源：report.json Flesch + Hallucination

| Method | Flesch RE | Hallucination | Overall |
|--------|-----------|---------------|---------|
| NutriAgent | 43.4 | 0.117 | 4.42 |
| DeepSeek-V4-Pro | 51.2 | 0.372 | 3.77 |
| DeepSeek-V4-Flash | 51.2 | 0.390 | 3.80 |
| MiniMax-M2.5 | 49.9 | 0.340 | 3.71 |
| Qwen3-8B | 44.5 | 0.339 | 3.11 |
| Qwen3.5-Flash | 40.8 | 0.347 | 3.44 |
| GLM-4.5-Air | 37.5 | 0.423 | 3.59 |

回归线：仅拟合 baselines（排除 NutriAgent）。

---

## Fig 7: Performance Breakdown (Expert Evaluation, n=54)

数据来源：§3.3 逐域/逐类型分析

### Panel (a): By Query Type

| Query Type | Correctness | Precision | Sci. Depth |
|------------|------------|-----------|------------|
| Definition | 5.00 | N/A | 4.86 |
| Single-value | 4.67 | 4.63 | 4.29 |
| Multi-hop | 4.75 | 4.75 | 4.50 |
| Comparison | 4.60 | 4.44 | 4.10 |
| Counterfactual | 5.00 | 5.00 | 4.00 |
| Open-ended | 3.86 | 1.50 | 3.71 |
| Constraint | 3.67 | 4.50 | 4.00 |

### Panel (b): By Knowledge Domain

| Domain | Correctness | Precision | Sci. Depth | Hallucination |
|--------|------------|-----------|------------|---------------|
| Terminology | 5.00 | 5.00 | 4.67 | 0.177 |
| Nutrient Req. | 4.58 | 4.45 | 4.50 | 0.062 |
| Production Perf. | 4.55 | 4.56 | 3.82 | 0.142 |
| Cross-Domain | 4.50 | 4.75 | 4.30 | 0.147 |
| Edge Cases | 4.80 | 4.00 | 4.40 | 0.120 |
| Ingredient Comp. | 4.20 | 4.12 | 4.00 | 0.097 |

---

## Fig 8: Domain Radar Chart

数据来源：Fig 7b 归一化

| Domain | Correctness (÷5) | Sci. Depth (÷5) | Consistency (1−Halluc.) |
|--------|------------------|-----------------|------------------------|
| Terminology | 1.000 | 0.934 | 0.823 |
| Nutrient Req. | 0.916 | 0.900 | 0.938 |
| Production Perf. | 0.910 | 0.764 | 0.858 |
| Cross-Domain | 0.900 | 0.860 | 0.853 |
| Edge Cases | 0.960 | 0.880 | 0.880 |
| Ingredient Comp. | 0.840 | 0.800 | 0.903 |

---

## Fig 9: Cost-Quality Trade-off

数据来源：report.json cost_tracker + Table 8

| Method | Cost/Query (USD) | Overall Quality | Hallucination |
|--------|-----------------|-----------------|---------------|
| NutriAgent | $0.000723 | 4.42 | 0.117 |
| DeepSeek-V4-Pro | $0.000158 | 3.77 | 0.372 |
| DeepSeek-V4-Flash | $0.000054 | 3.80 | 0.390 |
| MiniMax-M2.5 | $0.000526 | 3.71 | 0.340 |
| GLM-4.5-Air | $0.000144 | 3.59 | 0.423 |
| Qwen3.5-Flash | $0.000084 | 3.44 | 0.347 |
| Qwen3-8B | $0.000082 | 3.11 | 0.339 |

---

## Fig 10: Bilingual Evaluation (Expert Evaluation)

数据来源：§3.5 + report.json

| Metric | English (n=42) | Chinese (n=12) |
|--------|---------------|----------------|
| Correctness | 4.55 | 4.58 |
| Precision | 4.48 | 4.40 |
| Sci. Depth | 4.19 | 4.42 |
| Hallucination | 0.099 | 0.306 |

Hallucination gap: 0.306 / 0.099 = 3.1×

---

## Fig 11: Query Composition

数据来源：§2.3 评估查询集

### Panel (a): Candidate Pool Breakdown

| Pool | single-value | comparison | open-ended | definition | multi-hop | constraint | counterfactual | Total |
|------|-------------|-----------|-----------|-----------|----------|-----------|---------------|-------|
| English Pool | 38 | 23 | 39 | 20 | 0 | 0 | 0 | 120 |
| English Advanced | 4 | 12 | 0 | 0 | 7 | 0 | 7 | 30 |
| Chinese Pool | 12 | 8 | 6 | 2 | 0 | 0 | 0 | 28 |
| Chinese Advanced | 3 | 6 | 0 | 0 | 5 | 0 | 3 | 17 |
| Curated (EN+ZH) | 21 | 10 | 7 | 7 | 4 | 3 | 2 | 54 |

### Panel (b): Language Split

| Language | Count | Percentage |
|----------|-------|-----------|
| English | 42 | 77.8% |
| Chinese | 12 | 22.2% |

### Panel (c): By Knowledge Domain

| Domain | Count |
|--------|-------|
| Ingredient Composition | 10 |
| Nutrient Requirements | 12 |
| Production Performance | 11 |
| Terminology | 6 |
| Cross-Domain | 10 |
| Edge Cases | 5 |

---

## Fig 12: Query-Response Examples

### Left (C-XD-007): Multi-Hop Success

- Query: ISA Brown at week 30, feed intake 112 g/day, Ca requirement 4.04%. Estimate daily Ca intake.
- Pipeline: Router → [Nutrition, Performance] → Synthesis
- Nutrition: Ca = 4.04%, retention = 50-60%
- Performance: intake = 112 g/d
- Synthesis: 112 × 4.04% = 4,525 mg Ca/day; 4,525 × 55% ≈ 2,489 mg available > eggshell 2,000-2,200 mg
- Score: C=5, P=5, D=5, H=0.032

### Right (C-XD-003): Constraint Failure

- Query: Can limestone at 9% inclusion meet Ca requirement of 4.04% for ISA Brown?
- Pipeline: Router → [Nutrition, Feed] → Synthesis
- Nutrition: Ca req = 4.04%
- Feed: limestone Ca = 35% (tool-retrieved)
- Synthesis ERROR: uses 38% (parametric) instead of 35%; 9% × 38% = 3.42% < 4.04%
- Score: C=3, P=4, D=4, H=0.227

---

## 数据溯源对照

| 图 | 正文位置 | 表格 | report.json |
|----|---------|------|------------|
| Fig 4 | §3.6.1 | Table 5 | ablation_*/ |
| Fig 5 | §3.2 | Table 3 | comp_layer_20260612_183548 |
| Fig 6 | §3.2 Text quality | — | comp_layer_20260612_183548 |
| Fig 7 | §3.3 | — | comp_layer_20260612_183548 |
| Fig 8 | §3.3 | — | Fig 7b 归一化 |
| Fig 9 | §3.2 Cost | Table 8 | comp_layer_20260612_183548 |
| Fig 10 | §3.5 | — | comp_layer_20260612_183548 |
| Fig 11 | §2.3 | Table 2 | — |
| Fig 12 | §3.6.1 | — | 人工构造案例 |
