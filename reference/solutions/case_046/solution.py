from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    in1 = pd.read_csv(inputs_dir / "input_01.csv")
    nice = pd.read_csv(inputs_dir / "input_02.csv")
    naughty = pd.read_csv(inputs_dir / "input_03.csv")

    def first3(s: str) -> str:
        if pd.isna(s):
            return ""
        return ''.join(str(s)).strip().lower().replace(" ", "")[:3]

    def norm(s: str) -> str:
        return ('' if pd.isna(s) else str(s)).strip().lower()

    s = in1.copy()
    s['__abbr'] = s['Name'].apply(first3)
    s['__addr_norm'] = s['Address'].apply(norm)

    for df in (nice, naughty):
        df['__abbr'] = df['Name'].apply(first3)
        df['__full_addr_norm'] = df['Address'].apply(norm)

    def match_list(list_df: pd.DataFrame, list_name: str) -> pd.DataFrame:
        merged = list_df.merge(s, on='__abbr', suffixes=("_list", "_base"))
        mask = merged.apply(lambda r: r['__addr_norm'] in r['__full_addr_norm'], axis=1)
        merged = merged[mask].copy()
        out = pd.DataFrame({
            'List': list_name,
            'Name': merged['Name_base'],
            'Item': merged['Item'],
            'Family Role': merged['Family Role'],
            'Elves Build Time (min)': merged['Elves Build Time (min)'],
            'Address-1': merged['Address_list'],
            'Reason': merged['Reason'],
        })
        return out

    nice_out = match_list(nice, 'Nice List')
    naughty_out = match_list(naughty, 'Naughty List')

    combined = pd.concat([nice_out, naughty_out], ignore_index=True)
    list_priority = pd.Categorical(combined['List'], categories=['Nice List', 'Naughty List'], ordered=True)
    combined = combined.assign(__ord=list_priority).sort_values(['Name', '__ord']).drop(columns='__ord')
    combined = combined.drop_duplicates(subset=['Name'])

    out1_cols = [
        'List', 'Name', 'Item', 'Family Role', 'Elves Build Time (min)', 'Address-1', 'Reason'
    ]
    out1 = combined.loc[:, out1_cols].copy()

    agg = out1.groupby('List', as_index=False)['Elves Build Time (min)'].sum()
    agg['Total Hours Build Time'] = np.ceil(agg['Elves Build Time (min)'] / 60.0).astype(int)
    out2 = agg[['Total Hours Build Time', 'List']].copy()
    order = pd.Categorical(out2['List'], categories=['Naughty List', 'Nice List'], ordered=True)
    out2 = out2.assign(__o=order).sort_values('__o').drop(columns='__o').reset_index(drop=True)

    return {
        'output_01.csv': out1,
        'output_02.csv': out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).write_text('')
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')

