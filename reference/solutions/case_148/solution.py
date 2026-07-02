
import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv", parse_dates=['Date'], dayfirst=True)
    df['Reporting Year'] = df['Date'].dt.year

    df['Date_str'] = df['Date'].dt.strftime('%b %Y')
    employment_range = df.groupby('Name')['Date'].agg(['min', 'max']).reset_index()
    employment_range['Employment Range'] = \
        employment_range['min'].dt.strftime('%b %Y') + ' to ' + employment_range['max'].dt.strftime('%b %Y')
    df = pd.merge(df, employment_range[['Name', 'Employment Range']], on='Name')

    yearly_summary = df.groupby(['Name', 'Reporting Year', 'Employment Range']).agg(
        months_worked=('Date', 'count'),
        annual_salary=('Annual Salary', 'first'),
        total_sales=('Sales', 'sum')
    ).reset_index()

    yearly_summary['Salary Paid'] = round((yearly_summary['annual_salary'] / 12) * yearly_summary['months_worked'], 2)
    yearly_summary['Yearly Bonus'] = round(yearly_summary['total_sales'] * 0.05, 2)
    yearly_summary['Total Paid'] = yearly_summary['Salary Paid'] + yearly_summary['Yearly Bonus']

    yearly_summary = yearly_summary.sort_values(by=['Name', 'Reporting Year'])
    yearly_summary['Tenure by End of Reporting Year'] = yearly_summary.groupby('Name')['months_worked'].cumsum()

    output_df = yearly_summary[[
        'Name',
        'Employment Range',
        'Reporting Year',
        'Tenure by End of Reporting Year',
        'Salary Paid',
        'Yearly Bonus',
        'Total Paid'
    ]]

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    solutions = solve(inputs_dir)

    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

    print(f"Solution script finished. Output generated in {cand_dir}")

