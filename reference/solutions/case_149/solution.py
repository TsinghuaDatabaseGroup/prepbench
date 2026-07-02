import pandas as pd
from pathlib import Path
from typing import Dict


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    oct_df = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    nov_df = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)

    def extract_oct_ytd(df: pd.DataFrame) -> pd.DataFrame:
        mask_footer = df['Date'].isna() & df['Salesperson'].notna()
        footers = df.loc[mask_footer].copy()
        ytd_map = {}
        for _, row in footers.iterrows():
            name = str(row['Salesperson']).strip()
            ytd_val = None
            for col in row.index:
                if col in ['RowID', 'Date', 'Salesperson']:
                    continue
                val = row[col]
                if pd.isna(val):
                    continue
                s = str(val).strip()
                if s.replace('-', '').isdigit():
                    ytd_val = int(s)
            if name and ytd_val is not None:
                ytd_map[name] = ytd_val
        return pd.DataFrame({"Salesperson": list(ytd_map.keys()), "Initial YTD": list(ytd_map.values())})

    def process_tracker(df: pd.DataFrame) -> pd.DataFrame:
        df = df.replace({'': pd.NA, 'nan': pd.NA})
        is_footer = df['Date'].isna() & df['Salesperson'].notna()
        fill_col = df['Salesperson'].where(is_footer)
        df['Salesperson'] = fill_col.bfill()
        df = df[~is_footer].copy()
        df = df[['RowID', 'Date', 'Salesperson',
                 'Road', 'Gravel', 'Mountain']].copy()
        df['Date'] = pd.to_datetime(
            df['Date'], format='%d/%m/%Y', errors='coerce')
        for c in ['Road', 'Gravel', 'Mountain']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
        df['RowID'] = pd.to_numeric(df['RowID'], errors='coerce')
        return df

    oct_ytd_df = extract_oct_ytd(oct_df)
    oct_clean = process_tracker(oct_df)
    nov_clean = process_tracker(nov_df)

    combined = pd.concat([oct_clean, nov_clean], ignore_index=True, sort=False)

    long_df = combined.melt(
        id_vars=['RowID', 'Date', 'Salesperson'],
        value_vars=['Road', 'Gravel', 'Mountain'],
        var_name='Bike Type',
        value_name='Sales'
    )

    long_df = long_df.merge(oct_ytd_df, on='Salesperson', how='left')

    long_df = long_df.sort_values(
        ['Salesperson', 'Date', 'RowID']).reset_index(drop=True)

    long_df['Sales'] = pd.to_numeric(
        long_df['Sales'], errors='coerce').fillna(0)
    long_df['Initial YTD'] = pd.to_numeric(
        long_df['Initial YTD'], errors='coerce').fillna(0)
    long_df['Month'] = long_df['Date'].dt.month
    sales_nov_sum = long_df.loc[long_df['Month'] == 11].groupby(
        'Salesperson')['Sales'].sum().rename('NovSum')
    long_df = long_df.merge(sales_nov_sum, on='Salesperson', how='left')
    long_df['NovSum'] = long_df['NovSum'].fillna(0)
    long_df['YTD Total'] = long_df['Initial YTD']
    long_df.loc[long_df['Month'] == 11, 'YTD Total'] = long_df.loc[long_df['Month']
                                                                   == 11, 'Initial YTD'] + long_df.loc[long_df['Month'] == 11, 'NovSum']

    out = long_df[['Salesperson', 'Date',
                   'Bike Type', 'Sales', 'YTD Total']].copy()
    out['Date'] = out['Date'].dt.strftime('%d/%m/%Y')
    cat_order = pd.CategoricalDtype(
        categories=['Gravel', 'Road', 'Mountain'], ordered=True)
    out['Bike Type'] = out['Bike Type'].astype(cat_order)
    out['Sales'] = out['Sales'].astype(int)
    out['YTD Total'] = out['YTD Total'].astype(int)

    out = out.sort_values(['Salesperson', 'Date', 'Bike Type'],
                          kind='mergesort').reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    results = solve(inputs_dir)

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    for filename, df in results.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
