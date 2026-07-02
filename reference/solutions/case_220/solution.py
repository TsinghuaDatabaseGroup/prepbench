import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    def clean_location(loc: str) -> str:
        loc_normalized = loc.replace('0', 'o').replace('3', 'e').lower()
        
        if 'london' in loc_normalized or 'londen' in loc_normalized:
            return 'London'
        elif 'manchester' in loc_normalized:
            return 'Manchester'
        elif 'liverpool' in loc_normalized or 'livrepool' in loc_normalized:
            return 'Liverpool'
        return loc
    
    df['Location'] = df['Location'].apply(clean_location)
    
    df_pivot = df.pivot_table(
        index=['Location', 'Nut Type'],
        columns='Category',
        values='Value',
        aggfunc='first'
    ).reset_index()
    
    df_pivot.columns.name = None
    
    df_pivot['Revenue'] = df_pivot['Price (£) per pack'] * df_pivot['Quant per Q']
    
    output = df_pivot.groupby('Location', as_index=False).agg({
        'Revenue': 'sum',
        'Price (£) per pack': 'mean'
    })
    
    output = output.rename(columns={
        'Price (£) per pack': 'Avg. Price (£) per pack'
    })
    
    output['Avg. Price (£) per pack'] = output['Avg. Price (£) per pack'].round(2)
    
    output = output.sort_values('Location')
    
    return {
        "output_01.csv": output,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8")
        print(f"已生成: {output_path}")

