from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path)

    df = df.drop_duplicates(subset=["Customer ID"], keep="first").copy()

    if "Customer ID" in df.columns:
        df["Customer ID"] = pd.to_numeric(df["Customer ID"], errors="coerce")

    cols = [
        "Customer ID",
        "First Name",
        "Last Name",
        "Phone Number",
        "Address",
    ]
    df = df[cols]

    df = df.sort_values(["Customer ID"]).reset_index(drop=True)

    return {"output_01.csv": df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


