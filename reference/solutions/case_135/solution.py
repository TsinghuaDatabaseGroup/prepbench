import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_df = pd.read_csv(inputs_dir / "input_01.csv")

    sold_df = input_df[input_df['Status'] != 'Return to Manufacturer'].copy()

    pivot_df = sold_df.pivot_table(
        index='Store',
        columns='Item',
        values='Number of Items',
        aggfunc='sum',
        fill_value=0
    )

    pivot_df['Items sold per store'] = pivot_df.sum(axis=1)

    pivot_df = pivot_df.reset_index()

    output_columns = [
        'Items sold per store',
        'Wheels',
        'Tyres',
        'Saddles',
        'Brakes',
        'Store'
    ]
    output_df = pivot_df[output_columns]

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

