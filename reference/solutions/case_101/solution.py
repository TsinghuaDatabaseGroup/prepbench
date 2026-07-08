from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv)
    
    df['Brand'] = df['Model'].str.extract(r'([A-Z]+)')
    
    df['Order Value'] = df['Value per Bike'] * df['Quantity']
    
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Shipping Date'] = pd.to_datetime(df['Shipping Date'], format='%d/%m/%Y')
    df['Days to Ship'] = (df['Shipping Date'] - df['Order Date']).dt.days
    
    agg1 = df.groupby(['Brand', 'Bike Type']).agg({
        'Quantity': 'sum',
        'Order Value': 'sum',
        'Value per Bike': 'mean'
    }).reset_index()
    
    agg1.columns = ['Brand', 'Bike Type', 'Quantity Sold', 'Order Value', 'Avg Bike Value per Brand']
    agg1['Avg Bike Value per Brand'] = agg1['Avg Bike Value per Brand'].round(1)
    
    agg2 = df.groupby(['Brand', 'Store']).agg({
        'Quantity': 'sum',
        'Order Value': 'sum',
        'Days to Ship': 'mean'
    }).reset_index()
    
    agg2.columns = ['Brand', 'Store', 'Total Quantity Sold', 'Total Order Value', 'Avg Days to Ship']
    agg2['Avg Days to Ship'] = agg2['Avg Days to Ship'].round(1)
    
    return {
        "output_01.csv": agg1,
        "output_02.csv": agg2,
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

