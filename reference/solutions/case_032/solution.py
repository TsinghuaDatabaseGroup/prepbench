import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_df = pd.read_csv(inputs_dir / "input_01.csv")

    df1 = input_df[['Customer', 'Address', 'Product 1', 'Sales']].copy()
    df1.rename(columns={'Product 1': 'Product', 'Sales': 'Sales'}, inplace=True)

    df2 = input_df[['Customer', 'Address', 'Product 2', 'Sales.1']].copy()
    df2.rename(columns={'Product 2': 'Product', 'Sales.1': 'Sales'}, inplace=True)

    df_unpivoted = pd.concat([df1, df2], ignore_index=True)
    
    df_unpivoted.dropna(subset=['Product'], inplace=True)

    df_unpivoted['Product'] = df_unpivoted['Product'].str.replace('-', ' ', regex=False)

    address_parts = df_unpivoted['Address'].str.split(', ', expand=True)
    address_parts.columns = ['Property Info', 'Town', 'Postal Code', 'Country']

    address_parts['Property Number'] = address_parts['Property Info'].str.extract(r'(\d+)').astype(int)

    df_processed = pd.concat([address_parts, df_unpivoted], axis=1)

    output_columns = [
        'Property Number',
        'Town',
        'Postal Code',
        'Country',
        'Customer',
        'Product',
        'Sales'
    ]
    output_df = df_processed[output_columns]

    output_df['Sales'] = output_df['Sales'].astype(int)

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

