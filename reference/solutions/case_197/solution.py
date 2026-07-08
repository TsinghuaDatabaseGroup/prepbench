import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    
    region_map = {
        'input_01.csv': 'London',
        'input_02.csv': 'Northern',
        'input_03.csv': 'Scotland',
        'input_04.csv': 'Wales'
    }
    
    all_data = []
    
    for input_file in sorted(inputs_dir.glob('input_*.csv')):
        region = region_map[input_file.name]
        
        month_row = pd.read_csv(input_file, skiprows=2, nrows=1, header=None)
        months = []
        for col_idx in range(1, len(month_row.columns)):
            val = str(month_row.iloc[0, col_idx]).strip()
            if val and val in month_map:
                months.append(val)
        
        df = pd.read_csv(input_file, skiprows=3, header=0)
        
        store_col = df.columns[0]
        
        for idx, row in df.iterrows():
            store = row[store_col]
            
            col_idx = 1
            for month_name in months:
                sales = row.iloc[col_idx]
                profit = row.iloc[col_idx + 1]
                
                month_num = month_map[month_name]
                date_str = f"01/{month_num}/2022"
                
                all_data.append({
                    'Region': region,
                    'Store': store,
                    'Date': date_str,
                    'Sales': int(sales),
                    'Profit': int(profit)
                })
                
                col_idx += 2
        
    result_df = pd.DataFrame(all_data)
    
    result_df = result_df[['Region', 'Store', 'Date', 'Sales', 'Profit']]
    
    return {'output_01.csv': result_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

