from __future__ import annotations

from pathlib import Path

import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    actions_path = inputs_dir / "input_01.csv"
    details_path = inputs_dir / "input_02.csv"

    actions = pd.read_csv(actions_path)
    details = pd.read_csv(details_path)

    cancelled_flag = (
        actions.groupby(["Flight Number", "Customer ID"])["Action"]
        .transform(lambda s: (s == "Cancelled").any())
    )
    actions = actions[~cancelled_flag].copy()

    actions["Date_dt"] = pd.to_datetime(actions["Date"], format="%Y-%m-%d")
    most_recent_date = (
        actions.groupby(["Flight Number", "Customer ID"])[
            "Date_dt"].transform("max")
    )
    actions = actions[actions["Date_dt"] == most_recent_date].copy()

    if "Row" in actions.columns:
        actions["Row"] = actions["Row"].astype("Int64")
    if "Seat" in actions.columns:
        actions["Seat"] = actions["Seat"].astype("Int64")

    actions["Customer ID"] = (
        actions["Customer ID"]
        .astype("Int64")
        .astype("string")
        .str.zfill(9)
    )

    actions = actions.sort_values(
        by=["Flight Number", "Class", "Date_dt", "Row", "Seat", "Customer ID"],
        ascending=[True, True, True, True, True, True],
    )

    actions["Number of seats"] = 1
    actions["Total Seats booked over time"] = actions.groupby(
        ["Flight Number", "Class"]
    )["Number of seats"].cumsum()
    actions = actions.drop(columns=["Number of seats"])

    if "Flight Date" in actions.columns:
        actions = actions.rename(
            columns={"Flight Date": "Flight Date_actions"})

    merged = details.merge(
        actions,
        on=["Flight Number", "Class"],
        how="left",
        sort=False,
    )

    merged["Total Seats booked over time"] = (
        merged["Total Seats booked over time"].fillna(0).astype(int)
    )

    merged["Flight Date"] = pd.to_datetime(
        merged["Flight Date"], format="%Y-%m-%d"
    )
    merged["Date_dt"] = pd.to_datetime(merged["Date_dt"])
    merged["Date_dt"] = merged["Date_dt"].fillna(pd.Timestamp(2024, 2, 28))

    merged["Flight Date"] = merged["Flight Date"].dt.strftime("%d/%m/%Y")
    merged["Date"] = merged["Date_dt"].dt.strftime("%d/%m/%Y")

    merged["Capacity %"] = (
        merged["Total Seats booked over time"] / merged["Capacity"]
    )

    out_cols = [
        "Flight Number",
        "Flight Date",
        "Class",
        "Total Seats booked over time",
        "Capacity",
        "Capacity %",
        "Customer ID",
        "Action",
        "Date",
        "Row",
        "Seat",
    ]
    output_df = merged[out_cols].copy()

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
