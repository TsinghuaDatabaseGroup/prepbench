import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    def merge_dates(row):
        date_value = None
        if pd.notna(row['Date of Order']) and str(row['Date of Order']).strip() != '':
            date_value = str(row['Date of Order']).strip()
        elif pd.notna(row['Purchase Date']) and str(row['Purchase Date']).strip() != '':
            date_value = str(row['Purchase Date']).strip()
        elif pd.notna(row['Order Date']) and str(row['Order Date']).strip() != '':
            date_value = str(row['Order Date']).strip()
        
        if date_value:
            try:
                date_obj = datetime.strptime(date_value, "%a %d %b %Y")
                return date_obj.strftime("%d/%m/%Y")
            except:
                try:
                    datetime.strptime(date_value, "%d/%m/%Y")
                    return date_value
                except:
                    return date_value
        return ''
    
    df['Order Date'] = df.apply(merge_dates, axis=1)
    
    def create_order_id(customer, order_number):
        parts = customer.split()
        if len(parts) >= 2:
            initials = parts[0][0] + parts[-1][0]
        elif len(parts) == 1:
            initials = parts[0][0] + parts[0][1] if len(parts[0]) > 1 else parts[0][0] + 'X'
        else:
            initials = 'XX'
        
        order_str = str(int(order_number))
        order_str_padded = order_str.zfill(6)
        order_id = initials + order_str_padded
        
        return order_id
    
    df['Order ID'] = df.apply(lambda row: create_order_id(row['Customer'], row['Order Number']), axis=1)
    
    output_df = df[['Order ID', 'Order Number', 'Customer', 'Order Date']].copy()
    
    output_df['Order Number'] = output_df['Order Number'].astype(int)
    
    return {
        'output_01.csv': output_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

