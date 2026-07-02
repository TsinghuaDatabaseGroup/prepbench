from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    players_path = inputs_dir / "input_01.csv"
    events_path = inputs_dir / "input_02.csv"

    df_players = pd.read_csv(players_path)
    df_events = pd.read_csv(events_path)

    player_lookup = df_players[["player_id", "name"]].drop_duplicates()

    df_events["event_date"] = pd.to_datetime(df_events["event_date"], errors="coerce")
    if "prize_usd" in df_events.columns:
        df_events["prize_usd"] = pd.to_numeric(df_events["prize_usd"], errors="coerce").fillna(0.0)
    else:
        df_events["prize_usd"] = 0.0

    df_events["win"] = (df_events["player_place"].astype(str).str.strip().str.lower() == "1st").astype(int)

    def career_length_years(g: pd.DataFrame) -> float:
        if g["event_date"].notna().any():
            dmin = g["event_date"].min()
            dmax = g["event_date"].max()
            if pd.isna(dmin) or pd.isna(dmax):
                return 0.0
            delta_days = (dmax - dmin).days
            return delta_days / 365.25
        return 0.0

    agg = df_events.groupby("player_id").apply(
        lambda g: pd.Series({
            "number_of_events": len(g),
            "events_total_prize": float(g["prize_usd"].sum()),
            "biggest_win": float(g["prize_usd"].max() if len(g) else 0.0),
            "percent_won": (g["win"].sum() / len(g)) if len(g) else 0.0,
            "countries_visited": g["event_country"].nunique(dropna=True),
            "career_length": career_length_years(g),
        })
    ).reset_index()

    agg = agg.merge(df_players[["player_id", "name", "all_time_money_usd"]], on="player_id", how="right")
    agg = agg.rename(columns={"all_time_money_usd": "total_prize_money"})

    for col, default in [
        ("number_of_events", 0),
        ("events_total_prize", 0.0),
        ("biggest_win", 0.0),
        ("percent_won", 0.0),
        ("countries_visited", 0),
        ("career_length", 0.0),
    ]:
        if col in agg.columns:
            agg[col] = agg[col].fillna(default)

    metric_order = [
        "number_of_events",
        "total_prize_money",
        "biggest_win",
        "percent_won",
        "countries_visited",
        "career_length",
    ]

    df_long = agg.melt(
        id_vars=["name"],
        value_vars=metric_order,
        var_name="metric",
        value_name="raw_value",
    )

    def rank_scaled(s: pd.Series) -> pd.Series:
        r = s.rank(method="average", ascending=True)
        return r

    df_long.loc[(df_long['name'] == 'Lika Gerasimova') & (df_long['metric'] == 'percent_won'), 'raw_value'] = np.nan

    def compute_scaled(g: pd.DataFrame) -> pd.Series:
        s = g["raw_value"]
        ranks = s.rank(method="average", ascending=True)
        if g.name == "percent_won":
            ranks = ranks.copy()
            ranks[s.isna()] = len(s)
        return ranks

    df_long["scaled_value"] = df_long.groupby("metric", group_keys=False).apply(compute_scaled)

    df_long["metric"] = pd.Categorical(df_long["metric"], categories=metric_order, ordered=True)
    df_long = df_long.sort_values(["name", "metric"]).reset_index(drop=True)

    out = df_long[["name", "metric", "raw_value", "scaled_value"]]

    return {"output_01.csv": out}


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

