import pandas as pd
from pathlib import Path
from datetime import datetime


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_orders = pd.read_csv(inputs_dir / "input_01.csv")
    
    df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'])
    df_orders['Ship Date'] = pd.to_datetime(df_orders['Ship Date'])
    
    df_orders['Year'] = df_orders['Order Date'].dt.year
    
    first_purchase = df_orders.groupby('Customer ID')['Year'].min().reset_index()
    first_purchase.columns = ['Customer ID', 'First Purchase']
    
    customer_info = df_orders[['Customer ID', 'Customer Name']].drop_duplicates()
    
    min_year = df_orders['Year'].min()
    max_year = df_orders['Year'].max()
    
    scaffold_list = []
    for _, row in first_purchase.iterrows():
        customer_id = row['Customer ID']
        first_year = row['First Purchase']
        for year in range(first_year, max_year + 1):
            scaffold_list.append({
                'Customer ID': customer_id,
                'Year': year,
                'First Purchase': first_year
            })
    
    df_scaffold = pd.DataFrame(scaffold_list)
    
    orders_by_customer_year = df_orders.groupby(['Customer ID', 'Year']).size().reset_index(name='has_order')
    orders_by_customer_year['Order?'] = 1
    
    df_scaffold = df_scaffold.merge(
        orders_by_customer_year[['Customer ID', 'Year', 'Order?']],
        on=['Customer ID', 'Year'],
        how='left'
    )
    df_scaffold['Order?'] = df_scaffold['Order?'].fillna(0).astype(int)
    
    cohort_year_counts = df_scaffold[df_scaffold['Order?'] == 1].groupby(['First Purchase', 'Year'])['Customer ID'].nunique().reset_index()
    cohort_year_counts.columns = ['First Purchase', 'Year', 'Customer_Count']
    
    cohort_year_counts = cohort_year_counts.sort_values(['First Purchase', 'Year'])
    cohort_year_counts['Prev_Year_Count'] = cohort_year_counts.groupby('First Purchase')['Customer_Count'].shift(1)
    cohort_year_counts['YoY Difference'] = cohort_year_counts['Customer_Count'] - cohort_year_counts['Prev_Year_Count']
    
    df_scaffold = df_scaffold.merge(
        cohort_year_counts[['First Purchase', 'Year', 'YoY Difference']],
        on=['First Purchase', 'Year'],
        how='left'
    )
    
    df_scaffold = df_scaffold.sort_values(['Customer ID', 'Year'])
    df_scaffold['Prev_Year_Order'] = df_scaffold.groupby('Customer ID')['Order?'].shift(1).fillna(0).astype(int)
    
    def classify_customer(row):
        if row['Order?'] == 0:
            return 'Sleeping'
        elif row['Year'] == row['First Purchase']:
            return 'New'
        elif row['Prev_Year_Order'] == 1:
            return 'Consistent'
        else:
            return 'Returning'
    
    df_scaffold['Customer Classification'] = df_scaffold.apply(classify_customer, axis=1)
    
    df_orders_with_info = df_orders.merge(
        first_purchase,
        on='Customer ID',
        how='left'
    )
    
    scaffold_cols = df_scaffold[['Customer ID', 'Year', 'Customer Classification', 'YoY Difference', 'Order?', 'Prev_Year_Order']]
    df_orders_with_info = df_orders_with_info.merge(
        scaffold_cols,
        on=['Customer ID', 'Year'],
        how='left'
    )
    
    df_orders_with_info['Order?'] = 1
    
    df_scaffold_no_orders = df_scaffold[df_scaffold['Order?'] == 0].copy()
    df_scaffold_no_orders = df_scaffold_no_orders.merge(
        customer_info,
        on='Customer ID',
        how='left'
    )
    
    for col in df_orders.columns:
        if col not in ['Customer ID', 'Customer Name', 'Year']:
            df_scaffold_no_orders[col] = None
    
    order_cols_base = ['Customer Classification', 'YoY Difference', 'Order?', 'Year', 'First Purchase']
    order_cols_rest = [col for col in df_orders.columns if col not in ['Year']]
    order_cols = order_cols_base + order_cols_rest
    
    df_orders_with_info = df_orders_with_info[order_cols]
    df_scaffold_no_orders = df_scaffold_no_orders[order_cols]
    
    df_final = pd.concat([df_orders_with_info, df_scaffold_no_orders], ignore_index=True)
    
    df_final['Order Date'] = df_final['Order Date'].apply(
        lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else ''
    )
    df_final['Ship Date'] = df_final['Ship Date'].apply(
        lambda x: x.strftime('%d/%m/%Y') if pd.notna(x) else ''
    )
    
    df_final['Order?'] = df_final['Order?'].astype(int)
    df_final['Year'] = df_final['Year'].astype(int)
    df_final['First Purchase'] = df_final['First Purchase'].astype(int)
    
    df_final['YoY Difference'] = df_final['YoY Difference'].apply(
        lambda x: '' if pd.isna(x) else int(x)
    )
    
    df_final['Postal Code'] = df_final['Postal Code'].apply(
        lambda x: int(x) if pd.notna(x) and str(x) != '' else ''
    )
    
    def format_discount(x):
        if pd.isna(x) or x == '':
            return ''
        try:
            val = float(x)
            if val == int(val):
                return int(val)
            return val
        except:
            return x
    
    df_final['Discount'] = df_final['Discount'].apply(format_discount)
    
    output_cols = [
        'Customer Classification', 'YoY Difference', 'Order?', 'Year', 'First Purchase',
        'Row ID', 'Order ID', 'Order Date', 'Ship Date', 'Ship Mode',
        'Customer Name', 'Segment', 'Country/Region', 'City', 'State',
        'Postal Code', 'Region', 'Product ID', 'Category', 'Sub-Category',
        'Product Name', 'Sales', 'Quantity', 'Discount', 'Profit', 'Customer ID'
    ]
    
    df_final = df_final[output_cols]
    
    for col in ['Sales', 'Quantity', 'Discount', 'Profit']:
        if col in df_final.columns:
            df_final[col] = df_final[col].apply(
                lambda x: round(float(x), 4) if pd.notna(x) and x != '' else x
            )
    
    classification_order = {'New': 1, 'Sleeping': 2, 'Returning': 3, 'Consistent': 4}
    df_final['_sort_classification'] = df_final['Customer Classification'].map(classification_order)
    
    df_final = df_final.sort_values(
        ['_sort_classification', 'Year', 'First Purchase', 'Customer ID', 'Order?', 'Row ID'],
        na_position='last'
    )
    df_final = df_final.drop(columns=['_sort_classification'])
    
    return {'output_01.csv': df_final}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

