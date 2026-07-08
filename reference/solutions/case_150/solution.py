from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def _to_date_str(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, dayfirst=True).dt.strftime("%d/%m/%Y")


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inp_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp_path, dtype=str)

    df.columns = [c.strip() for c in df.columns]

    order_split = df["OrderID"].str.split("-", n=1, expand=True)
    df["Store"] = order_split[0]
    df["OrderID_num"] = pd.to_numeric(order_split[1], errors="coerce")

    df["Order Date_dt"] = pd.to_datetime(df["Order Date"], dayfirst=True)

    df["Returned"] = (df["Return State"].fillna(
        "").str.strip() == "Return Processed").astype(int)

    def parse_price(x: str) -> float:
        if pd.isna(x):
            return np.nan
        x = str(x).replace("£", "").replace(",", "").strip()
        return float(x) if x != "" else np.nan

    df["Unit Price_num"] = df["Unit Price"].map(parse_price)
    df["Quantity_num"] = pd.to_numeric(
        df["Quantity"], errors="coerce").fillna(0).astype(int)

    df["Sales"] = (df["Unit Price_num"] * df["Quantity_num"]).round(2)

    store_first = (
        df.groupby("Store", as_index=False)["Order Date_dt"].min().rename(
            columns={"Order Date_dt": "First Order_dt"})
    )
    store_dim = store_first.copy()
    store_dim["First Order"] = store_dim["First Order_dt"].dt.strftime(
        "%d/%m/%Y")
    store_dim = store_dim.sort_values(
        ["First Order_dt", "Store"]).reset_index(drop=True)
    store_dim.insert(0, "StoreID", np.arange(1, len(store_dim) + 1))
    store_dim = store_dim[["StoreID", "Store", "First Order"]]

    cust_stats = (
        df.assign(Order_group=df["Store"].astype(
            str) + "-" + df["OrderID_num"].astype(str))
        .groupby("Customer", as_index=False)
        .agg(
            First_Order_dt=("Order Date_dt", "min"),
            Number_of_Orders=("Order_group", lambda s: s.nunique()),
            Returned_cnt=("Returned", "sum"),
            Total_lines=("Returned", "count"),
        )
    )
    from decimal import Decimal, ROUND_HALF_UP

    def _half_up(num, den):
        if den == 0:
            return 0.0
        return float((Decimal(str(num)) / Decimal(str(den))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    cust_stats["Return %"] = [_half_up(n, d) for n, d in zip(
        cust_stats["Returned_cnt"], cust_stats["Total_lines"])]
    cust_dim = cust_stats.rename(columns={
        "First_Order_dt": "First Order_dt",
        "Number_of_Orders": "Number of Orders",
    })
    cust_dim["First Order"] = cust_dim["First Order_dt"].dt.strftime(
        "%d/%m/%Y")
    cust_dim = cust_dim.sort_values(["First Order_dt", "Customer"], key=lambda x: x.str.lower(
    ) if x.name == 'Customer' else x).reset_index(drop=True)
    cust_dim.insert(0, "CustomerID", np.arange(1, len(cust_dim) + 1))
    cust_dim = cust_dim[[
        "CustomerID", "Customer", "Return %", "Number of Orders", "First Order"
    ]]

    prod_first = (
        df.groupby(["Category", "Sub-Category", "Product Name",
                   "Unit Price_num"], as_index=False)["Order Date_dt"]
        .min()
        .rename(columns={"Order Date_dt": "First Sold_dt"})
    )
    prod_dim = prod_first.copy()
    prod_dim["First Sold"] = prod_dim["First Sold_dt"].dt.strftime("%d/%m/%Y")
    prod_dim = prod_dim.sort_values(
        ["First Sold_dt", "Product Name"],
        key=lambda col: col.str.lower() if col.name == "Product Name" else col
    ).reset_index(drop=True)
    prod_dim.insert(0, "ProductID", np.arange(1, len(prod_dim) + 1))
    prod_dim = prod_dim.rename(columns={"Unit Price_num": "Unit Price"})
    prod_dim = prod_dim[[
        "ProductID", "Category", "Sub-Category", "Product Name", "Unit Price", "First Sold"
    ]]

    fact = df.copy()
    fact["StoreID"] = fact["Store"].map(
        store_dim.set_index("Store")["StoreID"])
    fact["CustomerID"] = fact["Customer"].map(
        cust_dim.set_index("Customer")["CustomerID"])

    fact = fact.merge(
        prod_dim[["ProductID", "Category", "Sub-Category",
                  "Product Name", "Unit Price"]],
        left_on=["Category", "Sub-Category", "Product Name", "Unit Price_num"],
        right_on=["Category", "Sub-Category", "Product Name", "Unit Price"],
        how="left",
    )

    fact["Order Date"] = fact["Order Date_dt"].dt.strftime("%d/%m/%Y")

    fact_out = fact[[
        "StoreID", "CustomerID", "OrderID_num", "Order Date", "ProductID", "Returned", "Quantity_num", "Sales"
    ]].rename(columns={
        "OrderID_num": "OrderID",
        "Quantity_num": "Quantity",
    })

    out = {
        "output_04.csv": store_dim,
        "output_01.csv": cust_dim,
        "output_03.csv": prod_dim,
        "output_02.csv": fact_out,
    }
    return out


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

    for fname in dfs.keys():
        print(f"Wrote {cand_dir / fname}")
