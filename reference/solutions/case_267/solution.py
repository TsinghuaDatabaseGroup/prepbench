from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def months_between(start_year: int, start_month: int, end_year: int, end_month: int) -> int:
        return (end_year - start_year) * 12 + (end_month - start_month)

    df_plan = pd.read_csv(inputs_dir / "input_01.csv")
    df_loans = pd.read_csv(inputs_dir / "input_02.csv")

    plan_row = df_plan.loc[df_plan["Loan"].str.strip().str.lower() == "undergraduate"].iloc[0]
    annual_interest: float = float(plan_row["Interest"])
    threshold: float = float(plan_row["Repayment Threshold"])
    repayment_rate_pct: float = float(plan_row["% Repayment over Threshold"])

    monthly_rate = annual_interest / 12.0

    records = []
    for _, row in df_loans.iterrows():
        amount_per_year = float(row["Amount per year"])
        start_str = str(row["Course Start"]).strip()
        parts = start_str.split()
        start_year = int(parts[-1])
        start_month = 9
        length_years = int(row["Course Length (years)"])

        for i in range(length_years):
            pay_year = start_year + i
            pay_month = 9
            months = months_between(pay_year, pay_month, 2024, 4)
            records.append({
                "amount": amount_per_year,
                "months": months,
            })

    df_payments = pd.DataFrame.from_records(records)

    df_payments["amount_with_interest"] = df_payments["amount"] * (1.0 + monthly_rate) ** df_payments["months"]

    total_borrowed = float(df_payments["amount"].sum())
    total_with_interest = float(df_payments["amount_with_interest"].sum())

    salary = 35000.0
    annual_repayment = max(0.0, (salary - threshold)) * (repayment_rate_pct / 100.0)
    monthly_repayment = annual_repayment / 12.0

    current_balance_after_repayment = max(0.0, total_with_interest - monthly_repayment)

    interest_next_month = current_balance_after_repayment * monthly_rate

    result = pd.DataFrame([
        {
            "Monthly Repayment": round(monthly_repayment, 2),
            "Total Borrowed": round(total_borrowed, 0),
            "Total Borrowed + Interest": round(current_balance_after_repayment, 2),
            "Interest to be added next month": round(interest_next_month, 2),
        }
    ])

    result = result.astype({
        "Monthly Repayment": float,
        "Total Borrowed": float,
        "Total Borrowed + Interest": float,
        "Interest to be added next month": float,
    })

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False)


