from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    is_dash = df["Gap"] == "-"
    time_parts = df["Gap"].str.extract(
        r"^\+\s*(\d{2})h\s*(\d{2})'\s*(\d{2})''$").fillna(0).astype(int)
    df["gap_minutes"] = np.where(
        is_dash,
        0.0,
        (time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]) / 60.0
    )

    grp = df.groupby("Team", as_index=False).agg(
        avg_gap_min=("gap_minutes", "mean"),
        riders=("Rider", "count"),
    )

    grp["Team Avg Gap in Mins"] = np.floor(grp["avg_gap_min"]).astype(int)
    grp["Number of Riders"] = grp["riders"].astype(int)
    grp = grp[grp["Number of Riders"] >= 7]

    out = grp.sort_values(["Team Avg Gap in Mins", "Team"]).head(2)[
        ["Team Avg Gap in Mins", "Team", "Number of Riders"]
    ].reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
