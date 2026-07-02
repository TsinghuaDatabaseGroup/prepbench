
import pandas as pd
from pathlib import Path
import numpy as np

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df.replace('-', np.nan, inplace=True)
    df.dropna(subset=['HTf', 'HTa'], inplace=True)

    df['Diff'] = pd.to_numeric(df['Diff'])

    df['Rank'] = df['Diff'].rank(method='min', ascending=False)

    venue_stats = df.groupby('Venue').agg(
        Number_of_Games=('Venue', 'size'),
        Best_Rank=('Rank', 'min'),
        Worst_Rank=('Rank', 'max'),
        Avg_Rank=('Rank', 'mean')
    ).reset_index()

    venue_stats.rename(columns={
        'Number_of_Games': 'Number of Games',
        'Best_Rank': 'Best Rank (Standard Competition)',
        'Worst_Rank': 'Worst Rank (Standard Competition)',
        'Avg_Rank': 'Avg. Rank (Standard Competition)'
    }, inplace=True)

    venue_stats['Best Rank (Standard Competition)'] = venue_stats['Best Rank (Standard Competition)'].astype(int)
    venue_stats['Worst Rank (Standard Competition)'] = venue_stats['Worst Rank (Standard Competition)'].astype(int)

    venue_stats['Avg. Rank (Standard Competition)'] = venue_stats['Avg. Rank (Standard Competition)'].round(9)

    order = [
        'Pretoria', 'Marseille', 'Auckland', 'Twickenham', 'Colombes',
        'Parc des Princes', 'Richmond', 'Sydney', 'Leicester', 'Stade de France'
    ]
    venue_stats['Venue'] = pd.Categorical(venue_stats['Venue'], categories=order, ordered=True)
    venue_stats = venue_stats.sort_values('Venue')
    
    final_df = venue_stats[[
        'Venue',
        'Number of Games',
        'Best Rank (Standard Competition)',
        'Worst Rank (Standard Competition)',
        'Avg. Rank (Standard Competition)'
    ]]

    return {"output_01.csv": final_df}

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
