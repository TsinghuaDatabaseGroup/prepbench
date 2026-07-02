import re
from pathlib import Path

import pandas as pd


def _parse_duration_to_minutes(value: str) -> float:
    if pd.isna(value):
        return 0.0
    text = str(value).strip()
    if not text:
        return 0.0

    hours = 0
    minutes = 0

    hour_match = re.search(r'(\d+)\s*h', text)
    minute_match = re.search(r'(\d+)\s*m', text)

    if hour_match:
        hours = int(hour_match.group(1))
    if minute_match:
        minutes = int(minute_match.group(1))

    if not hour_match and not minute_match:
        try:
            return float(text)
        except ValueError:
            return 0.0

    return float(hours * 60 + minutes)


def _derive_city_from_team(team_name: str) -> str:
    parts = team_name.strip().split()
    if len(parts) <= 1:
        return parts[0]
    return " ".join(parts[:-1])


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    travel_matrix_path = inputs_dir / "input_01.csv"
    teams_path = inputs_dir / "input_02.csv"

    travel_raw = pd.read_csv(travel_matrix_path)
    first_col = travel_raw.columns[0]
    travel_raw = travel_raw.rename(columns={first_col: "From"})
    travel_raw.columns = travel_raw.columns.str.strip()

    travel_long = (
        travel_raw.melt(id_vars="From", var_name="To", value_name="duration")
        .assign(From=lambda df: df["From"].str.strip(), To=lambda df: df["To"].str.strip())
    )
    travel_long["Travel Mins"] = travel_long["duration"].apply(_parse_duration_to_minutes)
    travel_long = travel_long.drop(columns=["duration"])

    teams = pd.read_csv(teams_path)
    teams = teams.rename(columns={
        "Team": "Home Team",
        "Conference": "Home Conference",
        "Division": "Home Division",
    })
    teams = teams.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    teams["Home City"] = teams["Home Team"].apply(_derive_city_from_team)

    away_teams = teams.rename(
        columns={
            "Home Team": "Away Team",
            "Home Conference": "Away Conference",
            "Home Division": "Away Division",
            "Home City": "Away City",
        }
    )

    pairs = (
        teams.assign(_key=1)
        .merge(away_teams.assign(_key=1), on="_key", how="outer")
        .drop(columns="_key")
    )
    pairs = pairs[pairs["Home Team"] != pairs["Away Team"]]

    travel_lookup = travel_long.rename(columns={"From": "Home City", "To": "Away City"})
    pairs = pairs.merge(travel_lookup, on=["Home City", "Away City"], how="left")

    pairs["Travel Mins"] = pairs["Travel Mins"].fillna(0.0)

    same_conference = pairs["Home Conference"] == pairs["Away Conference"]
    pairs["Away Games"] = same_conference.map(lambda same: 1.5 if same else 1.0)

    pairs["Travel Contribution"] = pairs["Travel Mins"] * pairs["Away Games"]

    totals = (
        pairs.groupby(["Home Team", "Home Conference", "Home Division"], as_index=False, sort=False)[
            "Travel Contribution"
        ]
        .sum()
        .rename(columns={"Travel Contribution": "Travel Mins"})
    )

    totals = totals.sort_values("Home Team").reset_index(drop=True)

    return {
        "output_01.csv": totals,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8", float_format="%.10g")
