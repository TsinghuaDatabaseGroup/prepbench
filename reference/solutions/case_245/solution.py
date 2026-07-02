from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    y5_details = pd.read_csv(inputs_dir / "input_01.csv")
    y5_choices = pd.read_csv(inputs_dir / "input_02.csv")
    y6_details = pd.read_csv(inputs_dir / "input_03.csv")
    y6_choices = pd.read_csv(inputs_dir / "input_04.csv")

    y5 = y5_details.merge(y5_choices, on="Full Name", how="left")
    y6 = y6_details.merge(y6_choices, on="Full Name", how="left")

    all_students = pd.concat([y5, y6], ignore_index=True)

    song_col = None
    if "Song Recommendation" in all_students.columns and "Song Choice" in all_students.columns:
        all_students["Song"] = all_students["Song Recommendation"].where(
            all_students["Song Recommendation"].notna(), all_students["Song Choice"]
        )
        song_col = "Song"
    elif "Song Recommendation" in all_students.columns:
        song_col = "Song Recommendation"
        all_students["Song"] = all_students[song_col]
    elif "Song Choice" in all_students.columns:
        song_col = "Song Choice"
        all_students["Song"] = all_students[song_col]
    else:
        all_students["Song"] = pd.NA

    grouped = (
        all_students.groupby(["Year Group", "Song"], dropna=False)
        .agg(**{"Number of Votes": ("Full Name", "count")})
        .reset_index()
    )

    grouped = grouped[grouped["Number of Votes"] >= 5]

    output = grouped.rename(columns={"Song": "Song Recommendation"})
    output = output[["Number of Votes", "Year Group", "Song Recommendation"]]

    output = output.sort_values(by=["Year Group", "Number of Votes", "Song Recommendation"], ascending=[True, False, True])
    output = output.reset_index(drop=True)

    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

