from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    laps_fp = inputs_dir / "input_01.csv"
    drivers_fp = inputs_dir / "input_02.csv"
    df_laps = pd.read_csv(laps_fp)
    df_drivers = pd.read_csv(drivers_fp)

    df_laps["lap_duration"] = pd.to_numeric(df_laps["lap_duration"], errors="coerce")
    df_valid = df_laps.dropna(subset=["lap_duration", "driver_number"]).copy()

    df_best = (
        df_valid.sort_values(["driver_number", "lap_duration"])
        .groupby("driver_number", as_index=False).first()[["driver_number", "lap_duration"]]
    )

    df_out = df_best.merge(df_drivers, on="driver_number", how="left")

    df_out["Position"] = df_out["lap_duration"].rank(method="first", ascending=True).astype(int)

    df_out = df_out[[
        "Position",
        "driver_number",
        "driver_code",
        "driver_name",
        "constructor_sponsor_name",
        "lap_duration",
    ]]

    df_out = df_out.sort_values("Position").reset_index(drop=True)

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

