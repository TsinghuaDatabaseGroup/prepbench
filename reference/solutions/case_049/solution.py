import pandas as pd
from pathlib import Path
import pytz

def calculate_streak(series):
    if len(series) == 0:
        return "W0"
    last_result = series.iloc[-1]
    streak = 0
    for result in reversed(series.values):
        if result == last_result:
            streak += 1
        else:
            break
    prefix = 'W' if last_result == 1 else 'L'
    return f"{prefix}{streak}"

def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    team_list = pd.read_csv(inputs_dir / 'input_01.csv')
    game_files = ['input_02.csv', 'input_03.csv', 'input_04.csv', 'input_05.csv']
    all_games = pd.concat([pd.read_csv(inputs_dir / f) for f in game_files], ignore_index=True)

    all_games.dropna(subset=['Date', 'Start (ET)'], inplace=True)
    
    start_norm = all_games['Start (ET)'].astype(str).str.strip().str.lower()
    start_norm = start_norm.str.replace(r"(\d{1,2}:\d{2})([ap])$", r"\1\2m", regex=True)
    datetime_str = all_games['Date'].astype(str).str.strip() + ' ' + start_norm
    all_games['DateTimeET'] = pd.to_datetime(datetime_str, format='%a %b %d %Y %I:%M%p', errors='coerce')
    all_games = all_games[all_games['DateTimeET'].notna()].copy()
    all_games['DateTimeUTC'] = all_games['DateTimeET'].dt.tz_localize('US/Eastern').dt.tz_convert('UTC')

    cutoff_utc = pd.Timestamp('2020-01-06 11:00:00', tz='UTC')

    all_games = all_games[all_games['DateTimeUTC'] < cutoff_utc].copy()

    all_games['PTS'] = pd.to_numeric(all_games['PTS'], errors='coerce')
    all_games['PTS.1'] = pd.to_numeric(all_games['PTS.1'], errors='coerce')
    all_games = all_games[all_games['PTS'].notna() & all_games['PTS.1'].notna()].copy()

    all_games = all_games.merge(team_list[['Team', 'Conference']], left_on='Visitor/Neutral', right_on='Team', how='left').rename(columns={'Conference': 'Visitor_Conf'})
    all_games = all_games.merge(team_list[['Team', 'Conference']], left_on='Home/Neutral', right_on='Team', how='left').rename(columns={'Conference': 'Home_Conf'})
    all_games.drop(columns=['Team_x', 'Team_y'], inplace=True)

    all_games['Winner'] = all_games.apply(lambda row: row['Home/Neutral'] if row['PTS.1'] > row['PTS'] else row['Visitor/Neutral'], axis=1)

    game_log = []
    for i, row in all_games.iterrows():
        home_team, visitor_team = row['Home/Neutral'], row['Visitor/Neutral']
        home_win = 1 if row['Winner'] == home_team else 0
        game_log.append({'Team': home_team, 'Date': row['DateTimeUTC'], 'Win': home_win, 'is_home': 1, 'is_conf': 1 if row['Home_Conf'] == row['Visitor_Conf'] else 0})
        game_log.append({'Team': visitor_team, 'Date': row['DateTimeUTC'], 'Win': 1 - home_win, 'is_home': 0, 'is_conf': 1 if row['Home_Conf'] == row['Visitor_Conf'] else 0})

    team_games = pd.DataFrame(game_log).sort_values(['Team', 'Date'])

    standings = team_games.groupby('Team')['Win'].agg(W='sum', L=lambda x: len(x) - x.sum()).reset_index()
    standings['Pct'] = (standings['W'] / (standings['W'] + standings['L'])).fillna(0).round(3)

    home_record = team_games[team_games['is_home'] == 1].groupby('Team')['Win'].agg(W='sum', L=lambda x: len(x) - x.sum()).reset_index()
    home_record['Home'] = home_record['W'].astype(str) + '-' + home_record['L'].astype(str)
    standings = standings.merge(home_record[['Team', 'Home']], on='Team', how='left', suffixes=('', '_hr'))

    away_record = team_games[team_games['is_home'] == 0].groupby('Team')['Win'].agg(W='sum', L=lambda x: len(x) - x.sum()).reset_index()
    away_record['Away'] = away_record['W'].astype(str) + '-' + away_record['L'].astype(str)
    standings = standings.merge(away_record[['Team', 'Away']], on='Team', how='left', suffixes=('', '_ar'))

    conf_record = team_games[team_games['is_conf'] == 1].groupby('Team')['Win'].agg(W='sum', L=lambda x: len(x) - x.sum()).reset_index()
    conf_record['Conf'] = conf_record['W'].astype(str) + '-' + conf_record['L'].astype(str)
    standings = standings.merge(conf_record[['Team', 'Conf']], on='Team', how='left', suffixes=('', '_cr'))

    last_10_games = team_games.groupby('Team').tail(10)
    l10_record = last_10_games.groupby('Team')['Win'].agg(W='sum', L=lambda x: len(x) - x.sum()).reset_index()
    l10_record['L10'] = l10_record['W'].astype(str) + '-' + l10_record['L'].astype(str)
    standings = standings.merge(l10_record[['Team', 'L10']], on='Team', how='left', suffixes=('', '_l10'))

    streaks = team_games.groupby('Team')['Win'].apply(calculate_streak).reset_index(name='Strk')
    standings = standings.merge(streaks, on='Team', how='left')

    standings.fillna('0-0', inplace=True)
    
    standings = standings.merge(team_list, on='Team')
    
    final_cols = ['Rank', 'Team', 'W', 'L', 'Pct', 'Conf', 'Home', 'Away', 'L10', 'Strk']
    
    standings = standings.sort_values(by=['Pct', 'Team'], ascending=[False, True])

    eastern_df = standings[standings['Conference'] == 'Eastern'].copy()
    eastern_df['Rank'] = eastern_df['Pct'].rank(method='max', ascending=False).astype(int)
    eastern_df = eastern_df.sort_values(by='Rank')[final_cols]
    
    western_df = standings[standings['Conference'] == 'Western'].copy()
    western_df['Rank'] = western_df['Pct'].rank(method='max', ascending=False).astype(int)
    western_df = western_df.sort_values(by='Rank')[final_cols]

    return {
        'output_01.csv': western_df,
        'output_02.csv': eastern_df
    }

if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    results = solve(inputs_dir)

    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
