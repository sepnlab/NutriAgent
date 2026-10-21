# E6: PoultryDB retrieval hit@k

Queries with target_doc: 44.

- hit@1: 27.3%
- hit@3: 54.5%
- hit@5: 63.6%
- MRR: 0.411

| Type | n | hit@1 | hit@5 |
|---|---:|---:|---:|
| comparison | 10 | 10.0% | 50.0% |
| constraint | 2 | 0.0% | 0.0% |
| counterfactual | 2 | 100.0% | 100.0% |
| definition | 7 | 71.4% | 100.0% |
| multi-hop | 3 | 0.0% | 66.7% |
| open-ended | 5 | 20.0% | 80.0% |
| single-value | 15 | 20.0% | 53.3% |

## Misses at k=5

| ID | Type | Targets |
|---|---|---|
| C-NR-005 | comparison | 2 |
| C-NR-010 | single-value | 1 |
| C-NR-011 | comparison | 1 |
| C-NR-012 | single-value | 1 |
| C-PM-001 | single-value | 1 |
| C-PM-002 | single-value | 1 |
| C-PM-003 | comparison | 2 |
| C-PM-004 | comparison | 2 |
| C-PM-005 | open-ended | 1 |
| C-PM-007 | single-value | 1 |
| C-PM-009 | single-value | 1 |
| C-PM-010 | comparison | 2 |
| C-PM-011 | single-value | 1 |
| C-XD-003 | constraint | 2 |
| C-XD-009 | multi-hop | 1 |
| C-XD-010 | constraint | 2 |
