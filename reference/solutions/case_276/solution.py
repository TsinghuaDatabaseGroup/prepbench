from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def compute_loyalty_points(sales: pd.Series) -> pd.Series:
        points = sales.astype(float) / 50.0
        return points.round(1)

    def categorize_points(points: pd.Series) -> pd.Series:
        def label(x: float) -> str:
            if pd.isna(x):
                return "No Byte"
            if x >= 7:
                return "Mega Byte"
            if x >= 5:
                return "Byte"
            return "No Byte"

        return points.map(label)

    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df["Loyalty Points"] = compute_loyalty_points(df["Sale Total"].astype(float))
    df["Category"] = categorize_points(df["Loyalty Points"])

    df["Gender"] = df["Gender"].astype(str).str.strip().str.title()

    counts = df.groupby(["Category", "Gender"], as_index=False).size().rename(columns={"size": "Count"})

    totals = counts.groupby("Category", as_index=False)["Count"].sum().rename(columns={"Count": "Total"})
    counts = counts.merge(totals, on="Category", how="left")

    counts["Percentage"] = (counts["Count"] / counts["Total"]) * 100.0
    counts["Percentage"] = counts["Percentage"].round(1)

    pivot = counts.pivot(index="Category", columns="Gender", values="Percentage").reset_index()

    if "Female" not in pivot.columns:
        pivot["Female"] = 0.0
    if "Male" not in pivot.columns:
        pivot["Male"] = 0.0

    out = pivot[["Category", "Female", "Male"]].copy()
    out["Female"] = out["Female"].astype(float)
    out["Male"] = out["Male"].astype(float)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        (cand_dir / filename).write_text("") if data is None else None
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


