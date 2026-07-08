import pandas as pd
from pathlib import Path
from datetime import datetime

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)
    
    def extract_timestamp(filename: str) -> str:
        if filename.endswith('.csv'):
            csv_pos = filename.rfind('.csv')
            if csv_pos >= 19:
                return filename[csv_pos - 19:csv_pos]
        return ""
    
    df['file_timestamp'] = df['filename'].apply(extract_timestamp)
    
    df['file_timestamp_dt'] = pd.to_datetime(df['file_timestamp'], format='%Y-%m-%d_%H-%M-%S', errors='coerce')
    
    latest_files = df.groupby(['candidate_id', 'position_id'])['file_timestamp_dt'].max().reset_index()
    latest_files.columns = ['candidate_id', 'position_id', 'max_file_timestamp']
    
    df = df.merge(latest_files, on=['candidate_id', 'position_id'], how='left')
    df_latest = df[df['file_timestamp_dt'] == df['max_file_timestamp']].copy()
    
    df_latest['ts'] = pd.to_datetime(df_latest['ts']).dt.strftime('%d/%m/%Y %H:%M:%S')
    
    output_01 = df_latest[['candidate_id', 'position_id', 'status', 'ts', 'filename']].copy()
    output_01 = output_01.sort_values(['candidate_id', 'position_id', 'ts']).reset_index(drop=True)
    
    output_01['candidate_id'] = output_01['candidate_id'].astype(int)
    output_01['position_id'] = output_01['position_id'].astype(int)
    
    df_latest['ts_dt'] = pd.to_datetime(df_latest['ts'], format='%d/%m/%Y %H:%M:%S')
    
    max_ts = df_latest.groupby(['candidate_id', 'position_id'])['ts_dt'].max().reset_index()
    max_ts.columns = ['candidate_id', 'position_id', 'max_ts']
    
    output_02 = df_latest.merge(max_ts, on=['candidate_id', 'position_id'], how='inner')
    output_02 = output_02[output_02['ts_dt'] == output_02['max_ts']].copy()
    
    output_02 = output_02[['candidate_id', 'position_id', 'status']].copy()
    output_02.columns = ['candidate_id', 'position_id', 'current_status']
    output_02 = output_02.sort_values(['candidate_id', 'position_id']).reset_index(drop=True)
    
    output_02['candidate_id'] = output_02['candidate_id'].astype(int)
    output_02['position_id'] = output_02['position_id'].astype(int)
    
    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

