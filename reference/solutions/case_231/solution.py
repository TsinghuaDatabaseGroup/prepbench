import pandas as pd
from pathlib import Path


def format_number(value, is_moving_avg=False):
    if pd.isna(value):
        return ''
    f = float(value)
    if abs(f) < 1e-10:
        return '0'
    if abs(f - round(f)) < 1e-10:
        return str(int(round(f)))
    if is_moving_avg:
        s = f'{f:.9f}'.rstrip('0').rstrip('.')
        return s
    s = f'{f:.6f}'.rstrip('0').rstrip('.')
    return s


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / 'input_01.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df_filtered = df[df['Date'] < pd.to_datetime('2023-07-01')].copy()

    df_filtered['Month'] = df_filtered['Date'].dt.to_period(
        'M').dt.to_timestamp()
    monthly_agg = df_filtered.groupby(['Month', 'Store', 'Bike Type']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    min_months = monthly_agg.groupby(['Store', 'Bike Type'])[
        'Month'].min().reset_index()
    min_months.rename(columns={'Month': 'min_month'}, inplace=True)

    end_date = pd.to_datetime('2023-06-01')

    scaffold = pd.concat([
        pd.DataFrame({
            'Month': pd.date_range(start=row['min_month'], end=end_date, freq='MS'),
            'Store': row['Store'],
            'Bike Type': row['Bike Type']
        })
        for _, row in min_months.iterrows()
    ], ignore_index=True)

    df_scaffolded = pd.merge(scaffold, monthly_agg, on=[
                             'Month', 'Store', 'Bike Type'], how='left')
    df_scaffolded['Sales'] = df_scaffolded['Sales'].fillna(0)
    df_scaffolded['Profit'] = df_scaffolded['Profit'].fillna(0)

    df_scaffolded = df_scaffolded.sort_values(
        by=['Store', 'Bike Type', 'Month'])
    df_scaffolded['3 Month Moving Average Profit'] = df_scaffolded.groupby(['Store', 'Bike Type'])['Profit'] \
        .rolling(window=3, min_periods=3).mean().reset_index(level=[0, 1], drop=True)

    output_df = df_scaffolded[['Month', 'Store', 'Bike Type',
                               'Sales', 'Profit', '3 Month Moving Average Profit']]

    output_df['Sales'] = output_df['Sales'].astype(
        float).apply(lambda x: format_number(x, False))
    output_df['Profit'] = output_df['Profit'].astype(
        float).apply(lambda x: format_number(x, False))
    output_df['3 Month Moving Average Profit'] = output_df['3 Month Moving Average Profit'].astype(
        float).apply(lambda x: format_number(x, True))

    return {'output_01.csv': output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df['Month'] = pd.to_datetime(df['Month']).dt.strftime('%d/%m/%Y')
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
