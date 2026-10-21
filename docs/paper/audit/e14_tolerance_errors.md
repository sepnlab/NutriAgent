# E14: numeric error audit (relative-error tolerance)

Numeric queries: 36.

| Label | n |
|---|---:|
| correct | 32 |
| wrong_value | 4 |
| no_numeric_answer | 0 |

Pass rate: new relative-error rule 88.9%; old interval rule 88.9%.
At ±2%: new 83.3%; old 83.3%.

## Failures

| ID | Type | Expected | Best parsed | Label |
|---|---|---:|---:|---|
| C-FIB-005 | comparison | 11.6 | 8.5 | wrong_value |
| C-FIB-010 | comparison | 2260.0 | 48.0 | wrong_value |
| C-XD-001 | multi-hop | 0.27 | 0.25 | wrong_value |
| C-XD-006 | counterfactual | 1.45 | 5.125 | wrong_value |
