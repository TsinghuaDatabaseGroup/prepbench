import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    
    df = pd.read_csv(inputs_dir / "input_01.csv")
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    max_date = df['Date'].max()
    
    results = []
    
    for (player, session), group in df.groupby(['Player', 'Session']):
        group = group.sort_values('Date').reset_index(drop=True)
        
        for idx, row in group.iterrows():
            current_date = row['Date']
            current_score = row['Score']
            
            if idx < len(group) - 1:
                next_date = group.iloc[idx + 1]['Date']
                date_range = pd.date_range(start=current_date, end=next_date - timedelta(days=1), freq='D')
            else:
                next_date = max_date
                date_range = pd.date_range(start=current_date, end=next_date, freq='D')
            
            for date in date_range:
                if date.weekday() < 5:
                    if date == current_date:
                        flag = 'Actual'
                    else:
                        flag = 'Carried over'
                    
                    results.append({
                        'Player': player,
                        'Session': session,
                        'Session Date': date.strftime('%d/%m/%Y'),
                        'Score': current_score,
                        'Flag': flag
                    })
    
    result_df = pd.DataFrame(results)
    
    result_df = result_df[['Flag', 'Player', 'Session', 'Score', 'Session Date']]
    
    result_df['Score'] = result_df['Score'].astype(int)
    
    return {'output_01.csv': result_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

