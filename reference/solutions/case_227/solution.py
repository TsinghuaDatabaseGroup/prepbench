from __future__ import annotations

from pathlib import Path
from typing import Dict, List
import re
import pandas as pd
from datetime import datetime


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	east_path = inputs_dir / "input_01.csv"
	lookup_path = inputs_dir / "input_02.csv"
	west_path = inputs_dir / "input_03.csv"

	df_east = pd.read_csv(east_path, dtype=str)
	def normalize_east_id(s: str) -> int:
		if s is None:
			return None
		m = re.search(r"(\d+)$", str(s).strip())
		return int(m.group(1)) if m else None
	df_east["Student ID Num"] = df_east["Student ID"].map(normalize_east_id)
	df_east["Region"] = "EAST"
	df_east["Full Name"] = (df_east["First Name"].fillna("").str.strip() + " " + df_east["Last Name"].fillna("").str.strip()).str.upper()
	def parse_east_date(s: str) -> str:
		if s is None:
			return None
		s = str(s).strip()
		try:
			dt = datetime.strptime(s, "%A, %d %B, %Y")
			return dt.strftime("%Y-%m-%d")
		except Exception:
			return s
	df_east["Date of Birth"] = df_east["Date of Birth"].map(parse_east_date)
	df_east_std = df_east[["Student ID Num", "Full Name", "Date of Birth", "Region", "Subject", "Grade"]].rename(
		columns={"Student ID Num": "Student ID"}
	).copy()

	df_west = pd.read_csv(west_path, dtype=str)
	def split_west_id(s: str) -> int:
		if s is None:
			return None
		m = re.match(r"(\d+)-", str(s).strip())
		return int(m.group(1)) if m else None
	df_west["Student ID"] = df_west["Student ID"].map(split_west_id)
	df_west["Region"] = "WEST"
	df_west["Full Name"] = (df_west["First Name"].fillna("").str.strip() + " " + df_west["Last Name"].fillna("").str.strip()).str.upper()
	def parse_west_date(s: str) -> str:
		if s is None:
			return None
		s = str(s).strip()
		try:
			dt = datetime.strptime(s, "%d/%m/%Y")
			return dt.strftime("%Y-%m-%d")
		except Exception:
			return s
	df_west["Date of Birth"] = df_west["Date of Birth"].map(parse_west_date)
	num_to_letter = {
		"1": "A",
		"2": "B",
		"3": "C",
		"4": "D",
		"5": "E",
		"6": "F",
	}
	df_west["Grade"] = df_west["Grade"].map(lambda x: num_to_letter.get(str(x).strip(), x))
	df_west_std = df_west[["Student ID", "Full Name", "Date of Birth", "Region", "Subject", "Grade"]].copy()

	combined = pd.concat([df_east_std, df_west_std], ignore_index=True)

	letter_score = {"A": 50, "B": 40, "C": 30, "D": 20, "E": 10, "F": 0}
	combined["Grade Score Single"] = combined["Grade"].map(lambda x: letter_score.get(str(x).strip().upper(), 0))

	pivot = combined.pivot_table(
		index=["Student ID", "Full Name", "Date of Birth", "Region"],
		columns="Subject",
		values="Grade",
		aggfunc="first"
	).reset_index()
	score_sum = combined.groupby(["Student ID", "Full Name", "Date of Birth", "Region"], as_index=False)["Grade Score Single"].sum()
	pivot = pivot.merge(score_sum, on=["Student ID", "Full Name", "Date of Birth", "Region"], how="left")
	pivot = pivot.rename(columns={
		"Grade Score Single": "Grade Score"
	})

	df_lookup = pd.read_csv(lookup_path, dtype={"Student ID": int, "School Name": str, "School ID": int})
	out = pivot.merge(df_lookup, on="Student ID", how="left")
	out["School Name"] = out["School Name"].replace({
		"St Marys": "St. Mary's",
		"Viliers Hill": "Villiers Hill",
	})

	out = out[[
		"Student ID",
		"Full Name",
		"Date of Birth",
		"Region",
		"School Name",
		"School ID",
		"English",
		"Science",
		"Maths",
		"Grade Score",
	]].copy()

	return {"output_01.csv": out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)
	res = solve(inputs_dir)
	for fname, df in res.items():
		(df if df is not None else pd.DataFrame()).to_csv(cand_dir / fname, index=False, encoding="utf-8")


