# D4 RAG ITT sensitivity (proxy failures)

The Rev.1 D4 rescore includes all 54 correctness scores but does not preserve a
retrieval-failure flag; the four submitted-run exclusions cannot be reconstructed
exactly. As a conservative, clearly labeled proxy, the **16 E6 hit@5 misses** are
scored as system failures (1; sensitivity 0) in the +RAG condition. This is not an
exact reconstruction of the submitted exclusions and is reported as a sensitivity
analysis, not as the primary D4 estimate.

Proxy failure IDs: C-NR-005, C-NR-010, C-NR-011, C-NR-012, C-PM-001, C-PM-002, C-PM-003, C-PM-004, C-PM-005, C-PM-007, C-PM-009, C-PM-010, C-PM-011, C-XD-003, C-XD-009, C-XD-010.

| Metric | Analysis | n | +RAG | no-RAG | Δ | 95% CI | Wilcoxon p |
|---|---|---:|---:|---:|---:|---|---:|
| correctness | itt_floor_1 | 54 | 3.500 | 4.519 | -1.019 | -1.519 to -0.519 | 0.0008 |
| correctness | itt_floor_0 | 54 | 3.204 | 4.519 | -1.315 | -1.944 to -0.704 | 0.0005 |
| correctness | complete_case | 54 | 4.519 | 4.519 | +0.000 | -0.204 to +0.185 | 0.9857 |
| precision | itt_floor_1 | 45 | 3.156 | 4.333 | -1.178 | -1.778 to -0.600 | 0.0008 |
| precision | itt_floor_0 | 45 | 2.800 | 4.333 | -1.533 | -2.267 to -0.844 | 0.0007 |
| precision | complete_case | 45 | 4.356 | 4.333 | +0.022 | -0.244 to +0.289 | 0.8240 |
| scientific_depth | itt_floor_1 | 46 | 2.957 | 3.957 | -1.000 | -1.413 to -0.609 | 0.0001 |
| scientific_depth | itt_floor_0 | 46 | 2.674 | 3.957 | -1.283 | -1.826 to -0.783 | 0.0001 |
| scientific_depth | complete_case | 46 | 3.804 | 3.957 | -0.152 | -0.391 to +0.087 | 0.2598 |

The proxy ITT does not support a RAG correctness or precision benefit; the direction
is neutral-to-negative, consistent with the complete-case null result. Because the
failure set is a proxy, this analysis is labeled in the manuscript and supplement
and is not used to claim an exact intention-to-treat effect.
