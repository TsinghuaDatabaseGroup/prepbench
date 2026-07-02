from __future__ import annotations

from pathlib import Path
import pandas as pd
import re

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv", header=None, names=['c0', 'data_str', 'c2', 'c3'])
    
    df = df[df['data_str'].str.contains("Work Experience:", na=False)].copy()

    pattern = re.compile(
        r"Application Date: (?P<month>.*?), "
        r"Work Experience: (?P<work_exp>.*?), "
        r"Supervised: (?P<supervised>.*?), "
        r"Industry Experience: (?P<industry_exp>.*?) "
        r"\((?P<count>\d+)\)"
    )

    parsed_data = df['data_str'].str.extract(pattern)
    df = pd.concat([df.reset_index(drop=True), parsed_data], axis=1)

    df['count'] = pd.to_numeric(df['count'])

    df['Application Month'] = pd.to_datetime(df['month'], format='%B %Y') + pd.offsets.MonthEnd(1)

    def get_lower_bound(s: str) -> int:
        s = str(s).strip()
        if 'years' in s:
            s = s.replace(' years', '')
        if s == 'None':
            return 0
        if s.endswith('+'):
            try:
                return int(s[:-1])
            except (ValueError, IndexError):
                return 0
        if '-' in s:
            try:
                return int(s.split('-')[0])
            except (ValueError, IndexError):
                return 0
        try:
            return int(s)
        except (ValueError, IndexError):
            return 0

    df['work_exp_lower'] = df['work_exp'].apply(get_lower_bound)
    df['supervised_lower'] = df['supervised'].apply(get_lower_bound)

    preferred_work_exp = df['work_exp_lower'] >= 4
    preferred_supervised = df['supervised_lower'] > 10
    preferred_industry_exp = df['industry_exp'] == 'Yes'

    df['is_preferred'] = preferred_work_exp & preferred_supervised & preferred_industry_exp

    monthly_summary = df.groupby('Application Month').agg(
        total_candidates=('count', 'sum'),
        preferred_categories=('is_preferred', 'sum')
    ).reset_index()

    monthly_summary['pct_of_candidates'] = (
        (monthly_summary['preferred_categories'] / monthly_summary['total_candidates'] * 100).round(1)
    )

    final_df = monthly_summary.rename(columns={
        'Application Month': 'Application Month',
        'total_candidates': 'Total Candidates',
        'preferred_categories': 'Candidates with Preferred Qualifications',
        'pct_of_candidates': '% of Candidates'
    })
    
    final_df['Application Month'] = final_df['Application Month'].dt.strftime('%d/%m/%Y')

    return {"output_01.csv": final_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")