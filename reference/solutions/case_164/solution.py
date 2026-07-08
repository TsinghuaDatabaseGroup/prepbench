import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    customer_sales = df.groupby('Customer ID').agg({
        'First Name': 'first',
        'Surname': 'first',
        'Sales': 'sum'
    }).reset_index()
    customer_sales['Sales'] = customer_sales['Sales'].round(3)
    
    customer_sales = customer_sales.rename(columns={'Surname': 'Last Name'})
    
    total_sales = customer_sales['Sales'].sum()
    
    customer_sales['% of Total'] = (customer_sales['Sales'] / total_sales) * 100
    
    customer_sales = customer_sales.sort_values('% of Total', ascending=False).reset_index(drop=True)
    
    customer_sales['Running % of Total Sales'] = customer_sales['% of Total'].cumsum()
    
    customer_sales['% of Total'] = customer_sales['% of Total'].round(9)
    
    customer_sales['Running % of Total Sales'] = customer_sales['Running % of Total Sales'].round(2)
    
    target_percentage = 80.0
    
    mask = customer_sales['Running % of Total Sales'] <= target_percentage
    filtered_customers = customer_sales[mask].copy()
    
    output_01 = filtered_customers[[
        'Customer ID',
        'First Name',
        'Last Name',
        'Sales',
        '% of Total',
        'Running % of Total Sales'
    ]].copy()
    
    output_01['Customer ID'] = output_01['Customer ID'].astype(int)
    output_01['Sales'] = output_01['Sales'].astype(float)
    output_01['% of Total'] = output_01['% of Total'].astype(float)
    output_01['Running % of Total Sales'] = output_01['Running % of Total Sales'].astype(float)
    
    total_customers = len(customer_sales)
    filtered_customer_count = len(filtered_customers)
    filtered_customer_percentage = int(round((filtered_customer_count / total_customers) * 100, 0))
    
    result_text = f"{filtered_customer_percentage}% of Customers account for {int(target_percentage)}% of Sales"
    output_02 = pd.DataFrame({
        'Result': [result_text]
    })
    
    return {
        'output_01.csv': output_01,
        'output_02.csv': output_02
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        if filename == 'output_01.csv':
            with open(cand_dir / filename, 'w', encoding='utf-8') as f:
                f.write(','.join(df.columns) + '\n')
                for idx, row in df.iterrows():
                    values = []
                    for col in df.columns:
                        val = row[col]
                        if col == 'Customer ID':
                            values.append(str(int(val)))
                        elif col == '% of Total':
                            values.append(f'{val:.9f}')
                        elif col == 'Running % of Total Sales':
                            values.append(f'{val:.2f}')
                        elif col == 'Sales':
                            values.append(str(val))
                        else:
                            values.append(str(val))
                    f.write(','.join(values) + '\n')
        else:
            df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
