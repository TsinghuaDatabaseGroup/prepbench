from __future__ import annotations

from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df['Date_dt'] = pd.to_datetime(df['Date'])
    
    min_date = df['Date_dt'].min()
    
    first_sessions = df.sort_values('Date_dt').groupby(['Player', 'Session']).first().reset_index()
    first_sessions = first_sessions[['Player', 'Session', 'Date_dt']].copy()
    
    pre_first_rows = []
    for _, row in first_sessions.iterrows():
        player = row['Player']
        session = row['Session']
        first_date = row['Date_dt']
        
        date_range = pd.date_range(start=min_date, end=first_date - pd.Timedelta(days=1), freq='D')
        
        weekdays = date_range[date_range.weekday < 5]
        
        for date in weekdays:
            pre_first_rows.append({
                'Player': player,
                'Session': session,
                'Date_dt': date,
                'Score': 0,
                'Flag': 'Pre First Session'
            })
    
    pre_first_df = pd.DataFrame(pre_first_rows)
    
    df_sorted = df.sort_values(['Player', 'Session', 'Date_dt']).copy()
    
    max_date = df_sorted['Date_dt'].max()
    
    filled_rows = []
    
    for (player, session), group in df_sorted.groupby(['Player', 'Session']):
        first_date = group['Date_dt'].min()
        
        all_dates = pd.date_range(start=first_date, end=max_date, freq='D')
        
        weekdays = all_dates[all_dates.weekday < 5]
        
        score_lookup = dict(zip(group['Date_dt'], group['Score']))
        
        last_score = None
        
        for date in weekdays:
            if date in score_lookup:
                last_score = score_lookup[date]
                filled_rows.append({
                    'Player': player,
                    'Session': session,
                    'Date_dt': date,
                    'Score': last_score,
                    'Flag': 'Actual'
                })
            elif last_score is not None:
                filled_rows.append({
                    'Player': player,
                    'Session': session,
                    'Date_dt': date,
                    'Score': last_score,
                    'Flag': 'Carried over'
                })
    
    filled_df = pd.DataFrame(filled_rows)
    
    combined_df = pd.concat([pre_first_df, filled_df], ignore_index=True)
    
    combined_df = combined_df.drop_duplicates(subset=['Player', 'Session', 'Date_dt'], keep='first')
    
    combined_df = combined_df[combined_df['Date_dt'].dt.weekday < 5].copy()
    
    output_df = combined_df.copy()
    output_df['Session Date'] = output_df['Date_dt'].dt.strftime('%d/%m/%Y')
    
    final_df = output_df[['Flag', 'Session Date', 'Player', 'Session', 'Score']].copy()
    
    final_df = final_df.sort_values(['Player', 'Session', 'Session Date']).reset_index(drop=True)
    
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

