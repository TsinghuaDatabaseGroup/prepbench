from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	input_files = sorted(inputs_dir.glob("input_*.csv"))
	frames: list[pd.DataFrame] = []
	for f in input_files:
		df = pd.read_csv(f)
		frames.append(df)
	if len(frames) == 0:
		return {"output_01.csv": pd.DataFrame(columns=[
			"Sort",
			"School Name",
			"Date",
			"Total Cost",
			"Gas Cost",
			"Electricity Cost",
			"Water Cost",
			"Maintenance Cost",
		])}

	raw = pd.concat(frames, ignore_index=True)

	expected_cols = {"School Name", "Year", "Month", "Name", "Value"}
	missing = expected_cols - set(raw.columns)
	if missing:
		raise ValueError(f"Missing required columns in input: {missing}")

	pivot = raw.pivot_table(
		index=["School Name", "Year", "Month"],
		columns="Name",
		values="Value",
		aggfunc="sum",
	).reset_index()

	cost_cols = ["Gas Cost", "Electricity Cost", "Water Cost", "Maintenance Cost"]
	for col in cost_cols:
		if col not in pivot.columns:
			pivot[col] = 0

	for col in cost_cols:
		pivot[col] = pd.to_numeric(pivot[col], errors="coerce").fillna(0).astype(int)

	pivot["Total Cost"] = pivot[cost_cols].sum(axis=1).astype(int)

	month_to_num = {
		"January": 1,
		"February": 2,
		"March": 3,
		"April": 4,
		"May": 5,
		"June": 6,
		"July": 7,
		"August": 8,
		"September": 9,
		"October": 10,
		"November": 11,
		"December": 12,
	}
	month_num = pivot["Month"].map(month_to_num)
	if month_num.isna().any():
		month_num = pd.to_numeric(pivot["Month"], errors="coerce")
	pivot["_month_num"] = month_num

	pivot["Date"] = (
		pd.to_datetime(
			dict(year=pivot["Year"].astype(int), month=pivot["_month_num"].astype(int), day=1),
			errors="raise",
		).dt.strftime("%d/%m/%Y")
	)

	pivot = pivot.sort_values(by=["School Name", "Year", "_month_num"]).reset_index(drop=True)

	pivot["Sort"] = pivot.groupby("School Name").cumcount() + 1

	out_cols = [
		"Sort",
		"School Name",
		"Date",
		"Total Cost",
		"Gas Cost",
		"Electricity Cost",
		"Water Cost",
		"Maintenance Cost",
	]
	out = pivot[out_cols].copy()

	int_cols = ["Sort", "Total Cost", "Gas Cost", "Electricity Cost", "Water Cost", "Maintenance Cost"]
	for col in int_cols:
		out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0).astype(int)

	return {
		"output_01.csv": out
	}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(exist_ok=True, parents=True)

	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		(df).to_csv(cand_dir / filename, index=False, encoding="utf-8")




















