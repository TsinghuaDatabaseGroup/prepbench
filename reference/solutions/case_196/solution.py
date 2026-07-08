import pandas as pd
from pathlib import Path
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    input_file = inputs_dir / "input_01.csv"

    with open(input_file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        year_match = re.search(r'(\d{4})', first_line)
        year = year_match.group(1)

    month_row = pd.read_csv(input_file, skiprows=2, nrows=1, header=None)
    months = []
    for col_idx in range(1, len(month_row.columns)):
        month_val = month_row.iloc[0, col_idx]
        if pd.notna(month_val):
            months.append(str(month_val).strip())

    df = pd.read_csv(input_file, skiprows=3, header=0)

    stores = df.iloc[:, 0].tolist()

    results = []

    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
        'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
        'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    for store_idx, store in enumerate(stores):
        for month_idx, month in enumerate(months):
            sales_col = 1 + month_idx * 2
            profit_col = 2 + month_idx * 2

            sales = df.iloc[store_idx, sales_col]
            profit = df.iloc[store_idx, profit_col]

            month_num = month_map[month]
            date_str = f"01/{month_num}/{year}"

            results.append({
                'Store': store,
                'Date': date_str,
                'Sales': sales,
                'Profit': profit
            })

    output_df = pd.DataFrame(results)

    output_df['Store'] = output_df['Store'].astype(str)
    output_df['Date'] = output_df['Date'].astype(str)
    output_df['Sales'] = pd.to_numeric(
        output_df['Sales'], errors='coerce').astype(int)
    output_df['Profit'] = pd.to_numeric(
        output_df['Profit'], errors='coerce').astype(int)

    return {
        "output_01.csv": output_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
