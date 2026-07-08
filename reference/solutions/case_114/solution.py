from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    menu_fp = inputs_dir / "input_01.csv"
    orders_fp = inputs_dir / "input_02.csv"

    menu = pd.read_csv(menu_fp)
    orders = pd.read_csv(orders_fp)

    groups = [
        ("Pizza", "Pizza", "Pizza Price ", "Pizza ID"),
        ("Pasta", "Pasta", "Pasta Price", "Pasta ID"),
        ("House Plates", "House Plates", "House Plates Prices", "House Plates ID"),
    ]

    long_parts: list[pd.DataFrame] = []
    for type_name, name_col, price_col, id_col in groups:
        cols = [name_col, price_col, id_col]
        existing = [c for c in cols if c in menu.columns]
        if len(existing) < 3:
            tmp = menu.reindex(columns=cols)
        else:
            tmp = menu[cols].copy()
        tmp = tmp.rename(
            columns={name_col: "Name", price_col: "Price", id_col: "ID"})
        tmp["Type"] = type_name
        long_parts.append(tmp)

    menu_long = pd.concat(long_parts, ignore_index=True)
    menu_long = menu_long.dropna(subset=["ID", "Price", "Name"]).copy()

    def _to_id_str(x):
        try:
            xi = int(float(x))
            return str(xi)
        except Exception:
            return pd.NA

    menu_long["ID"] = menu_long["ID"].apply(_to_id_str)
    menu_long = menu_long.dropna(subset=["ID"]).copy()
    menu_long["Price"] = menu_long["Price"].astype(float)

    orders_exp = orders.copy()
    orders_exp["Order Date"] = pd.to_datetime(
        orders_exp["Order Date"], errors="coerce")
    orders_exp["Weekday"] = orders_exp["Order Date"].dt.day_name()

    orders_exp["ID"] = orders_exp["Order"].astype(str).str.split("-")
    orders_exp = orders_exp.explode("ID").reset_index(drop=True)
    orders_exp["ID"] = orders_exp["ID"].str.strip()

    fact = orders_exp.merge(menu_long[["ID", "Price"]], on="ID", how="left")

    fact["AdjPrice"] = fact["Price"]
    fact.loc[fact["Weekday"] == "Monday",
             "AdjPrice"] = fact.loc[fact["Weekday"] == "Monday", "AdjPrice"] * 0.5

    out1 = (
        fact.groupby("Weekday", as_index=False)["AdjPrice"].sum()
    )
    out1 = out1.rename(columns={"AdjPrice": "Price"})

    out1["Price"] = out1["Price"].round(0).astype(int)

    weekday_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]
    out1["_ord"] = out1["Weekday"].apply(
        lambda x: weekday_order.index(x) if x in weekday_order else 99)
    out1 = out1.sort_values(["_ord"]).drop(
        columns=["_ord"]).reset_index(drop=True)

    out2 = (
        orders_exp.groupby("Customer Name", as_index=False)["ID"].count()
        .rename(columns={"ID": "Count Items"})
    )
    max_count = out2["Count Items"].max()
    out2 = out2[out2["Count Items"] == max_count].sort_values(
        ["Customer Name"]).head(1).reset_index(drop=True)

    out2["Count Items"] = out2["Count Items"].astype(int)

    outputs: dict[str, pd.DataFrame] = {
        "output_01.csv": out1[["Price", "Weekday"]],
        "output_02.csv": out2[["Count Items", "Customer Name"]],
    }
    return outputs


if __name__ == "__main__":
    import sys

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
