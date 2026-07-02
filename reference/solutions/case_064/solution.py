import pandas as pd
from pathlib import Path
from collections import defaultdict


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file, header=None)


    in_squad_count = defaultdict(int)
    appearances = defaultdict(int)
    mins_played = defaultdict(int)

    for idx in range(7, len(df)):
        row = df.iloc[idx]

        if pd.isna(row.iloc[0]) or str(row.iloc[0]).strip() == '':
            continue

        starting_xi = []
        for col_idx in range(9, 20):
            player = str(row.iloc[col_idx]).strip()
            if player and player != 'nan':
                starting_xi.append((col_idx - 8, player))

        substitutes = []
        for col_idx in range(31, 38):
            player = str(row.iloc[col_idx]).strip()
            if player and player != 'nan':
                substitutes.append((col_idx - 19, player))

        for pos, player in starting_xi + substitutes:
            in_squad_count[player] += 1

        starting_players = {player for _, player in starting_xi}
        for player in starting_players:
            appearances[player] += 1

        substitutions = []

        if not pd.isna(row.iloc[21]) and str(row.iloc[21]).strip() != '':
            sub_off = int(float(row.iloc[21]))
            sub_on = int(float(row.iloc[22]))
            sub_time = float(row.iloc[23])
            substitutions.append((sub_off, sub_on, sub_time))

        if not pd.isna(row.iloc[24]) and str(row.iloc[24]).strip() != '':
            sub_off = int(float(row.iloc[24]))
            sub_on = int(float(row.iloc[25]))
            sub_time = float(row.iloc[26])
            substitutions.append((sub_off, sub_on, sub_time))

        if not pd.isna(row.iloc[27]) and str(row.iloc[27]).strip() != '':
            sub_off = int(float(row.iloc[27]))
            sub_on = int(float(row.iloc[28]))
            sub_time = float(row.iloc[29])
            substitutions.append((sub_off, sub_on, sub_time))

        substitutions.sort(key=lambda x: x[2])

        player_mins = {player: 90.0 for _, player in starting_xi}
        for _, player in substitutes:
            if player not in player_mins:
                player_mins[player] = 0.0

        for sub_off_pos, sub_on_pos, sub_time in substitutions:
            sub_off_player = None
            for pos, player in starting_xi:
                if pos == sub_off_pos:
                    sub_off_player = player
                    break

            sub_on_player = None
            for pos, player in substitutes:
                if pos == sub_on_pos:
                    sub_on_player = player
                    break

            if sub_off_player and sub_on_player:
                player_mins[sub_off_player] = sub_time

                player_mins[sub_on_player] = max(0, 90 - sub_time)

                appearances[sub_on_player] += 1

        for player, mins in player_mins.items():
            mins_played[player] += int(mins)

    all_players = set(in_squad_count.keys())
    results = []

    for player in sorted(all_players):
        in_squad = in_squad_count[player]
        apps = appearances[player]
        mins = mins_played[player]
        mins_per_game = mins / apps if apps > 0 else 0

        results.append({
            'In Squad': in_squad,
            'Player Name': player,
            'Mins Played': mins,
            'Appearances': apps,
            'Mins per Game': mins_per_game
        })

    df_result = pd.DataFrame(results)

    df_result = df_result.sort_values(
        ['In Squad', 'Player Name'], ascending=[False, True])

    return {
        'output_01.csv': df_result.reset_index(drop=True)
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
