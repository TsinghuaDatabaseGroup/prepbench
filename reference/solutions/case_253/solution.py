from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	def parse_percent(s: pd.Series) -> pd.Series:
		return pd.to_numeric(s.str.replace("%", "", regex=False), errors="coerce") / 100.0

	def parse_currency(s: pd.Series) -> pd.Series:
		return pd.to_numeric(s.str.replace("£", "", regex=False).str.replace(",", "", regex=False), errors="coerce")

	def format_provider(name: str, has_conditions: str | float | None) -> str:
		if isinstance(has_conditions, str) and has_conditions.strip().upper() == "Y":
			return f"{name} (Conditions Apply)"
		return name

	planned_monthly_deposit = 300.0

	input_path = inputs_dir / "input_01.csv"
	raw = pd.read_csv(input_path)
	raw["Interest"] = parse_percent(raw["Interest"].astype(str))
	raw["Max Monthly Deposit"] = parse_currency(raw["Max Monthly Deposit"].astype(str))
	raw["Provider"] = [
		format_provider(p, c if "Has Additional Conditions" in raw.columns else None)
		for p, c in zip(raw["Provider"], raw.get("Has Additional Conditions", pd.Series([None] * len(raw))))
	]

	providers = raw[["Provider", "Interest", "Max Monthly Deposit"]].copy()

	records: List[dict] = []
	summary_rows: List[Tuple[str, float, float]] = []

	for _, row in providers.iterrows():
		provider = row["Provider"]
		apr = float(row["Interest"])
		max_monthly = float(row["Max Monthly Deposit"])
		monthly_rate = apr / 12.0

		monthly_deposit = min(planned_monthly_deposit, max_monthly)
		leftover_each_month = max(planned_monthly_deposit - monthly_deposit, 0.0)

		interest_balance = 0.0
		no_interest_balance = 0.0
		total_interest_accrued = 0.0

		month_savings_list: List[float] = []

		for month in range(1, 13):
			interest_balance += monthly_deposit
			interest_amount = interest_balance * monthly_rate
			interest_balance += interest_amount
			total_interest_accrued += interest_amount
			no_interest_balance += leftover_each_month
			total_savings = interest_balance + no_interest_balance
			month_savings_list.append(total_savings)

		max_possible_savings = month_savings_list[-1]
		summary_rows.append((provider, max_possible_savings, total_interest_accrued))

		for idx, savings_val in enumerate(month_savings_list, start=1):
			records.append(
				{
					"Provider": provider,
					"Interest": apr,
					"Max Monthly Deposit": max_monthly,
					"Customer Planned Deposit": planned_monthly_deposit,
					"Monthly Deposit": monthly_deposit,
					"Leftover Savings which won't receive interest": leftover_each_month,
					"Month": idx,
					"Savings each month": savings_val,
					"Max Possible Savings": max_possible_savings,
					"Total Interest": total_interest_accrued,
				}
			)

	df = pd.DataFrame.from_records(records)

	summary_df = pd.DataFrame(summary_rows, columns=["Provider", "Max Possible Savings", "Total Interest"])
	summary_df["rank_max_savings"] = summary_df["Max Possible Savings"].rank(method="dense", ascending=False).astype(int)
	summary_df["rank_total_interest"] = summary_df["Total Interest"].rank(method="dense", ascending=False).astype(int)

	df = df.merge(
		summary_df[["Provider", "rank_max_savings", "rank_total_interest"]],
		on="Provider",
		how="left",
	)
	df.rename(
		columns={
			"rank_max_savings": "Providers Ranked by Max Savings",
			"rank_total_interest": "Providers Ranked by Total Interest",
		},
		inplace=True,
	)

	def round2(x: pd.Series) -> pd.Series:
		return pd.to_numeric(x, errors="coerce").round(2)

	df["Savings each month"] = round2(df["Savings each month"])
	df["Max Possible Savings"] = round2(df["Max Possible Savings"])
	df["Total Interest"] = round2(df["Total Interest"])
	df["Interest"] = pd.to_numeric(df["Interest"], errors="coerce")
	df["Max Monthly Deposit"] = pd.to_numeric(df["Max Monthly Deposit"], errors="coerce")
	df["Customer Planned Deposit"] = pd.to_numeric(df["Customer Planned Deposit"], errors="coerce")
	df["Monthly Deposit"] = pd.to_numeric(df["Monthly Deposit"], errors="coerce")
	df["Leftover Savings which won't receive interest"] = pd.to_numeric(
		df["Leftover Savings which won't receive interest"], errors="coerce"
	)
	df["Month"] = pd.to_numeric(df["Month"], errors="coerce")

	final_cols = [
		"Providers Ranked by Max Savings",
		"Providers Ranked by Total Interest",
		"Provider",
		"Interest",
		"Max Monthly Deposit",
		"Customer Planned Deposit",
		"Monthly Deposit",
		"Leftover Savings which won't receive interest",
		"Month",
		"Savings each month",
		"Max Possible Savings",
		"Total Interest",
	]
	df = df[final_cols]

	df = df.sort_values(
		by=["Providers Ranked by Max Savings", "Providers Ranked by Total Interest", "Provider", "Month"],
		ascending=[True, True, True, True],
		kind="mergesort",
	).reset_index(drop=True)

	return {"output_01.csv": df}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		(df).to_csv(cand_dir / filename, index=False, encoding="utf-8")




















