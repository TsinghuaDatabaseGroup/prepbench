from pathlib import Path
from typing import Dict

import pandas as pd


def _detect_demographic_column(columns: list[str]) -> str:
	lower = {c.lower(): c for c in columns}
	for candidate in ["demographic", "demographiic", "demagraphic"]:
		if candidate in lower:
			return lower[candidate]
	if "Demographic" in columns:
		return "Demographic"
	raise KeyError("Demographic column not found (possible misspellings: Demographic/Demographiic/Demagraphic).")


def _format_date_to_ddmmyyyy(date_series: pd.Series) -> pd.Series:
	parsed = pd.to_datetime(date_series, errors="coerce", infer_datetime_format=True)
	return parsed.dt.strftime("%d/%m/%Y")


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	file_to_month = {
		"input_01.csv": 4,
		"input_02.csv": 8,
		"input_03.csv": 12,
		"input_04.csv": 2,
		"input_05.csv": 1,
		"input_06.csv": 7,
		"input_07.csv": 6,
		"input_08.csv": 3,
		"input_09.csv": 5,
		"input_10.csv": 11,
		"input_11.csv": 10,
		"input_12.csv": 9,
	}

	all_frames: list[pd.DataFrame] = []
	for fname, month in file_to_month.items():
		fpath = inputs_dir / fname
		if not fpath.exists():
			continue
		df = pd.read_csv(fpath)
		demo_col = _detect_demographic_column(list(df.columns))
		day = pd.to_numeric(df["Joining Day"], errors="coerce").astype("Int64")
		joining_date = pd.to_datetime(
			{
				"year": 2023,
				"month": month,
				"day": day,
			},
			errors="coerce",
		)
		df = df.assign(**{
			"Joining Date": joining_date.dt.strftime("%d/%m/%Y"),
		})
		df = df[["ID", "Joining Day", "Joining Date", demo_col, "Value"]].rename(columns={demo_col: "Demographic"})
		all_frames.append(df)

	if not all_frames:
		empty = pd.DataFrame(columns=["ID", "Joining Date", "Account Type", "Date of Birth", "Ethnicity"])
		return {"output_01.csv": empty}

	union_df = pd.concat(all_frames, ignore_index=True)

	pivot_df = (
		union_df
		.pivot_table(index=["ID", "Joining Day", "Joining Date"], columns="Demographic", values="Value", aggfunc="first")
		.reset_index()
	)

	for col in ["Account Type", "Date of Birth", "Ethnicity"]:
		if col not in pivot_df.columns:
			pivot_df[col] = pd.NA

	pivot_df["_jd"] = pd.to_datetime(pivot_df["Joining Date"], format="%d/%m/%Y", errors="coerce")
	pivot_df = pivot_df.sort_values(by=["_jd", "ID"], kind="mergesort")
	pivot_df = pivot_df.drop_duplicates(subset=["ID"], keep="first")
	pivot_df = pivot_df.drop(columns=["_jd", "Joining Day"])

	pivot_df["Date of Birth"] = _format_date_to_ddmmyyyy(pivot_df["Date of Birth"])

	out = pivot_df[["ID", "Joining Date", "Account Type", "Date of Birth", "Ethnicity"]].copy()
	out["ID"] = out["ID"].astype(str)

	out = out.sort_values(by=["ID"], kind="mergesort").reset_index(drop=True)

	return {"output_01.csv": out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	result = solve(inputs_dir)
	for fname, df in result.items():
		(df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)).to_csv(cand_dir / fname, index=False, encoding="utf-8")


