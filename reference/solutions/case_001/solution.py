import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv_path)
    
    df['Date'] = pd.to_datetime(
        df['When Sold Year'].astype(str) + '-' + 
        df['When Sold Month'].astype(str).str.zfill(2) + '-01',
        format='%Y-%m-%d'
    )
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
    
    df['Total Car Sales'] = df['Red Cars'] + df['Silver Cars'] + df['Black Cars'] + df['Blue Cars']
    
    aggregated = df.groupby(['Date', 'Dealership'], as_index=False).agg({
        'Total Car Sales': 'sum',
        'Red Cars': 'sum',
        'Silver Cars': 'sum',
        'Black Cars': 'sum',
        'Blue Cars': 'sum'
    })
    
    aggregated = aggregated.rename(columns={'Total Car Sales': 'Total Cars Sold'})
    
    output = aggregated[[
        'Total Cars Sold',
        'Date',
        'Dealership',
        'Red Cars',
        'Silver Cars',
        'Black Cars',
        'Blue Cars'
    ]].copy()
    
    output = output.sort_values(['Date', 'Dealership']).reset_index(drop=True)
    
    return {'output_01.csv': output}

BASE_DIR = Path(__file__).parent

if __name__ == "__main__":
    inputs_dir = BASE_DIR / "inputs"
    out_dir = BASE_DIR / "cand"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        df.to_csv(out_dir / name, index=False, encoding="utf-8")
