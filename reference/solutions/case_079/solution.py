import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    daily_sales = pd.read_csv(inputs_dir / "input_01.csv")
    scent_info = pd.read_csv(inputs_dir / "input_02.csv")
    orders = pd.read_csv(inputs_dir / "input_03.csv")
    
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
    orders['Date'] = pd.to_datetime(orders['Date'])
    
    df = daily_sales.merge(scent_info, on='Scent Code', how='left')
    
    df['Units Sold'] = df['Daily Sales'] / df['Price']
    
    
    def get_week_start(date):
        weekday = date.weekday()
        if weekday == 2:
            return date
        elif weekday < 2:
            days_back = weekday + 5
            return date - timedelta(days=days_back)
        else:
            days_back = weekday - 2
            return date - timedelta(days=days_back)
    
    df['Week Start'] = df['Date'].apply(get_week_start)
    
    weekly_summary = df.groupby(['Week Start', 'Scent Code', 'Scent', 'Price', 'Cost']).agg({
        'Units Sold': 'sum',
        'Daily Sales': 'sum'
    }).reset_index()
    weekly_summary.columns = ['Week Start', 'Scent Code', 'Scent', 'Price', 'Cost', 'Weekly Units Sold', 'Weekly Sales']
    
    orders['Week Start'] = orders['Date']
    weekly_summary = weekly_summary.merge(orders[['Week Start', 'Units Ordered']], on='Week Start', how='left')
    
    weekly_summary['Waste'] = weekly_summary['Units Ordered'] - weekly_summary['Weekly Units Sold']
    
    weekly_summary['Waste Cost'] = weekly_summary['Cost'] * weekly_summary['Waste']
    
    weekly_summary['Profit'] = weekly_summary['Weekly Sales'] - weekly_summary['Waste Cost']
    
    total_profit = weekly_summary.groupby('Scent').agg({
        'Profit': 'sum'
    }).reset_index()
    total_profit.columns = ['Scent', 'Total Profit']
    
    total_profit = total_profit.sort_values('Total Profit', ascending=False).reset_index(drop=True)
    total_profit['Profitability Rank'] = range(1, len(total_profit) + 1)
    
    result = total_profit[['Profitability Rank', 'Scent', 'Total Profit']]
    
    return {
        'output_01.csv': result
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

