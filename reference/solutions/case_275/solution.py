from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve() -> Dict[str, pd.DataFrame]:
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    df_names = pd.read_csv(inputs_dir / "input_01.csv")
    df_txn = pd.read_csv(inputs_dir / "input_02.csv")

    df_txn["Date"] = pd.to_datetime(df_txn["Date"], errors="coerce")

    df = df_txn.merge(
        df_names[["First Name", "Last Name", "Customer ID"]],
        on=["First Name", "Last Name"],
        how="left",
    )

    def channel(row: pd.Series) -> str:
        if str(row.get("Online", "")).strip().lower() == "yes":
            return "Online"
        return "In-Person"

    df["Online or In Person"] = df.apply(channel, axis=1)

    df["Weekday"] = df["Date"].dt.day_name()

    df["Sales"] = pd.to_numeric(df["Sale Total"], errors="coerce")

    df = df[df["Weekday"] == "Monday"].copy()

    df = df.sort_values(["Sales", "Receipt Number"], ascending=[False, True])
    df["Rank"] = df["Sales"].rank(method="min", ascending=False).astype(int)

    out_cols = [
        "Rank",
        "Customer ID",
        "Receipt Number",
        "Gender",
        "Online or In Person",
        "Sales",
        "Weekday",
    ]

    out = df[out_cols].copy()

    return {
        "output_01.csv": out,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve()
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
