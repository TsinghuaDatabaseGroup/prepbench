from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df_pat = pd.read_csv(inputs_dir / "input_01.csv", parse_dates=["First Visit"])
    df_scaffold = pd.read_csv(inputs_dir / "input_02.csv")
    
    df_scaffold = df_scaffold[df_scaffold["Value"] >= 1].copy()
    df_scaffold = df_scaffold.rename(columns={"Value": "DayIndex"})
    
    df_pat["_key"] = 1
    df_scaffold["_key"] = 1
    daily = pd.merge(df_pat, df_scaffold, on="_key").drop(columns="_key")
    
    daily = daily[daily["DayIndex"] <= daily["Length of Stay"]].copy()
    
    daily["Date"] = daily["First Visit"] + pd.to_timedelta(daily["DayIndex"] - 1, unit="D")
    daily["Cost per Day"] = pd.cut(daily["DayIndex"], bins=[0, 3, 7, float("inf")], labels=[100, 80, 75]).astype(int)

    out2 = daily.groupby("Date", as_index=False).agg(**{
        "Cost per Day": ("Cost per Day", "sum"),
        "Number of Patients": ("Name", "nunique"),
    })
    out2["Avg Cost per Day"] = (out2["Cost per Day"] / out2["Number of Patients"]).round(2)
    out2["Date"] = out2["Date"].dt.strftime("%d/%m/%Y")
    out2 = out2[["Avg Cost per Day", "Date", "Cost per Day", "Number of Patients"]]

    per_person = daily.groupby("Name", as_index=False).agg(**{
        "Cost": ("Cost per Day", "sum"),
        "Days": ("DayIndex", "max"),
    })
    per_person["Avg Cost per Day per person"] = (per_person["Cost"] / per_person["Days"]).round(2)
    out1 = per_person[["Cost", "Name", "Avg Cost per Day per person"]]

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

