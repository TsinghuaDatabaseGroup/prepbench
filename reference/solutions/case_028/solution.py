from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)

    header = df.iloc[0].fillna("")
    rename_map = {col: str(header[col]).strip() for col in df.columns if str(header[col]).strip()}
    df = df.rename(columns=rename_map).iloc[1:].reset_index(drop=True)

    interaction_cols = ["Manager", "Coworker", "Customer", "No One"]
    task_cols = ["On Task", "Off Task"]
    proximity_cols = ["Next to (<2m)", "Close to (<5m)", "Further(>5m)"]
    base_cols = ["Employee", "Observation Start Time", "Observation Interval", "Observation Length (mins)"]
    df = df[base_cols + interaction_cols + task_cols + proximity_cols]

    def pick_label(cols: list[str], default: str) -> pd.Series:
        mask = df[cols].eq("X")
        return mask.idxmax(axis=1).where(mask.any(axis=1), default)

    df["Interaction"] = pick_label(interaction_cols, "")
    df["Task Engagement"] = pick_label(task_cols, "")
    df["Manager Proximity"] = pick_label(proximity_cols, "NA")

    out = df[
        [
            "Task Engagement",
            "Manager Proximity",
            "Interaction",
            "Employee",
            "Observation Start Time",
            "Observation Length (mins)",
            "Observation Interval",
        ]
    ].copy()

    out["Observation Length (mins)"] = pd.to_numeric(out["Observation Length (mins)"], errors="coerce").astype(int)
    out["Observation Interval"] = pd.to_numeric(out["Observation Interval"], errors="coerce").astype(int)

    out = out.sort_values(["Employee", "Observation Interval"])
    base_date = pd.Timestamp("2019-08-16")
    base_time = pd.to_timedelta(out.groupby("Employee")["Observation Start Time"].transform("first"))
    offsets = out.groupby("Employee")["Observation Length (mins)"].shift(fill_value=0).groupby(out["Employee"]).cumsum()
    out["Observation Start Time"] = (
        base_date + base_time + pd.to_timedelta(offsets, unit="m")
    ).dt.strftime("%d/%m/%Y %H:%M:%S")

    sort_cols = [
        "Task Engagement",
        "Manager Proximity",
        "Interaction",
        "Employee",
        "Observation Start Time",
        "Observation Length (mins)",
        "Observation Interval",
    ]
    return {"output_01.csv": out.sort_values(sort_cols).reset_index(drop=True)}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

