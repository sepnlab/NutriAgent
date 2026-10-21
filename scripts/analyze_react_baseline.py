import json
b = json.load(open('logs/react_broiler.json', encoding='utf-8'))
l = json.load(open('logs/react_layer.json', encoding='utf-8'))
all_r = b['per_query'] + l['per_query']
print('Broiler summary:', b['summary'])
print('Layer summary:', l['summary'])
print()
print('=== Sample responses ===')
types = {}
for r in all_r:
    qt = r['query_type']
    if qt not in types:
        types[qt] = r
for qt, r in list(types.items())[:5]:
    print(f'[{qt}] {r["query"][:60]}...')
    print(f'  -> {r["response"][:200]}')
    print()
print('=== Distribution by type ===')
from collections import Counter
c = Counter(r['query_type'] for r in all_r)
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')

print()
print('=== Short/error responses ===')
short = [r for r in all_r if len(r['response']) < 100]
print(f'  Short (<100 chars): {len(short)}')
err = [r for r in all_r if 'Error' in r['response'] or 'error' in r['response'][:50]]
print(f'  With error: {len(err)}')
