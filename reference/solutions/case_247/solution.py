from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	events_path = inputs_dir / "input_02.csv"
	clubs_path = inputs_dir / "input_01.csv"

	events = pd.read_csv(events_path)
	events["Date"] = pd.to_datetime(events["Date"], dayfirst=True, infer_datetime_format=True)

	clubs = pd.read_csv(clubs_path)
	clubs = clubs.rename(columns={"Day of Week": "Day of Week", "After School Club": "After School Club"})

	start_date = events["Date"].min()
	end_date = events["Date"].max()

	all_days = pd.DataFrame({"Date": pd.date_range(start=start_date, end=end_date, freq="D")})
	all_days = all_days[all_days["Date"].dt.weekday <= 4].reset_index(drop=True)

	day_name_map = {
		0: "Monday",
		1: "Tuesday",
		2: "Wednesday",
		3: "Thursday",
		4: "Friday",
	}
	all_days["Day of Week"] = all_days["Date"].dt.weekday.map(day_name_map)

	all_days = all_days.merge(clubs, on="Day of Week", how="left")

	all_days = all_days.merge(events, on="Date", how="left")

	all_days["Event"] = all_days["Event"].fillna("N/A")

	all_days["Date"] = all_days["Date"].dt.strftime("%d/%m/%Y")

	out = all_days[["Date", "Event", "Day of Week", "After School Club"]].copy()
	return {"output_01.csv": out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	results = solve(inputs_dir)
	for filename, df in results.items():
		df.to_csv(cand_dir / filename, index=False, encoding="utf-8")




















