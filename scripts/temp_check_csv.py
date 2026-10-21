import pandas as pd, os
root = 'D:/Geqi_series/NutriChat'
for species in ('broiler', 'layer'):
    cd = os.path.join(root, 'corpus', species)
    print(f'\n=== {species} ===')
    for fn in ['feed_ingredient_bank.csv', 'feed_ingredient_amino_acids.csv', 'feed_ingredient_digestibility.csv']:
        p = os.path.join(cd, fn)
        if os.path.exists(p):
            df = pd.read_csv(p)
            icol = [c for c in df.columns if 'ingredient' in c.lower()]
            print(f'  {fn}: {len(df)} rows, cols={list(df.columns)[:8]}..., ingest_cols={icol}')
        else:
            print(f'  {fn}: MISSING')
