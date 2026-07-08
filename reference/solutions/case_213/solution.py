from __future__ import annotations
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv)

    df['Balance Date'] = pd.to_datetime(df['Balance Date'], format='%d/%m/%Y')

    df['Transaction Value'] = pd.to_numeric(
        df['Transaction Value'], errors='coerce')

    df['Transaction Order'] = df.groupby('Account Number')['Balance Date'].rank(
        method='first', ascending=True).astype(int)

    total_tx_value = df.groupby(['Account Number', 'Balance Date'])[
        'Transaction Value'].sum().reset_index()
    total_tx_value.rename(
        columns={'Transaction Value': 'Total Transaction Value'}, inplace=True)

    df = df.merge(total_tx_value, on=[
                  'Account Number', 'Balance Date'], how='left')


    df_sorted = df.sort_values(['Account Number', 'Balance Date']).copy()
    df_sorted['Prev Balance'] = df_sorted.groupby('Account Number')[
        'Balance'].shift(1)
    daily_max_date = df_sorted.groupby(['Account Number', 'Balance Date'])[
        'Balance Date'].transform('max')
    df_sorted['Date Rank'] = df_sorted.groupby(
        'Account Number')['Balance Date'].rank(method='dense')
    prev_date_balance = df_sorted.groupby(['Account Number', 'Date Rank'])[
        'Balance'].last().reset_index()
    prev_date_balance['Next Date Rank'] = prev_date_balance['Date Rank'] + 1
    prev_date_balance = prev_date_balance.rename(
        columns={'Balance': 'Prev Date Balance'})
    df_sorted = df_sorted.merge(prev_date_balance[['Account Number', 'Next Date Rank', 'Prev Date Balance']],
                                left_on=['Account Number', 'Date Rank'],
                                right_on=['Account Number', 'Next Date Rank'],
                                how='left')
    df_sorted['Prev Balance'] = df_sorted['Prev Date Balance'].fillna(
        df_sorted['Prev Balance']).fillna(0)

    df_sorted['Expected Balance'] = df_sorted['Prev Balance'].fillna(
        0) + df_sorted['Total Transaction Value'].fillna(0)
    df_sorted['Balance Diff'] = (df_sorted['Balance'].astype(
        float) - df_sorted['Expected Balance'].fillna(0)).abs()

    agg_df = df_sorted.sort_values(['Account Number', 'Balance Date', 'Balance Diff']).groupby([
        'Account Number', 'Balance Date']).first().reset_index()
    agg_df = agg_df.drop(
        columns=['Date Rank', 'Next Date Rank', 'Prev Date Balance'], errors='ignore')
    if 'Total Transaction Value' not in agg_df.columns:
        total_tx_value = df.groupby(['Account Number', 'Balance Date'])[
            'Transaction Value'].sum().reset_index()
        total_tx_value.rename(
            columns={'Transaction Value': 'Total Transaction Value'}, inplace=True)
        agg_df = agg_df.merge(total_tx_value, on=[
                              'Account Number', 'Balance Date'], how='left')
    agg_df['Transaction Value'] = agg_df['Total Transaction Value']
    agg_df = agg_df.drop(
        columns=['Prev Balance', 'Expected Balance', 'Balance Diff'], errors='ignore')

    def calc_order(group):
        sorted_group = group.sort_values(['Balance Date', 'Total Transaction Value'],
                                         ascending=[True, False], na_position='last')
        sorted_group['Order'] = range(1, len(sorted_group) + 1)
        return sorted_group['Order']

    agg_df['Order'] = agg_df.groupby(
        'Account Number', group_keys=False).apply(calc_order).values

    agg_df['Max Order'] = agg_df.groupby(['Account Number', 'Balance Date'])[
        'Order'].transform('max')

    daily_df = agg_df[agg_df['Max Order'] == agg_df['Order']].copy()
    if 'Transaction Value' in daily_df.columns and 'Total Transaction Value' in daily_df.columns:
        daily_df = daily_df.drop(columns=['Transaction Value'])
    daily_df.rename(
        columns={'Total Transaction Value': 'Transaction Value'}, inplace=True)
    daily_df = daily_df[['Account Number', 'Balance Date',
                         'Transaction Value', 'Balance']].copy()

    daily_df['Transaction Order'] = daily_df.groupby('Account Number')[
        'Balance Date'].rank(method='first', ascending=True).astype(int)

    order_minus_1 = daily_df.copy()
    order_minus_1['Transaction Order'] = order_minus_1['Transaction Order'] - 1
    order_minus_1['Balance Date Upper Bound'] = order_minus_1['Balance Date'] - \
        timedelta(days=1)
    order_minus_1 = order_minus_1[[
        'Account Number', 'Transaction Order', 'Balance Date Upper Bound']].copy()

    merged = daily_df.merge(
        order_minus_1,
        on=['Account Number', 'Transaction Order'],
        how='left'
    )

    max_balance_date = merged.groupby('Account Number')[
        'Balance Date'].transform('max')
    merged['Balance Date Upper Bound'] = merged['Balance Date Upper Bound'].fillna(
        max_balance_date)

    result_rows = []

    for account_num in merged['Account Number'].unique():
        account_data = merged[merged['Account Number'] == account_num].copy()
        account_data = account_data.sort_values('Balance Date')

        start_date = datetime(2023, 1, 31)
        end_date = datetime(2023, 2, 14)
        all_dates = pd.date_range(start=start_date, end=end_date, freq='D')

        date_df = pd.DataFrame({'Date': all_dates})
        date_df['Account Number'] = account_num

        account_data['Date'] = account_data['Balance Date']
        result = date_df.merge(
            account_data[['Date', 'Transaction Value', 'Balance']],
            on='Date',
            how='left'
        )


        result = result.sort_values('Date')


        filled_balance = result['Balance'].ffill()
        mask = result['Balance'].isna()
        result.loc[mask, 'Balance'] = filled_balance[mask]

        if pd.isna(result.iloc[0]['Balance']):
            if len(account_data) > 0:
                earliest = account_data.iloc[0]
                if earliest['Date'] <= result.iloc[0]['Date']:
                    result.iloc[0, result.columns.get_loc(
                        'Balance')] = earliest['Balance']
                    filled_balance = result['Balance'].ffill()
                    mask = result['Balance'].isna()
                    result.loc[mask, 'Balance'] = filled_balance[mask]

        result_rows.append(result)

    final_df = pd.concat(result_rows, ignore_index=True)

    filter_date = datetime(2023, 2, 1)
    final_df = final_df[final_df['Date'] == filter_date].copy()

    final_df = final_df[['Account Number',
                         'Transaction Value', 'Balance']].copy()

    final_df['Transaction Value'] = final_df['Transaction Value'].where(
        pd.notna(final_df['Transaction Value']), None)

    final_df = final_df.sort_values('Account Number').reset_index(drop=True)

    return {
        "output_01.csv": final_df,
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
