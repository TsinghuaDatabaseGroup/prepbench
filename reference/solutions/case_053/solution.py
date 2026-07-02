
import pandas as pd
from pathlib import Path
import platform

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    current_employees = pd.read_csv(inputs_dir / "input_01.csv")
    past_employees = pd.read_csv(inputs_dir / "input_02.csv")
    reporting_dates = pd.read_csv(inputs_dir / "input_03.csv")

    current_employees['Leave Date'] = pd.to_datetime('2020-03-01')
    all_employees = pd.concat([current_employees, past_employees], ignore_index=True)
    all_employees['Salary'] = all_employees['Salary'].astype(str).str.replace('[£,]', '', regex=True).astype(float).astype(int)
    all_employees['Join Date'] = pd.to_datetime(all_employees['Join Date'], format='%m/%d/%Y')
    all_employees['Leave Date'] = pd.to_datetime(all_employees['Leave Date'])

    reporting_dates['MonthStart'] = pd.to_datetime(reporting_dates['Month'], format='%b-%Y')
    reporting_dates['MonthEnd'] = reporting_dates['MonthStart'] + pd.offsets.MonthEnd(1)

    merged_df = all_employees.assign(key=1).merge(reporting_dates.assign(key=1), on='key').drop('key', axis=1)
    
    active_employees = merged_df[
        (merged_df['Join Date'] <= merged_df['MonthEnd']) &
        (merged_df['Leave Date'] > merged_df['MonthEnd'])
    ]

    result = active_employees.groupby('MonthStart').agg(
        Total_Monthly_Salary=('Salary', 'sum'),
        Current_Employees=('Employee ID', 'count')
    ).reset_index()

    result['Avg_Salary_per_Current_Employee'] = result['Total_Monthly_Salary'] / result['Current_Employees']

    result.rename(columns={
        'MonthStart': 'Month',
        'Total_Monthly_Salary': 'Total Monthly Salary',
        'Current_Employees': 'Current Employees',
        'Avg_Salary_per_Current_Employee': 'Avg Salary per Current Employee'
    }, inplace=True)

    date_format = '%-m/%-d/%Y' if platform.system() != 'Windows' else '%#m/%#d/%Y'
    result['Month'] = result['Month'].dt.strftime(date_format)

    result['Avg Salary per Current Employee'] = result['Avg Salary per Current Employee'].round(9)

    final_df = result[['Total Monthly Salary', 'Month', 'Current Employees', 'Avg Salary per Current Employee']]

    return {"output_01.csv": final_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    if not cand_dir.exists():
        cand_dir.mkdir()

    outputs = solve(inputs_dir)

    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, sep=',', encoding='utf-8')
