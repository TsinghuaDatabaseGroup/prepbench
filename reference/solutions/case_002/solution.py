from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    frames: list[pd.DataFrame] = []
    for p in sorted(inputs_dir.glob("*.csv")):
        df = pd.read_csv(p, dtype=str, keep_default_na=False)
        frames.append(df)

    raw = pd.concat(frames, ignore_index=True, sort=False)

    expected_cols = ["City", "Metric", "Measure", "Value", "Date"]
    for c in expected_cols:
        if c not in raw.columns:
            raw[c] = ""
    df = raw[expected_cols].copy()

    df = df.replace({"": np.nan})
    df = df.dropna(how="all")

    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df["Date_dt"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Value", "Date_dt", "City", "Metric", "Measure"])

    df["City_clean"] = df["City"]

    df["Metric_clean"] = df["Metric"].str.strip() + " - " + \
        df["Measure"].str.strip()

    required_metrics = [
        "Wind Speed - mph",
        "Max Temperature - Celsius",
        "Min Temperature - Celsius",
        "Precipitation - mm",
    ]
    df = df[df["Metric_clean"].isin(required_metrics)].copy()

    grp = (
        df.sort_values(["Date_dt"])
        .groupby(["City_clean", "Date_dt", "Metric_clean"], as_index=False)["Value"].first()
    )

    wide = grp.pivot_table(index=["City_clean", "Date_dt"],
                           columns="Metric_clean", values="Value", aggfunc="first").reset_index()
    for col in required_metrics:
        if col not in wide.columns:
            wide[col] = np.nan

    wide = wide[["City_clean", "Date_dt"] + required_metrics]

    wide = wide.rename(columns={
        "City_clean": "City",
        "Date_dt": "Date",
    })

    mask_dates = (wide["Date"] >= pd.Timestamp(2019, 2, 16)) & (
        wide["Date"] <= pd.Timestamp(2019, 2, 22))
    mask_cities = wide["City"].isin(["London", "Edinburgh"])
    wide = wide[mask_dates & mask_cities].copy()

    wide["Date"] = wide["Date"].dt.strftime("%d/%m/%Y")

    city_order = pd.Categorical(wide["City"], categories=[
                                "Edinburg", "Edinburgh", "London"], ordered=True)
    wide = wide.assign(_city_order=city_order)
    wide = wide.sort_values(by=["_city_order", "Date"]).drop(
        columns=["_city_order"]).reset_index(drop=True)

    for col in required_metrics:
        wide[col] = wide[col].astype("Int64").astype(int)

    final_cols = [
        "City",
        "Date",
        "Wind Speed - mph",
        "Max Temperature - Celsius",
        "Min Temperature - Celsius",
        "Precipitation - mm",
    ]
    wide = wide[final_cols]

    return {"output_01.csv": wide}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")
