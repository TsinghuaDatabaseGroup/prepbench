import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    df['Lesson Name'] = df['Lesson Name'].replace('', pd.NA)
    df['Subject'] = df['Subject'].replace('', pd.NA)
    
    df = df.sort_values(['Weekday', 'Lesson Time', 'Teacher', 'Week'])
    
    group_cols = ['Weekday', 'Lesson Time', 'Teacher']
    df['Lesson Name'] = df.groupby(group_cols)['Lesson Name'].ffill().bfill()
    df['Subject'] = df.groupby(group_cols)['Subject'].ffill().bfill()
    
    avg_attendance = df.groupby(['Weekday', 'Subject', 'Lesson Name'])['Attendance'].mean().reset_index()
    avg_attendance.columns = ['Weekday', 'Subject', 'Lesson Name', 'Avg. Attendance per Subject & Lesson']
    
    df = df.merge(avg_attendance, on=['Weekday', 'Subject', 'Lesson Name'], how='left')
    
    df['Time'] = df['Lesson Time'].apply(lambda x: f"{x}:00" if len(x) == 5 else x)
    
    output_df = df[[
        'Weekday',
        'Time',
        'Week',
        'Teacher',
        'Subject',
        'Lesson Name',
        'Attendance',
        'Avg. Attendance per Subject & Lesson'
    ]].copy()
    
    output_df['Week'] = output_df['Week'].astype(int)
    output_df['Attendance'] = output_df['Attendance'].astype(int)
    output_df['Avg. Attendance per Subject & Lesson'] = output_df['Avg. Attendance per Subject & Lesson'].astype(float)
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    output_df['Weekday'] = pd.Categorical(output_df['Weekday'], categories=weekday_order, ordered=True)
    output_df = output_df.sort_values(['Weekday', 'Time', 'Week']).reset_index(drop=True)
    output_df['Weekday'] = output_df['Weekday'].astype(str)
    
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

