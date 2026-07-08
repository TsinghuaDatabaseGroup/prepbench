from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    store_names = {
        "input_01.csv": "Manchester",
        "input_02.csv": "London",
        "input_03.csv": "Leeds",
        "input_04.csv": "York",
        "input_05.csv": "Birmingham"
    }
    
    all_dfs = []
    for filename, store_name in store_names.items():
        df = pd.read_csv(inputs_dir / filename)
        df['Store'] = store_name
        all_dfs.append(df)
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    def date_to_quarter(date_str):
        date = pd.to_datetime(date_str)
        return date.quarter
    
    combined_df['Quarter'] = combined_df['Date'].apply(date_to_quarter)
    
    id_vars = ['Date', 'Store', 'Quarter']
    value_vars = [col for col in combined_df.columns if col not in id_vars]
    
    melted_df = pd.melt(
        combined_df,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='Customer_Product',
        value_name='Products Sold'
    )
    
    split_cols = melted_df['Customer_Product'].str.split(' - ', n=1, expand=True)
    melted_df['Customer Types'] = split_cols[0]
    melted_df['Product'] = split_cols[1]
    
    melted_df = melted_df.drop(columns=['Date', 'Customer_Product'])
    
    melted_df['Products Sold'] = pd.to_numeric(melted_df['Products Sold'], errors='coerce').fillna(0).astype(int)
    
    output_01 = melted_df.groupby(['Product', 'Quarter'], as_index=False)['Products Sold'].sum()
    output_01 = output_01.sort_values(['Product', 'Quarter'])
    
    output_02 = melted_df.groupby(['Store', 'Customer Types', 'Product'], as_index=False)['Products Sold'].sum()
    output_02 = output_02.sort_values(['Store', 'Customer Types', 'Product'])
    
    output_01 = output_01[['Product', 'Quarter', 'Products Sold']]
    output_02 = output_02[['Store', 'Customer Types', 'Product', 'Products Sold']]
    
    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

