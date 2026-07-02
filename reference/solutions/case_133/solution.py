from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict


def _levenshtein(a: str, b: str) -> int:
    la, lb = len(a), len(b)
    dp = list(range(lb + 1))
    for i in range(1, la + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, lb + 1):
            temp = dp[j]
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[j] = min(
                dp[j] + 1,
                dp[j - 1] + 1,
                prev + cost
            )
            prev = temp
    return dp[lb]


def _clean_store_names(targets: pd.DataFrame, valid_stores: pd.Series) -> pd.DataFrame:
    valid_list = sorted(valid_stores.unique().tolist())

    def map_store(s: str) -> str:
        if s in valid_list:
            return s
        distances = [(v, _levenshtein(s, v)) for v in valid_list]
        distances.sort(key=lambda x: (x[1], x[0]))
        return distances[0][0] if distances else s
    targets = targets.copy()
    targets["Store"] = targets["Store"].astype(str).map(map_store)
    return targets


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    sales = pd.read_csv(inputs_dir / "input_01.csv")
    targets = pd.read_csv(inputs_dir / "input_02.csv")

    id_cols = ["Store", "Employee"]
    month_cols = [c for c in sales.columns if c not in id_cols]
    sales_long = sales.melt(
        id_vars=id_cols, value_vars=month_cols, var_name="Month", value_name="Sales")

    avg_sales = (
        sales_long.groupby(id_cols, as_index=False)["Sales"].mean()
        .rename(columns={"Sales": "Avg monthly Sales"})
    )
    avg_sales["Avg monthly Sales"] = avg_sales["Avg monthly Sales"].round().astype(
        int)

    targets_clean = _clean_store_names(targets, sales["Store"])

    merged = avg_sales.merge(
        targets_clean, on=["Store", "Employee"], how="left")

    sales_with_target = sales_long.merge(
        targets_clean, on=["Store", "Employee"], how="left")

    sales_with_target = sales_with_target.dropna(subset=["Monthly Target"])

    cond = sales_with_target["Sales"] >= sales_with_target["Monthly Target"]
    pct_met = (
        sales_with_target.assign(hit=cond.astype(int))
        .groupby(id_cols, as_index=False)
        .agg(months_met=("hit", "sum"), months_total=("hit", "count"))
    )
    pct_met["% of months target met"] = (
        pct_met["months_met"] * 100 / pct_met["months_total"]).round().astype(int)
    pct_met = pct_met[id_cols + ["% of months target met"]]

    out = (
        merged.merge(pct_met, on=id_cols, how="left")
    )

    out = out.dropna(subset=["Monthly Target"])
    out = out[out["Avg monthly Sales"] < 0.9 * out["Monthly Target"]]

    out = out[["Store", "Employee", "Avg monthly Sales",
               "% of months target met", "Monthly Target"]]
    out = out.sort_values(["Store", "Employee"],
                          kind="mergesort").reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    import json

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
