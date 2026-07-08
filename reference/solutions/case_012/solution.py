from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_auto = pd.read_csv(inputs_dir / "input_01.csv")
    df_auto["Start Date / Time"] = pd.to_datetime(df_auto["Start Date / Time"])
    df_auto["End Date / Time"] = pd.to_datetime(df_auto["End Date / Time"])
    df_auto["Error Source"] = "Automatic Error log"
    df_auto = df_auto[["Start Date / Time",
                       "End Date / Time", "System", "Error", "Error Source"]]

    df_manual = pd.read_csv(inputs_dir / "input_02.csv")
    df_manual["Start Date / Time"] = pd.to_datetime(
        df_manual["Start Date"].astype(
            str) + " " + df_manual["Start Time"].astype(str)
    )
    df_manual["End Date / Time"] = pd.to_datetime(
        df_manual["End Date"].astype(
            str) + " " + df_manual["End Time"].astype(str)
    )
    df_manual["Error"] = df_manual["Error"].replace(
        {"Planed Outage": "Planned Outage"})
    df_manual["Error Source"] = "Manual capture error list"
    df_manual = df_manual[["Start Date / Time",
                           "End Date / Time", "System", "Error", "Error Source"]]

    df_auto_overlap = df_auto[["System", "Start Date / Time", "End Date / Time"]].rename(
        columns={"Start Date / Time": "auto_start",
                 "End Date / Time": "auto_end"}
    )
    df_manual_overlap = df_manual[[
        "System", "Start Date / Time", "End Date / Time"]].copy()
    df_manual_overlap["_idx"] = df_manual_overlap.index

    overlap_check = df_manual_overlap.merge(
        df_auto_overlap, on="System", how="left")
    overlap_check["_is_overlap"] = (
        (overlap_check["auto_start"] < overlap_check["End Date / Time"])
        & (overlap_check["auto_end"] > overlap_check["Start Date / Time"])
    ).fillna(False)
    manual_has_overlap = overlap_check.groupby("_idx")["_is_overlap"].any()
    df_manual_keep = df_manual.loc[~df_manual.index.isin(
        manual_has_overlap[manual_has_overlap].index)].copy()

    df_manual_keep = df_manual_keep.sort_values(
        "Start Date / Time", ascending=False).reset_index(drop=True)

    df_all = pd.concat([df_auto, df_manual_keep], ignore_index=True)

    df_all["_hours_true"] = (df_all["End Date / Time"] -
                             df_all["Start Date / Time"]).dt.total_seconds() / 3600.0
    df_all["Downtime in Hours"] = df_all["_hours_true"].round(1)
    total_per_sys_display = df_all.groupby(
        "System")["Downtime in Hours"].sum().round(1)
    total_per_sys_true = df_all.groupby("System")["_hours_true"].sum()

    df_all = df_all.merge(
        total_per_sys_display.rename("Total Downtime in Hours"), left_on="System", right_index=True, how="left"
    ).merge(
        total_per_sys_true.rename("_total_true"), left_on="System", right_index=True, how="left"
    )
    df_all["% of system downtime"] = (
        df_all["_hours_true"] / df_all["_total_true"]).round(2)

    df_all_out = pd.DataFrame({
        "% of system downtime": df_all["% of system downtime"],
        "Total Downtime in Hours": df_all["Total Downtime in Hours"],
        "Downtime in Hours": df_all["Downtime in Hours"],
        "Error Source": df_all["Error Source"],
        "Error": df_all["Error"],
        "Start Date / Time": df_all["Start Date / Time"].dt.strftime("%d/%m/%Y %H:%M"),
        "End Date / Time": df_all["End Date / Time"].dt.strftime("%d/%m/%Y %H:%M"),
        "System": df_all["System"],
    })

    return {"output_01.csv": df_all_out}


if __name__ == "__main__":
    import sys

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        out_fp = cand_dir / filename
        df.to_csv(out_fp, index=False, encoding="utf-8")
