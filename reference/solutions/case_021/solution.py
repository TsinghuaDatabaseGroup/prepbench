import pandas as pd
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP


def _cost_for_day(day_index: pd.Series) -> pd.Series:
    return pd.cut(day_index, bins=[0, 3, 7, float('inf')], labels=[100, 80, 75]).astype(int)


def _round_half_up_series(s: pd.Series, ndigits: int = 2) -> pd.Series:
    return s.apply(lambda x: float(Decimal(str(x)).quantize(Decimal('0.' + '0'*(ndigits-1) + '1'), rounding=ROUND_HALF_UP)))


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_new_patients = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    df_old_patients = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)
    df_checkup_schedule = pd.read_csv(inputs_dir / "input_03.csv")

    df_old_patients = df_old_patients.rename(columns={'Name': 'Patient Name'})

    df_new_patients['First Visit'] = pd.to_datetime(
        df_new_patients['First Visit'], format='%d/%m/%Y')
    df_old_patients['First Visit'] = pd.to_datetime(
        df_old_patients['First Visit'], format='%Y-%m-%d')

    df_all = pd.concat([df_old_patients, df_new_patients], ignore_index=True)
    df_all['Length of Stay'] = df_all['Length of Stay'].astype(int)
    df_all['Leave Date'] = df_all['First Visit'] + \
        pd.to_timedelta(df_all['Length of Stay'] - 1, unit='d')

    df_all_expanded = df_all.loc[df_all.index.repeat(
        df_all['Length of Stay'])].reset_index(drop=True)
    df_all_expanded['DayIndex'] = df_all_expanded.groupby(
        ['Patient Name', 'First Visit']).cumcount() + 1
    df_all_expanded['Date in Hospital'] = df_all_expanded['First Visit'] + \
        pd.to_timedelta(df_all_expanded['DayIndex'] - 1, unit='d')
    df_all_expanded['Cost'] = _cost_for_day(df_all_expanded['DayIndex'])
    df_initial = df_all_expanded[[
        'Patient Name', 'Date in Hospital', 'Cost']].copy()

    df_checkups = df_all[['Patient Name', 'Leave Date']].assign(key=1).merge(
        df_checkup_schedule.assign(key=1), on='key'
    ).drop('key', axis=1)
    df_checkups['Checkin Date'] = df_checkups.apply(
        lambda r: r['Leave Date'] + pd.DateOffset(months=int(r['Months After Leaving'])), axis=1
    )
    df_checkups_expanded = df_checkups.loc[df_checkups.index.repeat(
        df_checkups['Length of Stay'])].reset_index(drop=True)
    df_checkups_expanded['DayIndex'] = df_checkups_expanded.groupby(
        ['Patient Name', 'Checkin Date']).cumcount() + 1
    df_checkups_expanded['Date in Hospital'] = df_checkups_expanded['Checkin Date'] + \
        pd.to_timedelta(df_checkups_expanded['DayIndex'] - 1, unit='d')
    df_checkups_expanded['Cost'] = _cost_for_day(
        df_checkups_expanded['DayIndex'])
    df_checkup_daily = df_checkups_expanded[[
        'Patient Name', 'Date in Hospital', 'Cost']].copy()

    df_daily = pd.concat([df_initial, df_checkup_daily], ignore_index=True)

    g = df_daily.groupby('Date in Hospital', as_index=False).agg(**{
        'Total Cost per Day': ('Cost', 'sum'),
        'Number of Patients': ('Patient Name', 'nunique')
    })
    g['Avg Cost per Day'] = g['Total Cost per Day'] / g['Number of Patients']
    out1 = g[['Avg Cost per Day', 'Total Cost per Day',
              'Date in Hospital', 'Number of Patients']].copy()
    out1['Avg Cost per Day'] = out1['Avg Cost per Day'].round(2)

    p = df_daily.groupby('Patient Name', as_index=False).agg(**{
        'Total Cost per Day': ('Cost', 'sum'),
        'Days': ('Date in Hospital', 'count')
    })
    p['Avg Cost per Day'] = _round_half_up_series(
        p['Total Cost per Day'] / p['Days'], 2)
    out2 = p[['Avg Cost per Day', 'Total Cost per Day', 'Patient Name']].copy()

    return {
        'output_01.csv': out1,
        'output_02.csv': out2
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        if filename == 'output_01.csv':
            df = df.copy()
            df['Date in Hospital'] = pd.to_datetime(
                df['Date in Hospital']).dt.strftime('%d/%m/%Y')
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
