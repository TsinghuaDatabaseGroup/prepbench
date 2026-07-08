from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_amount(value: str) -> int:
        if pd.isna(value):
            return 0
        s = str(value).strip()
        s_clean = s.replace(",", "")
        multiplier = 1.0
        if s_clean.endswith("K") or s_clean.endswith("k"):
            multiplier = 1_000.0
            s_clean = s_clean[:-1]
        elif s_clean.endswith("M") or s_clean.endswith("m"):
            multiplier = 1_000_000.0
            s_clean = s_clean[:-1]
        try:
            number = float(s_clean)
        except ValueError:
            s_digits = "".join(ch for ch in s_clean if ch.isdigit() or ch in ".-+")
            number = float(s_digits) if s_digits else 0.0
        return int(round(number * multiplier))

    years = list(range(2018, 2023))
    input_files: List[Path] = sorted(inputs_dir.glob("input_*.csv"))
    input_files.sort(key=lambda p: p.name)

    records = []
    for idx, file_path in enumerate(input_files):
        year = years[idx]
        df = pd.read_csv(file_path)
        sales = df["Sales"].apply(parse_amount)
        profits = df["Profits"].apply(parse_amount)
        total_sales = int(sales.sum())
        total_profits = int(profits.sum())
        records.append({"Year": year, "Sales": total_sales, "Profits": total_profits})

    out = pd.DataFrame(records, columns=["Year", "Sales", "Profits"])
    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


