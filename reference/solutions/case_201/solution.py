from __future__ import annotations

from pathlib import Path
import pandas as pd

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    df['ts'] = pd.to_datetime(df['ts'], format='%d/%m/%Y %H:%M:%S')

    df['rank'] = df.groupby(['candidate_id', 'position_id'])['ts'].rank(method='first', ascending=False)

    latest_status = df[df['rank'] == 1].copy()
    withdrew = latest_status[latest_status['status'] == 'Candidate Withdrew'].copy()
    withdrew = withdrew[['candidate_id', 'position_id']]

    status_before = df[df['rank'] == 2].copy()

    withdrew_details = pd.merge(withdrew, status_before, on=['candidate_id', 'position_id'], how='inner')

    withdrawals_count = withdrew_details.groupby('status').size().reset_index(name='withdrawals')
    withdrawals_count = withdrawals_count.rename(columns={'status': 'status_before_withdrawal'})

    total_in_status = df[['status', 'candidate_id', 'position_id']].drop_duplicates()
    total_in_status = total_in_status.groupby('status').size().reset_index(name='total_in_status')
    total_in_status = total_in_status.rename(columns={'status': 'status_before_withdrawal'})

    result_df = pd.merge(total_in_status, withdrawals_count, on='status_before_withdrawal', how='left')
    result_df['withdrawals'] = result_df['withdrawals'].fillna(0).astype(int)

    result_df['pct_withdrawn'] = (result_df['withdrawals'] / result_df['total_in_status'] * 100).round(1)

    final_df = result_df[['status_before_withdrawal', 'withdrawals', 'total_in_status', 'pct_withdrawn']]

    final_df = final_df.sort_values(by='status_before_withdrawal').reset_index(drop=True)

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

