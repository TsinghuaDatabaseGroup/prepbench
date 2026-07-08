from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict

BIG6 = {"Arsenal", "Chelsea", "Liverpool", "Man Utd", "Man City", "Spurs"}


def _parse_fixtures(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[df["Result"].astype(str).str.contains(r"\d+\s*-\s*\d+", na=False)]
    goals = df["Result"].str.extract(r"\s*(\d+)\s*-\s*(\d+)\s*")
    goals.columns = ["Home Goals", "Away Goals"]
    goals = goals.astype(int)
    df = pd.concat([df.reset_index(drop=True), goals.reset_index(drop=True)], axis=1)
    return df


def _team_points_goal_diff(df_fixt: pd.DataFrame) -> pd.DataFrame:
    recs = []
    for _, r in df_fixt.iterrows():
        hg = int(r["Home Goals"])
        ag = int(r["Away Goals"])
        if hg > ag:
            h_pts, a_pts = 3, 0
        elif hg < ag:
            h_pts, a_pts = 0, 3
        else:
            h_pts, a_pts = 1, 1
        recs.append({
            "Team": r["Home Team"],
            "GP": 1,
            "PTS": h_pts,
            "GD": hg - ag,
        })
        recs.append({
            "Team": r["Away Team"],
            "GP": 1,
            "PTS": a_pts,
            "GD": ag - hg,
        })
    team = pd.DataFrame.from_records(recs)
    if team.empty:
        return pd.DataFrame(columns=["Team", "Total Games Played", "Total Points", "Goal Difference"])    
    agg = team.groupby("Team", as_index=False).agg({
        "GP": "sum",
        "PTS": "sum",
        "GD": "sum",
    })
    agg = agg.rename(columns={
        "GP": "Total Games Played",
        "PTS": "Total Points",
        "GD": "Goal Difference",
    })
    return agg


def _rank_table(tbl: pd.DataFrame) -> pd.DataFrame:
    ordered = tbl.sort_values([
        "Total Points", "Goal Difference", "Team"
    ], ascending=[False, False, True]).reset_index(drop=True)
    ordered.insert(0, "Position", range(1, len(ordered) + 1))
    return ordered


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)
    df_fixt = _parse_fixtures(df)

    tbl = _team_points_goal_diff(df_fixt)
    out1 = _rank_table(tbl)[["Position", "Team", "Total Games Played", "Total Points", "Goal Difference"]]

    mask_non_big6 = (~df_fixt["Home Team"].isin(BIG6)) & (~df_fixt["Away Team"].isin(BIG6))
    df_fixt_no_big6 = df_fixt.loc[mask_non_big6].copy()
    tbl2 = _team_points_goal_diff(df_fixt_no_big6)

    out2_ranked = _rank_table(tbl2)[["Position", "Team", "Total Games Played", "Total Points", "Goal Difference"]]

    orig_pos = out1.set_index("Team")["Position"].to_dict()
    out2_ranked.insert(0, "Position Change", out2_ranked["Team"].map(lambda t: orig_pos.get(t, None)))
    out2_ranked["Position Change"] = out2_ranked["Position Change"] - out2_ranked["Position"]

    for col in ["Position", "Total Games Played", "Total Points", "Goal Difference"]:
        if col in out1.columns:
            out1[col] = out1[col].astype(int)
    for col in ["Position", "Total Games Played", "Total Points", "Goal Difference", "Position Change"]:
        if col in out2_ranked.columns:
            out2_ranked[col] = out2_ranked[col].astype(int)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2_ranked,
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
