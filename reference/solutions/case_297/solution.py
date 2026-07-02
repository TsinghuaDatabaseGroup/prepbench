from __future__ import annotations
import pandas as pd
from pathlib import Path
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv, dtype=str)

    def get_year(series):
        if series <= 2:
            return 2004
        else:
            return 2002 + series

    df['Series'] = df['Series'].astype(int)
    df['Year'] = df['Series'].apply(get_year)

    df = df[df['Couple'] != 'Couple'].copy()

    def is_group_dance(dance):
        if pd.isna(dance):
            return False
        return 'Group' in str(dance) or 'Marathon' in str(dance)

    df['is_group'] = df['Dance'].apply(is_group_dance)
    df.loc[df['is_group'], 'Couple'] = 'Group'
    df = df.drop(columns=['is_group'])

    df['Couple'] = df['Couple'].str.replace(r'\d', '', regex=True)

    def split_scores(scores):
        if pd.isna(scores) or scores == 'No scoresreceived':
            return pd.Series([None, None])
        match = re.match(r'(\d+)\s*\(', str(scores))
        if match:
            total_score = int(match.group(1))
            judges_scores = re.search(r'\((.*?)\)', str(scores))
            if judges_scores:
                judges_str = judges_scores.group(1)
                return pd.Series([total_score, judges_str])
            return pd.Series([total_score, None])
        return pd.Series([None, None])

    score_split = df['Scores'].apply(split_scores)
    df['Total Score'] = score_split[0]
    df['Judges Scores'] = score_split[1]
    df = df.drop(columns=['Scores'])

    df.loc[df['Couple'] == 'Group', 'Total Score'] = None

    df['Week_original'] = df['Week'].copy()

    def split_week(week):
        if pd.isna(week):
            return pd.Series([None, None])
        week_str = str(week)
        week_match = re.search(r'Week\s+(\d+)', week_str)
        if week_match:
            week_num = int(week_match.group(1))
        else:
            week_num = None

        if ':' in week_str:
            theme = week_str.split(':', 1)[1].strip()
        else:
            theme = None

        return pd.Series([week_num, theme])

    week_split = df['Week'].apply(split_week)
    df['Week'] = week_split[0]
    df['Theme'] = week_split[1]

    def extract_stage_and_theme(row):
        week_original = row['Week_original']
        theme = row['Theme']

        if pd.isna(theme):
            return pd.Series([None, None])

        week_str = str(week_original) if pd.notna(week_original) else ''
        theme_lower = str(theme).lower()

        has_quarter = 'quarter' in theme_lower
        has_semi = 'semi' in theme_lower
        has_final = theme_lower == 'final' or (theme_lower.endswith(
            ' final') and 'quarter' not in theme_lower and 'semi' not in theme_lower)

        is_theme_week = re.search(
            r'\s+Week\s*\(', week_str, re.IGNORECASE) is not None

        stage = None
        if has_quarter:
            if is_theme_week:
                stage = None
            else:
                stage = 'Quarter Final'
        elif has_semi:
            stage = 'Semi Final'
        elif has_final:
            stage = 'Final'

        theme_str = str(theme)
        theme_str = re.sub(r'\(?\s*Quarter\s*-?\s*final\s*\)?',
                           '', theme_str, flags=re.IGNORECASE)
        theme_str = re.sub(r'\(?\s*Semi\s*-?\s*final\s*\)?',
                           '', theme_str, flags=re.IGNORECASE)
        theme_str = re.sub(r'\(?\s*Final\s*\)?', '',
                           theme_str, flags=re.IGNORECASE)
        theme_str = re.sub(r'\s+Week\s*$', '', theme_str, flags=re.IGNORECASE)
        theme_str = theme_str.strip()
        cleaned_theme = theme_str if theme_str else None

        return pd.Series([stage, cleaned_theme])

    stage_theme = df.apply(extract_stage_and_theme, axis=1)
    df['Stage'] = stage_theme[0]
    df['Theme'] = stage_theme[1]
    df = df.drop(columns=['Week_original'])

    def clean_theme(theme):
        if pd.isna(theme):
            return None
        theme_str = str(theme)
        theme_str = re.sub(r'[[:punct:]]', '', theme_str)
        theme_str = theme_str.replace(' Night', '').replace('Night', '')
        if theme_str == 'Hollywood':
            theme_str = 'Movie'
        return theme_str if theme_str else None

    df['Theme'] = df['Theme'].apply(clean_theme)

    def process_music(music):
        if pd.isna(music):
            return []
        music_str = str(music)
        music_str = music_str.replace(',"', '|').replace(
            '&"', '|').replace('& "', '|')
        songs = [s.strip() for s in music_str.split('|') if s.strip()]
        return songs

    group_dances = df[df['Couple'] == 'Group'].copy()
    non_group_dances = df[df['Couple'] != 'Group'].copy()

    if len(group_dances) > 0:
        group_by_cols_for_group = [
            'Year', 'Series', 'Week', 'Stage', 'Theme', 'Theme Detail',
            'Judges Scores', 'Dance', 'Music', 'Result'
        ]
        group_by_cols_for_group = [
            col for col in group_by_cols_for_group if col in group_dances.columns]
        group_dances = group_dances.groupby(
            group_by_cols_for_group, dropna=False).first().reset_index()
        group_dances['Couple'] = 'Group'
        group_dances['Total Score'] = None

    if len(group_dances) > 0:
        df = pd.concat([non_group_dances, group_dances], ignore_index=True)
    else:
        df = non_group_dances

    music_expanded = []
    for idx, row in df.iterrows():
        songs = process_music(row['Music'])
        if not songs:
            music_expanded.append({
                'idx': idx,
                'Song': None,
                'Artist': None
            })
        else:
            for song in songs:
                if '—' in song:
                    parts = song.split('—', 1)
                    song_name = parts[0].strip().strip('"').strip()
                    artist = parts[1].strip() if len(parts) > 1 else None
                else:
                    song_name = song.strip().strip('"').strip()
                    artist = None

                song_name = song_name.replace('"', '')

                music_expanded.append({
                    'idx': idx,
                    'Song': song_name,
                    'Artist': artist
                })

    music_df = pd.DataFrame(music_expanded)

    df = df.reset_index(drop=True)
    df['idx'] = df.index
    df = df.merge(music_df, on='idx', how='left')
    df = df.drop(columns=['idx', 'Music'])

    def merge_theme_detail(row):
        details = []
        for col in ['Film', 'Broadway musical', 'Musical', 'Country', 'CelebratingBBC']:
            val = row.get(col, '')
            if pd.notna(val) and str(val).strip():
                details.append(str(val).strip())
        return ' '.join(details) if details else None

    df['Theme Detail'] = df.apply(merge_theme_detail, axis=1)

    df = df.drop(columns=['Film', 'Broadway musical',
                 'Musical', 'Country', 'CelebratingBBC'])

    group_by_cols = [
        'Year', 'Series', 'Week', 'Stage', 'Theme', 'Theme Detail',
        'Couple', 'Total Score', 'Judges Scores', 'Dance', 'Song', 'Artist', 'Result'
    ]

    group_dances = df[df['Couple'] == 'Group'].copy()
    non_group_dances = df[df['Couple'] != 'Group'].copy()

    if len(group_dances) > 0:
        group_by_cols_for_group = [
            'Year', 'Series', 'Week', 'Stage', 'Theme', 'Theme Detail',
            'Judges Scores', 'Dance', 'Song', 'Artist', 'Result'
        ]
        group_dances = group_dances.groupby(
            group_by_cols_for_group, dropna=False).first().reset_index()
        group_dances['Couple'] = 'Group'
        group_dances['Total Score'] = None

    df = pd.concat([non_group_dances, group_dances], ignore_index=True)

    df = df.groupby(group_by_cols, dropna=False).first().reset_index()

    df['Judges Scores'] = df['Judges Scores'].replace(['null', '""', ''], None)
    df.loc[df['Judges Scores'].isna(), 'Judges Scores'] = None

    output_cols = [
        'Year', 'Series', 'Week', 'Stage', 'Theme', 'Theme Detail',
        'Couple', 'Total Score', 'Judges Scores', 'Dance', 'Song', 'Artist', 'Result'
    ]
    df = df[output_cols].copy()

    df['Year'] = df['Year'].astype(int)
    df['Series'] = df['Series'].astype(int)
    df['Week'] = df['Week'].astype(int)
    df['Total Score'] = df['Total Score'].astype(float).astype('Int64')

    return {
        "output_01.csv": df
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
