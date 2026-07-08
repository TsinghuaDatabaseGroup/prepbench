from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_scores = pd.read_csv(inputs_dir / "input_01.csv")

    df_meta = pd.read_csv(inputs_dir / "input_02.csv", skipinitialspace=True)
    df_meta.columns = [c.strip() for c in df_meta.columns]
    for col in df_meta.columns:
        if df_meta[col].dtype == object:
            df_meta[col] = df_meta[col].astype(str).str.strip()

    df_meta = df_meta.rename(columns={"Student ID": "Student ID"})

    subject_cols = [c for c in df_scores.columns if c != "Student ID"]
    df_long = df_scores.melt(
        id_vars=["Student ID"],
        value_vars=subject_cols,
        var_name="Subject",
        value_name="Grade",
    )

    df_long = df_long.merge(df_meta[["Student ID", "Class"]], on="Student ID", how="left")

    df_avg = (
        df_long.groupby(["Subject", "Class"], as_index=False)["Grade"]
        .mean()
    )

    df_avg["Grade"] = df_avg["Grade"].round(1)
    idx_min = df_avg.groupby("Subject")["Grade"].idxmin()
    df_worst = df_avg.loc[idx_min].copy()

    df_out = df_worst[["Subject", "Grade", "Class"]]

    df_out["Grade"] = pd.to_numeric(df_out["Grade"])

    df_out = df_out.sort_values(["Subject", "Class"]).reset_index(drop=True)

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for filename, df in results.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

