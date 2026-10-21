# E15: entity-resolution perturbation test

Cases: 39; resolved 71.8%; family-correct 64.1%.

| Category | n | Resolved | Family-correct |
|---|---:|---:|---:|
| ambiguous_family | 5 | 100.0% | 80.0% |
| case_whitespace | 4 | 100.0% | 100.0% |
| chinese_alias | 8 | 0.0% | 0.0% |
| commodity_short | 7 | 100.0% | 100.0% |
| exact_canonical | 7 | 100.0% | 100.0% |
| misspelling | 8 | 62.5% | 37.5% |

## Failures

| Input | Category | Expected | Got |
|---|---|---|---|
| maise | misspelling | maize | not found |
| soyabean meal | misspelling | soybean meal | not found |
| wheatt | misspelling | wheat | wheat bran |
| soya meal | misspelling | soybean meal | not found |
| corn meal | misspelling | maize | corn gluten feed |
| 苜蓿粉 | chinese_alias | alfalfa | not found |
| 苹果渣 | chinese_alias | apple pomace | not found |
| 面包副产物 | chinese_alias | bakery byproduct | not found |
| 大麦 | chinese_alias | barley | not found |
| 大麦DDGS | chinese_alias | barley distillers grains | not found |
| 大麦胚芽 | chinese_alias | barley rootlets | not found |
| 甜菜粕 | chinese_alias | beet pulp | not found |
| 饼干副产物 | chinese_alias | biscuit byproduct | not found |
| wheat | ambiguous_family | wheat | wheat bran |
