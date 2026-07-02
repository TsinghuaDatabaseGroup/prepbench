from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	def parse_date(series: pd.Series) -> pd.Series:
		return pd.to_datetime(series, format="%d/%m/%Y", dayfirst=True, errors="coerce")

	def month_diff(a: pd.Series, b: pd.Series) -> pd.Series:
		return (b.dt.year - a.dt.year) * 12 + (b.dt.month - a.dt.month)

	input_file = inputs_dir / "input_01.csv"
	df = pd.read_csv(input_file, dtype={"dc_nbr": "int64", "employee_id": "string"})

	df["month_end_date"] = parse_date(df["month_end_date"])
	df["hire_date"] = parse_date(df["hire_date"])
	if "leave_date" in df.columns:
		df["leave_date"] = parse_date(df["leave_date"])
	if "tenure_months" in df.columns:
		df["tenure_months"] = pd.to_numeric(df["tenure_months"], errors="coerce")

	ee_count_by_dc = df.groupby("dc_nbr", as_index=False)["employee_id"].nunique().rename(columns={"employee_id": "ee_count"})

	df_sorted = df.sort_values(["employee_id", "month_end_date"])
	grouped = df_sorted.groupby("employee_id", sort=False, group_keys=False)

	def detect_transfers(g: pd.DataFrame) -> pd.DataFrame:
		g = g.sort_values("month_end_date")
		g["next_dc"] = g["dc_nbr"].shift(-1)
		g["next_date"] = g["month_end_date"].shift(-1)
		g["months_to_next"] = month_diff(g["month_end_date"], g["next_date"])
		mask = (g["next_dc"].notna()) & (g["dc_nbr"] != g["next_dc"]) & (g["months_to_next"] >= 1) & (g["months_to_next"] <= 2)
		transfers = g.loc[mask, ["employee_id", "dc_nbr", "month_end_date", "tenure_months"]].copy()
		transfers.rename(columns={"dc_nbr": "from_dc", "month_end_date": "transfer_month"}, inplace=True)
		return transfers

	transfers = grouped.apply(detect_transfers)
	if not transfers.empty:
		transfers["from_dc"] = transfers["from_dc"].astype("int64")
	else:
		transfers = pd.DataFrame(columns=["employee_id", "from_dc", "transfer_month", "tenure_months"])

	xfer_count_by_dc = transfers.groupby("from_dc", as_index=False).size().rename(columns={"from_dc": "dc_nbr", "size": "xfer_count"})
	xfer_unique_emp_by_dc = transfers.groupby("from_dc", as_index=False)["employee_id"].nunique().rename(
		columns={"from_dc": "dc_nbr", "employee_id": "xfer_unique_ee"}
	)
	avg_tenure_by_dc = transfers.groupby("from_dc", as_index=False)["tenure_months"].mean().rename(
		columns={"from_dc": "dc_nbr", "tenure_months": "avg_tenure_months"}
	)

	result = ee_count_by_dc.merge(xfer_count_by_dc, on="dc_nbr", how="left")
	result = result.merge(xfer_unique_emp_by_dc, on="dc_nbr", how="left")
	result = result.merge(avg_tenure_by_dc, on="dc_nbr", how="left")
	result["xfer_count"] = result["xfer_count"].fillna(0).astype(int)
	result["xfer_unique_ee"] = result["xfer_unique_ee"].fillna(0).astype(int)
	result["avg_tenure_months"] = result["avg_tenure_months"].fillna(0.0)

	result["xfer_pct"] = np.where(
		result["ee_count"] > 0,
		(result["xfer_unique_ee"] / result["ee_count"]) * 100.0,
		0.0,
	)

	def round_and_trim(series: pd.Series) -> pd.Series:
		num = pd.to_numeric(series, errors="coerce").round(2)
		as_int = num.astype("int64")
		is_int = np.isclose(num, as_int)
		out = num.astype(object)
		out[is_int] = as_int[is_int]
		return pd.to_numeric(out, errors="coerce")

	result["xfer_pct"] = round_and_trim(result["xfer_pct"])
	result["avg_tenure_months"] = round_and_trim(result["avg_tenure_months"])

	total_ee = int(df["employee_id"].nunique())
	total_xfers = int(result["xfer_count"].sum())
	total_unique_transfer_employees = transfers["employee_id"].nunique() if not transfers.empty else 0
	total_xfer_pct = 0.0
	if total_ee > 0:
		total_xfer_pct = (total_unique_transfer_employees / total_ee) * 100.0
	total_avg_tenure = float(transfers["tenure_months"].mean()) if not transfers.empty else 0.0

	total_row = pd.DataFrame(
		{
			"dc_nbr": ["Total"],
			"ee_count": [total_ee],
			"xfer_count": [total_xfers],
			"xfer_pct": [round_and_trim(pd.Series([total_xfer_pct])).iloc[0]],
			"avg_tenure_months": [round_and_trim(pd.Series([total_avg_tenure])).iloc[0]],
		}
	)

	result["dc_nbr"] = result["dc_nbr"].astype(str)
	def sort_key(x: str) -> tuple:
		if x == "Total":
			return (1, np.inf)
		try:
			return (0, int(x))
		except Exception:
			return (0, np.inf)

	result = result.sort_values(by="dc_nbr", key=lambda s: s.map(sort_key))

	final_cols = ["dc_nbr", "ee_count", "xfer_count", "xfer_pct", "avg_tenure_months"]
	output_df = pd.concat([result[final_cols], total_row[final_cols]], ignore_index=True)

	output_df["dc_nbr"] = output_df["dc_nbr"].astype(str)
	for col in ["ee_count", "xfer_count"]:
		output_df[col] = pd.to_numeric(output_df[col], downcast="integer")
	for col in ["xfer_pct", "avg_tenure_months"]:
		output_df[col] = pd.to_numeric(output_df[col])

	return {"output_01.csv": output_df}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		out_path = cand_dir / filename
		df.to_csv(out_path, index=False, encoding="utf-8")


