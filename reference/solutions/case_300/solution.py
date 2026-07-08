from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    inv = pd.read_csv(inputs_dir / "input_01.csv", parse_dates=["Inventory Date"])
    products = pd.read_csv(inputs_dir / "input_02.csv")

    products["Category"] = products["Category"].astype(str).str.strip()
    products["Product"] = products["Product"].astype(str).str.strip()

    inv = inv.sort_values(["Store", "Product ID", "Inventory Date"]).reset_index(drop=True)

    def compute_by_group(g: pd.DataFrame) -> pd.DataFrame:
        g = g.sort_values("Inventory Date").copy()
        qty = g["Quantity Available"].astype(int).values
        n = len(g)
        orders = [0] * n
        sold = [0] * n

        prev_qty = qty[0]
        for i in range(n):
            if i == 0:
                orders[i] = 0
            else:
                orders[i] = (30 - prev_qty) if prev_qty <= 10 else 0
            sales_i = prev_qty + orders[i] - qty[i]
            sold[i] = max(0, int(sales_i))
            prev_qty = qty[i]

        g["Ordered"] = orders
        g["Sold"] = sold
        return g

    inv_calc = inv.groupby(["Store", "Product ID"], group_keys=False).apply(compute_by_group)

    grouped = inv_calc.groupby(["Store", "Product ID"], as_index=False)
    summary = grouped.agg(
        **{
            "Total Quantity Sold": ("Sold", "sum"),
            "Avg Quantity Sold per Week": ("Sold", "mean"),
        }
    )
    sizes = grouped.size().rename(columns={"size": "Weeks"})
    qa_flags = inv_calc.assign(order_trigger=(inv_calc["Quantity Available"] <= 10))
    orders_per_group = qa_flags.groupby(["Store", "Product ID"], as_index=False)["order_trigger"].sum()
    orders_per_group = orders_per_group.rename(columns={"order_trigger": "Orders"})
    aux = sizes.merge(orders_per_group, on=["Store", "Product ID"], how="left")
    def avg_every_k_weeks(row):
        w = int(row.get("Weeks", 0))
        o = int(row.get("Orders", 0))
        if o <= 0:
            return 0.0
        return w / o
    aux["Avg Order Frequency"] = aux.apply(avg_every_k_weeks, axis=1)
    summary = summary.merge(aux[["Store", "Product ID", "Avg Order Frequency"]], on=["Store", "Product ID"], how="left")

    summary["Avg Quantity Sold per Week"] = summary["Avg Quantity Sold per Week"].round(1)
    summary["Avg Order Frequency"] = summary["Avg Order Frequency"].round(1)

    out = summary.merge(products, on="Product ID", how="left")
    out = out[[
        "Store",
        "Category",
        "Product",
        "Total Quantity Sold",
        "Avg Quantity Sold per Week",
        "Avg Order Frequency",
    ]]

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


