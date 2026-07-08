import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_df = pd.read_csv(inputs_dir / "input_01.csv")
    min_num = input_df['Numbers'].min()
    max_num = input_df['Numbers'].max()
    
    numbers = list(range(min_num, max_num + 1))
    
    rows = []
    for i in numbers:
        row = {'Number': i}
        for j in numbers:
            row[str(j)] = i * j
        rows.append(row)
    
    result = pd.DataFrame(rows)
    
    columns = ['Number'] + [str(i) for i in numbers]
    result = result[columns]
    
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

