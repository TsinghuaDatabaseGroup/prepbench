from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_grand = pd.read_csv(inputs_dir / "input_01.csv")
    df_stage_types = pd.read_csv(inputs_dir / "input_02.csv")
    df_stages = pd.read_csv(inputs_dir / "input_03.csv")
    df_wins = pd.read_csv(inputs_dir / "input_04.csv")

    df_stage_types["Stage Type ID"] = df_stage_types["Stage Type ID"].astype(float)
    id_to_type = dict(zip(df_stage_types["Stage Type ID"], df_stage_types["Stage Type"]))

    stages = df_stages.copy()
    stages = stages[~stages["Stage"].fillna("").str.contains("Restday", case=False, na=False)]

    def parse_stage_number(stage_str: str) -> int:
        s = str(stage_str)
        if s.startswith("Prologue"):
            return 0
        try:
            after = s.split("Stage ", 1)[1]
            num_part = after.split(" ", 1)[0]
            return int(num_part)
        except Exception:
            return None

    def parse_origin_dest(stage_str: str) -> str:
        s = str(stage_str)
        if "|" in s:
            return s.split("|", 1)[1].strip()
        return s.strip()

    def parse_time_trial(stage_str: str) -> str:
        s = str(stage_str)
        if "(ITT)" in s:
            return "Individual"
        if "(TTT)" in s:
            return "Team"
        return ""

    stages["Stage Number"] = stages["Stage"].apply(parse_stage_number)
    stages["Origin - Destination"] = stages["Stage"].apply(parse_origin_dest)
    stages["Time Trial?"] = stages["Stage"].apply(parse_time_trial)
    stages["Stage Type"] = stages["Stage Type"].astype(float).map(id_to_type)
    stages = stages[[
        "Year",
        "Stage Number",
        "Origin - Destination",
        "Time Trial?",
        "KM",
        "Stage Type",
    ]].dropna(subset=["Stage Number"]).copy()

    wins = df_wins.copy()
    wins = wins[wins["Race"].str.contains(r"Tour de France \| Stage", regex=True, na=False)]
    wins["Year"] = pd.to_datetime(wins["Date"]).dt.year
    wins["Stage Number"] = wins["Race"].str.extract(r"Stage\s+(\d+)").astype(int)
    wins_key = wins[["Year", "Stage Number"]].drop_duplicates()
    wins_key["Stage Won?"] = True

    out = stages.merge(wins_key, on=["Year", "Stage Number"], how="left")
    out["Stage Won?"] = out["Stage Won?"].fillna(False).astype(bool).map(lambda x: "Yes" if x else "")

    ans = df_grand.copy()
    ans = ans[ans["Grand tour"].str.strip().str.lower() == "tour de france"].copy()
    ans = ans.rename(columns={
        "Season": "Year",
        "GC": "General Classification Finishing Position",
        "Points": "Points Finishing Position",
    })
    ans = ans[["Year", "General Classification Finishing Position", "Points Finishing Position"]].copy()
    ans["General Classification Finishing Position"] = ans["General Classification Finishing Position"].astype(str)
    ans["Points Finishing Position"] = pd.to_numeric(ans["Points Finishing Position"], errors="coerce")

    out = out.merge(ans, on="Year", how="left")

    out = out[[
        "Stage Won?",
        "Stage Number",
        "Origin - Destination",
        "Time Trial?",
        "General Classification Finishing Position",
        "Points Finishing Position",
        "Year",
        "KM",
        "Stage Type",
    ]].copy()

    out["Stage Number"] = out["Stage Number"].astype(int)
    out["Year"] = out["Year"].astype(int)
    out["KM"] = pd.to_numeric(out["KM"], errors="coerce")

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


