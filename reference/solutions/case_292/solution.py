from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    df = df.rename(
        columns={
            "Home Team": "home_team",
            "Away Team": "away_team",
            "Home Score": "home_score",
            "Away Score": "away_score",
            "Matchday": "matchday",
        }
    )

    home = df[["matchday", "home_team", "home_score", "away_score"]].copy()
    home["Team"] = home["home_team"]
    home["Goals For"] = home["home_score"]
    home["Goals Against"] = home["away_score"]

    away = df[["matchday", "away_team", "home_score", "away_score"]].copy()
    away["Team"] = away["away_team"]
    away["Goals For"] = away["away_score"]
    away["Goals Against"] = away["home_score"]

    long_df = pd.concat([
        home[["matchday", "Team", "Goals For", "Goals Against"]],
        away[["matchday", "Team", "Goals For", "Goals Against"]],
    ], ignore_index=True)

    long_df["Goal Difference"] = long_df["Goals For"] - long_df["Goals Against"]

    def result_points(gf: int, ga: int) -> int:
        if gf > ga:
            return 3
        if gf == ga:
            return 1
        return 0

    def result_char(gf: int, ga: int) -> str:
        if gf > ga:
            return "W"
        if gf == ga:
            return "D"
        return "L"

    long_df["Points"] = [result_points(gf, ga) for gf, ga in zip(long_df["Goals For"], long_df["Goals Against"])]
    long_df["Result"] = [result_char(gf, ga) for gf, ga in zip(long_df["Goals For"], long_df["Goals Against"])]
    long_df["Latest Result"] = long_df["Goals For"].astype(str) + "-" + long_df["Goals Against"].astype(str)

    long_df = long_df.sort_values(["Team", "matchday"]).reset_index(drop=True)

    long_df["Goal Difference (RT)"] = long_df.groupby("Team")["Goal Difference"].cumsum()
    long_df["Points (RT)"] = long_df.groupby("Team")["Points"].cumsum()

    def build_last5(group: pd.DataFrame) -> pd.Series:
        res = group["Result"].tolist()
        out = []
        for i in range(len(res)):
            window = res[max(0, i - 4): i + 1]
            pad_len = 5 - len(window)
            out.append("-" * pad_len + "".join(window))
        return pd.Series(out, index=group.index)

    long_df["Last 5 games"] = long_df.groupby("Team", group_keys=False).apply(build_last5)

    def day_rank(day_df: pd.DataFrame) -> pd.DataFrame:
        ranked = day_df.sort_values(
            by=["Points (RT)", "Goal Difference (RT)", "Team"],
            ascending=[False, False, False],
            kind="mergesort",
        ).copy()
        ranked["Position"] = range(1, len(ranked) + 1)
        return ranked

    ranked_all = long_df.groupby("matchday", group_keys=False).apply(day_rank)

    out = ranked_all[[
        "matchday",
        "Position",
        "Team",
        "Goal Difference (RT)",
        "Points (RT)",
        "Latest Result",
        "Last 5 games",
    ]].copy()

    out = out.rename(columns={"matchday": "Matchday"})
    out["Matchday"] = out["Matchday"].astype(int)
    out["Position"] = out["Position"].astype(int)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False)
