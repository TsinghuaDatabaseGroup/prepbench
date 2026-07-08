from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_bench = pd.read_csv(inputs_dir / "input_01.csv")
    df_students = pd.read_csv(inputs_dir / "input_02.csv")
    df_times = pd.read_csv(inputs_dir / "input_03.csv")

    df_bench.columns = [c.strip() for c in df_bench.columns]
    for c in df_bench.columns:
        if df_bench[c].dtype == object:
            df_bench[c] = df_bench[c].astype(str).str.strip()
    df_times["track_event"] = df_times["track_event"].astype(str).str.strip()
    df = pd.merge(df_students, df_times, on="id", how="inner")
    df["gender"] = df["gender"].astype(str).str.strip()
    df_bench["Gender"] = df_bench["Gender"].astype(str).str.strip()
    df = pd.merge(
        df,
        df_bench.rename(columns={"Age": "Age_bench"}),
        left_on=["gender", "age", "track_event"],
        right_on=["Gender", "Age_bench", "Event"],
        how="left",
    )
    df = df.drop(columns=["Gender", "Age_bench", "Event"])
    df = df[df["time"] <= df["Benchmark"]]
    df = df[~((df["track_event"] == "200m") & (df["time"] < 25.0))]
    out = df.rename(
        columns={
            "first_name": "first_name",
            "last_name": "last_name",
            "gender": "Gender",
            "age": "Age",
            "track_event": "Event",
            "time": "time",
        }
    )[["id", "first_name", "last_name", "Gender", "Age", "Event", "time", "Benchmark"]].copy()
    out["Rank"] = out.groupby("Event")["time"].rank(method="min", ascending=True).astype(int)
    out = out[["Rank", "id", "first_name", "last_name", "Gender", "Age", "Event", "time", "Benchmark"]]
    out = out.sort_values(by=["Event", "Rank", "time", "id"]).reset_index(drop=True)
    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


