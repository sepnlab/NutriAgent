# D6: LLM backbone ablation (Rev.1, n=54 re-score)

| Backbone | Correctness | Precision | Depth | n (C/P/D) |
|---|---:|---:|---:|---:|
| DeepSeek-V4-Pro | 4.67±0.58 | 4.48±0.78 | 3.87±0.70 | 54/46/54 |
| DeepSeek-V4-Flash | 4.61±0.71 | 4.48±0.84 | 4.04±0.61 | 54/46/54 |
| Qwen3.8-27B | 4.50±0.91 | 4.24±1.13 | 3.69±0.77 | 54/45/54 |
| Qwen3.8-Flash | 4.43±0.96 | 4.17±1.27 | 3.80±0.83 | 54/46/54 |
| Qwen3-8B | 3.81±1.17 | 3.78±1.38 | 2.93±0.71 | 54/45/46 |

DeepSeek-V4-Pro leads by 0.06 correctness but has lower depth than DeepSeek-V4-Flash
(3.87 vs 4.04). Qwen3-8B is the clear outlier (−0.80 C, −1.11 D vs DeepSeek-V4-Flash).
The submitted ordering (DeepSeek-V4-Flash 4.85 > DeepSeek-V4-Pro 4.74) is not replicated.
Source: `docs/paper/audit/d6_rescored.json`.
