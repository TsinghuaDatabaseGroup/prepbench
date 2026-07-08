from decimal import Decimal, InvalidOperation

import pandas as pd
from pathlib import Path

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def format_dialogue_value(value: str) -> str:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return value
        text = str(value).strip()
        if '.' not in text:
            return text
        try:
            dec = Decimal(text)
        except InvalidOperation:
            return text
        quantized = dec.quantize(Decimal('0.000001'))
        normalized = quantized.normalize()
        formatted = format(normalized, 'f')
        if formatted == '-0':
            formatted = '0'
        return formatted

    dialogue_df = pd.read_csv(inputs_dir / "input_03.csv", dtype={'dialogue': str})
    dialogue_df['time_in_secs'] = pd.to_numeric(dialogue_df['time_in_secs'], errors='coerce')
    dialogue_df['dialogue'] = dialogue_df['dialogue'].apply(format_dialogue_value)
    episode_df = pd.read_csv(inputs_dir / "input_04.csv")
    
    episode_df['runtime_in_secs'] = pd.to_numeric(episode_df['runtime_in_secs'], errors='coerce')
    episode_end = episode_df[['Episode', 'runtime_in_secs']].copy()
    episode_end.columns = ['Episode', 'time_in_secs']
    episode_end['name'] = 'END'
    episode_end['youtube_timestamp'] = ''
    episode_end['dialogue'] = ''
    episode_end['section'] = ''
    
    combined_df = pd.concat([dialogue_df, episode_end], ignore_index=True)
    
    combined_df = combined_df.sort_values(['Episode', 'time_in_secs']).reset_index(drop=True)
    combined_df['rank'] = combined_df.groupby('Episode')['time_in_secs'].rank(method='dense', ascending=True)
    
    
    def get_next_time(group):
        next_times = []
        times = group['time_in_secs'].values
        for i in range(len(times)):
            current_time = times[i]
            next_time = None
            for j in range(i + 1, len(times)):
                if times[j] != current_time:
                    next_time = times[j]
                    break
            next_times.append(next_time)
        return pd.Series(next_times, index=group.index)
    
    combined_df['next_time_in_secs'] = combined_df.groupby('Episode', group_keys=False).apply(get_next_time).reset_index(level=0, drop=True)
    
    episode_end_dict = dict(zip(episode_end['Episode'], episode_end['time_in_secs']))
    combined_df['next_time_in_secs'] = combined_df.apply(
        lambda row: row['next_time_in_secs'] if pd.notna(row['next_time_in_secs']) else episode_end_dict.get(row['Episode'], row['next_time_in_secs']),
        axis=1
    )
    
    combined_df['Duration'] = combined_df['next_time_in_secs'] - combined_df['time_in_secs']
    
    merged_df = combined_df[combined_df['name'] != 'END'].copy()
    
    merged_df = merged_df[merged_df['section'] == 'Gameplay'].copy()
    
    def split_names(name_str):
        if pd.isna(name_str):
            return []
        name_str = str(name_str).strip()
        if not name_str:
            return []
        if name_str == 'ALL':
            return ['ALL']
        names = [n.strip() for n in name_str.split(',') if n.strip()]
        return names
    
    expanded_rows = []
    for idx, row in merged_df.iterrows():
        names = split_names(row['name'])
        if not names:
            continue
        for name in names:
            expanded_rows.append({
                'Episode': row['Episode'],
                'name': name,
                'start_time': row['time_in_secs'],
                'Duration': row['Duration'],
                'youtube_timestamp': row['youtube_timestamp'],
                'dialogue': row['dialogue'],
                'section': row['section']
            })
    
    result_df = pd.DataFrame(expanded_rows)
    
    result_df['start_time'] = result_df['start_time'].astype(int)
    result_df['Duration'] = result_df['Duration'].astype(int)
    
    result_df = result_df[result_df['Duration'] > 0].copy()
    
    result_df = result_df[[
        'Episode',
        'name',
        'start_time',
        'Duration',
        'youtube_timestamp',
        'dialogue',
        'section'
    ]]
    
    result_df = result_df.drop_duplicates(keep='first').reset_index(drop=True)
    
    result_df = result_df.sort_values([
        'Episode',
        'name',
        'start_time',
        'Duration',
        'youtube_timestamp',
        'dialogue',
        'section'
    ]).reset_index(drop=True)
    
    return {
        'output_01.csv': result_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')

