from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    couples_path = inputs_dir / "input_01.csv"
    gifts_path = inputs_dir / "input_02.csv"

    df_couples = pd.read_csv(couples_path)
    df_gifts = pd.read_csv(gifts_path)

    df_couples["Relationship Start"] = pd.to_datetime(df_couples["Relationship Start"], errors="coerce")

    today = pd.Timestamp(2024, 2, 14)

    def count_valentines(start: pd.Timestamp) -> int:
        if pd.isna(start):
            return 0
        if start > today:
            return 0
        start_year = start.year
        valentines_start_year = pd.Timestamp(start_year, 2, 14)
        count = 0
        for year in range(start_year, 2024 + 1):
            valentines_day = pd.Timestamp(year, 2, 14)
            if valentines_day >= start:
                count += 1
        return count

    df_couples["Number of Valentine's Days as a Couple"] = df_couples["Relationship Start"].apply(count_valentines)

    def to_ordinal(n: int) -> str:
        if 10 <= (n % 100) <= 13:
            suffix = "th"
        else:
            last = n % 10
            if last == 1:
                suffix = "st"
            elif last == 2:
                suffix = "nd"
            elif last == 3:
                suffix = "rd"
            else:
                suffix = "th"
        return f"{n}{suffix}"

    df_couples["Year"] = df_couples["Number of Valentine's Days as a Couple"].apply(to_ordinal)

    df_out = df_couples.merge(df_gifts, on="Year", how="left")

    df_out = df_out[[
        "Couple",
        "Number of Valentine's Days as a Couple",
        "Gift",
    ]]

    df_out = df_out.sort_values(["Number of Valentine's Days as a Couple", "Couple"], ascending=[True, True])

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    import sys

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

