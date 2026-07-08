
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    df['Sale Value'] = pd.to_numeric(df['Sale Value'])

    df[['Product Type', 'Quantity']] = df['Product Name'].str.split(
        ' - ', expand=True)
    df['Product Type'] = df['Product Type'].str.strip()

    df_liquid = df[df['Product Type'] == 'Liquid'].copy()
    df_bars = df[df['Product Type'] == 'Bar'].copy()

    def process_group(df_in, is_liquid):
        df_proc = df_in.copy()

        if is_liquid:
            df_proc['Value'] = df_proc['Quantity'].str.extract(
                '(\\d+\\.?\\d*)').astype(float)
            df_proc['Unit'] = df_proc['Quantity'].str.extract('([a-zA-Z]+)')
            df_proc['Quantity'] = df_proc.apply(
                lambda row: row['Value'] * 1000 if pd.notna(
                    row['Unit']) and row['Unit'].lower() == 'l' else row['Value'],
                axis=1
            ).astype(int)
        else:
            df_proc['Quantity'] = df_proc['Quantity'].str.extract(
                '(\\d+)').astype(int)

        agg_df = df_proc.groupby(['Store Name', 'Region', 'Quantity']).agg(
            **{'Sale Value': ('Sale Value', 'sum'),
               'Present in N orders': ('Order ID', 'nunique')}
        ).reset_index()

        agg_df['Sale Value'] = agg_df['Sale Value'].round(2)

        final_df = agg_df[['Quantity', 'Store Name',
                           'Region', 'Sale Value', 'Present in N orders']]
        return final_df

    liquid_output = process_group(df_liquid, is_liquid=True)
    bars_output = process_group(df_bars, is_liquid=False)

    return {
        'output_01.csv': bars_output,
        'output_02.csv': liquid_output
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
