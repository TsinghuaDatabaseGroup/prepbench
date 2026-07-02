
import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    stock_levels = pd.read_csv(inputs_dir / "input_01.csv")
    store_requests = pd.read_csv(inputs_dir / "input_02.csv")

    stock_levels['Date'] = pd.to_datetime(stock_levels['Date'])
    store_requests['Date Required'] = pd.to_datetime(store_requests['Date Required'])

    supplier_mapping = stock_levels[['Product', 'Scent', 'Supplier']].drop_duplicates()
    store_requests_with_supplier = pd.merge(store_requests, supplier_mapping, on=['Product', 'Scent'], how='left')

    stock_levels = stock_levels.sort_values(by=['Product', 'Scent', 'Supplier', 'Date'])
    stock_levels['Cumulative Stock'] = stock_levels.groupby(['Product', 'Scent', 'Supplier'])['Quantity'].cumsum()

    store_requests_with_supplier = store_requests_with_supplier.sort_values(by=['Product', 'Scent', 'Supplier', 'Date Required'])
    store_requests_with_supplier['Cumulative Requested'] = store_requests_with_supplier.groupby(['Product', 'Scent', 'Supplier'])['Quantity Requested'].cumsum()


    def find_fulfillment_date(row):
        product_stock = stock_levels[
            (stock_levels['Product'] == row['Product']) &
            (stock_levels['Scent'] == row['Scent']) &
            (stock_levels['Supplier'] == row['Supplier']) &
            (stock_levels['Cumulative Stock'] >= row['Cumulative Requested'])
        ]
        if not product_stock.empty:
            first_available_date = product_stock['Date'].min()
            return max(row['Date Required'], first_available_date)
        return pd.NaT

    req = store_requests_with_supplier.copy()
    req['Date Fulfilled'] = req.apply(find_fulfillment_date, axis=1)
    req['Date Fulfilled'] = pd.to_datetime(req['Date Fulfilled'])
    req['Date Required'] = pd.to_datetime(req['Date Required'])
    req['Days Request Delayed'] = (req['Date Fulfilled'] - req['Date Required']).dt.days
    req['Days Request Delayed'] = req['Days Request Delayed'].apply(lambda x: max(0, x) if pd.notnull(x) else x)
    req['Stock Ready?'] = req['Days Request Delayed'] == 0

    output_02 = req.copy()
    output_02['Date Required'] = output_02['Date Required'].dt.strftime('%d/%m/%Y')
    output_02['Date Fulfilled'] = output_02['Date Fulfilled'].dt.strftime('%d/%m/%Y')
    output_02 = output_02[[
        'Store', 'Product', 'Scent', 'Supplier', 'Quantity Requested',
        'Date Required', 'Stock Ready?', 'Date Fulfilled', 'Days Request Delayed'
    ]]

    stock_sorted = stock_levels.sort_values(['Supplier', 'Product', 'Scent', 'Date']).copy()

    req_ps = store_requests[['Product','Scent']].drop_duplicates()
    stock_ps = stock_sorted[['Product','Scent']].drop_duplicates()
    zero_ps = pd.merge(stock_ps, req_ps, on=['Product','Scent'], how='left', indicator=True)
    zero_ps = zero_ps[zero_ps['_merge']=='left_only'][['Product','Scent']]
    zero_df = (
        stock_sorted.merge(zero_ps, on=['Product','Scent'], how='inner')
        .groupby(['Supplier','Product','Scent'], as_index=False)['Quantity']
        .sum()
        .rename(columns={'Quantity':'Surplus Product'})
    )

    req_counts_df = req.groupby(['Product','Scent']).size().reset_index(name='cnt')
    req_single = req.merge(req_counts_df, on=['Product','Scent'], how='left')
    req_single = req_single[req_single['cnt'] == 1]
    req_single = req_single[req_single['Date Fulfilled'] > req_single['Date Required']]

    records = []
    for _, r in req_single.iterrows():
        supplier, product, scent = r['Supplier'], r['Product'], r['Scent']
        fulfilled_date = r['Date Fulfilled']
        grp = stock_sorted[(stock_sorted['Supplier']==supplier)&
                           (stock_sorted['Product']==product)&
                           (stock_sorted['Scent']==scent)]
        surplus_amt = int(grp.loc[grp['Date'] > fulfilled_date, 'Quantity'].sum())
        if surplus_amt>0:
            records.append({'Supplier': supplier, 'Product': product, 'Scent': scent, 'Surplus Product': surplus_amt})

    delayed_df = pd.DataFrame(records)

    output_01 = pd.concat([zero_df, delayed_df], ignore_index=True)

    return {"output_01.csv": output_01, "output_02.csv": output_02}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
