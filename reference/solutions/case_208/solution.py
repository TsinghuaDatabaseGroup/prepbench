from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv)

    df['Bank'] = df['Transaction Code'].str.split(
        '-', n=1, expand=True)[0].str.strip()

    df['Transaction Date'] = pd.to_datetime(
        df['Transaction Date'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df['Transaction Date'] = df['Transaction Date'].dt.strftime(
        '%B')

    aggregated = df.groupby(['Transaction Date', 'Bank'], as_index=False)[
        'Value'].sum()

    aggregated['Bank Rank per Month'] = aggregated.groupby(
        'Transaction Date')['Value'].rank(method='min', ascending=False).astype(int)

    avg_rank_per_bank = aggregated.groupby(
        'Bank')['Bank Rank per Month'].mean().reset_index()
    avg_rank_per_bank.columns = ['Bank', 'Avg Rank per Bank']
    avg_rank_per_bank['Avg Rank per Bank'] = avg_rank_per_bank['Avg Rank per Bank'].round(
        9)
    aggregated = aggregated.merge(avg_rank_per_bank, on='Bank', how='left')

    avg_value_per_rank = aggregated.groupby('Bank Rank per Month')[
        'Value'].mean().reset_index()
    avg_value_per_rank.columns = [
        'Bank Rank per Month', 'Avg Transaction Value per Rank']
    avg_value_per_rank['Avg Transaction Value per Rank'] = avg_value_per_rank['Avg Transaction Value per Rank'].round(
        9)
    aggregated = aggregated.merge(
        avg_value_per_rank, on='Bank Rank per Month', how='left')

    output = aggregated[[
        'Transaction Date',
        'Bank',
        'Value',
        'Bank Rank per Month',
        'Avg Transaction Value per Rank',
        'Avg Rank per Bank'
    ]].copy()

    output['Avg Transaction Value per Rank'] = output['Avg Transaction Value per Rank'].round(
        9)
    output['Avg Rank per Bank'] = output['Avg Rank per Bank'].round(9)

    output = output.sort_values(
        ['Transaction Date', 'Bank Rank per Month']).reset_index(drop=True)

    return {
        "output_01.csv": output,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
