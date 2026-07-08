from __future__ import annotations
from pathlib import Path
import pandas as pd
import math


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    freq_df = pd.read_csv(inputs_dir / "input_01.csv")
    prod_df = pd.read_csv(inputs_dir / "input_02.csv")
    cust_df = pd.read_csv(inputs_dir / "input_03.csv")

    prod_df["Product"] = prod_df["Product"].astype(str).str.strip()
    prod_df["Price"] = pd.to_numeric(prod_df["Price"], errors="coerce")

    freq_map = {
        "week": 52,
        "month": 12,
        "quarter": 4,
        "year": 1,
    }
    freq_lookup = dict(zip(freq_df["Subscription Frequency"], freq_df["Frequency"].str.strip()))

    cust_exploded = cust_df.copy()
    cust_exploded["Packages"] = cust_exploded["Packages"].astype(str)
    cust_exploded = cust_exploded.assign(
        Subscription_Package=cust_exploded["Packages"].str.split("|")
    ).explode("Subscription_Package", ignore_index=True)
    cust_exploded["Subscription_Package"] = pd.to_numeric(cust_exploded["Subscription_Package"], errors="coerce").astype("Int64")

    tmp = cust_exploded[cust_exploded["Subscription_Package"].notna()].copy()
    tmp = tmp[tmp["Subscription_Package"] != 7]
    tmp["freq_text"] = tmp["Frequency"].map(freq_lookup)
    tmp["multiplier"] = tmp["freq_text"].map(freq_map).fillna(0).astype(int)
    annual_orders_by_pkg = (
        tmp.groupby("Subscription_Package", as_index=False)["multiplier"].sum()
        .rename(columns={"Subscription_Package": "Subscription Package", "multiplier": "annual_orders"})
    )

    price_map = prod_df.set_index("Subscription Package")["Price"].to_dict()
    annual_orders_by_pkg["price"] = annual_orders_by_pkg["Subscription Package"].map(price_map)

    weighted_sum = (annual_orders_by_pkg["annual_orders"] * annual_orders_by_pkg["price"]).sum()
    total_orders = annual_orders_by_pkg["annual_orders"].sum()
    mystery_price = math.floor(weighted_sum / total_orders) if total_orders > 0 else 0

    out02 = prod_df.copy()
    out02.loc[out02["Subscription Package"] == 7, "Price"] = mystery_price
    out02["Subscription Package"] = pd.to_numeric(out02["Subscription Package"]).astype(int)
    out02["Price"] = pd.to_numeric(out02["Price"]).astype(int)
    out02 = out02[["Subscription Package", "Product", "Price"]]

    cust_exploded["freq_text"] = cust_exploded["Frequency"].map(freq_lookup)
    cust_exploded["multiplier"] = cust_exploded["freq_text"].map(freq_map).fillna(0).astype(int)

    prices_df = out02[["Subscription Package", "Price"]].rename(columns={"Subscription Package": "Subscription_Package", "Price": "Price_per_period"})
    cust_prices = cust_exploded.merge(prices_df, how="left", on="Subscription_Package")

    cust_prices["Price_per_period"] = cust_prices["Price_per_period"].fillna(0)

    cust_prices["annual_cost"] = cust_prices["Price_per_period"] * cust_prices["multiplier"]

    out01 = (
        cust_prices.groupby("Name", as_index=False)["annual_cost"].sum()
        .rename(columns={"annual_cost": "Subscription Cost (Per Annum)"})
    )

    out01["Subscription Cost (Per Annum)"] = out01["Subscription Cost (Per Annum)"].astype(int)
    out01 = out01[["Subscription Cost (Per Annum)", "Name"]]

    return {
        "output_02.csv": out02,
        "output_01.csv": out01,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

