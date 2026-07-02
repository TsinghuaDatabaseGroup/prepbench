from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    src = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)

    src.columns = [c.strip() for c in src.columns]

    dt = pd.to_datetime(src["Date"].str.strip(
    ) + " " + src["Time"].str.strip(), dayfirst=True, errors="coerce")
    src["Datetime"] = dt

    src["Batch No."] = src["Batch No."].astype(int)

    result_mask = src["Data Type"].eq("Result Data")
    results = src.loc[result_mask, ["Batch No.",
                                    "Data Parameter", "Data Value", "Datetime"]].copy()

    results.sort_values(["Batch No.", "Datetime"], inplace=True)
    bike_type_map = (results[results["Data Parameter"].eq("Bike Type")]
                     .dropna(subset=["Data Value"])
                     .groupby("Batch No.")
                     ["Data Value"].last())
    batch_status_map = (results[results["Data Parameter"].eq("Batch Status")]
                        .dropna(subset=["Data Value"])
                        .groupby("Batch No.")
                        ["Data Value"].last())

    proc = src[src["Data Type"].eq("Process Data")].copy()

    is_stage = proc["Data Parameter"].eq("Name of Process Stage")

    proc.sort_values(["Batch No.", "Datetime"], inplace=True)
    proc["Name of Process Step"] = np.where(
        is_stage, proc["Data Value"], np.nan)
    proc["Name of Process Step"] = proc.groupby(
        "Batch No.")["Name of Process Step"].ffill()

    proc_params = proc.loc[~is_stage].copy()

    def parse_param(s: str) -> tuple[str | None, str | None]:
        if not isinstance(s, str):
            return None, None
        s = s.strip()
        if s.startswith("Target "):
            return "Target", s[len("Target "):]
        if s.startswith("Actual "):
            return "Actual", s[len("Actual "):]
        return None, None

    kinds, params = zip(*proc_params["Data Parameter"].map(parse_param))
    proc_params["kind"] = list(kinds)
    proc_params["Data Parameter Clean"] = list(params)

    wanted = {"Current", "Voltage", "Gas Flow", "Temperature", "Pressure"}
    proc_params = proc_params[proc_params["Data Parameter Clean"].isin(
        wanted)].copy()

    proc_params["Target"] = np.where(proc_params["kind"].eq(
        "Target"), proc_params["Data Value"], np.nan)
    proc_params["Actual"] = np.where(proc_params["kind"].eq(
        "Actual"), proc_params["Data Value"], np.nan)

    proc_params["Target"] = pd.to_numeric(
        proc_params["Target"], errors="coerce")
    proc_params["Actual"] = pd.to_numeric(
        proc_params["Actual"], errors="coerce")

    proc_params["Bike Type"] = proc_params["Batch No."].map(bike_type_map)
    bs = proc_params["Batch No."].map(batch_status_map)
    with np.errstate(all='ignore'):
        proc_params["Batch Status"] = pd.to_numeric(
            bs, errors="coerce").astype("Int64")
    proc_params.loc[proc_params["Batch Status"].isna(
    ), "Batch Status"] = bs[proc_params["Batch Status"].isna()].astype(str)
    try:
        proc_params["Batch Status"] = proc_params["Batch Status"].astype(int)
    except Exception:
        pass

    if "Data Parameter" in proc_params.columns:
        proc_params.drop(columns=["Data Parameter"], inplace=True)
    proc_params.rename(
        columns={"Data Parameter Clean": "Data Parameter"}, inplace=True)

    out = proc_params[[
        "Batch No.",
        "Name of Process Step",
        "Bike Type",
        "Batch Status",
        "Datetime",
        "Data Parameter",
        "Target",
        "Actual",
    ]].copy()

    out["Datetime"] = pd.to_datetime(
        out["Datetime"]).dt.strftime("%d/%m/%Y %H:%M:%S")

    out.sort_values(["Batch No.", "Datetime",
                    "Name of Process Step", "Data Parameter"], inplace=True)
    out.reset_index(drop=True, inplace=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
