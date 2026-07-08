import pandas as pd
from pathlib import Path
from datetime import date, timedelta
from typing import Dict
import math


def monday_before_feb_1(year: int) -> date:
    feb1 = date(year, 2, 1)
    wd = feb1.weekday()
    days_back = wd + 7 if wd == 0 else wd
    return feb1 - timedelta(days=days_back)


def compute_reporting_fields(d: date, selected_year: int) -> Dict[str, int]:
    start_selected = monday_before_feb_1(selected_year)
    if d >= start_selected:
        reporting_year = selected_year
    else:
        reporting_year = selected_year - 1

    start_ry = monday_before_feb_1(reporting_year)
    reporting_day = (d - start_ry).days + 1
    reporting_week = math.ceil(reporting_day / 7)
    reporting_month = math.ceil(reporting_week / 4)

    return {
        "Reporting Year": reporting_year,
        "Reporting Month": reporting_month,
        "Reporting Week": reporting_week,
        "Reporting Day": reporting_day,
    }


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    inp = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    year = int(inp.loc[0, "Year"])

    start_d = date(year, 1, 1)
    end_d = date(year, 12, 31)
    all_dates = [start_d + timedelta(days=i) for i in range((end_d - start_d).days + 1)]

    rows = []
    for d in all_dates:
        fields = compute_reporting_fields(d, year)
        rows.append({
            "Calendar Date": d.strftime("%d/%m/%Y"),
            **fields,
        })

    out = pd.DataFrame(rows, columns=[
        "Calendar Date",
        "Reporting Year",
        "Reporting Month",
        "Reporting Week",
        "Reporting Day",
    ])

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        df.to_csv(cand_dir / name, index=False, encoding="utf-8")


















