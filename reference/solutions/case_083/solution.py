import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    start_date = pd.to_datetime('2019-04-01')
    end_date = pd.to_datetime('2020-09-08')

    holidays_df = pd.read_csv(inputs_dir / 'input_02.csv')
    total_holidays = holidays_df['Holidays'].sum()

    all_dates = pd.date_range(start=start_date + pd.Timedelta(days=1), end=end_date, freq='D')

    dates_df = pd.DataFrame(all_dates, columns=['date'])

    weekdays_df = dates_df[dates_df['date'].dt.dayofweek < 5]

    
    bank_holidays_2019 = ['2019-04-19', '2019-04-22', '2019-05-06', '2019-05-27', '2019-08-26', '2019-12-25', '2019-12-26']
    bank_holidays_2020 = ['2020-01-01', '2020-04-10', '2020-04-13', '2020-05-08', '2020-05-25', '2020-08-31']
    

    import numpy as np
    
    uk_bank_holidays = [
        '2019-04-19',
        '2019-04-22',
        '2019-05-06',
        '2019-05-27',
        '2019-08-26',
        '2019-12-25',
        '2019-12-26',
        '2020-01-01',
        '2020-04-10',
        '2020-04-13',
        '2020-05-08',
        '2020-05-25',
        '2020-08-31',
    ]

    net_work_days = np.busday_count((start_date + pd.Timedelta(days=1)).date(), (end_date + pd.Timedelta(days=1)).date(), holidays=uk_bank_holidays)

    working_days = net_work_days - total_holidays

    output_df = pd.DataFrame({
        'Start Date': [start_date.strftime('%d/%m/%Y')],
        'Today': [end_date.strftime('%d/%m/%Y')],
        'Working Days': [working_days]
    })

    return {"output_01.csv": output_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
