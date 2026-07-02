from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def _format_dd_mm_yyyy(day: int, month: int, year: int) -> str:
        return f"{day:02d}/{month:02d}/{year:d}"
    year = 2024
    all_dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="D")

    day_of_year = all_dates.dayofyear

    new_month = ((day_of_year - 1) // 28) + 1
    new_day = ((day_of_year - 1) % 28) + 1

    original_date_str = [d.strftime("%d/%m/%Y") for d in all_dates]
    new_date_str = [_format_dd_mm_yyyy(int(d), int(m), year) for d, m in zip(new_day, new_month)]

    df = pd.DataFrame({
        "Date": original_date_str,
        "New Date": new_date_str,
    })

    orig_month = [d.month for d in all_dates]
    mask_changed = pd.Series(orig_month) != pd.Series(new_month)
    df_out = df.loc[mask_changed].copy()

    return {"output_01.csv": df_out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


