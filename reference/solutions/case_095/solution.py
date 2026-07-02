import math
from datetime import datetime as dt
from pathlib import Path

import pandas as pd


def _parse_start_datetime(date_value: str, start_str: str) -> pd.Timestamp:
    date_ts = pd.to_datetime(date_value, errors="coerce")
    if pd.isna(date_ts):
        return pd.NaT

    start = (start_str or "").strip().lower()
    if start.endswith("a") or start.endswith("p"):
        suffix = start[-1]
        time_part = start[:-1]
        start_formatted = f"{time_part}{'AM' if suffix == 'a' else 'PM'}"
    else:
        start_formatted = start

    if start_formatted:
        try:
            time_obj = dt.strptime(start_formatted, "%I:%M%p").time()
            combined = dt.combine(date_ts.date(), time_obj)
            return pd.Timestamp(combined)
        except ValueError:
            pass

    return pd.Timestamp(date_ts.date())


def _load_games(inputs_dir: Path) -> pd.DataFrame:
    monthly_frames: list[pd.DataFrame] = []
    for input_path in sorted(inputs_dir.glob("input_*.csv")):
        df = pd.read_csv(input_path)
        df = df.dropna(subset=["Visitor/Neutral", "Home/Neutral", "PTS", "PTS.1"], how="any")
        monthly_frames.append(df)

    games = pd.concat(monthly_frames, ignore_index=True)
    games = games.rename(
        columns={
            "Visitor/Neutral": "Visitor",
            "PTS": "Visitor Points",
            "Home/Neutral": "Home",
            "PTS.1": "Home Points",
            "Start (ET)": "Start",
        }
    )

    games["Visitor Points"] = pd.to_numeric(games["Visitor Points"], errors="coerce")
    games["Home Points"] = pd.to_numeric(games["Home Points"], errors="coerce")
    games = games.dropna(subset=["Visitor Points", "Home Points"])

    games["Game DateTime"] = games.apply(
        lambda row: _parse_start_datetime(row["Date"], row.get("Start", "")), axis=1
    )

    return games


def _build_team_game_rows(games: pd.DataFrame) -> pd.DataFrame:
    records: list[dict] = []

    for _, row in games.iterrows():
        visitor = row["Visitor"]
        home = row["Home"]
        visitor_pts = int(row["Visitor Points"])
        home_pts = int(row["Home Points"])
        game_dt = row["Game DateTime"]

        if visitor_pts == home_pts:
            winner = visitor
        else:
            winner = visitor if visitor_pts > home_pts else home

        records.append(
            {
                "Team": visitor,
                "Opponent": home,
                "Is Home": False,
                "Team Points": visitor_pts,
                "Opponent Points": home_pts,
                "Is Win": 1 if winner == visitor else 0,
                "Game DateTime": game_dt,
            }
        )
        records.append(
            {
                "Team": home,
                "Opponent": visitor,
                "Is Home": True,
                "Team Points": home_pts,
                "Opponent Points": visitor_pts,
                "Is Win": 1 if winner == home else 0,
                "Game DateTime": game_dt,
            }
        )

    team_games = pd.DataFrame.from_records(records)
    team_games = team_games.sort_values(["Team", "Game DateTime", "Opponent"]).reset_index(drop=True)

    team_games = team_games.groupby("Team", group_keys=False).head(82).copy()
    team_games["Game Number per Team"] = team_games.groupby("Team").cumcount() + 1
    team_games["Win"] = team_games.groupby("Team")["Is Win"].cumsum()
    return team_games


def _rank_by_game_number(team_games: pd.DataFrame) -> pd.DataFrame:

    ranked = team_games[["Team", "Game Number per Team", "Win"]].copy()
    ranked = ranked.sort_values(
        ["Game Number per Team", "Win", "Team"],
        ascending=[True, False, True],
    )
    ranked["Rank1"] = ranked.groupby("Game Number per Team").cumcount() + 1
    ranked = ranked.sort_values(["Game Number per Team", "Rank1"]).reset_index(drop=True)
    return ranked


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    games = _load_games(inputs_dir)
    team_games = _build_team_game_rows(games)
    ranked = _rank_by_game_number(team_games)

    ranked = ranked[["Rank1", "Win", "Game Number per Team", "Team"]].copy()
    ranked["Rank1"] = ranked["Rank1"].astype(int)
    ranked["Win"] = ranked["Win"].astype(int)
    ranked["Game Number per Team"] = ranked["Game Number per Team"].astype(int)

    ranked = ranked.sort_values(["Game Number per Team", "Rank1"]).reset_index(drop=True)

    return {"output_01.csv": ranked}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
