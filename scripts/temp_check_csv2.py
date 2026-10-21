import pandas as pd, os
root = 'D:/Geqi_series/NutriChat'
cd = os.path.join(root, 'corpus', 'shared')
for fn in ['feed_ingredient_bank.csv', 'feed_ingredient_amino_acids.csv', 'feed_ingredient_digestibility.csv']:
    p = os.path.join(cd, fn)
    if os.path.exists(p):
        df = pd.read_csv(p)
        icol = [c for c in df.columns if 'ingredient' in c.lower() or 'Ingredient' in c]
        print(f'\n{fn}: {len(df)} rows, columns={list(df.columns)}, ingest_cols={icol}')
        if icol:
            print(f'  Sample ingredients: {df[icol[0]].dropna().unique()[:5]}')
        print(f'  First row values sample: {dict(df.iloc[0])}')
    else:
        print(f'{fn}: NOT FOUND at {p}')
