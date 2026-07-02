import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['Sale Date'] = pd.to_datetime(df['Sale Date'], format='%d/%m/%Y %H:%M:%S')
    df['Date'] = df['Sale Date'].dt.date
    
    sales_dates = set(df['Date'].unique())
    
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D').date
    
    no_sales_dates = [date for date in all_dates if date not in sales_dates]
    
    no_sales_df = pd.DataFrame({'Date': no_sales_dates})
    no_sales_df['Date'] = pd.to_datetime(no_sales_df['Date'])
    no_sales_df['Day of the Week'] = no_sales_df['Date'].dt.day_name()
    
    result = no_sales_df.groupby('Day of the Week', as_index=False).size()
    result.columns = ['Day of the Week', 'Number of Days']
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    result['Day of the Week'] = pd.Categorical(result['Day of the Week'], categories=day_order, ordered=True)
    result = result.sort_values('Day of the Week').reset_index(drop=True)
    
    result['Day of the Week'] = result['Day of the Week'].astype(str)
    
    return {
        "output_01.csv": result
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

