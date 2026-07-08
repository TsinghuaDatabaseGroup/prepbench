import pandas as pd
from pathlib import Path
from typing import Dict
from dateutil.easter import easter as easter_sunday
from datetime import timedelta


WEEKDAY_ABBR = {
    0: ("M", 1),
    1: ("Tu", 2),
    2: ("W", 3),
    3: ("Th", 4),
    4: ("F", 5),
    5: ("Sa", 6),
    6: ("Su", 7),
}


def compute_easter_week_number(dates: pd.Series) -> pd.Series:
    years = dates.dt.year
    easter_monday_pydate = years.map(lambda y: easter_sunday(
        int(y)) - timedelta(days=easter_sunday(int(y)).weekday()))
    easter_monday = pd.to_datetime(easter_monday_pydate)
    week1_monday = easter_monday - pd.to_timedelta(11 * 7, unit="D")
    week_num = ((dates.dt.normalize() - week1_monday) //
                pd.Timedelta(days=7)) + 1
    return week_num.astype(int)


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_files = sorted((inputs_dir).glob("input_*.csv"))
    frames = []
    for f in input_files:
        df = pd.read_csv(f)
        frames.append(df)
    data = pd.concat(frames, ignore_index=True)

    data["Sales Date"] = pd.to_datetime(data["Sales Date"], errors="coerce")

    data["Year"] = data["Sales Date"].dt.year

    data["Easter Week Number"] = compute_easter_week_number(data["Sales Date"])

    weekday_num = data["Sales Date"].dt.weekday
    data["Weekday"] = weekday_num.map(lambda d: WEEKDAY_ABBR[int(d)][0])
    data["Weekday Order"] = weekday_num.map(lambda d: WEEKDAY_ABBR[int(d)][1])

    data["Sales"] = data["Price"].astype(
        float) * data["Quantity Sold"].astype(float)

    data["Sales Date"] = data["Sales Date"].dt.strftime("%d/%m/%Y")

    output_cols = [
        "Year",
        "Sales Date",
        "Easter Week Number",
        "Weekday",
        "Weekday Order",
        "Product",
        "Price",
        "Quantity Sold",
        "Sales",
    ]

    out = data[output_cols].copy()

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
