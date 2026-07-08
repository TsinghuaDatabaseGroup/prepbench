import pandas as pd
from pathlib import Path
import re
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    rates_df = pd.read_csv(inputs_dir / "input_01.csv")
    
    def extract_rate(rate_str):
        match = re.search(r'= ([\d.]+) USD', rate_str)
        if match:
            return float(match.group(1))
        return None
    
    rates_df['Rate'] = rates_df['British Pound to US Dollar'].apply(extract_rate)
    rates_df['Date'] = pd.to_datetime(rates_df['Date'])
    
    rates_df['Year'] = rates_df['Date'].dt.year
    rates_df['Week'] = rates_df['Date'].dt.strftime('%U').astype(int)
    
    rates_df = rates_df[~((rates_df['Date'] == pd.Timestamp('2019-12-29')) & (rates_df['Year'] == 2019) & (rates_df['Week'] == 51))]
    
    weekly_rates = rates_df.groupby(['Year', 'Week']).agg({
        'Rate': ['max', 'min']
    }).reset_index()
    weekly_rates.columns = ['Year', 'Week', 'Best_Rate', 'Worst_Rate']
    
    sales_df = pd.read_csv(inputs_dir / "input_02.csv")
    
    sales_df['US_Percent'] = sales_df['US Stock sold (%)'] / 100
    sales_df['UK_Percent'] = 1 - sales_df['US_Percent']
    
    sales_df['US_Sales_GBP'] = sales_df['Sales Value'] * sales_df['US_Percent']
    sales_df['UK_Sales_GBP'] = sales_df['Sales Value'] * sales_df['UK_Percent']
    
    sales_df['Week_U'] = sales_df['Week'] - 1
    
    merged = sales_df.merge(
        weekly_rates,
        left_on=['Year', 'Week_U'],
        right_on=['Year', 'Week'],
        how='inner',
        suffixes=('', '_rate')
    )
    
    merged['US Sales (USD) Best Case'] = merged['US_Sales_GBP'] * merged['Best_Rate']
    merged['US Sales (USD) Worst Case'] = merged['US_Sales_GBP'] * merged['Worst_Rate']
    merged['US Sales Potential Variance'] = (
        merged['US Sales (USD) Best Case'] - merged['US Sales (USD) Worst Case']
    )
    
    output = pd.DataFrame({
        'Week': merged.apply(lambda row: f"wk {int(row['Week'])} {int(row['Year'])}", axis=1),
        'UK Sales Value (GBP)': merged['UK_Sales_GBP'].round(2),
        'US Sales (USD) Best Case': merged['US Sales (USD) Best Case'].round(2),
        'US Sales (USD) Worst Case': merged['US Sales (USD) Worst Case'].round(2),
        'US Sales Potential Variance': merged['US Sales Potential Variance'].round(2)
    })
    
    output['Sort_Year'] = merged['Year']
    output['Sort_Week'] = merged['Week']
    output = output.sort_values(['Sort_Year', 'Sort_Week']).drop(columns=['Sort_Year', 'Sort_Week'])
    
    output = output.reset_index(drop=True)
    
    return {'output_01.csv': output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8')
