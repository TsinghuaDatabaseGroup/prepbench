from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OUTPUT_FILE = "output_01.csv"
CURRENT_END_DATE = pd.Timestamp("2024-06-05")
REMAP_DATES = {pd.Timestamp("2024-05-28"): CURRENT_END_DATE}


def _clean_names(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower().str.title()


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    salaries = pd.read_csv(inputs_dir / "input_02.csv")
    tenures = pd.read_csv(inputs_dir / "input_03.csv")
    amount_paid = pd.read_csv(inputs_dir / "input_01.csv")

    salaries["Name"] = _clean_names(salaries["Name"])
    tenures["Name"] = _clean_names(tenures["Name"])
    amount_paid["Name"] = _clean_names(amount_paid["Name"])

    end_raw = tenures["End Date"].astype(str).str.strip().str.lower()
    tenures["Is Current"] = end_raw.eq("current")
    tenures["Start Date"] = pd.to_datetime(
        tenures["Start Date"], errors="coerce")
    tenures["End Date"] = (
        pd.to_datetime(tenures["End Date"], errors="coerce")
        .fillna(CURRENT_END_DATE)
        .replace(REMAP_DATES)
    )

    tenures["Tenure"] = (tenures["End Date"] - tenures["Start Date"]).dt.days

    tenure_salary = tenures.merge(
        salaries,
        on="Name",
        how="inner",
        validate="one_to_one",
    )

    tenure_salary["Expected Total Salary"] = np.rint(
        (tenure_salary["Tenure"] / 365) * tenure_salary["Salary"]
    ).astype(int)

    full = tenure_salary.merge(
        amount_paid,
        on="Name",
        how="inner",
        validate="one_to_one",
    )

    mismatch_mask = full["Expected Total Salary"] != full["Amount Paid"]
    current_mask = full["Is Current"]

    result = full.loc[
        mismatch_mask & current_mask,
        ["Name", "Salary", "Expected Total Salary", "Amount Paid"],
    ].sort_values("Name")

    return {OUTPUT_FILE: result.reset_index(drop=True)}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
