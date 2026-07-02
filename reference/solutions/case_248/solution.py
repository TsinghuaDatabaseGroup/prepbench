from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	df = pd.read_csv(inputs_dir / "input_01.csv")
	def extract_project(value: str) -> str | None:
		if isinstance(value, str):
			v = value.strip()
			if v and not v.lower().startswith("expense") and not v.lower().startswith("invoice"):
				return v
		return None
	project_headers = df["Project"].apply(extract_project)
	df["Project Name"] = project_headers.ffill()

	df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce")
	df["Invoiced Amount"] = pd.to_numeric(df["Invoiced Amount"], errors="coerce")

	df_tx = df[~(df["Cost"].isna() & df["Invoiced Amount"].isna())].copy()

	agg = df_tx.groupby("Project Name", as_index=False).agg(
		{"Invoiced Amount": "sum", "Cost": "sum"}
	)
	agg["Profit"] = agg["Invoiced Amount"] - agg["Cost"]

	out = agg[["Project Name", "Invoiced Amount", "Cost", "Profit"]]
	return {"output_01.csv": out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(exist_ok=True)
	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		df.to_csv(cand_dir / filename, index=False, encoding="utf-8")




















