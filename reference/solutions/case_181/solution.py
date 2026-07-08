import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    week27_sales = pd.read_csv(inputs_dir / "input_01.csv")
    store_lookup = pd.read_csv(inputs_dir / "input_02.csv")
    east_sales_people = pd.read_csv(inputs_dir / "input_03.csv")
    west_sales_people = pd.read_csv(inputs_dir / "input_04.csv")
    
    east_sales_people['Region'] = 'East'
    west_sales_people['Region'] = 'West'
    
    sales_people = pd.concat([east_sales_people, west_sales_people], ignore_index=True)
    
    sales_people.rename(columns={'Store': 'StoreID'}, inplace=True)
    
    sales_people = sales_people.merge(store_lookup, on='StoreID', how='left')
    
    sales_people = sales_people.drop(columns=['Region_x'])
    sales_people.rename(columns={'Region_y': 'Region'}, inplace=True)
    
    store_totals = week27_sales.groupby('Store Name')['Sale Value'].sum().reset_index()
    store_totals.rename(columns={'Sale Value': 'Store Total Sales'}, inplace=True)
    
    result = sales_people.merge(store_totals, on='Store Name', how='left')
    
    result['Sales per Person'] = (result['Percent of Store Sales'] / 100) * result['Store Total Sales']
    
    result['Sale Value'] = result['Store Total Sales']
    
    output = result[['Sales per Person', 'Region', 'Store Name', 'Sales Person', 'Percent of Store Sales', 'Sale Value']].copy()
    
    output['Sales per Person'] = output['Sales per Person'].round(4)
    output['Percent of Store Sales'] = output['Percent of Store Sales'].astype(int)
    output['Sale Value'] = output['Sale Value'].round(2)
    
    return {'output_01.csv': output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    cand_dir.mkdir(exist_ok=True)
    
    results = solve(inputs_dir)
    
    for filename, df in results.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved {filename}")

