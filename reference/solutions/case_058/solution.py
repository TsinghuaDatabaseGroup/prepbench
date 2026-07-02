import pandas as pd
from pathlib import Path
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    total_sales = pd.read_csv(inputs_dir / 'input_01.csv')
    percentages = pd.read_csv(inputs_dir / 'input_02.csv')
    lookup = pd.read_csv(inputs_dir / 'input_03.csv')

    lookup['Size'] = lookup['Product'].str.extract(r'(50g|100g|250ml|0\.5l)$')[0]
    lookup['Product_ID'] = lookup['Product'].str.replace(r'(50g|100g|250ml|0\.5l)$', '', regex=True)
    lookup = lookup[['Scent', 'Product_ID', 'Size']]

    percentages = percentages[percentages['Percentage of Sales'] > 0]
    percentages['Week Commencing'] = pd.to_datetime(percentages['Week Commencing'])
    percentages['Year_Week'] = percentages['Week Commencing'].apply(
        lambda x: int(f"{x.isocalendar().year}{x.isocalendar().week:02d}")
    )
    percentages = percentages.rename(columns={'Product ID': 'Product_ID', 'Percentage of Sales': 'Percentage'})
    percentages['Product_ID'] = percentages['Product_ID'].astype(str)

    scent_mapping = {
        'CO    CO       NUT   ': 'Coconut',
        'HON      EY    ': 'Honey',
        'LAV     END     AR    ': 'Lavendar',
        'LE     MON     GR     ASS    ': 'Lemongrass',
        'MI    NT': 'Mint',
        'OR  ANGE    ': 'Orange',
        'TEA     TREE     ': 'Tea Tree',
        'VAN       ILL     A   ': 'Vanilla'
    }
    total_sales['Scent'] = total_sales['Scent'].map(scent_mapping)
    total_sales = total_sales.rename(columns={'Total Scent Sales': 'Total_Sales'})
    total_sales['Year_Week'] = total_sales['Year Week Number']
    
    df = pd.merge(total_sales, lookup, on='Scent', how='left')
    
    df = pd.merge(df, percentages, on=['Product_ID', 'Year_Week', 'Size'], how='left')
    
    df = df.dropna(subset=['Percentage'])
    
    df['Sales'] = df['Total_Sales'] * df['Percentage']

    output_df = df[['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales']]
    output_df = output_df.rename(columns={'Scent': 'Secnt'})
    
    output_df['Year Week Number'] = output_df['Year Week Number'].astype(int)
    output_df['Sales'] = output_df['Sales'].astype(float)
    
    output_df['Sales'] = output_df['Sales'].apply(lambda x: round(float(x), 2))
    
    output_df = output_df.drop_duplicates()
    
    scent_order = ['Coconut', 'Honey', 'Lavendar', 'Lemongrass', 'Mint', 'Orange', 'Tea Tree', 'Vanilla']
    size_order = ['50g', '250ml', '100g', '0.5l']
    
    output_df['Secnt'] = pd.Categorical(output_df['Secnt'], categories=scent_order, ordered=True)
    output_df['Size'] = pd.Categorical(output_df['Size'], categories=size_order, ordered=True)
    
    output_df = output_df.sort_values(['Year Week Number', 'Secnt', 'Size'])
    
    output_df['Secnt'] = output_df['Secnt'].astype(str)
    output_df['Size'] = output_df['Size'].astype(str)
    
    output_df = output_df.reset_index(drop=True)

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    if not cand_dir.exists():
        cand_dir.mkdir()

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
