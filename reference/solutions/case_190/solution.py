import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['Employee'] = df['Employee'].ffill()
    
    df['Work Level'] = df['Work Level'].ffill()
    
    df['Work Level'] = df['Work Level'].astype(float).astype(int)
    
    df['Stage'] = df['Stage'].str.replace('Work Anniverary', 'Work Anniversary', regex=False)
    
    if df['Date'].dtype != 'object':
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')
    else:
        df['Date'] = df['Date'].astype(str)
    
    df = df.sort_values('Record ID').reset_index(drop=True)
    
    return {
        "output_01.csv": df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

