from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd

CURRENT_END_DATE = pd.Timestamp("2024-06-12")
WEEKS_PER_YEAR = 52


def _parse_start_date(value: object) -> pd.Timestamp:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return pd.NaT
    return pd.to_datetime(text.split(" ")[0], format="%Y-%m-%d", errors="coerce")


def _parse_end_date(value: object) -> pd.Timestamp:
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return pd.NaT
    if text.lower().startswith("current"):
        return CURRENT_END_DATE
    return pd.to_datetime(text.split(" ")[0], format="%Y-%m-%d", errors="coerce")


def _align_start(date_value: pd.Timestamp) -> pd.Timestamp:
    days_until_sunday = (6 - date_value.weekday()) % 7
    return (date_value + pd.Timedelta(days=days_until_sunday)).normalize()


def _align_end(date_value: pd.Timestamp) -> pd.Timestamp:
    days_since_sunday = (date_value.weekday() - 6) % 7
    return (date_value - pd.Timedelta(days=days_since_sunday)).normalize()


def _expand_weekly_rows(df: pd.DataFrame) -> pd.DataFrame:
    records: List[dict[str, object]] = []
    for row in df.itertuples(index=False):
        start: pd.Timestamp = row.start_date
        end: pd.Timestamp = row.end_date
        salary: float = row.salary
        if pd.isna(start) or pd.isna(end) or pd.isna(salary):
            continue
        aligned_start = _align_start(start)
        aligned_end = _align_end(end)
        if aligned_end < aligned_start:
            continue
        weekly_salary = salary / WEEKS_PER_YEAR
        week_dates = pd.date_range(
            start=aligned_start, end=aligned_end, freq="7D")
        for week_date in week_dates:
            records.append(
                {
                    "Week": week_date,
                    "Weekly Salary": weekly_salary,
                }
            )
    return pd.DataFrame(records, columns=["Week", "Weekly Salary"])


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    managers = pd.read_csv(inputs_dir / "input_01.csv")
    expenses = pd.read_csv(inputs_dir / "input_02.csv")

    managers["start_date"] = managers["Start Date"].apply(
        _parse_start_date).dt.normalize()
    managers["end_date"] = managers["End Date"].apply(
        _parse_end_date).dt.normalize()
    managers["salary"] = pd.to_numeric(managers["Salary"], errors="coerce")

    weekly_detail = _expand_weekly_rows(
        managers[["start_date", "end_date", "salary"]])

    weekly_totals = (
        weekly_detail.groupby("Week", as_index=False)["Weekly Salary"].sum()
        if not weekly_detail.empty
        else pd.DataFrame(columns=["Week", "Weekly Salary"])
    )
    weekly_totals.rename(
        columns={"Weekly Salary": "Salary Payments"}, inplace=True)
    weekly_totals["Salary Payments"] = weekly_totals["Salary Payments"].round(
        2)
    weekly_totals.sort_values("Week", inplace=True)
    weekly_totals["Week"] = weekly_totals["Week"].dt.strftime("%d/%m/%Y")

    if weekly_detail.empty:
        annual = pd.DataFrame(columns=["Year", "% Spent on Manager Salaries"])
    else:
        weekly_detail["Year"] = weekly_detail["Week"].dt.year
        annual_salary = (
            weekly_detail.groupby("Year", as_index=False)[
                "Weekly Salary"].sum()
        )
        annual_salary["Weekly Salary"] = annual_salary["Weekly Salary"].round(
            2)
        expenses["Year"] = pd.to_numeric(
            expenses["Year"], errors="coerce").astype("Int64")
        expenses["Expenses"] = pd.to_numeric(
            expenses["Expenses"], errors="coerce")
        annual = annual_salary.merge(expenses, on="Year", how="inner")
        annual["% Spent on Manager Salaries"] = (
            annual["Weekly Salary"] / annual["Expenses"] * 100
        ).round(1)
        annual["Year"] = annual["Year"].astype(int)
        annual = annual.loc[:, ["Year", "% Spent on Manager Salaries"]]
        annual.sort_values("Year", inplace=True)

    return {
        "output_01.csv": weekly_totals[["Week", "Salary Payments"]],
        "output_02.csv": annual[["Year", "% Spent on Manager Salaries"]],
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
