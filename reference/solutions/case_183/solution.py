import pandas as pd
from pathlib import Path
from datetime import datetime
import math

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    today = datetime(2022, 8, 10)
    
    df['Monthly Capital Payment'] = df['Monthly Payment'] * (df['% of Monthly Repayment going to Capital'] / 100)
    
    df['Months to Payoff'] = df.apply(
        lambda row: math.ceil(row['Capital Repayment Remaining'] / row['Monthly Capital Payment']),
        axis=1
    )
    
    store_data = {}
    for _, row in df.iterrows():
        store_data[row['Store']] = {
            'initial_capital': row['Capital Repayment Remaining'],
            'monthly_capital': row['Monthly Capital Payment'],
            'months_to_payoff': row['Months to Payoff']
        }
    
    max_months = max(data['months_to_payoff'] for data in store_data.values())
    
    rows = []
    for month_offset in range(max_months):
        year = today.year + (today.month + month_offset - 1) // 12
        month = (today.month + month_offset - 1) % 12 + 1
        date_str = f"10/{month:02d}/{year}"
        
        for store, data in store_data.items():
            if month_offset < data['months_to_payoff']:
                remaining_capital = data['initial_capital'] - (month_offset + 1) * data['monthly_capital']
                
                total_capital = 0
                for other_store, other_data in store_data.items():
                    if month_offset < other_data['months_to_payoff']:
                        other_remaining = other_data['initial_capital'] - (month_offset + 1) * other_data['monthly_capital']
                        total_capital += other_remaining
                
                rows.append({
                    'Monthly Payment Date': date_str,
                    'Store': store,
                    'Capital Outstanding Total': total_capital,
                    'Remaining Capital to Repay': remaining_capital
                })
    
    result_df = pd.DataFrame(rows)
    result_df['Capital Outstanding Total'] = result_df['Capital Outstanding Total'].astype(float)
    result_df['Remaining Capital to Repay'] = result_df['Remaining Capital to Repay'].astype(float)
    
    return {
        'output_01.csv': result_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

