import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['scheduled_date_parsed'] = pd.to_datetime(df['scheduled_date'], format='%m/%d/%Y')
    
    earliest_date = df['scheduled_date_parsed'].min()
    latest_date = df['scheduled_date_parsed'].max()
    
    start_date = datetime(earliest_date.year, 1, 1)
    end_date = datetime(latest_date.year, 12, 31)
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    calendar_df = pd.DataFrame({'scheduled_date_parsed': date_range})
    
    df['full_name'] = df['first_name'] + ' ' + df['last_name']
    
    employees_df = df[['emp_id', 'first_name', 'last_name', 'full_name']].drop_duplicates()
    
    calendar_df['key'] = 1
    employees_df['key'] = 1
    employee_calendar = calendar_df.merge(employees_df, on='key', how='outer').drop('key', axis=1)
    
    employee_calendar['scheduled_date'] = employee_calendar['scheduled_date_parsed'].dt.strftime('%-m/%-d/%Y')
    employee_calendar['scheduled_date'] = employee_calendar['scheduled_date_parsed'].apply(
        lambda x: f"{x.month}/{x.day}/{x.year}"
    )
    
    df_scheduled = df[['emp_id', 'scheduled_date_parsed']].copy()
    df_scheduled['scheduled'] = True
    df_scheduled = df_scheduled.drop_duplicates(subset=['emp_id', 'scheduled_date_parsed'])
    
    result = employee_calendar.merge(
        df_scheduled[['emp_id', 'scheduled_date_parsed', 'scheduled']],
        on=['emp_id', 'scheduled_date_parsed'],
        how='left'
    )
    
    result['scheduled'] = result['scheduled'].fillna(False)
    
    output = result[[
        'scheduled_date',
        'emp_id',
        'full_name',
        'first_name',
        'last_name',
        'scheduled'
    ]].copy()
    
    output['emp_id'] = output['emp_id'].astype(int)
    output['scheduled'] = output['scheduled'].astype(bool)
    
    output = output.sort_values(['scheduled_date', 'emp_id']).reset_index(drop=True)
    
    return {
        'output_01.csv': output
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

