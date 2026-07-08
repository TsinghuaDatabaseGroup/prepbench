from __future__ import annotations
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv)

    store_bike_split = df["Store - Bike"].str.split(" - ", n=1, expand=True)
    df["Store"] = store_bike_split[0].str.strip()
    df["Bike"] = store_bike_split[1].str.strip()

    def clean_bike(bike_str):
        bike_str = bike_str.strip()
        if bike_str in ["Graval", "Gravle"]:
            return "Gravel"
        elif bike_str == "Mountaen":
            return "Mountain"
        elif bike_str in ["Rood", "Rowd"]:
            return "Road"
        elif bike_str in ["Mountain", "Gravel", "Road"]:
            return bike_str
        else:
            return bike_str

    df["Bike"] = df["Bike"].apply(clean_bike)

    date_series = pd.to_datetime(
        df["Date"], format="%Y-%m-%d", errors="coerce")
    df["Quarter"] = date_series.dt.quarter
    df["Day of Month"] = date_series.dt.day

    df = df[df["Order ID"] > 10].copy()

    output_df = df[[
        "Quarter",
        "Day of Month",
        "Store",
        "Bike",
        "Order ID",
        "Customer Age",
        "Bike Value",
        "Existing Customer?"
    ]].copy()

    output_df = output_df.reset_index(drop=True)

    return {
        "output_01.csv": output_df,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
