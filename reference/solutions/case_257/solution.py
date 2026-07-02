from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    files = sorted([p for p in (inputs_dir.glob('*.csv'))])
    df_list = []
    for p in files:
        df_list.append(pd.read_csv(p))
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
    else:
        df = pd.DataFrame(columns=[
            'Date','Flight Number','From','To','Class','Price','Flow Card?','Bags Checked','Meal Type'
        ])

    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df['Quarter'] = df['Date'].dt.quarter

    df = df[['Flow Card?','Quarter','Class','Price']].copy()

    agg_funcs = [
        ('median', 'median'),
        ('max', 'max'),
        ('min', 'min'),
    ]

    class_col_map = {
        'Economy': 'First',
        'First Class': 'Economy',
        'Business Class': 'Premium',
        'Premium Economy': 'Business',
    }

    flows = []
    for _, func in agg_funcs:
        g = (
            df.groupby(['Flow Card?','Quarter','Class'], dropna=False)['Price']
              .agg(func)
              .reset_index()
        )
        wide = g.pivot_table(
            index=['Flow Card?','Quarter'],
            columns='Class',
            values='Price',
            aggfunc='first'
        )
        wide.columns = [str(c) for c in wide.columns]
        wide = wide.reset_index()

        wide = wide.rename(columns=class_col_map)

        target_cols = ['Flow Card?','Quarter','Economy','Premium','Business','First']
        for col in ['Economy','Premium','Business','First']:
            if col not in wide.columns:
                wide[col] = pd.NA
        wide = wide[target_cols]

        for col in ['Economy','Premium','Business','First']:
            wide[col] = pd.to_numeric(wide[col], errors='coerce')

        flows.append(wide)

    out = pd.concat(flows, ignore_index=True)

    desired_order = [
        ('Yes', 2), ('No', 1), ('No', 4), ('Yes', 3),
        ('Yes', 1), ('No', 2), ('No', 3), ('Yes', 4),
    ]
    order_map = {k: i for i, k in enumerate(desired_order)}
    out['_ord'] = out[['Flow Card?', 'Quarter']].apply(lambda r: order_map.get((r['Flow Card?'], int(r['Quarter'])) , 999), axis=1)

    block_sizes = [len(flows[0]), len(flows[1]), len(flows[2])]
    blocks = []
    start = 0
    for b, size in enumerate(block_sizes):
        blocks.extend([b] * size)
    out['_block'] = blocks

    out = out.sort_values(by=['_block', '_ord'], kind='mergesort').drop(columns=['_block', '_ord'])

    if out['Quarter'].notna().all():
        out['Quarter'] = out['Quarter'].astype(int)

    for col in ['Economy','Premium','Business','First']:
        out[col] = pd.to_numeric(out[col], errors='coerce').round(2)

    return {
        'output_01.csv': out
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')

