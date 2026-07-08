from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    contracts = pd.read_csv(inputs_dir / "input_01.csv")
    lengths = pd.read_csv(inputs_dir / "input_02.csv")

    contracts["Contract Length (months)"] = contracts["Contract Length (months)"].astype(int)
    contracts["Monthly Cost"] = contracts["Monthly Cost"].astype(int)
    contracts["Start Date"] = pd.to_datetime(contracts["Start Date"], format="%Y-%m-%d", errors="raise")

    names_in_order = list(contracts["Name"])
    rr_order = list(reversed(names_in_order))
    name_order_map = {n: i for i, n in enumerate(rr_order)}

    contracts_ = contracts.copy()
    contracts_["__key"] = 1
    lengths_ = lengths.copy()
    lengths_["__key"] = 1
    exp = pd.merge(contracts_, lengths_, on="__key").drop(columns=["__key"])

    exp = exp[exp["Length"] <= exp["Contract Length (months)"]].copy()

    exp["idx"] = exp["Length"] - 1

    exp["Payment Date"] = exp["Start Date"] + exp["idx"].apply(lambda m: pd.DateOffset(months=int(m)))
    exp["Payment Date"] = pd.to_datetime(exp["Payment Date"]) 

    exp["name_order"] = exp["Name"].map(name_order_map)
    exp = exp.sort_values(["idx", "name_order"]).reset_index(drop=True)

    out_cols = [
        "Payment Date",
        "Name",
        "Monthly Cost",
        "Contract Length (months)",
        "Start Date",
    ]

    out = exp[out_cols].copy()

    for c in ["Payment Date", "Start Date"]:
        out[c] = out[c].dt.strftime("%d/%m/%Y")

    out["Monthly Cost"] = out["Monthly Cost"].astype(int)
    out["Contract Length (months)"] = out["Contract Length (months)"].astype(int)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

