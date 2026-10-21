# 数据审计报告（自动生成）

> 生成时间：2026-10-20T12:36:37.205659+08:00  
> 查询集：`queries/layer/evaluation_queries_curated.json`  
> 脚本：`scripts/paper/data_audit.py`

## 1. 数据集完备度

| 数据集 | 文件 | 行 | 键 | 参数列 | 名义单元格 | 实有 | 完备度 | 全空列数 |
|---|---|---:|---|---:|---:|---:|---:|---:|
| Feed ingredient bank | `corpus/shared/feed_ingredient_bank.csv` | 108 | Ingredient | 38 | 4104 | 2376 | 57.9% | 16 |
| Feed ingredient amino acids | `corpus/shared/feed_ingredient_amino_acids.csv` | 108 | Ingredient | 19 | 2052 | 2052 | 100.0% | 0 |
| Feed ingredient digestibility | `corpus/shared/feed_ingredient_digestibility.csv` | 108 | Ingredient | 40 | 4320 | 4320 | 100.0% | 0 |
| Layer nutrient requirements | `corpus/layer/nutrient_requirements.csv` | 103 | Breed/Phase | 20 | 2060 | 1517 | 73.6% | 0 |
| Layer vitamin / mineral specifications | `corpus/layer/nutrient_vitamin_mineral.csv` | 30 | Breed/Phase | 18 | 540 | 540 | 100.0% | 0 |
| Layer production benchmarks | `corpus/layer/performance_management.csv` | 1131 | Breed/Week | 12 | 13572 | 5798 | 42.7% | 3 |
| Terminology definitions | `corpus/shared/definitions.csv` | 556 | Term | — | — | — | — | — |

## 2. 品种与 phase

- **Layer nutrient requirements**：17 个品种；phase 标签 55 个；每品种 phase 数 {'Beinong 1': 3, 'Beinong 2': 5, 'Dawu Fen 1': 5, 'Dawu He': 5, 'Dawu Jinfeng': 8, 'Hisex Brown': 4, 'Hy-Line Brown': 5, 'Hy-Line Pink': 5, 'Hy-Line W-36': 5, 'ISA Brown': 7, 'Jingbai 939': 8, 'Jingfen 6': 9, 'Jinghong 1 v3.0': 9, 'Lohmann Grey': 4, 'Lohmann Pink': 7, 'Nongda 3': 6, 'Nongda 6': 8}
- **Layer vitamin / mineral specifications**：13 个品种；phase 标签 10 个；每品种 phase 数 {'Beinong 2': 2, 'Dawu Jinfeng': 2, 'Hy-Line Brown': 2, 'Hy-Line Pink': 2, 'Hy-Line W-36': 2, 'ISA Brown': 2, 'Jingbai 939': 2, 'Jingfen 6': 2, 'Jinghong 1 v3.0': 2, 'Lohmann Grey': 2, 'Lohmann Pink': 2, 'Nongda 3': 6, 'Nongda 6': 2}
- **Layer production benchmarks**：16 个品种；phase 标签 — 个；每品种 phase 数 —

## 3. 计数口径

- 记录数合计：**1928**（{'feed_entries': 108, 'nutrition_breed_phase_entries': 103, 'vitamin_mineral_entries': 30, 'performance_records': 1131, 'definitions': 556}）
- 标量单元格（名义）：**26648**
- 标量单元格（实有）：**16603**
- 标量 + 定义（名义）：**27204**
- 标量 + 定义（实有）：**17159**
- PoultryDB 文档：**2144**

> 论文 14,800 的口径：feed 108x97 + nutrition 2,060 + vitamin 540 + performance 1,131 + definitions 556 = 14,767 (mixes scalar cells with records and definitions)

## 4. 查询集

- 总数：**54**
- 语言：{'en': 42, 'zh': 12}
- 类型：{'single-value': 21, 'comparison': 10, 'open-ended': 7, 'definition': 7, 'multi-hop': 4, 'constraint': 3, 'counterfactual': 2}
- 领域：{'Feed Ingredient Bank': 10, 'Nutrient Requirements': 12, 'Performance Management': 11, 'Definitions': 6, 'Cross-Domain': 10, 'Edge Cases': 5}
- expected_value：**36**；expected_behavior：**5**
- 中文题品种提及：{'Dawu Jinfeng': 5, 'Jingfen 6': 3, 'Hy-Line Brown': 1}

### 中文题清单

| ID | 类型 | 查询 |
|---|---|---|
| C-FIB-009 | single-value | 玉米的粗蛋白含量是多少？ |
| C-FIB-010 | comparison | 豆粕48和菜粕的代谢能各是多少？哪个更高？ |
| C-NR-010 | single-value | 大午金凤在产蛋I期的钙需要量是多少？ |
| C-NR-011 | comparison | 大午金凤从产蛋I期到产蛋III期，钙需要量怎么变化？ |
| C-NR-012 | single-value | 大午金凤在产蛋I期的SID蛋氨酸需要量是多少？ |
| C-PM-009 | single-value | 京粉6号在第30周的产蛋率是多少？ |
| C-PM-010 | comparison | 京粉6号和海兰褐在第30周的产蛋率各是多少？哪个更高？ |
| C-PM-011 | single-value | 京粉6号第30周的产蛋率和蛋重各是多少？ |
| C-DEF-005 | definition | 什么是代谢能？它和消化能有什么区别？ |
| C-DEF-006 | open-ended | 蛋鸡饲料配方为什么优先用代谢能而不是消化能？ |
| C-XD-009 | multi-hop | 一个产蛋I期配方用60%玉米（总赖氨酸0.247%，SID消化率90%）和25%豆粕48（总赖氨酸0.620%，SID消化率88%）。这两样原料的SID赖氨酸加起来是多少？能不能满足大午金凤蛋鸡的需要量（0.76%）？ |
| C-XD-010 | constraint | 石灰石含钙35%，大午金凤蛋鸡的钙需要量是3.90%。配方里要加多少石灰石才能满足？ |
