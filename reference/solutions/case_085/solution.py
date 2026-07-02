import pandas as pd
from pathlib import Path
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    orders_df = pd.read_csv(inputs_dir / "input_01.csv")
    prices_df = pd.read_csv(inputs_dir / "input_02.csv")

    price_dict = {}
    for i in range(0, len(prices_df.columns), 2):
        item_col, price_col = prices_df.columns[i], prices_df.columns[i+1]
        cat_dict = prices_df[[item_col, price_col]].dropna().set_index(item_col)[price_col].to_dict()
        price_dict.update(cat_dict)

    if 'English Breakfast' in price_dict:
        price_dict['English Breakfast Tea'] = price_dict.pop('English Breakfast')

    orders_melted = orders_df.melt(id_vars='Person', value_name='OrderString').dropna()
    orders_melted['Person'] = orders_melted['Person'].str.strip()

    weekly_spend_list = []
    sorted_price_items = sorted(price_dict.items(), key=lambda x: len(x[0]), reverse=True)

    for person, group in orders_melted.groupby('Person'):
        week_orders_str = ' , '.join(group['OrderString'])
        
        total_spend = 0
        temp_orders_str = week_orders_str.lower()

        for item, price in sorted_price_items:
            item_lower = item.lower()
            count = temp_orders_str.count(item_lower)
            if count > 0:
                total_spend += count * price
                temp_orders_str = temp_orders_str.replace(item_lower, '')

        weekly_spend_list.append({'Person': person, 'WeeklySpend': total_spend})

    spend_df = pd.DataFrame(weekly_spend_list)
    spend_df['Monthly Spend'] = spend_df['WeeklySpend'] * 4
    spend_df['Potential Savings'] = spend_df['Monthly Spend'] - 20
    spend_df['Worthwhile?'] = spend_df['Potential Savings'] > 0

    output_df = spend_df[['Person', 'Monthly Spend', 'Potential Savings', 'Worthwhile?']].copy()
    output_df['Monthly Spend'] = output_df['Monthly Spend'].round(2)
    output_df['Potential Savings'] = output_df['Potential Savings'].round(2)

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
