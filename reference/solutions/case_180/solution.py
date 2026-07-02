import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    sales_df = pd.read_csv(inputs_dir / "input_01.csv")
    targets_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    sales_df['Product Type'] = sales_df['Product Name'].str.split(' - ').str[0]
    
    sales_summary = sales_df.groupby(['Store Name', 'Product Type']).agg({
        'Sale Value': 'sum',
        'Region': 'first'
    }).reset_index()
    
    targets_long = targets_df.melt(
        id_vars=['PRODUCT'],
        var_name='STORE',
        value_name='TARGET_VALUE'
    )
    
    targets_long['TARGET_VALUE'] = targets_long['TARGET_VALUE'].astype(str).str.rstrip('%').str.strip()
    targets_long['TARGET_VALUE'] = pd.to_numeric(targets_long['TARGET_VALUE'], errors='coerce')
    
    targets_long['Target'] = targets_long['TARGET_VALUE'] * 1000
    
    sales_summary['Store Name'] = sales_summary['Store Name'].str.title()
    sales_summary['Product Type'] = sales_summary['Product Type'].str.title()
    
    targets_long['STORE'] = targets_long['STORE'].str.title()
    targets_long['PRODUCT'] = targets_long['PRODUCT'].str.title()
    
    result = sales_summary.merge(
        targets_long[['STORE', 'PRODUCT', 'Target']],
        left_on=['Store Name', 'Product Type'],
        right_on=['STORE', 'PRODUCT'],
        how='left'
    )
    
    result = result.drop(columns=['STORE', 'PRODUCT'])
    
    result['Beats Target?'] = result['Sale Value'] >= result['Target']
    
    result = result.rename(columns={
        'Product Type': 'PRODUCT',
        'Sale Value': 'Sale Value'
    })
    
    result = result[['Beats Target?', 'Target', 'Store Name', 'Region', 'Sale Value', 'PRODUCT']]
    
    return {'output_01.csv': result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    cand_dir.mkdir(exist_ok=True)
    
    results = solve(inputs_dir)
    
    for filename, df in results.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8')
