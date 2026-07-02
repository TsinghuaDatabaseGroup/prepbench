from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_bool(val: object) -> bool:
        s = str(val).strip().lower()
        if s in {"true", "1", "yes"}:
            return True
        if s in {"false", "0", "no"}:
            return False
        return False

    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path, dtype=str)

    required_cols = [
        "Complaint ID",
        "Receipt Number",
        "Customer ID",
        "Date Received",
        "Date Resolved",
        "Timely Response",
        "Response to Consumer",
        "Issue Type",
        "Product Category",
        "Product ID",
        "Complaint Description",
    ]

    df = df[required_cols].copy()

    df["Timely Response"] = df["Timely Response"].map(parse_bool)


    return {"output_01.csv": df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


