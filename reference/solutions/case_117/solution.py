from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    in_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(in_path)

    df["Scheduled Date"] = pd.to_datetime(
        df["Scheduled Date"], format="%Y-%m-%d", errors="raise")
    df = df.rename(columns={
        "Completed In Days from Scheduled Date": "Days Difference to Schedule",
    })
    df["Days Difference to Schedule"] = pd.to_numeric(
        df["Days Difference to Schedule"], downcast="integer")

    df["Completed Date"] = df["Scheduled Date"] + \
        pd.to_timedelta(df["Days Difference to Schedule"], unit="D")

    grp_cols = ["Project", "Sub-project", "Owner"]
    pivot = (
        df.pivot_table(index=grp_cols, columns="Task",
                       values="Completed Date", aggfunc="first")
        .reset_index()
    )
    for task in ["Scope", "Build", "Deliver"]:
        if task not in pivot.columns:
            pivot[task] = pd.NaT

    pivot["Scope to Build Time"] = (pivot["Build"] - pivot["Scope"]).dt.days
    pivot["Build to Delivery Time"] = (
        pivot["Deliver"] - pivot["Build"]).dt.days

    df = df.merge(
        pivot[grp_cols + ["Scope to Build Time", "Build to Delivery Time"]],
        on=grp_cols,
        how="left",
    )

    df["Completed Weekday"] = df["Completed Date"].dt.day_name()

    group_order = (
        df[grp_cols]
        .drop_duplicates()
        .reset_index(drop=True)
        .assign(__grp_order=lambda _d: range(len(_d)))
    )
    df = df.merge(group_order, on=grp_cols, how="left")
    task_cat = pd.CategoricalDtype(["Scope", "Build", "Deliver"], ordered=True)
    df["Task"] = df["Task"].astype(task_cat)
    df = df.sort_values(["__grp_order", "Task"], kind="stable").drop(
        columns=["__grp_order"])

    df_out = df.copy()
    for col in ["Scheduled Date", "Completed Date"]:
        df_out[col] = df_out[col].dt.strftime("%d/%m/%Y")

    out_cols = [
        "Completed Weekday",
        "Task",
        "Scope to Build Time",
        "Build to Delivery Time",
        "Days Difference to Schedule",
        "Project",
        "Sub-project",
        "Owner",
        "Scheduled Date",
        "Completed Date",
    ]
    df_out = df_out[out_cols]

    for col in ["Scope to Build Time", "Build to Delivery Time", "Days Difference to Schedule"]:
        df_out[col] = pd.to_numeric(df_out[col], downcast="integer")

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
