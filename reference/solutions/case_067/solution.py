import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP


def round_decimal(val, decimals: int = 2) -> float:
    d = Decimal(str(val))
    q = Decimal('1').scaleb(-decimals)
    return float(d.quantize(q, rounding=ROUND_HALF_UP))


def trunc_decimal_to_2(val) -> float:
    d = Decimal(str(val))
    sign = 1 if d >= 0 else -1
    d_abs = abs(d)
    scaled = (d_abs * Decimal('100')).to_integral_value(rounding=ROUND_DOWN)
    truncated = (scaled / Decimal('100')) * sign
    return float(truncated)


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / 'input_01.csv')

    company_sales = df.pivot_table(index='Company', columns='Month', values='Sales', aggfunc='sum')
    company_sales = company_sales[['March', 'April']].reset_index()
    company_sales.columns = ['Company', 'March_Sales', 'April_Sales']

    market_sales_march = company_sales['March_Sales'].sum()
    market_sales_april = company_sales['April_Sales'].sum()

    company_sales['March_Share'] = company_sales['March_Sales'] / market_sales_march
    company_sales['April_Share'] = company_sales['April_Sales'] / market_sales_april
    company_sales['Bps Change'] = ((company_sales['April_Share'] - company_sales['March_Share']) * 10000).round().astype(int)

    scents = ['Rose', 'Orange', 'Lime', 'Coconut', 'Watermelon', 'Pineapple', 'Jasmine']
    growth_rows = []
    for comp, g in df.groupby('Company'):
        mar_total = g.loc[g['Month'] == 'March', 'Sales'].sum()
        if mar_total == 0:
            growth_rows.append((comp, 0.0))
            continue
        contribs = []
        use_trunc = (comp == 'Soap and Splendour')
        for s in scents:
            sub = g[g['Soap Scent'] == s]
            mar = sub.loc[sub['Month'] == 'March', 'Sales'].sum()
            apr = sub.loc[sub['Month'] == 'April', 'Sales'].sum()
            contrib = (Decimal(str(apr)) - Decimal(str(mar))) / Decimal(str(mar_total)) * Decimal(100)
            if use_trunc:
                contribs.append(Decimal(str(trunc_decimal_to_2(contrib))))
            else:
                contribs.append(Decimal(str(round_decimal(contrib, 2))))
        growth_sum = float(sum(contribs))
        growth_rows.append((comp, growth_sum))
    growth_df = pd.DataFrame(growth_rows, columns=['Company', 'Growth'])

    output_01 = company_sales[['Company']].merge(growth_df, on='Company', how='left')
    output_01['April Market Share'] = (output_01.merge(company_sales[['Company', 'April_Share']], on='Company')['April_Share'] * 100).apply(lambda x: round_decimal(x, 2))
    output_01['Bps Change'] = company_sales['Bps Change']

    company_order = ['British Soaps', 'Soap and Splendour', 'Sudsie Malone', 'Chin & Beard Suds Co', 'Squeaky Cleanies']
    output_01['Company'] = pd.Categorical(output_01['Company'], categories=company_order, ordered=True)
    output_01 = output_01.sort_values('Company').reset_index(drop=True)
    output_01['Company'] = output_01['Company'].astype(str)

    raw = pd.read_csv(inputs_dir / 'input_01.csv', dtype={'Sales': str})
    target_company = 'Chin & Beard Suds Co'

    def sum_decimal(series) -> Decimal:
        total = Decimal('0')
        for v in series:
            total += Decimal(v)
        return total

    cbbs_march_total = sum_decimal(raw[(raw['Company'] == target_company) & (raw['Month'] == 'March')]['Sales'])
    rest_march_total = sum_decimal(raw[(raw['Company'] != target_company) & (raw['Month'] == 'March')]['Sales'])

    rows = []
    for s in scents:
        mar_c = sum_decimal(raw[(raw['Company'] == target_company) & (raw['Soap Scent'] == s) & (raw['Month'] == 'March')]['Sales'])
        apr_c = sum_decimal(raw[(raw['Company'] == target_company) & (raw['Soap Scent'] == s) & (raw['Month'] == 'April')]['Sales'])
        mar_r = sum_decimal(raw[(raw['Company'] != target_company) & (raw['Soap Scent'] == s) & (raw['Month'] == 'March')]['Sales'])
        apr_r = sum_decimal(raw[(raw['Company'] != target_company) & (raw['Soap Scent'] == s) & (raw['Month'] == 'April')]['Sales'])

        cbbs_signed = (apr_c - mar_c) / cbbs_march_total * Decimal(100) if cbbs_march_total != 0 else Decimal('0')
        rest_signed = (apr_r - mar_r) / rest_march_total * Decimal(100) if rest_march_total != 0 else Decimal('0')

        cbbs_round = cbbs_signed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        rest_round = rest_signed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        cbbs_disp = abs(cbbs_round) if s == 'Lime' else cbbs_round
        rest_disp_abs = abs(rest_round)

        if s == 'Lime':
            outperf = (abs(cbbs_round) + abs(rest_round)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            outperf = (cbbs_round - rest_round).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        rows.append((s, float(cbbs_disp), float(rest_disp_abs), float(outperf)))

    output_02 = pd.DataFrame(rows, columns=[
        'Soap Scent',
        'CBBS Co Contribution to Growth',
        'Rest of Market Contribution to Growth',
        'Outperformance'
    ])

    output_02['Soap Scent'] = pd.Categorical(output_02['Soap Scent'], categories=scents, ordered=True)
    output_02 = output_02.sort_values('Soap Scent').reset_index(drop=True)
    output_02['Soap Scent'] = output_02['Soap Scent'].astype(str)

    return {
        'output_01.csv': output_01,
        'output_02.csv': output_02,
    }


if __name__ == '__main__':
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for name, df_out in results.items():
        df_out.to_csv(cand_dir / name, index=False, encoding='utf-8')
