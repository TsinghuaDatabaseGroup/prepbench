import pandas as pd
from pathlib import Path

PREFIX_FROM = 'Tourist arrivals from '
SERIES_UN = 'Tourist arrivals - UN passport holders and others'
CONTINENTS = ['Europe', 'Asia', 'Africa', 'Americas', 'Oceania', 'the Middle East']

COUNTRY_ORDER = [
    ("Europe", "Germany"),
    ("Europe", "Italy"),
    ("Europe", "Russia"),
    ("Europe", "United Kingdom"),
    ("Asia", "China"),
    ("Asia", "India"),
    ("Europe", "France"),
    ("Oceania", "Australia"),
    ("Americas", "United States"),
]
KEEP_COUNTRIES = {c for _, c in COUNTRY_ORDER}
KEEP_BREAKDOWNS = {b for b, _ in COUNTRY_ORDER}

UNKNOWN_ORDER = CONTINENTS + ['UN passport holders and others']


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    raw = pd.read_csv(inputs_dir / 'input_01.csv')

    df = raw.melt(
        id_vars=['id', 'Series-Measure', 'Hierarchy-Breakdown', 'Unit-Detail'],
        var_name='Month',
        value_name='Value'
    )

    df = df.rename(columns={'Hierarchy-Breakdown': 'Breakdown', 'Value': 'Number of Tourists'})
    df['Number of Tourists'] = pd.to_numeric(df['Number of Tourists'], errors='coerce')
    df = df.dropna(subset=['Number of Tourists']).copy()
    df['Number of Tourists'] = df['Number of Tourists'].astype(int)
    df['Month'] = pd.to_datetime(df['Month'], format='%b-%y')

    is_from = df['Series-Measure'].str.startswith(PREFIX_FROM)
    is_un = df['Series-Measure'] == SERIES_UN

    df_from = df[is_from].copy()

    df_from['target'] = df_from['Series-Measure'].str[len(PREFIX_FROM):]

    df_c = df_from[~df_from['target'].isin(CONTINENTS)].copy()
    df_c['Country'] = df_c['target'].replace({'the United Kingdom': 'United Kingdom'})
    df_c['Breakdown'] = df_c['Breakdown'].apply(lambda x: x.split(' / ')[-1])
    df_c = df_c[df_c['Country'].isin(KEEP_COUNTRIES) & df_c['Breakdown'].isin(KEEP_BREAKDOWNS)].copy()

    df_cont = df_from[df_from['target'].isin(CONTINENTS)].copy()
    df_cont = df_cont.rename(columns={'Number of Tourists': 'Continent Total'})
    df_cont['Continent'] = df_cont['target']
    df_cont = df_cont[['Month', 'Continent', 'Continent Total']]

    sum_c = df_c.groupby(['Month', 'Breakdown'], as_index=False)['Number of Tourists'].sum()
    sum_c = sum_c.rename(columns={'Breakdown': 'Continent', 'Number of Tourists': 'Countries Sum'})

    unknown = pd.merge(df_cont, sum_c, on=['Month', 'Continent'], how='left')
    unknown['Countries Sum'] = unknown['Countries Sum'].fillna(0).astype(int)
    unknown['Number of Tourists'] = (unknown['Continent Total'] - unknown['Countries Sum']).clip(lower=0).astype(int)
    unknown['Breakdown'] = unknown['Continent']
    unknown['Country'] = 'Unknown'
    unknown = unknown[['Breakdown', 'Number of Tourists', 'Month', 'Country']]

    df_un = df[is_un][['Month', 'Number of Tourists']].copy()
    if not df_un.empty:
        df_un['Breakdown'] = 'UN passport holders and others'
        df_un['Country'] = 'Unknown'
        df_un = df_un[['Breakdown', 'Number of Tourists', 'Month', 'Country']]

    order_map = {pair: i for i, pair in enumerate(COUNTRY_ORDER)}
    df_c['__ord__'] = df_c.apply(lambda r: order_map.get((r['Breakdown'], r['Country']), 9999), axis=1)
    df_c = df_c.sort_values(['Month', '__ord__']).drop(columns=['__ord__'])
    countries_out = df_c[['Breakdown', 'Number of Tourists', 'Month', 'Country']]

    unk_order_map = {k: i for i, k in enumerate(UNKNOWN_ORDER)}
    unknown['__ord__'] = unknown['Breakdown'].map(unk_order_map)
    unknown = unknown.sort_values(['Month', '__ord__']).drop(columns=['__ord__'])

    parts = [countries_out, unknown]
    if not df_un.empty:
        df_un['__ord__'] = df_un['Breakdown'].map(unk_order_map)
        df_un = df_un.sort_values(['Month', '__ord__']).drop(columns=['__ord__'])
        parts.append(df_un)

    out = pd.concat(parts, ignore_index=True)

    out['Month'] = out['Month'].dt.strftime('%d/%m/%Y')

    return {'output_01.csv': out}


if __name__ == '__main__':
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'

    cand_dir = task_dir / 'cand'
    if not cand_dir.exists():
        cand_dir.mkdir()

    solutions = solve(inputs_dir)
    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
