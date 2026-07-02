from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	input_file = inputs_dir / "input_01.csv"
	df = pd.read_csv(input_file)

	df["Tournament Date"] = pd.to_datetime(df["Tournament Date"], format="%Y-%m-%d")

	def compute_experience(group: pd.DataFrame) -> pd.DataFrame:
		group = group.sort_values("Tournament Date", ascending=True).copy()
		running_from_current = group["Matches Played in Tournament"].iloc[::-1].cumsum().iloc[::-1]
		group["Experience at beginning of Tournament"] = (
			group["Total Matches"] - running_from_current
		).astype(int)
		return group

	df = df.groupby(["Team", "Player ID"], group_keys=False).apply(compute_experience)

	df["Tournament Date"] = df["Tournament Date"].dt.strftime("%d/%m/%Y")

	out_cols = [
		"Team",
		"Player ID",
		"Total Matches",
		"Tournament Date",
		"Experience at beginning of Tournament",
		"Matches Played in Tournament",
	]
	df_out = df[out_cols].copy()

	df_out["Player ID"] = df_out["Player ID"].astype(int)
	df_out["Total Matches"] = df_out["Total Matches"].astype(int)
	df_out["Experience at beginning of Tournament"] = df_out["Experience at beginning of Tournament"].astype(int)
	df_out["Matches Played in Tournament"] = df_out["Matches Played in Tournament"].astype(int)

	return {"output_01.csv": df_out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	results = solve(inputs_dir)
	for filename, df in results.items():
		df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


