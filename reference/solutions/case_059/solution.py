import pandas as pd
from pathlib import Path
import numpy as np

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    sla = pd.read_csv(inputs_dir / 'input_01.csv')
    tickets_list = []
    for fname in ['input_02.csv', 'input_03.csv', 'input_04.csv']:
        fpath = inputs_dir / fname
        if fpath.exists():
            tickets_list.append(pd.read_csv(fpath))
    tickets = pd.concat(tickets_list, ignore_index=True)

    tickets[['Ticket ID', 'Department', 'Name']] = tickets['Ticket'].str.split(' / ', expand=True)
    tickets['Department'] = tickets['Department'].str.strip()
    tickets['Ticket ID'] = tickets['Ticket ID'].str.strip()

    tickets['Timestamp'] = pd.to_datetime(tickets['Timestamp'])

    current_status = tickets.loc[tickets.groupby('Ticket ID')['Status No.'].idxmax()]

    output_01 = current_status.groupby('Status Name').size().reset_index(name='Ticket Count')
    output_01.rename(columns={'Status Name': 'Current Status'}, inplace=True)
    
    
    start_dates = tickets.groupby('Ticket ID')['Timestamp'].min().reset_index()
    start_dates.rename(columns={'Timestamp': 'Start Date'}, inplace=True)

    closed_tickets = tickets[tickets['Status Name'] == 'Closed']
    end_dates = closed_tickets.groupby('Ticket ID')['Timestamp'].max().reset_index()
    end_dates.rename(columns={'Timestamp': 'End Date'}, inplace=True)

    ticket_durations = pd.merge(start_dates, end_dates, on='Ticket ID', how='left')
    
    def adjust_for_weekends(df, date_col):
        is_saturday = df[date_col].dt.dayofweek == 5
        df.loc[is_saturday, date_col] = df.loc[is_saturday, date_col].dt.normalize() + pd.Timedelta(days=2)
        is_sunday = df[date_col].dt.dayofweek == 6
        df.loc[is_sunday, date_col] = df.loc[is_sunday, date_col].dt.normalize() + pd.Timedelta(days=1)
        return df

    ticket_durations = adjust_for_weekends(ticket_durations, 'Start Date')
    
    closed_with_end_date = ticket_durations.dropna(subset=['End Date']).copy()
    is_saturday_close = closed_with_end_date['End Date'].dt.dayofweek == 5
    closed_with_end_date.loc[is_saturday_close, 'End Date'] = closed_with_end_date.loc[is_saturday_close, 'End Date'].dt.normalize() - pd.Timedelta(seconds=1)
    is_sunday_close = closed_with_end_date['End Date'].dt.dayofweek == 6
    closed_with_end_date.loc[is_sunday_close, 'End Date'] = closed_with_end_date.loc[is_sunday_close, 'End Date'].dt.normalize() - pd.Timedelta(days=1, seconds=1)
    
    ticket_durations.update(closed_with_end_date)

    def calculate_business_days(start, end):
        if pd.isna(end):
            return np.nan
        total_days = (end.normalize() - start.normalize()).days
        bus_days = np.busday_count(start.date(), end.date())
        start_time_fraction = (pd.Timedelta(days=1) - (start - start.normalize())) / pd.Timedelta(days=1)
        end_time_fraction = (end - end.normalize()) / pd.Timedelta(days=1)
        
        if bus_days == 0:
            return (end - start) / pd.Timedelta(days=1)
        
        business_duration = (bus_days - 1) + start_time_fraction + end_time_fraction
        return business_duration

    ticket_durations['Business Days Open'] = ticket_durations.apply(
        lambda row: calculate_business_days(row['Start Date'], row['End Date']), axis=1
    )

    ticket_info = current_status[['Ticket ID', 'Department']].drop_duplicates()
    analysis_df = pd.merge(ticket_durations, ticket_info, on='Ticket ID')
    analysis_df = pd.merge(analysis_df, sla, on='Department')

    closed_analysis = analysis_df.dropna(subset=['End Date'])
    closed_analysis['Met SLA'] = closed_analysis['Business Days Open'] <= closed_analysis['SLA Agreement']
    
    missed_sla = closed_analysis[~closed_analysis['Met SLA']].shape[0]
    on_track = closed_analysis[closed_analysis['Met SLA']].shape[0]
    
    output_02 = pd.DataFrame({
        'Metric': ['Missed SLA', 'On Track to Meet SLA'],
        'Total': [missed_sla, on_track]
    })

    sla_18_depts = sla[sla['SLA Agreement'] == 18]['Department'].tolist()
    closed_analysis_filtered = closed_analysis[closed_analysis['Department'].isin(sla_18_depts)]
    
    dept_sla = closed_analysis_filtered.groupby('Department')['Met SLA'].agg(['count', 'sum']).reset_index()
    dept_sla.rename(columns={'count': 'Total Closed', 'sum': 'Met SLA Count'}, inplace=True)
    dept_sla['Achieved %'] = (dept_sla['Met SLA Count'] / dept_sla['Total Closed']) * 100
    dept_sla = dept_sla[dept_sla['Achieved %'] > 0]
    dept_sla = dept_sla.sort_values(by=['Achieved %', 'Department'], ascending=[False, True])
    dept_sla['Department Rank'] = range(1, len(dept_sla) + 1)
    
    output_03 = dept_sla[['Department Rank', 'Department', 'Achieved %']]
    output_03['Achieved %'] = output_03['Achieved %'].round(2)

    return {
        'output_01.csv': output_01,
        'output_02.csv': output_02,
        'output_03.csv': output_03
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    
    if not cand_dir.exists():
        cand_dir.mkdir()

    solutions = solve(inputs_dir)
    
    for filename, df in solutions.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
