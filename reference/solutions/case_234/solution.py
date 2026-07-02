from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
import numpy as np


def _parse_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="%d/%m/%Y", errors="coerce", dayfirst=True)


def _build_generation_name(row: pd.Series) -> str:
    gen = row["generation"]
    start = row["start_year"]
    end = row["end_year"]
    if pd.isna(start) and pd.isna(end):
        return gen
    if pd.isna(start) and not pd.isna(end):
        return f"{gen} (born in or before {int(end)})"
    if not pd.isna(start) and pd.isna(end):
        return f"{gen} (born in or after {int(start)})"
    return f"{gen} ({int(start)}-{int(end)})"


def _compute_age_years(birth_date: pd.Timestamp, as_of: pd.Timestamp) -> float:
    if pd.isna(birth_date) or pd.isna(as_of):
        return np.nan
    years = as_of.year - birth_date.year
    if (as_of.month, as_of.day) < (birth_date.month, birth_date.day):
        years -= 1
    return years


def _age_to_range(age_years: float) -> str:
    if pd.isna(age_years):
        return "Not Provided"
    age = int(age_years)
    if age < 20:
        return "Under 20 years"
    if age >= 70:
        return "70+ years"
    start = (age // 5) * 5
    if start < 20:
        start = 20
    end = start + 4
    return f"{start}-{end} years"


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    ee_dim = pd.read_csv(inputs_dir / "input_01.csv", dtype={"employee_id": str, "guid": str})
    monthly = pd.read_csv(inputs_dir / "input_02.csv", dtype={"employee_id": str, "guid": str})
    gens = pd.read_csv(inputs_dir / "input_03.csv")

    gens["start_year"] = pd.to_numeric(gens["start_year"], errors="coerce")
    gens["end_year"] = pd.to_numeric(gens["end_year"], errors="coerce")
    gens["generation_name"] = gens.apply(_build_generation_name, axis=1)

    ee_dim["date_of_birth_parsed"] = _parse_date(ee_dim["date_of_birth"])
    ee_dim["birth_year"] = ee_dim["date_of_birth_parsed"].dt.year

    def map_generation_name(birth_year: float) -> str:
        if pd.isna(birth_year):
            return "Not Provided"
        match = gens[
            ((gens["start_year"].isna()) | (gens["start_year"] <= birth_year))
            & ((gens["end_year"].isna()) | (gens["end_year"] >= birth_year))
        ]
        if match.empty:
            return "Not Provided"
        return match.iloc[0]["generation_name"]

    ee_dim["generation_name"] = ee_dim["birth_year"].apply(map_generation_name)

    out1_cols = [
        "employee_id",
        "guid",
        "first_name",
        "last_name",
        "generation_name",
        "nationality",
        "gender",
        "email",
        "hire_date",
        "leave_date",
    ]
    output_01 = ee_dim.copy()
    output_01 = output_01[out1_cols]

    monthly_parsed = monthly.copy()
    monthly_parsed["month_end_date_parsed"] = _parse_date(monthly_parsed["month_end_date"])
    ee_for_age = ee_dim[["employee_id", "date_of_birth_parsed", "hire_date", "leave_date", "guid"]].copy()
    merged = monthly_parsed.merge(ee_for_age, on=["employee_id", "guid"], how="left", suffixes=("", "_ee"))
    merged["age_years"] = merged.apply(
        lambda r: _compute_age_years(r["date_of_birth_parsed"], r["month_end_date_parsed"]), axis=1
    )
    merged["age_range"] = merged["age_years"].apply(_age_to_range)

    out2_cols = [
        "employee_id",
        "age_range",
        "guid",
        "dc_nbr",
        "month_end_date",
        "hire_date",
        "leave_date",
    ]
    output_02 = merged[out2_cols].copy()

    output_01 = output_01.sort_values(by=["employee_id"], kind="mergesort").reset_index(drop=True)
    output_02 = output_02.sort_values(by=["employee_id", "month_end_date", "dc_nbr"], kind="mergesort").reset_index(drop=True)

    return {
        "output_01.csv": output_01,
        "output_02.csv": output_02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

