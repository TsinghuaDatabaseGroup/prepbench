from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def build_long_records(matches: pd.DataFrame) -> pd.DataFrame:
        home = matches.rename(columns={
            "Home Team": "Team",
            "Home Score": "GF",
            "Away Score": "GA",
        })[["Matchday", "Team", "GF", "GA"]]

        away = matches.rename(columns={
            "Away Team": "Team",
            "Away Score": "GF",
            "Home Score": "GA",
        })[["Matchday", "Team", "GF", "GA"]]

        long_df = pd.concat([home, away], ignore_index=True)
        long_df["GF"] = pd.to_numeric(long_df["GF"], errors="coerce")
        long_df["GA"] = pd.to_numeric(long_df["GA"], errors="coerce")
        long_df["GD"] = long_df["GF"] - long_df["GA"]

        def points_row(row) -> int:
            if row.GF > row.GA:
                return 3
            if row.GF == row.GA:
                return 1
            return 0

        long_df["PTS"] = long_df.apply(points_row, axis=1)
        return long_df

    def running_totals(long_df: pd.DataFrame) -> pd.DataFrame:
        long_df = long_df.sort_values(["Team", "Matchday"]).copy()
        long_df["GF_RT"] = long_df.groupby("Team")["GF"].cumsum()
        long_df["GA_RT"] = long_df.groupby("Team")["GA"].cumsum()
        long_df["GD_RT"] = long_df.groupby("Team")["GD"].cumsum()
        long_df["PTS_RT"] = long_df.groupby("Team")["PTS"].cumsum()
        return long_df

    def assign_positions(rt: pd.DataFrame) -> pd.DataFrame:
        def rank_one(md_df: pd.DataFrame) -> pd.DataFrame:
            ordered = md_df.sort_values(
                by=["PTS_RT", "GD_RT", "Team"], ascending=[False, False, True]
            ).copy()
            ordered = md_df.sort_values(
                by=["PTS_RT", "GD_RT", "Team"], ascending=[False, False, False]
            ).copy()
            ordered["Position"] = range(1, len(ordered) + 1)
            return ordered

        out = (
            rt.groupby("Matchday", group_keys=False)
            .apply(rank_one)
            .sort_values(["Matchday", "Position", "Team"])
        )
        return out

    matches = pd.read_csv(inputs_dir / "input_01.csv")
    matches = matches[[
        "Away Score", "Away Team", "Home Score", "Home Team", "Matchday"
    ]].copy()

    long_df = build_long_records(matches)
    rt = running_totals(long_df)
    ranked = assign_positions(rt)

    out = ranked[[
        "Matchday",
        "Team",
        "GF_RT",
        "GA_RT",
        "GD_RT",
        "PTS_RT",
        "Position",
    ]].copy()

    out = out.rename(columns={
        "GF_RT": "Goals For (RT)",
        "GA_RT": "Goals Against (RT)",
        "GD_RT": "Goal Difference (RT)",
        "PTS_RT": "Points (RT)",
    })

    out["Matchday"] = pd.to_numeric(out["Matchday"], errors="coerce")
    out["Position"] = pd.to_numeric(out["Position"], errors="coerce")
    for col in ["Goals For (RT)", "Goals Against (RT)", "Goal Difference (RT)", "Points (RT)"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


