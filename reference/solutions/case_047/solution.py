import pandas as pd
import re
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['Profit'] = pd.to_numeric(df['Profit'], errors='coerce')
    
    def get_level(item):
        match = re.match(r'^(\d+(?:\.\d+)*)', item)
        if match:
            num_part = match.group(1)
            return num_part.count('.') + 1
        return 0
    
    df['level'] = df['Item'].apply(get_level)
    
    
    for idx in df[df['level'] == 2].index:
        item = df.loc[idx, 'Item']
        match = re.match(r'^(\d+)\.(\d+)', item)
        if match:
            prefix = match.group(1) + '.' + match.group(2)
            children = df[(df['level'] == 3) & (df['Item'].str.startswith(prefix + '.'))]
            if len(children) > 0:
                df.loc[idx, 'Profit'] = children['Profit'].sum()
    
    for idx in df[df['level'] == 1].index:
        item = df.loc[idx, 'Item']
        match = re.match(r'^(\d+)\.', item)
        if match:
            prefix = match.group(1)
            children = df[(df['level'] == 2) & (df['Item'].str.startswith(prefix + '.'))]
            if len(children) > 0:
                df.loc[idx, 'Profit'] = children['Profit'].sum()
    
    def add_leading_spaces(item, level):
        if level == 2:
            return '     ' + item
        elif level == 3:
            return '          ' + item
        else:
            return item
    
    df['Item'] = df.apply(lambda row: add_leading_spaces(row['Item'], row['level']), axis=1)
    
    output = df[['Item', 'Profit']].copy()
    output['Profit'] = output['Profit'].astype(int)
    
    return {'output_01.csv': output}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
