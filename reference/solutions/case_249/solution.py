from pathlib import Path
from typing import Dict

import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    df = df[df["Arrival Time"].notna()].copy()

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
    df["ScheduledDT"] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Scheduled Start Time"])
    df["ArrivalDT"] = pd.to_datetime(df["Date"].dt.strftime("%Y-%m-%d") + " " + df["Arrival Time"])

    df["LatenessSeconds"] = (df["ArrivalDT"] - df["ScheduledDT"]).dt.total_seconds()

    grp = df.groupby("Day of Week", as_index=False)["LatenessSeconds"].mean()

    grp["LatenessSecondsRounded"] = grp["LatenessSeconds"].round().astype(int)
    grp["LatenessSecondsRounded"] = grp["LatenessSecondsRounded"].clip(lower=0)
    grp["Minutes Late"] = (grp["LatenessSecondsRounded"] // 60).astype(int)
    grp["Seconds Late"] = (grp["LatenessSecondsRounded"] % 60).astype(int)

    grp = grp.sort_values("LatenessSecondsRounded", ascending=False).reset_index(drop=True)
    grp["Rank"] = np.arange(1, len(grp) + 1)

    out1 = grp[["Rank", "Day of Week", "Minutes Late", "Seconds Late"]].copy()
    out1 = out1.rename(columns={"Day of Week": "Day of the Week"})

    VERY_LATE_THRESHOLD = 5 * 60
    per_student = (
        df.groupby("Student ID")
        .agg(
            present_days=("ArrivalDT", "count"),
            very_late_days=("LatenessSeconds", lambda s: (s > VERY_LATE_THRESHOLD).sum()),
        )
        .reset_index()
    )
    per_student["% Days Very Late"] = (per_student["very_late_days"] / per_student["present_days"]) * 100
    per_student["% Days Very Late"] = per_student["% Days Very Late"].round(1)

    per_student = per_student.sort_values(["% Days Very Late", "Student ID"], ascending=[False, True]).reset_index(drop=True)
    per_student["Rank"] = np.arange(1, len(per_student) + 1)

    out2 = per_student[["Rank", "Student ID", "% Days Very Late"]].copy()

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

