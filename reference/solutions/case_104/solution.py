from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv, dtype=str)
    
    df['From Date Parsed'] = pd.to_datetime(df['From Date'], format='%d/%m/%Y', errors='coerce')
    
    latest_info = df.loc[df.groupby('Client')['From Date Parsed'].idxmax()][
        ['Client', 'Client ID', 'Account Manager', 'From Date']
    ].copy()
    
    client_mapping = latest_info.set_index('Client').to_dict('index')
    
    def update_client_info(row):
        client = row['Client']
        if client in client_mapping:
            row['Client ID'] = client_mapping[client]['Client ID']
            row['Account Manager'] = client_mapping[client]['Account Manager']
            row['From Date'] = client_mapping[client]['From Date']
        return row
    
    df_updated = df.apply(update_client_info, axis=1)
    
    output_df = df_updated[[
        'Training',
        'Contact Email',
        'Contact Name',
        'Client',
        'Client ID',
        'Account Manager',
        'From Date'
    ]].copy()
    
    output_df = output_df.drop_duplicates()
    
    output_df['Client ID'] = output_df['Client ID'].astype(int)
    
    return {
        "output_01.csv": output_df,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

