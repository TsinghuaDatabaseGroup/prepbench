import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    sessions_df = pd.read_csv(inputs_dir / "input_02.csv")
    pricing_df = pd.read_csv(inputs_dir / "input_01.csv")
    
    sessions_df['location'] = sessions_df['location'].replace('Edinurgh', 'Edinburgh')
    
    sessions_df['t'] = pd.to_datetime(sessions_df['t'], format='ISO8601')
    
    sessions_df['timestamp_str'] = sessions_df['t'].dt.strftime('%d/%m/%Y %H:%M:%S')
    
    aggregated = sessions_df.groupby(['userID', 'timestamp_str', 'location'], as_index=False).agg({
        'duration': 'sum',
        'content_type': 'first'
    })
    
    aggregated['timestamp'] = pd.to_datetime(aggregated['timestamp_str'], format='%d/%m/%Y %H:%M:%S')
    aggregated = aggregated.drop(columns=['timestamp_str'])
    
    def update_content_type(row):
        location = row['location']
        original_content_type = row['content_type']
        
        if location in ['London', 'Cardiff', 'Edinburgh']:
            return 'Primary'
        else:
            if pd.isna(original_content_type) or original_content_type == '':
                return 'Secondary'
            elif original_content_type == 'Preserved':
                return 'Preserved'
            else:
                return 'Secondary'
    
    aggregated['content_type'] = aggregated.apply(update_content_type, axis=1)
    
    
    aggregated['month_datetime'] = aggregated['timestamp'].dt.to_period('M').dt.to_timestamp()
    aggregated['month'] = aggregated['timestamp'].dt.strftime('%m %Y')
    
    primary_rows = aggregated['content_type'] == 'Primary'
    if primary_rows.any():
        primary_min_by_user = aggregated[primary_rows].groupby('userID')['month_datetime'].min().reset_index()
        primary_min_by_user['min_month'] = primary_min_by_user['month_datetime'].dt.strftime('%m %Y')
        primary_min_by_user = primary_min_by_user[['userID', 'min_month']].copy()
        primary_min_by_user['content_type'] = 'Primary'
    else:
        primary_min_by_user = pd.DataFrame(columns=['userID', 'min_month', 'content_type'])
    
    min_months_datetime = aggregated.groupby(['userID', 'location', 'content_type'])['month_datetime'].min().reset_index()
    min_months_datetime['min_month'] = min_months_datetime['month_datetime'].dt.strftime('%m %Y')
    min_months = min_months_datetime[['userID', 'location', 'content_type', 'min_month']].copy()
    
    if len(primary_min_by_user) > 0:
        for _, row in primary_min_by_user.iterrows():
            user_id = row['userID']
            min_month = row['min_month']
            min_months.loc[(min_months['userID'] == user_id) & (min_months['content_type'] == 'Primary'), 'min_month'] = min_month
    
    result = aggregated.merge(min_months, on=['userID', 'location', 'content_type'], how='left')
    
    pricing_df['Month'] = pricing_df['Month'].str.strip()
    result = result.merge(
        pricing_df[['Month', 'Avg_Price', 'Content_Type']],
        left_on=['min_month', 'content_type'],
        right_on=['Month', 'Content_Type'],
        how='left'
    )
    
    result.loc[result['content_type'] == 'Preserved', 'Avg_Price'] = 14.98
    
    
    output = result[[
        'userID',
        'timestamp',
        'location',
        'content_type',
        'duration',
        'Avg_Price'
    ]].copy()
    
    output['timestamp'] = output['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
    
    output['userID'] = output['userID'].astype(int)
    output['duration'] = output['duration'].astype(int)
    output['Avg_Price'] = output['Avg_Price'].astype(float)
    
    output = output.sort_values(['userID', 'timestamp', 'location', 'content_type']).reset_index(drop=True)
    
    return {
        'output_01.csv': output
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
