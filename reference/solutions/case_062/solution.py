import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df1 = pd.read_csv(inputs_dir / "input_01.csv")
    df2 = pd.read_csv(inputs_dir / "input_02.csv")
    
    df1['Store'] = 'Lewisham'
    df2['Store'] = 'Camden'
    
    df_sales = pd.concat([df1, df2], ignore_index=True)
    
    sales_cols = [col for col in df_sales.columns if col.startswith('Sales ')]
    profit_cols = [col for col in df_sales.columns if col.startswith('Profit ')]
    
    def extract_date(col_name):
        return col_name.split(' ', 1)[1]
    
    result_rows = []
    
    for idx, row in df_sales.iterrows():
        store = row['Store']
        category = row['Category']
        scent = row['Scent']
        
        for sales_col, profit_col in zip(sales_cols, profit_cols):
            date_str = extract_date(sales_col)
            sales = row[sales_col]
            profit = row[profit_col]
            
            result_rows.append({
                'Store': store,
                'Category': category,
                'Scent': scent,
                'Date': date_str,
                'Sales': sales,
                'Profit': profit
            })
    
    df_result = pd.DataFrame(result_rows)
    
    df_staff = pd.read_csv(inputs_dir / "input_03.csv")
    
    df_staff['Month'] = pd.to_datetime(df_staff['Month'])
    df_staff['Date'] = df_staff['Month'].dt.strftime('%d/%m/%Y')
    
    staff_rows = []
    for idx, row in df_staff.iterrows():
        date_str = row['Date']
        for store in ['Lewisham', 'Camden', 'Dulwich']:
            if store in df_staff.columns:
                staff_rows.append({
                    'Store': store,
                    'Date': date_str,
                    'Staff days worked': row[store]
                })
    
    df_staff_long = pd.DataFrame(staff_rows)
    
    df_final = df_result.merge(
        df_staff_long,
        on=['Store', 'Date'],
        how='left'
    )
    
    df_final = df_final[[
        'Store',
        'Category',
        'Scent',
        'Date',
        'Sales',
        'Profit',
        'Staff days worked'
    ]]
    
    scent_order = {'Mint': 0, 'Lemon': 1, 'Raspberry': 2}
    df_final['_scent_order'] = df_final['Scent'].map(scent_order)
    df_final = df_final.sort_values(
        by=['Store', 'Category', '_scent_order', 'Date']
    ).drop(columns=['_scent_order']).reset_index(drop=True)
    
    return {
        'output_01.csv': df_final
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(
            cand_dir / filename,
            index=False,
            encoding='utf-8'
        )

