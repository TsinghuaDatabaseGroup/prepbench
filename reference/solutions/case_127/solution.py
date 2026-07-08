from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
from typing import Dict


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def read_clean_csv(p: Path, competition: str) -> pd.DataFrame:
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        df.columns = [c.strip() for c in df.columns]
        for c in df.columns:
            if df[c].dtype == object:
                df[c] = (
                    df[c]
                    .astype(str)
                    .str.replace("\xa0", " ", regex=False)
                    .str.strip()
                )
        df["Competition"] = competition
        return df

    wc_path = inputs_dir / "input_01.csv"
    eu_path = inputs_dir / "input_02.csv"
    df_wc = read_clean_csv(wc_path, "World Cup")
    df_eu = read_clean_csv(eu_path, "Euros")
    df_all = pd.concat([df_wc, df_eu], ignore_index=True)

    def norm_team(x: str) -> str:
        x = (x or "").replace("\xa0", " ").strip()
        x = " ".join(x.split())
        mapping = {
            "West Germany": "Germany",
        }
        return mapping.get(x, x)

    for col in ["Winner", "Loser"]:
        if col in df_all.columns:
            df_all[col] = df_all[col].apply(norm_team)

    if "Penalty Number" not in df_all.columns:
        alt_cols = [c for c in df_all.columns if c.lower().startswith("penalty number")]
        if alt_cols:
            df_all["Penalty Number"] = df_all[alt_cols[0]]

    def parse_outcome(cell: str) -> str | None:
        if cell is None:
            return None
        s = str(cell).strip()
        if s == "" or s.lower() == "nan":
            return None
        if "Penalty scored" in s:
            return "scored"
        if "Penalty missed" in s:
            return "missed"
        return None

    win_taker_col = [c for c in df_all.columns if c.lower().startswith("winning team taker")]
    lose_taker_col = [c for c in df_all.columns if c.lower().startswith("losing team taker")]
    if win_taker_col:
        win_taker_col = win_taker_col[0]
    else:
        win_taker_col = "Winning team Taker"
    if lose_taker_col:
        lose_taker_col = lose_taker_col[0]
    else:
        lose_taker_col = "Losing team Taker"

    penalties = []
    for _, r in df_all.iterrows():
        try:
            pen_no = int(str(r.get("Penalty Number", "").strip()).rstrip(","))
        except Exception:
            pen_no = pd.NA
        outcome_w = parse_outcome(r.get(win_taker_col))
        if outcome_w is not None and pd.notna(pen_no):
            penalties.append({
                "Competition": r["Competition"],
                "No": str(r.get("No.", "")).strip(),
                "Team": norm_team(r.get("Winner", "")),
                "Penalty Number": int(pen_no),
                "outcome": outcome_w,
            })
        outcome_l = parse_outcome(r.get(lose_taker_col))
        if outcome_l is not None and pd.notna(pen_no):
            penalties.append({
                "Competition": r["Competition"],
                "No": str(r.get("No.", "")).strip(),
                "Team": norm_team(r.get("Loser", "")),
                "Penalty Number": int(pen_no),
                "outcome": outcome_l,
            })

    df_pen = pd.DataFrame(penalties)

    shootouts = (
        df_all[["Competition", "No.", "Winner", "Loser"]]
        .drop_duplicates()
        .rename(columns={"Winner": "WinnerTeam", "Loser": "LoserTeam", "No.": "No"})
    )

    all_teams_rows = []
    for _, s in shootouts.iterrows():
        all_teams_rows.append({"Team": s["WinnerTeam"], "win": 1, "total": 1})
        all_teams_rows.append({"Team": s["LoserTeam"], "win": 0, "total": 1})
    df_team_shootouts = pd.DataFrame(all_teams_rows)
    agg = df_team_shootouts.groupby("Team", as_index=False).sum()
    agg = agg.rename(columns={"win": "Shootouts", "total": "Total Shootouts"})

    agg = agg[agg["Shootouts"] > 0].copy()

    agg["Shootout Win %"] = (agg["Shootouts"] / agg["Total Shootouts"] * 100).round().astype(int)
    agg["Win % Rank"] = agg["Shootout Win %"].rank(method="dense", ascending=False).astype(int)

    out1 = agg[["Win % Rank", "Shootout Win %", "Total Shootouts", "Shootouts", "Team"]].copy()
    out1 = out1.sort_values(by=["Win % Rank", "Shootout Win %", "Total Shootouts", "Team"], ascending=[True, False, False, True]).reset_index(drop=True)

    pen_grp = df_pen.groupby("Penalty Number").agg(
        **{
            "Penalties Scored": ("outcome", lambda s: int((s == "scored").sum())),
            "Penalties Missed": ("outcome", lambda s: int((s == "missed").sum())),
        }
    ).reset_index()
    pen_grp["Total Penalties"] = pen_grp["Penalties Scored"] + pen_grp["Penalties Missed"]
    pen_grp = pen_grp[pen_grp["Total Penalties"] > 0].copy()
    pen_grp["Penalty Scored %"] = (pen_grp["Penalties Scored"] / pen_grp["Total Penalties"] * 100).round().astype(int)
    pen_grp["Rank"] = pen_grp["Penalty Scored %"].rank(method="dense", ascending=False).astype(int)

    out2 = pen_grp[["Rank", "Penalty Scored %", "Penalties Scored", "Penalties Missed", "Total Penalties", "Penalty Number"]].copy()
    out2 = out2.sort_values(by=["Rank", "Penalty Scored %", "Total Penalties", "Penalty Number"], ascending=[True, False, False, True]).reset_index(drop=True)

    team_pen = df_pen.groupby("Team").agg(
        **{
            "Penalties Scored": ("outcome", lambda s: int((s == "scored").sum())),
            "Penalties Missed": ("outcome", lambda s: int((s == "missed").sum())),
        }
    ).reset_index()
    team_pen["Total"] = team_pen["Penalties Scored"] + team_pen["Penalties Missed"]
    team_pen = team_pen[team_pen["Total"] > 0].copy()
    team_pen["% Total Penalties Scored"] = (team_pen["Penalties Scored"] / team_pen["Total"] * 100).round().astype(int)
    team_pen["Penalties Scored %Rank"] = team_pen["% Total Penalties Scored"].rank(method="dense", ascending=False).astype(int)

    out3 = team_pen[["Penalties Scored %Rank", "% Total Penalties Scored", "Penalties Missed", "Penalties Scored", "Team"]].copy()
    out3 = out3.sort_values(by=["Penalties Scored %Rank", "% Total Penalties Scored", "Penalties Scored", "Team"], ascending=[True, False, False, True]).reset_index(drop=True)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
        "output_03.csv": out3,
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).write_text("")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

