from __future__ import annotations
from pathlib import Path
import pandas as pd
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def parse_with_percent(path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)
        def split_pageviews(val: str):
            m = re.match(r"\s*(\d+)\s*\(([^)]+)\)\s*", str(val))
            if not m:
                raise ValueError(f"Unexpected Pageviews format: {val}")
            value = int(m.group(1))
            pct_str = m.group(2).strip()
            if pct_str.startswith('<'):
                pct = 0.5
            else:
                pct = float(pct_str.rstrip('%'))
            return value, pct
        vals = df['Pageviews'].apply(split_pageviews)
        df['Value'] = [v for v, _ in vals]
        df['Percent'] = [p for _, p in vals]
        return df[['Entry', 'Value', 'Percent']]

    def parse_values_only(path: Path, percent_mode: str = 'round', target_sum: int | None = None) -> pd.DataFrame:
        df = pd.read_csv(path)
        df.rename(columns={'Pageviews': 'Value'}, inplace=True)
        total = df['Value'].sum()
        if percent_mode == 'round':
            df['Percent'] = (df['Value'] / total * 100).round().astype(int)
        elif percent_mode == 'floor_with_target':
            vals = df['Value'].tolist()
            shares = [v * 100 / total for v in vals]
            floors = [int(s) for s in shares]
            remainders = [s - f for s, f in zip(shares, floors)]
            s = sum(floors)
            if target_sum is None:
                target_sum = s
            need = max(0, int(target_sum) - s)
            order = sorted(range(len(vals)), key=lambda i: (-remainders[i], i))
            inc = set(order[:need])
            perc = [floors[i] + (1 if i in inc else 0) for i in range(len(vals))]
            df['Percent'] = perc
        elif percent_mode == 'floor':
            df['Percent'] = (df['Value'] / total * 100).apply(lambda x: int(x))
        else:
            raise ValueError('Unknown percent_mode')
        return df[['Entry', 'Value', 'Percent']]

    browsers_all_time = parse_with_percent(inputs_dir / 'input_01.csv')
    browsers_this_month = parse_with_percent(inputs_dir / 'input_02.csv')

    origin_this_month = parse_values_only(inputs_dir / 'input_03.csv', percent_mode='floor_with_target', target_sum=94)
    origin_all_time = parse_values_only(inputs_dir / 'input_04.csv', percent_mode='floor_with_target', target_sum=94)

    os_all_time = parse_with_percent(inputs_dir / 'input_05.csv')
    os_this_month = parse_with_percent(inputs_dir / 'input_06.csv')

    b_tm = browsers_this_month.rename(columns={'Entry': 'Browser', 'Value': 'This Month Pageviews Value', 'Percent': 'This Month Pageviews %'}).copy()
    b_at = browsers_all_time.rename(columns={'Entry': 'Browser', 'Value': 'All Time Pageviews Value', 'Percent': 'All Time Pageviews %'}).copy()
    b_tm['__order_tm'] = range(len(b_tm))
    b_at['__order_at'] = range(len(b_at))
    browser_df = pd.merge(b_tm, b_at, on='Browser', how='outer')
    browser_df['Change in % this month'] = browser_df['This Month Pageviews %'] - browser_df['All Time Pageviews %']
    browser_df['__order_tm'] = browser_df['__order_tm'].fillna(1e9)
    browser_df = browser_df.sort_values(['__order_tm', '__order_at'])
    browser_df = browser_df[[
        'Change in % this month',
        'Browser',
        'This Month Pageviews Value',
        'This Month Pageviews %',
        'All Time Pageviews Value',
        'All Time Pageviews %'
    ]]

    o_tm = os_this_month.rename(columns={'Entry': 'Operating System', 'Value': 'This Month Pageviews Value', 'Percent': 'This Month Pageviews %'}).copy()
    o_at = os_all_time.rename(columns={'Entry': 'Operating System', 'Value': 'All Time Pageviews Value', 'Percent': 'All Time Pageviews %'}).copy()
    o_tm['__order_tm'] = range(len(o_tm))
    o_at['__order_at'] = range(len(o_at))
    os_df = pd.merge(o_tm, o_at, on='Operating System', how='outer')
    os_df['Change in % this month'] = os_df['This Month Pageviews %'] - os_df['All Time Pageviews %']
    os_df['__order_tm'] = os_df['__order_tm'].fillna(1e9)
    os_df = os_df.sort_values(['__order_tm', '__order_at'])
    os_df = os_df[[
        'Change in % this month',
        'Operating System',
        'This Month Pageviews Value',
        'This Month Pageviews %',
        'All Time Pageviews Value',
        'All Time Pageviews %'
    ]]

    g_tm = origin_this_month.rename(columns={'Entry': 'Origin', 'Value': 'This Month Pageviews', 'Percent': 'This Month Pageviews %'}).copy()
    g_at = origin_all_time.rename(columns={'Entry': 'Origin', 'Value': 'All Time Pageviews', 'Percent': 'All Time Views %'}).copy()
    g_tm['__order_tm'] = range(len(g_tm))
    g_at['__order_at'] = range(len(g_at))
    origin_df = pd.merge(g_tm, g_at, on='Origin', how='outer')
    origin_df['Change in % pageviews'] = origin_df['This Month Pageviews %'] - origin_df['All Time Views %']
    origin_df['__order_tm'] = origin_df['__order_tm'].fillna(1e9)
    origin_df = origin_df.sort_values(['__order_tm', '__order_at'])
    origin_df = origin_df[[
        'Change in % pageviews',
        'This Month Pageviews %',
        'All Time Views %',
        'Origin',
        'All Time Pageviews',
        'This Month Pageviews'
    ]]

    return {
        'output_01.csv': browser_df,
        'output_02.csv': os_df,
        'output_03.csv': origin_df,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)

    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')








