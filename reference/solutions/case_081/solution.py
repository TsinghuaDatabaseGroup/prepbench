import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df.columns = ['Row_ID'] + list(df.columns[1:])
    
    month_cols = [col for col in df.columns if col not in ['Row_ID', 'Store']]
    df = df[~(df['Store'].isna() & df[month_cols].isna().all(axis=1))].copy()
    
    df['Store'] = df['Store'].ffill()
    
    df = df[df['Store'].notna()].copy()
    
    df['Row_Type'] = None
    
    for store in df['Store'].unique():
        store_mask = df['Store'] == store
        store_indices = df[store_mask].index
        
        if len(store_indices) >= 3:
            df.loc[store_indices[0], 'Row_Type'] = 'Sales'
            df.loc[store_indices[1], 'Row_Type'] = 'Target'
            df.loc[store_indices[2], 'Row_Type'] = 'Difference'
    
    df = df[df['Row_Type'].notna()].copy()
    
    month_cols = [col for col in df.columns if col not in ['Row_ID', 'Store', 'Row_Type']]
    
    df_melted = df.melt(
        id_vars=['Store', 'Row_Type'],
        value_vars=month_cols,
        var_name='Month_Col',
        value_name='Value'
    )
    
    df_melted = df_melted[df_melted['Value'].notna()].copy()
    
    def extract_month(col_name):
        month_map = {
            'Jan': '01',
            'Feb': '02',
            'Mar': '03',
            'Apr': '04',
            'May': '05',
            'Jun': '06',
            'Jul': '07'
        }
        for month_name, month_num in month_map.items():
            if month_name in col_name:
                return f"01/{month_num}/2020"
        return None
    
    df_melted['Month'] = df_melted['Month_Col'].apply(extract_month)
    df_melted = df_melted[df_melted['Month'].notna()].copy()
    
    df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
    
    df_pivot = df_melted.pivot_table(
        index=['Store', 'Month'],
        columns='Row_Type',
        values='Value',
        aggfunc='first'
    ).reset_index()
    
    for col in ['Sales', 'Target', 'Difference']:
        if col not in df_pivot.columns:
            df_pivot[col] = None
    
    output = df_pivot[['Store', 'Month', 'Sales', 'Target', 'Difference']].copy()
    
    output['Sales'] = output['Sales'].astype(float)
    output['Target'] = output['Target'].astype(float)
    output['Difference'] = output['Difference'].astype(float)
    
    output = output.sort_values(by=['Store', 'Month']).reset_index(drop=True)
    
    return {
        "output_01.csv": output
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

