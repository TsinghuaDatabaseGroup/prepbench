from pathlib import Path
from typing import Dict
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="raise")

    valentines = pd.Timestamp("2019-02-14")
    df["Pre / Post Valentines Day"] = df["Date"].apply(lambda d: "Pre" if d <= valentines else "Post")

    df["Daily Store Sales"] = df["Value"].astype(int)

    df = df.sort_values(["Store", "Pre / Post Valentines Day", "Date"]).copy()
    df["Running Total Sales"] = df.groupby(["Store", "Pre / Post Valentines Day"])['Daily Store Sales'].cumsum()

    out = df[[
        "Pre / Post Valentines Day",
        "Store",
        "Date",
        "Running Total Sales",
        "Daily Store Sales",
    ]].copy()
    out["Date"] = out["Date"].dt.strftime("%d/%m/%Y")

    out["Running Total Sales"] = pd.to_numeric(out["Running Total Sales"]) 
    out["Daily Store Sales"] = pd.to_numeric(out["Daily Store Sales"]) 

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
