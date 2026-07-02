from __future__ import annotations
from pathlib import Path
import pandas as pd
import re
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    weekday_to_offset = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }

    base_weeks = {
        'input_01.csv': datetime(2019, 6, 17),
        'input_02.csv': datetime(2019, 6, 24),
    }

    def infer_date(weekday_str: str, base: datetime) -> str:
        off = weekday_to_offset[weekday_str.strip().lower()]
        d = base + timedelta(days=off)
        return d.strftime('%d/%m/%Y')

    def extract_policy(text: str) -> int | None:
        m = re.search(r"#(\d+)", str(text))
        return int(m.group(1)) if m else None

    def flag_statement(text: str) -> int:
        return int('statement' in str(text).lower())

    def flag_balance(text: str) -> int:
        t = str(text).lower()
        return 1 if 'balance' in t else 0

    def flag_complaint(text: str) -> int:
        t = str(text).lower()
        return 1 if 'complain' in t else 0

    records: list[dict] = []

    for fname in ['input_01.csv', 'input_02.csv']:
        fpath = inputs_dir / fname
        base = base_weeks[fname]
        df = pd.read_csv(fpath)
        for _, row in df.iterrows():
            policy = extract_policy(row["Notes"])
            if policy is None:
                continue
            true_date = infer_date(row["Date"], base)
            notes = row["Notes"]
            records.append({
                'Statement?': int(flag_statement(notes)),
                'True Date': true_date,
                'Balance?': int(flag_balance(notes)),
                'Complaint?': int(flag_complaint(notes)),
                'Policy Number': int(policy),
                'Customer ID': int(row.get('Customer ID')),
            })

    out_df = pd.DataFrame.from_records(records, columns=[
        'Statement?', 'True Date', 'Balance?', 'Complaint?', 'Policy Number', 'Customer ID'])

    out = {
        'output_01.csv': out_df
    }
    return out


if __name__ == "__main__":
    import json
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / 'inputs'
    cand_dir = task_dir / 'cand'
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding='utf-8')
