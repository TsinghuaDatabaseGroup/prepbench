import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df_input = pd.read_csv(input_file)
    
    grid_size = 4
    
    numbers = list(range(1, grid_size + 1))
    
    result_dict = {"Number": numbers}
    
    for col in range(1, grid_size + 1):
        result_dict[str(col)] = [num * col for num in numbers]
    
    df_output = pd.DataFrame(result_dict)
    
    return {"output_01.csv": df_output}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

