import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / 'input_01.csv')

    df_filtered = df[df['Status'] != 'Return to Manufacturer'].copy()

    df_filtered = df_filtered.drop(columns=['Status', 'Date'])

    total_items_per_store = df_filtered.groupby('Store')['Number of Items'].sum().reset_index()
    total_items_per_store.rename(columns={'Number of Items': 'Items sold per store'}, inplace=True)

    pivot_df = df_filtered.pivot_table(
        index='Store',
        columns='Item',
        values='Number of Items',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    output_df = pd.merge(pivot_df, total_items_per_store, on='Store')

    output_df = output_df[['Items sold per store', 'Wheels', 'Tyres', 'Saddles', 'Brakes', 'Store']]
    
    return {
        'output_01.csv': output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)
    
    outputs = solve(inputs_dir)
    
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

