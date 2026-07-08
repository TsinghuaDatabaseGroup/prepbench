import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def round_decimal(val, decimals: int = 2) -> float:
    d = Decimal(str(val))
    q = Decimal('1').scaleb(-decimals)
    return float(d.quantize(q, rounding=ROUND_HALF_UP))


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / 'input_01.csv', dtype={'Sales': str})
    df['Sales_Decimal'] = df['Sales'].apply(Decimal)

    company_sales = df.pivot_table(index='Company', columns='Month', values='Sales_Decimal', aggfunc='sum')
    company_sales = company_sales[['March', 'April']].reset_index()
    company_sales.columns = ['Company', 'March_Sales', 'April_Sales']

    market_sales_march = company_sales['March_Sales'].sum()
    market_sales_april = company_sales['April_Sales'].sum()

    company_sales['March_Share'] = company_sales['March_Sales'] / market_sales_march
    company_sales['April_Share'] = company_sales['April_Sales'] / market_sales_april
    company_sales['Bps Change'] = company_sales.apply(
        lambda row: int(((row['April_Share'] - row['March_Share']) * Decimal(10000)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)),
        axis=1,
    )
    company_sales['Growth'] = company_sales.apply(
        lambda row: round_decimal((row['April_Sales'] - row['March_Sales']) / row['March_Sales'] * Decimal(100), 2)
        if row['March_Sales'] != 0 else 0.0,
        axis=1,
    )

    scents = ['Rose', 'Orange', 'Lime', 'Coconut', 'Watermelon', 'Pineapple', 'Jasmine']

    output_01 = company_sales[['Company', 'Growth']].copy()
    output_01['April Market Share'] = (company_sales['April_Share'] * Decimal(100)).apply(lambda x: round_decimal(x, 2))
    output_01['Bps Change'] = company_sales['Bps Change']

    company_order = ['British Soaps', 'Soap and Splendour', 'Sudsie Malone', 'Chin & Beard Suds Co', 'Squeaky Cleanies']
    output_01['Company'] = pd.Categorical(output_01['Company'], categories=company_order, ordered=True)
    output_01 = output_01.sort_values('Company').reset_index(drop=True)
    output_01['Company'] = output_01['Company'].astype(str)

    target_company = 'Chin & Beard Suds Co'

    def sum_decimal(series) -> Decimal:
        total = Decimal('0')
        for v in series:
            total += Decimal(v)
        return total

    cbbs_march_total = sum_decimal(df[(df['Company'] == target_company) & (df['Month'] == 'March')]['Sales'])
    rest_march_total = sum_decimal(df[(df['Company'] != target_company) & (df['Month'] == 'March')]['Sales'])

    rows = []
    for s in scents:
        mar_c = sum_decimal(df[(df['Company'] == target_company) & (df['Soap Scent'] == s) & (df['Month'] == 'March')]['Sales'])
        apr_c = sum_decimal(df[(df['Company'] == target_company) & (df['Soap Scent'] == s) & (df['Month'] == 'April')]['Sales'])
        mar_r = sum_decimal(df[(df['Company'] != target_company) & (df['Soap Scent'] == s) & (df['Month'] == 'March')]['Sales'])
        apr_r = sum_decimal(df[(df['Company'] != target_company) & (df['Soap Scent'] == s) & (df['Month'] == 'April')]['Sales'])

        cbbs_signed = (apr_c - mar_c) / cbbs_march_total * Decimal(100) if cbbs_march_total != 0 else Decimal('0')
        rest_signed = (apr_r - mar_r) / rest_march_total * Decimal(100) if rest_march_total != 0 else Decimal('0')

        cbbs_round = cbbs_signed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        rest_round = rest_signed.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        outperf = (cbbs_round - rest_round).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        rows.append((s, float(cbbs_round), float(rest_round), float(outperf)))

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
