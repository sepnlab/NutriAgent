# D2: Specialist ablation (Rev.1, single pass, n=54)

| Variant | Correctness | Precision | Depth | n (C/P/D) |
|---|---:|---:|---:|---:|
| Full (4 Specialists) | 4.44±0.82 | 4.39±0.88 | 4.00±0.75 | 54/46/54 |
| w/o Feed | 4.67±0.58 | 4.48±0.86 | 3.94±0.66 | 54/46/53 |
| w/o Definitions | 4.57±0.69 | 4.43±0.89 | 3.79±0.70 | 54/46/52 |
| w/o Performance | 4.39±0.79 | 3.98±1.20 | 3.72±0.79 | 54/46/53 |
| w/o Nutrition | 4.37±0.83 | 4.20±1.09 | 3.98±0.65 | 54/46/51 |

All five variants were scored in the same pass. No removal lowers correctness materially;
removing Feed (+0.22) or Definitions (+0.13) is followed by a higher score, while
Performance/Nutrition are −0.06/−0.07. The earlier separate-pass values (Full 4.81,
w/o Nutrition 4.86) are not used: the same Full condition shifts by 0.37 across passes.
Single run, no intervals. Source: `docs/paper/audit/d2_rescored_all.json`.
