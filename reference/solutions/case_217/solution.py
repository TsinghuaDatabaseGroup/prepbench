from pathlib import Path
from typing import Dict

import pandas as pd


def _easter_sunday_gregorian(year: int) -> pd.Timestamp:
	a = year % 19
	b = year // 100
	c = year % 100
	d = b // 4
	e = b % 4
	f = (b + 8) // 25
	g = (b - f + 1) // 3
	h = (19 * a + b - d - g + 15) % 30
	i = c // 4
	k = c % 4
	l = (32 + 2 * e + 2 * i - h - k) % 7
	m = (a + 11 * h + 22 * l) // 451
	month = (h + l - 7 * m + 114) // 31
	day = ((h + l - 7 * m + 114) % 31) + 1
	return pd.Timestamp(year=year, month=int(month), day=int(day))


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
	years = list(range(1700, 2024))
	dates = [_easter_sunday_gregorian(y) for y in years]
	df = pd.DataFrame(
		{
			"Calculation1": range(1, len(years) + 1),
			"Easter Sunday": [d.strftime("%d/%m/%Y") for d in dates],
		}
	)
	return {"output_01.csv": df}


if __name__ == "__main__":
	task_dir = Path(__file__).parent
	inputs_dir = task_dir / "inputs"
	cand_dir = task_dir / "cand"
	cand_dir.mkdir(parents=True, exist_ok=True)

	result = solve(inputs_dir)
	for fname, df in result.items():
		(df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)).to_csv(cand_dir / fname, index=False, encoding="utf-8")