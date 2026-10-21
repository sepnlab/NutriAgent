"""修复查询集 + 创建 layer advanced 查询"""
import json, os, copy

LAYER_Q = 'queries/layer/evaluation_queries.json'
LAYER_CN = 'queries/layer/evaluation_queries_chinese.json'
LAYER_ADV = 'queries/layer/evaluation_queries_advanced.json'
LAYER_CN_ADV = 'queries/layer/evaluation_queries_chinese_advanced.json'

# ═══════════════════════════════════════════
# 1. 修复英文查询集（LSL → Lohmann Pink）
# ═══════════════════════════════════════════
with open(LAYER_Q, 'r', encoding='utf-8') as f:
    eng = json.load(f)

for cat_name, cat_data in eng.items():
    qs = cat_data if isinstance(cat_data, list) else cat_data.get('queries', [])
    for q in qs:
        txt = q.get('query', '')
        # 按最长匹配优先替换（一次性替换，不叠加）
        if 'Lohmann LSL-Classic' in txt:
            q['query'] = txt.replace('Lohmann LSL-Classic', 'Lohmann Pink')
            print(f'  [FIX] LSL-Classic -> Pink: {txt[:60]}')
        elif 'Lohmann LSL' in txt:
            q['query'] = txt.replace('Lohmann LSL', 'Lohmann Pink')
            print(f'  [FIX] LSL -> Pink: {txt[:60]}')
        elif 'LSL-Classic' in txt:
            q['query'] = txt.replace('LSL-Classic', 'Lohmann Pink')
            print(f'  [FIX] LSL-Classic -> Pink: {txt[:60]}')

with open(LAYER_Q, 'w', encoding='utf-8') as f:
    json.dump(eng, f, ensure_ascii=False, indent=2)
print('evaluation_queries.json fixed')

# ═══════════════════════════════════════════
# 2. 修复中文查询集（京粉1/2号 → 现有品种）
# ═══════════════════════════════════════════
with open(LAYER_CN, 'r', encoding='utf-8') as f:
    cn = json.load(f)

cn_fixes = {'京粉1号': '京粉6号', '京粉2号': '京红1号'}
for cat_name, cat_data in cn.items():
    qs = cat_data if isinstance(cat_data, list) else cat_data.get('queries', [])
    for q in qs:
        txt = q.get('query', '')
        if '京粉1号' in txt:
            q['query'] = txt.replace('京粉1号', '京粉6号')
            print(f'  [FIX] 京粉1号 -> 京粉6号')
        elif '京粉2号' in txt:
            q['query'] = txt.replace('京粉2号', '京红1号')
            print(f'  [FIX] 京粉2号 -> 京红1号')

with open(LAYER_CN, 'w', encoding='utf-8') as f:
    json.dump(cn, f, ensure_ascii=False, indent=2)
print('evaluation_queries_chinese.json fixed')

# ═══════════════════════════════════════════
# 3. 创建 layer advanced 查询集
# ═══════════════════════════════════════════
advanced = {
    "Performance Management Multi-Hop": [
        {"id": "L-ADV-PM-001", "query": "What is the egg mass per day for Hy-Line W-36 at 30 weeks, given its hen-day production rate and egg weight?", "type": "multi-hop"},
        {"id": "L-ADV-PM-002", "query": "For Lohmann Pink at 72 weeks, how does the mortality rate compare between Hy-Line W-36 and Jinghong 1 v3.0?", "type": "comparison"},
        {"id": "L-ADV-PM-003", "query": "Calculate the daily egg mass for Jingbai 939 at 40 weeks based on its production rate and egg weight.", "type": "multi-hop"},
        {"id": "L-ADV-PM-004", "query": "What is the body weight of Nongda 6 at 40 weeks, and how does it compare to Nongda 3?", "type": "multi-hop"},
        {"id": "L-ADV-PM-005", "query": "Which has higher peak production: Jingfen 6 or Hy-Line Pink? What are their respective peak values?", "type": "comparison"},
        {"id": "L-ADV-PM-006", "query": "What is the feed conversion ratio for Dawu Jinfeng at 72 weeks in kg feed per kg eggs?", "type": "derived"},
        {"id": "L-ADV-PM-007", "query": "Compare body weight trajectories: which breed reaches 1800g earliest, Beinong 1, Beinong 2, or Dawu Jinfeng?", "type": "comparison"},
        {"id": "L-ADV-PM-008", "query": "What is the cumulative egg count for Jinghong 1 v3.0 at 60 weeks and how does it compare to Jingbai 939?", "type": "multi-hop"},
    ],
    "Nutrient Requirements Multi-Hop": [
        {"id": "L-ADV-NR-001", "query": "What calcium level does Hy-Line Brown need during peak lay, and how does it change from pre-lay to peak?", "type": "multi-hop"},
        {"id": "L-ADV-NR-002", "query": "Compare the SID lysine requirements between Hy-Line W-36 and Jinghong 1 v3.0 during the peak laying phase.", "type": "comparison"},
        {"id": "L-ADV-NR-003", "query": "If Jingbai 939 consumes 105g of feed daily during Layer I, what is its daily methionine intake in mg?", "type": "multi-hop"},
        {"id": "L-ADV-NR-004", "query": "How does the calcium requirement change across the three laying phases for Dawu Jinfeng?", "type": "trend"},
        {"id": "L-ADV-NR-005", "query": "Compare crude protein requirements across all phases for Nongda 6 vs Nongda 3.", "type": "comparison"},
        {"id": "L-ADV-NR-006", "query": "What is the SID methionine+cysteine requirement for Lohmann Pink in Layer I phase?", "type": "multi-hop"},
        {"id": "L-ADV-NR-007", "query": "Does Jinghong 1 v3.0 have higher or lower calcium requirements than Hy-Line Brown in the peak phase?", "type": "comparison"},
        {"id": "L-ADV-NR-008", "query": "What is the choline requirement for Hy-Line Pink during the starter phase, in mg per kg of feed?", "type": "single-value"},
    ],
    "Cross-Breed Complex Comparison": [
        {"id": "L-ADV-CB-001", "query": "Compare the body weight at 40 weeks across Hy-Line W-36, Jingbai 939, and Nongda 6. Which is heaviest and which is lightest?", "type": "comparison"},
        {"id": "L-ADV-CB-002", "query": "Which Chinese breed has the highest peak egg production rate: Jinghong 1 v3.0, Jingfen 6, or Jingbai 939?", "type": "comparison"},
        {"id": "L-ADV-CB-003", "query": "Compare the calcium requirements during peak lay between international breeds (Hy-Line W-36, ISA Brown) and Chinese breeds (Jinghong 1, Dawu Jinfeng).", "type": "comparison"},
        {"id": "L-ADV-CB-004", "query": "Which breed reaches sexual maturity earliest based on weeks to 50% production: Hy-Line Pink, Lohmann Pink, or Lohmann Grey?", "type": "comparison"},
        {"id": "L-ADV-CB-005", "query": "Compare egg weight at 40 weeks between ISA Brown, Hy-Line Pink, and Beinong 1.", "type": "comparison"},
    ],
    "Constraint and Edge Case": [
        {"id": "L-ADV-CE-001", "query": "If a farmer wants a breed with <100g daily feed intake and >90% peak production, which breeds satisfy both constraints?", "type": "constraint"},
        {"id": "L-ADV-CE-002", "query": "Which Chinese layer breeds have a published SID amino acid profile? List their SID lysine requirements.", "type": "constraint"},
        {"id": "L-ADV-CE-003", "query": "What would happen to eggshell quality if calcium is reduced from 4.0% to 3.5% for Jinghong 1 v3.0 during Layer II?", "type": "counterfactual"},
        {"id": "L-ADV-CE-004", "query": "If Hy-Line Brown's daily feed intake drops from 112g to 100g during peak production, how would calcium intake change?", "type": "counterfactual"},
        {"id": "L-ADV-CE-005", "query": "Rank these breeds by body weight at 40 weeks: Hy-Line W-36, ISA Brown, Lohmann Pink, Nongda 6.", "type": "constraint"},
    ],
    "Vitamin and Mineral": [
        {"id": "L-ADV-VM-001", "query": "What is the Vitamin A requirement for Jinghong 1 v3.0 during the layer phase?", "type": "single-value"},
        {"id": "L-ADV-VM-002", "query": "Compare zinc requirements between Hy-Line Pink and Lohmann Pink.", "type": "comparison"},
        {"id": "L-ADV-VM-003", "query": "What selenium level is recommended for Jingbai 939 in the layer phase?", "type": "single-value"},
        {"id": "L-ADV-VM-004", "query": "Does Nongda 6 have published vitamin recommendations? If so, what is its Vitamin D3 level?", "type": "single-value"},
    ],
}

with open(LAYER_ADV, 'w', encoding='utf-8') as f:
    json.dump(advanced, f, ensure_ascii=False, indent=2)
print(f'Created {LAYER_ADV} ({sum(len(v) for v in advanced.values())} queries)')

# ═══════════════════════════════════════════
# 4. 创建中文 advanced 查询集
# ═══════════════════════════════════════════
cn_advanced = {
    "中国品种多跳推理": [
        {"id": "CN-ADV-001", "query": "京红1号3.0在产蛋I期的钙需要量是多少？与产蛋IV期相比如何变化？", "type": "multi-hop"},
        {"id": "CN-ADV-002", "query": "京白939在30周龄的日产蛋量是多少克？需要用到产蛋率和蛋重两个数据。", "type": "multi-hop"},
        {"id": "CN-ADV-003", "query": "京粉6号在产蛋高峰期的可消化赖氨酸需要量是多少？", "type": "single-value"},
        {"id": "CN-ADV-004", "query": "农大6号从育雏期到产蛋期的钙需要量如何变化？", "type": "trend"},
        {"id": "CN-ADV-005", "query": "比较京红1号3.0和京白939在40周龄的体重。", "type": "comparison"},
        {"id": "CN-ADV-006", "query": "北农2号的育雏期代谢能需要量是多少？", "type": "single-value"},
    ],
    "中国品种营养对比": [
        {"id": "CN-ADV-NR-001", "query": "京红1号3.0和大午金凤在产蛋高峰期的钙需要量有何不同？", "type": "comparison"},
        {"id": "CN-ADV-NR-002", "query": "京白939的粗蛋白需要量在育雏期和产蛋期分别是多少？", "type": "multi-hop"},
        {"id": "CN-ADV-NR-003", "query": "北农1号有哪些营养阶段数据可用？列出其粗蛋白需要量。", "type": "constraint"},
        {"id": "CN-ADV-NR-004", "query": "京粉6号的维生素A和维生素D3添加量在育雏期是多少？", "type": "single-value"},
        {"id": "CN-ADV-NR-005", "query": "大午金凤在Layer I和Layer III期的钙需要量差异有多大？", "type": "comparison"},
        {"id": "CN-ADV-NR-006", "query": "农大6号的胆碱推荐量在育雏期和产蛋期各是多少？", "type": "multi-hop"},
    ],
    "中国品种综合对比": [
        {"id": "CN-ADV-CB-001", "query": "在中国品种中，哪个品种的产蛋高峰期最高？京红1号、京粉6号还是大午金凤？", "type": "comparison"},
        {"id": "CN-ADV-CB-002", "query": "比较北农1号和北农2号的产蛋性能差异。", "type": "comparison"},
        {"id": "CN-ADV-CB-003", "query": "农大3号和农大6号在40周龄的蛋重和体重有何差异？", "type": "comparison"},
        {"id": "CN-ADV-CB-004", "query": "如果农户希望选择耗料量低(<100g/天)且产蛋率高的中国品种，有哪些选择？", "type": "constraint"},
        {"id": "CN-ADV-CB-005", "query": "京红1号3.0在60周龄的累计产蛋数是多少？与京粉6号相比如何？", "type": "multi-hop"},
    ],
}

with open(LAYER_CN_ADV, 'w', encoding='utf-8') as f:
    json.dump(cn_advanced, f, ensure_ascii=False, indent=2)
print(f'Created {LAYER_CN_ADV} ({sum(len(v) for v in cn_advanced.values())} queries)')

print('\nAll done!')
