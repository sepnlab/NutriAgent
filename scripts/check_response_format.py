import json, os, glob
logs = sorted(glob.glob('logs/log_*'))
resp_path = os.path.join(logs[-1], 'responses.json')
with open(resp_path, 'r', encoding='utf-8') as f:
    d = json.load(f)
print('Top keys:', list(d.keys()))
print('Queries[0] keys:', list(d['queries'][0].keys()))
print('Methods:', list(d['responses'].keys()))
for m in d['responses']:
    items = d['responses'][m]
    if items:
        print(f'{m}: {len(items)} responses, keys={list(items[0].keys())}')
        break
