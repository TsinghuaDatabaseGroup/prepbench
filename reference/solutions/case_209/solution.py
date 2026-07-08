from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	input_file = inputs_dir / "input_01.csv"
	df = pd.read_csv(input_file)

	mobile_cols = [
		"Mobile App - Ease of Use",
		"Mobile App - Ease of Access",
		"Mobile App - Navigation",
		"Mobile App - Likelihood to Recommend",
	]
	online_cols = [
		"Online Interface - Ease of Use",
		"Online Interface - Ease of Access",
		"Online Interface - Navigation",
		"Online Interface - Likelihood to Recommend",
	]

	df["avg_mobile"] = df[mobile_cols].mean(axis=1)
	df["avg_online"] = df[online_cols].mean(axis=1)
	df["diff"] = df["avg_mobile"] - df["avg_online"]

	def categorize(delta: float) -> str:
		if delta >= 2:
			return "Mobile App Superfan"
		if delta >= 1:
			return "Mobile App Fan"
		if delta <= -2:
			return "Online Interface Superfan"
		if delta <= -1:
			return "Online Interface Fan"
		return "Neutral"

	df["Preference"] = df["diff"].apply(categorize)

	total = len(df)
	counts = df["Preference"].value_counts().rename("count")
	percent = (counts / total * 100).round(1).rename("% of Total")
	out = percent.reset_index().rename(columns={"index": "Preference"})

	order = [
		"Mobile App Fan",
		"Neutral",
		"Mobile App Superfan",
		"Online Interface Fan",
		"Online Interface Superfan",
	]
	out = out.set_index("Preference").reindex(order).reset_index()

	return {"output_01.csv": out[["Preference", "% of Total"]]}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(exist_ok=True)

	outputs = solve(inputs_dir)
	for filename, df in outputs.items():
		(df.astype({"% of Total": "float64"})).to_csv(cand_dir / filename, index=False, encoding="utf-8")


