import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    sales = pd.read_csv(inputs_dir / "input_01.csv")
    targets = pd.read_csv(inputs_dir / "input_02.csv")
    actions_df = pd.read_csv(inputs_dir / "input_03.csv")

    sales = sales[sales['Store'] != 'Total']
    sales_long = sales.melt(id_vars='Store', var_name='Month_Year', value_name='Sales')
    sales_long['Month'] = sales_long['Month_Year'].str.extract(r'Month (\d+)').astype(int)
    sales_long['Quarter'] = (sales_long['Month'] - 1) // 3 + 1
    quarterly_sales = sales_long.groupby(['Store', 'Quarter'])['Sales'].sum().reset_index()

    targets_long = targets.melt(id_vars=['Location', 'Region'], var_name='Quarter', value_name='Target Value')
    targets_long['Quarter'] = targets_long['Quarter'].str.replace('Q', '').astype(int)
    targets_long.rename(columns={'Location': 'Store'}, inplace=True)

    df = pd.merge(quarterly_sales, targets_long, on=['Store', 'Quarter'])

    df['Variance to Target'] = df['Sales'] - df['Target Value']
    df['Variance to Target %'] = ((df['Sales'] / df['Target Value']) * 100).astype(int)

    def assign_action(var_pct):
        if var_pct > 150:
            return 'Smashing it. Share with all other stores what you are doing. Can you mentor the underachieving stores?', 'Above'
        elif var_pct > 125:
            return 'Brilliant work. Share ideas with other stores. Are you ready for next year?', 'Above'
        elif var_pct > 100:
            return 'Doing well. Try to share ideas with other stores but try to learn from others to stay ahead', 'Above'
        elif var_pct == 100:
            return 'Nice work. Thank you for your hard work. What can you do to exceed you target? Talk to 3 high performing stores', 'Meets'
        elif var_pct >= 75:
            return 'Close but not quite there. Please create an assessment on blockers to hitting your target and learn from those that did.', 'Below'
        elif var_pct >= 50:
            return 'This might have been poor targetting by Head Office. Please create an assessment on blockers as we will be in touch.', 'Below'
        else:
            return 'What went wrong? Create a detailed assessment on the blockers and we will schedule time to discuss in early January', 'Below'

    df[['Actions', 'Target']] = df['Variance to Target %'].apply(lambda x: pd.Series(assign_action(x)))
    
    df['Variance to Target %'] = df['Variance to Target %']

    output_df = df[[
        'Variance to Target',
        'Variance to Target %',
        'Target Value',
        'Sales',
        'Store',
        'Quarter',
        'Region',
        'Target',
        'Actions'
    ]]

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    
    cand_dir = task_dir / "cand"
    if not cand_dir.exists():
        cand_dir.mkdir()

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
