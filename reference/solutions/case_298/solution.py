
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df['Category'] = df['Category'].str.strip()

    df['Sales'] = df['Price'] * df['Quantity']

    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    category_sales.rename(columns={'Sales': 'Category Total Sales'}, inplace=True)
    df = pd.merge(df, category_sales, on='Category')

    df['% of Total'] = (df['Sales'] / df['Category Total Sales'])

    df = df.sort_values(by=['Category', 'Sales'], ascending=[True, True]).reset_index(drop=True)

    df['Cumulative %'] = df.groupby('Category')['% of Total'].cumsum()

    worst_sellers = df[df['Cumulative %'] <= 0.15].copy()

    output_df = worst_sellers[[
        'Category', 'Product', 'Product ID', 'Price', 'Sales', '% of Total']].copy()

    output_df['% of Total'] = output_df['% of Total'].round(2)

    output_df = output_df.sort_values(by=['Category', 'Sales'], ascending=[True, True]).reset_index(drop=True)

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

    print(f"Generated {len(solutions)} files in {cand_dir}")
