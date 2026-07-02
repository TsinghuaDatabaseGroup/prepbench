from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    in_file = inputs_dir / "input_01.csv"

    df = pd.read_csv(in_file, sep=r"\s{2,}", engine="python", dtype=str, keep_default_na=False)

    cols = list(df.columns)
    cols = [c.strip() for c in cols]
    df.columns = cols

    df = df.replace("", np.nan)
    df = df.dropna(how="all")

    rename_map = {}
    if "SEASON" in df.columns:
        rename_map["SEASON"] = "Season"
    if "LEAGUE" in df.columns:
        rename_map["LEAGUE"] = "League"
    if "P.1" in df.columns:
        rename_map["P"] = "P"
        rename_map["P.1"] = "Pts"
    else:
        pass
    for c in ["W","D","L","F","A","POS"]:
        if c in df.columns:
            rename_map[c] = c if c != "POS" else "POS"

    df = df.rename(columns=rename_map)

    for c in ["P","W","D","L","F","A","Pts"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if "POS" in df.columns:
        df["POS"] = df["POS"].astype(object)
        df.loc[df["POS"].astype(str).str.upper().str.contains("ABAND", na=False), "POS"] = np.nan

    df["Special Circumstances"] = "N/A"
    df.loc[df["Season"].eq("1939-40"), "Special Circumstances"] = "Abandoned due to WW2"

    incomplete_mask = df["Season"].eq("2021-22") | df[["P","W","D","L","F","A","Pts"]].isna().all(axis=1)
    df.loc[incomplete_mask, "Special Circumstances"] = "Incomplete"

    df.loc[df["Special Circumstances"].ne("N/A"), "POS"] = np.nan

    league_level = {
        "FL-CH": 0,
        "FL-1": 1,
        "EFL-1": 1,
        "FL-2": 2,
        "EFL-2": 2,
        "FL-3": 3,
        "FL-3S": 3,
        "FL-4": 4,
        "SOUTH-1": 2,
        "SOUTH-2": 3,
        "NAT-P": 5,
    }

    def compute_outcome(order_df: pd.DataFrame) -> pd.Series:
        levels = order_df["League"].map(league_level).astype("float")
        next_levels = levels.shift(-1)
        outcome = pd.Series([None]*len(order_df), index=order_df.index, dtype=object)
        mask_valid = levels.notna() & next_levels.notna()
        outcome.loc[mask_valid & (next_levels < levels)] = "Promoted"
        outcome.loc[mask_valid & (next_levels > levels)] = "Relegated"
        outcome.loc[mask_valid & (next_levels == levels)] = "Same League"
        outcome.loc[order_df["Special Circumstances"].eq("Incomplete")] = "N/A"
        return outcome.fillna("N/A")

    base = df.copy()

    def empty_row(season: str, sc: str) -> dict:
        return {
            "Season": season,
            "Outcome": "N/A",
            "Special Circumstances": sc,
            "League": np.nan,
            "P": np.nan,
            "W": np.nan,
            "D": np.nan,
            "L": np.nan,
            "F": np.nan,
            "A": np.nan,
            "Pts": np.nan,
            "POS": np.nan,
        }

    rows = []
    for i, r in base.reset_index(drop=True).iterrows():
        if r["Season"] == "1914-15":
            for s in ["1918-19", "1917-18", "1916-17", "1915-16"]:
                rows.append(empty_row(s, "WW1"))
        if r["Season"] == "1939-40":
            for s in ["1945-46", "1944-45", "1943-44", "1942-43", "1941-42", "1940-41"]:
                rows.append(empty_row(s, "WW2"))
        rec = r.to_dict()
        for k in ["Outcome","Special Circumstances","Pts"]:
            rec.setdefault(k, np.nan)
        rows.append(rec)

    out_df = pd.DataFrame(rows)

    mask_real = out_df["League"].notna()
    out_df.loc[mask_real & out_df["Season"].eq("1939-40"), "Special Circumstances"] = "Abandoned due to WW2"
    out_df.loc[mask_real & out_df["Season"].eq("2021-22"), "Special Circumstances"] = "Incomplete"
    out_df.loc[mask_real & ~out_df["Season"].isin(["1939-40","2021-22"]), "Special Circumstances"] = "N/A"

    out_df.loc[out_df["Special Circumstances"].ne("N/A"), "POS"] = np.nan

    out_df["Special Circumstances"] = out_df["Special Circumstances"].fillna("N/A")

    base_for_outcome = base.copy()
    base_for_outcome["Special Circumstances"] = "N/A"
    base_for_outcome.loc[base_for_outcome["Season"].eq("1939-40"), "Special Circumstances"] = "Abandoned due to WW2"
    base_for_outcome.loc[base_for_outcome["Season"].eq("2021-22"), "Special Circumstances"] = "Incomplete"
    season_to_outcome = compute_outcome(base_for_outcome)
    season_to_outcome.index = base_for_outcome["Season"].astype(str).values

    out_df["Outcome"] = np.where(
        out_df["League"].notna(),
        out_df["Season"].map(season_to_outcome).fillna("N/A"),
        "N/A",
    )

    out_df["Special Circumstances"] = out_df["Special Circumstances"].replace("", np.nan).fillna("N/A")

    out_df = out_df[[
        "Season","Outcome","Special Circumstances","League","P","W","D","L","F","A","Pts","POS"
    ]]

    for c in ["P","W","D","L","F","A","Pts"]:
        out_df[c] = pd.to_numeric(out_df[c], errors="coerce")

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text("")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

