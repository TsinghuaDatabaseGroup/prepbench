from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df["Date_dt"] = pd.to_datetime(df["Date"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    df = df.sort_values("Date_dt").reset_index(drop=True)

    df["Moving Avg Sales"] = df["Sales"].rolling(window=7, min_periods=7).mean().round(2)

    df["Date"] = df["Date_dt"].dt.strftime("%d/%m/%Y")

    out = df[["Date", "Sales", "Moving Avg Sales"]]

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, sdf in outputs.items():
        sdf.to_csv(cand_dir / filename, index=False, encoding="utf-8")
