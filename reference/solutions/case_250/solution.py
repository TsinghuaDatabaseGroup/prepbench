from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
from datetime import datetime
import math


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	term_files: List[Tuple[int, Path]] = []
	for idx in range(1, 7):
		term_files.append((idx, inputs_dir / f"input_0{idx}.csv"))
	names_path = inputs_dir / "input_08.csv"

	def parse_date_any(s: str) -> datetime | None:
		if s is None:
			return None
		txt = str(s).strip()
		if not txt:
			return None
		fmts = [
			"%m/%d/%Y",
			"%d.%m.%Y",
			"%Y-%m",
			"%d-%b-%Y",
			"%Y/%m/%d",
			"%d/%m/%Y",
		]
		for fmt in fmts:
			try:
				if fmt == "%Y-%m":
					dt = datetime.strptime(txt, "%Y-%m")
					return dt.replace(day=16)
				return datetime.strptime(txt, fmt)
			except Exception:
				continue
		return None

	def format_ddmmyyyy(dt: datetime | None) -> str:
		if dt is None:
			return ""
		return dt.strftime("%d/%m/%Y")

	df_names = pd.read_csv(names_path, dtype={"id": int, "first_name": str, "last_name": str})
	df_names["Student Name"] = (df_names["first_name"].fillna("").str.strip() + " " +
	                            df_names["last_name"].fillna("").str.strip())
	df_names = df_names[["id", "Student Name"]].copy()

	frames: List[pd.DataFrame] = []
	for term_no, p in term_files:
		df = pd.read_csv(p, dtype=str)
		df["id"] = df["id"].astype(int)
		dt_series = df["Date"].map(parse_date_any)
		df["Term Date"] = dt_series.map(format_ddmmyyyy)
		subcols = ["Subject_1_Grade", "Subject_2_Grade", "Subject_3_Grade", "Subject_4_Grade"]
		for c in subcols:
			df[c] = pd.to_numeric(df[c], errors="coerce")
		df["GPA"] = df[subcols].mean(axis=1)
		df["Term"] = f"Term {term_no}"
		frames.append(df[["id", "Term", "Term Date", "GPA"]].copy())

	all_terms = pd.concat(frames, ignore_index=True)
	all_terms = all_terms.merge(df_names, on="id", how="left")

	def term_key(t: str) -> int:
		try:
			return int(str(t).split()[-1])
		except Exception:
			return 0
	all_terms["__term_no"] = all_terms["Term"].map(term_key)
	all_terms = all_terms.sort_values(by=["id", "__term_no"]).reset_index(drop=True)
	all_terms["3 Term GPA Moving Average"] = (
		all_terms.groupby("id", as_index=False)["GPA"]
		.transform(lambda s: s.rolling(window=3, min_periods=3).mean())
	)
	all_terms["GPA"] = all_terms["GPA"].round(2)
	all_terms["3 Term GPA Moving Average"] = all_terms["3 Term GPA Moving Average"].round(2)

	out1 = all_terms.sort_values(by=["Student Name", "__term_no"], ascending=[False, True]).reset_index(drop=True)
	out1["Rank"] = out1.index + 1
	out1 = out1[[
		"Rank",
		"id",
		"Student Name",
		"Term",
		"Term Date",
		"GPA",
		"3 Term GPA Moving Average",
	]]

	top = all_terms[all_terms["__term_no"].isin([3, 6])].copy()
	top = top[top["3 Term GPA Moving Average"].notna()].copy()
	def select_by_term_size(group: pd.DataFrame) -> pd.DataFrame:
		term_no = int(group["__term_no"].iloc[0])
		k = 11 if term_no == 3 else 13
		ordered = group.sort_values(by=["3 Term GPA Moving Average", "GPA", "Student Name"],
		                            ascending=[False, False, True])
		return ordered.head(k)
	out2 = top.groupby("__term_no", group_keys=True).apply(select_by_term_size).reset_index(drop=True)
	out2 = out2[[
		"id",
		"Student Name",
		"Term",
		"Term Date",
		"GPA",
		"3 Term GPA Moving Average",
	]]

	return {
		"output_01.csv": out1,
		"output_02.csv": out2,
	}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	result = solve(inputs_dir)
	for fname, df in result.items():
		(df if df is not None else pd.DataFrame()).to_csv(cand_dir / fname, index=False, encoding="utf-8")


