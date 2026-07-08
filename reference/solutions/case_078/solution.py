import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df.columns = df.columns.str.strip()
    
    df['Store Manager'] = df['Store Manager'].ffill()
    
    if 'Row ID' in df.columns:
        df = df.drop(columns=['Row ID'])
    
    df = df.dropna()
    
    output_df = df[['Store Manager', 'Store', 'Sales Target']].copy()
    
    output_df['Store Manager'] = output_df['Store Manager'].astype(str)
    output_df['Store'] = output_df['Store'].astype(str)
    output_df['Sales Target'] = output_df['Sales Target'].astype(int)
    
    return {
        'output_01.csv': output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

