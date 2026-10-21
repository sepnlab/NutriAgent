# D4: RAG ablation (Rev.1, n=54 re-score)

| Variant | Correctness | Precision | Depth | n (C/P/D) |
|---|---:|---:|---:|---:|
| Multi-Agent (no RAG) | 4.52±0.77 | 4.33±1.04 | 3.96±0.82 | 54/45/46 |
| Multi-Agent + RAG | 4.52±0.79 | 4.37±1.06 | 3.74±0.78 | 54/46/54 |
| Δ (+RAG − no RAG) | **0.00** | +0.04 | −0.22 | — |

The earlier +0.14 correctness / −0.13 precision result (n=44/34) is not replicated.
RAG is a null result on correctness and precision; the depth difference favors no-RAG but
the no-RAG depth cell has n=46. Source: `docs/paper/audit/d4_rescored.json`.
