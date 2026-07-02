from pathlib import Path
from typing import Dict, List, Tuple

import re
import pandas as pd


def _read_month_file(path: Path) -> pd.DataFrame:
	df = pd.read_csv(path)
	normalized = {}
	for c in df.columns:
		key = re.sub(r"[^A-Za-z0-9]+", "", str(c)).lower()
		normalized[key] = c
	def pick(*cands: str) -> str:
		for k in cands:
			if k in normalized:
				return normalized[k]
		raise KeyError(f"Column not found among {df.columns}")

	col_store = pick("store")
	col_sales = pick("sales")
	col_order_date = pick("orderdate", "orderdate1", "orderdate2", "orderdate3", "orderdate4", "orderdate5", "orderdate6", "orderdate7", "orderdate8", "orderdate9", "orderdate0", "orderdate_", "orderdate__")
	if col_order_date not in df.columns:
		for raw in ["Order Date", "OrderDate", "Order  Date"]:
			if raw in df.columns:
				col_order_date = raw
				break
	def extract_year(s: str) -> int:
		if pd.isna(s):
			return pd.NA
		ss = str(s)
		m = re.search(r"(\d{4})", ss)
		return int(m.group(1)) if m else pd.NA

	out = pd.DataFrame(
		{
			"Store": df[col_store].astype(str),
			"Sales": pd.to_numeric(df[col_sales], errors="coerce").fillna(0).astype(float),
			"Year": df[col_order_date].map(extract_year),
		}
	)
	return out


def _assign_fiscal_quarter(file_index: int, year: int) -> int:
	if year == 2022:
		if file_index in (2, 6, 12):
			return 1
		if file_index in (3, 10, 11):
			return 2
	if year == 2023:
		if file_index in (4, 5, 8):
			return 3
		if file_index in (1, 7, 9):
			return 4
	return pd.NA


def _classify_store(diffs: List[float]) -> str:
	vals = [float(x) if pd.notna(x) else 0.0 for x in diffs]
	signs = [1 if v > 0 else (-1 if v < 0 else 0) for v in vals]
	pos_count = sum(1 for s in signs if s > 0)
	neg_count = sum(1 for s in signs if s < 0)
	if pos_count == 3:
		return "Going from strength to strength"
	if neg_count == 3:
		return "Going from bad to worse"
	if neg_count == 1 and pos_count == 2:
		neg_idx = signs.index(-1)
		if neg_idx == 0:
			return "Good growth in last half"
		if neg_idx == 1:
			return "Some good growth, but concerns in Q3"
		if neg_idx == 2:
			return "Good growth, until Q4"
	if pos_count == 1 and neg_count == 2:
		pos_idx = signs.index(1)
		if pos_idx == 0:
			return "Concerning performance in last half"
		if pos_idx == 1:
			return "Concerning performance, excluding Q3"
		if pos_idx == 2:
			return "Concerning performance, but improving in Q4"
	return "Concerning performance in last half"


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	all_rows: List[pd.DataFrame] = []
	for i in range(1, 13):
		fp = inputs_dir / f"input_{i:02d}.csv"
		if not fp.exists():
			continue
		df = _read_month_file(fp)
		df["file_index"] = i
		all_rows.append(df)
	combined = pd.concat(all_rows, ignore_index=True)

	combined["Quarter"] = [
		_assign_fiscal_quarter(int(fi), int(y)) if pd.notna(y) else pd.NA
		for fi, y in zip(combined["file_index"], combined["Year"])
	]
	combined = combined.dropna(subset=["Quarter"])
	combined["Quarter"] = combined["Quarter"].astype(int)

	quarterly = combined.groupby(["Store", "Quarter"], as_index=False)["Sales"].sum()

	quarterly = quarterly.sort_values(by=["Store", "Quarter"], kind="mergesort").reset_index(drop=True)
	quarterly["% Difference Q on Q"] = pd.NA
	for store, sdf in quarterly.groupby("Store"):
		idxs = sdf.index.tolist()
		prev_sales = None
		for idx in idxs:
			q = int(quarterly.at[idx, "Quarter"])
			sales = float(quarterly.at[idx, "Sales"])
			if q == 1 or prev_sales is None or prev_sales == 0:
				quarterly.at[idx, "% Difference Q on Q"] = pd.NA
			else:
				diff = (sales - prev_sales) / prev_sales * 100.0
				quarterly.at[idx, "% Difference Q on Q"] = round(diff + 1e-9, 1)
			prev_sales = sales

	def gather_diffs(g: pd.DataFrame) -> Tuple[float, float, float]:
		dmap = {int(r["Quarter"]): r["% Difference Q on Q"] for _, r in g.iterrows()}
		return (
			dmap.get(2, pd.NA),
			dmap.get(3, pd.NA),
			dmap.get(4, pd.NA),
		)

	evals = []
	for store, g in quarterly.groupby("Store"):
		diffs = list(gather_diffs(g))
		eval_text = _classify_store(diffs)
		for _, r in g.iterrows():
			evals.append((store, int(r["Quarter"]), eval_text))
	evals_df = pd.DataFrame(evals, columns=["Store", "Quarter", "Store Evaluation"])

	out = quarterly.merge(evals_df, on=["Store", "Quarter"], how="left")
	out = out[["Store", "Quarter", "Sales", "% Difference Q on Q", "Store Evaluation"]]

	return {"output_01.csv": out}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	result = solve(inputs_dir)
	for fname, df in result.items():
		(df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)).to_csv(cand_dir / fname, index=False, encoding="utf-8")


