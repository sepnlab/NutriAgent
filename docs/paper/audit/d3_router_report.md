# D3: Router strategy ablation (Rev.1, n=54)

| Router | Correctness | Precision | Depth | n (C/P/D) |
|---|---:|---:|---:|---:|
| LLM Router | 4.63±0.71 | 4.56±0.89 | 3.96±0.64 | 54/45/54 |
| Broadcast (All) | 4.59±0.71 | 4.47±0.85 | 4.00±0.64 | 54/43/54 |
| Keyword Router | 4.48±0.93 | 4.26±1.16 | 3.76±0.70 | 54/46/54 |

At n=54 the LLM router is highest; Broadcast is 0.04 lower and Keyword 0.15 lower.
The earlier n=44 read (LLM 4.63, Keyword 4.64, Broadcast 4.68; spread ≤0.05) is not
replicated. Single run, no significance test. Source: `docs/paper/audit/d3_rescored.json`.
