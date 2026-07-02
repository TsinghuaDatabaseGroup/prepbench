
import pandas as pd
from pathlib import Path
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / 'input_01.csv'
    df = pd.read_csv(input_file, header=None)

    split_indices = df[df.isnull().all(axis=1)].index.tolist()
    split_indices = [-1] + split_indices + [len(df)]

    all_branch_data = []

    for i in range(len(split_indices) - 1):
        start = split_indices[i] + 1
        end = split_indices[i+1]
        
        if start >= end:
            continue

        branch_block = df.iloc[start:end].reset_index(drop=True)
        first_name = str(branch_block.iloc[0, 1]) if branch_block.shape[0] > 0 else ''
        if first_name.startswith('Unnamed'):
            branch_block = branch_block.iloc[1:].reset_index(drop=True)
        if branch_block.empty:
            continue
        branch_name = branch_block.iloc[0, 1]
        
        header_cells = branch_block.iloc[0, 2:].tolist()
        header = [str(h).replace('Year ', '').strip() for h in header_cells if pd.notna(h)]
        data = branch_block.iloc[1:, 1:2+len(header)]
        data.columns = ['Measure'] + header
        
        melted_df = data.melt(
            id_vars=['Measure'], 
            value_vars=header, 
            var_name='Recorded Year', 
            value_name='Value'
        )
        melted_df['Branch'] = branch_name
        melted_df = melted_df.dropna(subset=['Value', 'Measure'])
        all_branch_data.append(melted_df)

    final_df = pd.concat(all_branch_data, ignore_index=True)

    def extract_multiplier(measure):
        if '(m)' in measure:
            return 1_000_000
        if '(k)' in measure:
            return 1_000
        return 1

    final_df['Multiplier'] = final_df['Measure'].apply(extract_multiplier)
    final_df['Clean Measure names'] = final_df['Measure'].str.replace(r' \(m\)| \(k\)', '', regex=True)

    final_df['Value'] = pd.to_numeric(final_df['Value'], errors='coerce')
    final_df = final_df.dropna(subset=['Value'])
    final_df['True Value'] = final_df['Value'] * final_df['Multiplier']

    output_df = final_df[['Branch', 'Clean Measure names', 'Recorded Year', 'True Value']].copy()
    output_df['Recorded Year'] = pd.to_numeric(output_df['Recorded Year'], errors='coerce')
    output_df = output_df.dropna(subset=['Recorded Year'])
    output_df['Recorded Year'] = output_df['Recorded Year'].astype(int)
    output_df['True Value'] = output_df['True Value'].round(0).astype(int)

    branch_order = ['Lewisham', 'York', 'Wimbledon']
    measure_order = ['Sales', 'Profit', 'Number of Staff', 'Staff Cost']
    year_order = [2021, 2020]

    output_df['Branch'] = pd.Categorical(output_df['Branch'], categories=branch_order, ordered=True)
    output_df['Clean Measure names'] = pd.Categorical(output_df['Clean Measure names'], categories=measure_order, ordered=True)
    output_df['Recorded Year'] = pd.Categorical(output_df['Recorded Year'], categories=year_order, ordered=True)

    output_df = output_df.sort_values(['Branch', 'Clean Measure names', 'Recorded Year']).reset_index(drop=True)

    output_df['Branch'] = output_df['Branch'].astype(str)
    output_df['Clean Measure names'] = output_df['Clean Measure names'].astype(str)
    output_df['Recorded Year'] = output_df['Recorded Year'].astype(int)
    output_df['True Value'] = output_df['True Value'].astype(int)

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)
    
    solutions = solve(inputs_dir)
    
    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

