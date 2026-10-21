# E11: bilingual breakdown (automated scores)

NutriAgent, MiMo-V2.5-Pro absolute scores, single run. Chinese n=12, English n=42; language is confounded with breed and data coverage.

| Language | Metric | Mean | SD | n | 95% bootstrap CI |
|---|---|---:|---:|---:|---|
| en | correctness | 4.69 | 0.643 | 42 | [4.476, 4.857] |
| en | precision | 4.686 | 0.867 | 35 | [4.371, 4.943] |
| en | scientific_depth | 4.262 | 0.767 | 42 | [4.024, 4.476] |
| zh | correctness | 4.917 | 0.289 | 12 | [4.75, 5.0] |
| zh | precision | 4.8 | 0.422 | 10 | [4.5, 5.0] |
| zh | scientific_depth | 4.417 | 0.669 | 12 | [4.0, 4.75] |

Chinese minus English: correctness = 0.226, precision = 0.114, scientific_depth = 0.155
