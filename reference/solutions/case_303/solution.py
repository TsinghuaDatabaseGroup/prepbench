import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def _safe_to_int(x: object, default: int = 0) -> int:
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return default
        s = str(x).strip()
        if s == "-" or s == "":
            return default
        return int(float(s))
    except Exception:
        return default


def _safe_to_float(x: object, default: float = 0.0) -> float:
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return default
        s = str(x).strip()
        if s == "-" or s == "":
            return default
        return float(s)
    except Exception:
        return default


def _parse_conf_record_wins(s: object) -> int:
    try:
        if s is None:
            return 0
        parts = str(s).strip().split("-")
        return _safe_to_int(parts[0], 0)
    except Exception:
        return 0


def _z_scores(values: pd.Series) -> pd.Series:
    vals = values.astype(float)
    mean = vals.mean()
    std = vals.std(ddof=1)
    if std == 0 or np.isclose(std, 0.0):
        return pd.Series([0.0] * len(vals), index=vals.index)
    return (vals - mean) / std


def _competition_rank_sorted(df_sorted: pd.DataFrame, key_cols: List[str]) -> pd.Series:
    ranks = []
    last_vals = None
    last_rank = 0
    for idx, row in df_sorted[key_cols].iterrows():
        cur_vals = tuple(row.values.tolist())
        if last_vals is None:
            last_rank = 1
        elif cur_vals != last_vals:
            last_rank = len(ranks) + 1
        ranks.append(last_rank)
        last_vals = cur_vals
    return pd.Series(ranks, index=df_sorted.index, dtype=int)


def _rank_with_keys(df: pd.DataFrame, by: List[Tuple[str, bool]]) -> pd.Series:
    sort_cols: List[str] = []
    ascending: List[bool] = []
    for col, desc in by:
        sort_cols.append(col)
        ascending.append(not desc)
    tmp = df.reset_index(drop=False)
    tmp_sorted = tmp.sort_values(sort_cols, ascending=ascending, kind="mergesort")
    key_cols = [c for c, _ in by]
    ranks_sorted = _competition_rank_sorted(tmp_sorted, key_cols)
    out = pd.Series(index=df.index, dtype=int)
    out.loc[tmp_sorted["index"].values] = ranks_sorted.values
    return out


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    nba = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    nfl = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)
    epl = pd.read_csv(inputs_dir / "input_03.csv", dtype=str)
    rugby = pd.read_csv(inputs_dir / "input_04.csv", dtype=str)

    nba_df = nba.copy()
    nba_df["Team"] = nba_df["Team"].astype(str)
    nba_df["Wins"] = nba_df["WWins"].map(_safe_to_int)
    nba_df["GB"] = nba_df["GBGames behind"].map(_safe_to_float)
    nba_df["ConfWins"] = nba_df["ConfConference record"].map(_parse_conf_record_wins)
    nba_df["Sport"] = "NBA"
    nba_df["Ranking Field"] = nba_df["Wins"]
    nba_df["Sport Rank"] = _rank_with_keys(
        nba_df, by=[("Ranking Field", True), ("ConfWins", True), ("GB", False)]
    )

    nfl_df = nfl.copy()
    nfl_df["Team"] = nfl_df["Team"].astype(str)
    nfl_df["Wins"] = nfl_df["WWins"].map(_safe_to_int)
    nfl_df["PF"] = nfl_df["PFPoints for"].map(_safe_to_int)
    nfl_df["PA"] = nfl_df["PAPoints against"].map(_safe_to_int)
    nfl_df["PD"] = nfl_df["PF"] - nfl_df["PA"]
    nfl_df["Sport"] = "NFL"
    nfl_df["Ranking Field"] = nfl_df["Wins"]
    nfl_df["Sport Rank"] = _rank_with_keys(
        nfl_df, by=[("Ranking Field", True), ("PD", True), ("PF", True)]
    )

    epl_df = epl.copy()
    epl_df.rename(columns={"Club": "Team"}, inplace=True)
    epl_df["Team"] = epl_df["Team"].astype(str)
    epl_df["Pts"] = epl_df["PtsPoints"].map(_safe_to_int)
    epl_df["Wins"] = epl_df["WWins"].map(_safe_to_int)
    epl_df["GF"] = epl_df["GFGoals scored"].map(_safe_to_int)
    epl_df["Sport"] = "Premier League"
    epl_df["Ranking Field"] = epl_df["Pts"]
    epl_df["Sport Rank"] = _rank_with_keys(
        epl_df, by=[("Ranking Field", True), ("Wins", True), ("GF", True)]
    )

    rugby_df = rugby.copy()
    rugby_df["Team"] = rugby_df["Team"].astype(str)
    rugby_df["PTS"] = rugby_df["PTS"].map(_safe_to_int)
    rugby_df["W"] = rugby_df["W"].map(_safe_to_int)
    rugby_df["PD"] = rugby_df["PD"].map(_safe_to_int)
    rugby_df["Sport"] = "Rugby Aviva Premiership"
    rugby_df["Ranking Field"] = rugby_df["PTS"]
    rugby_df["Sport Rank"] = _rank_with_keys(
        rugby_df, by=[("Ranking Field", True), ("W", True), ("PD", True)]
    )

    common_cols = ["Sport", "Team", "Ranking Field", "Sport Rank"]
    combined = pd.concat([
        nba_df[common_cols],
        nfl_df[common_cols],
        epl_df[common_cols],
        rugby_df[common_cols],
    ], ignore_index=True)

    combined["z-score"] = combined.groupby("Sport", group_keys=False)["Ranking Field"].apply(_z_scores)

    sport_counts = combined.groupby("Sport")["Team"].transform("count")
    combined["Sport Specific Percentile Rank"] = 1 - (combined["Sport Rank"].astype(float) / sport_counts.astype(float))

    combined = combined.sort_values(
        ["z-score", "Sport Specific Percentile Rank", "Ranking Field", "Team"],
        ascending=[False, False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)

    pos = np.arange(len(combined))
    within = combined.groupby(["z-score", "Sport Specific Percentile Rank"]).cumcount()
    combined["Cross Sport Rank"] = (pos - within + 1).astype(int)

    out1 = combined[[
        "Sport",
        "Cross Sport Rank",
        "Team",
        "z-score",
        "Ranking Field",
        "Sport Specific Percentile Rank",
    ]].copy()

    out2 = (
        out1.groupby("Sport", as_index=False)["Cross Sport Rank"].mean()
        .rename(columns={"Cross Sport Rank": "Avg Cross Sport Rank"})
    )

    return {"output_01.csv": out1, "output_02.csv": out2}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
