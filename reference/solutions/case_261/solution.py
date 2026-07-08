from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    month_cols = [str(i) for i in range(1, 13)]
    for c in month_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        else:
            df[c] = 0.0

    df["__row_number__"] = np.arange(1, len(df) + 1)

    df = df.sort_values("__row_number__").drop_duplicates(subset=["StaffID"], keep="last").copy()

    df["Salary"] = df[month_cols].sum(axis=1)

    allowance = 12570.0
    basic_upper = 50270.0
    higher_upper = 125140.0

    taxable_20 = (df["Salary"] - allowance).clip(lower=0)
    taxable_20 = taxable_20.clip(upper=(basic_upper - allowance))
    tax20 = taxable_20 * 0.20

    taxable_40 = (df["Salary"] - basic_upper).clip(lower=0)
    taxable_40 = taxable_40.clip(upper=(higher_upper - basic_upper))
    tax40 = taxable_40 * 0.40

    taxable_45 = (df["Salary"] - higher_upper).clip(lower=0)
    tax45 = taxable_45 * 0.45

    max_rate_flags = pd.Series(np.where(df["Salary"] > higher_upper, "45", np.where(df["Salary"] > basic_upper, "40", "20")), index=df.index)
    tax20_out = tax20
    tax40_out = tax40.where(max_rate_flags.isin(["40", "45"]), np.nan)
    tax45_out = tax45.where(max_rate_flags.eq("45"), np.nan)

    total_tax = (tax20_out.fillna(0) + tax40_out.fillna(0) + tax45_out.fillna(0))

    def max_rate_row(row_salary: float) -> str:
        if row_salary > higher_upper:
            return "45% rate"
        elif row_salary > basic_upper:
            return "40% rate"
        else:
            return "20% rate"

    max_rate = df["Salary"].apply(max_rate_row)

    out = pd.DataFrame({
        "StaffID": pd.to_numeric(df["StaffID"], errors="raise"),
        "Salary": df["Salary"].astype(float),
        "Max Tax Rate": max_rate.astype(str),
        "Total Tax Paid": total_tax.astype(float),
        "20% rate tax paid": tax20_out.astype(float),
        "40% rate paid": tax40_out.astype(float),
        "45% rate tax paid": tax45_out.astype(float),
    })


    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

