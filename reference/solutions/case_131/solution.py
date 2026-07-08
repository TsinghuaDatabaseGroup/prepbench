from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df["Date of Flight"] = pd.to_datetime(df["Date of Flight"], format="%d/%m/%Y")

    df["Flight"] = df["Departure"] + " to " + df["Destination"]

    df["days_until"] = (df["Date of Flight"] - df["Date"]).dt.days

    df["bucket"] = np.where(df["days_until"] < 7, "lt7", "ge7")

    grouped = df.groupby(["Flight", "Class", "bucket"])["Ticket Sales"].agg(total='sum', avg='mean')

    unstacked = grouped.unstack(level='bucket', fill_value=0)

    unstacked.columns = ['_'.join(col).strip() for col in unstacked.columns.values]
    unstacked = unstacked.reset_index()

    required_cols = {
        'total_ge7': 0,
        'total_lt7': 0,
        'avg_ge7': 0.0,
        'avg_lt7': 0.0
    }
    for col, default_val in required_cols.items():
        if col not in unstacked.columns:
            unstacked[col] = default_val

    final = pd.DataFrame({
        "Flight": unstacked["Flight"],
        "Class": unstacked["Class"],
        "Avg. daily sales 7 days or more until the flight": unstacked['avg_ge7'].round(0).astype(int),
        "Avg. daily sales less than 7 days until the flight": unstacked['avg_lt7'].round(0).astype(int),
        "Sales less than 7 days until the flight": unstacked['total_lt7'].round(0).astype(int),
        "Sales 7 days or more until the flight": unstacked['total_ge7'].round(0).astype(int),
    })

    final = final[[
        "Flight",
        "Class",
        "Avg. daily sales 7 days or more until the flight",
        "Avg. daily sales less than 7 days until the flight",
        "Sales less than 7 days until the flight",
        "Sales 7 days or more until the flight",
    ]]

    return {"output_01.csv": final}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    out_map = solve(inputs_dir)
    for fname, df in out_map.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
