from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def _parse_transaction_dates(series: pd.Series) -> pd.Series:
        parsed = pd.to_datetime(series, format="%a, %B %d, %Y", errors="coerce")
        fallback = pd.to_datetime(series, errors="coerce")
        return parsed.fillna(fallback)

    def _normalize_identifier(value):
        if pd.isna(value):
            return pd.NA
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return pd.NA
            if text.endswith(".0") and text.replace(".", "", 1).isdigit():
                text = text.split(".", 1)[0]
            return text
        if isinstance(value, (int, np.integer)):
            return str(int(value))
        if isinstance(value, (float, np.floating)):
            if np.isnan(value):
                return pd.NA
            return str(int(value))
        return pd.NA

    def _normalize_tier(value):
        if pd.isna(value):
            return pd.NA
        token = str(value).strip().lower()
        if not token:
            return pd.NA
        if "gold" in token or "goald" in token:
            return "Gold"
        if "silv" in token or "sliv" in token:
            return "Silver"
        if "bron" in token:
            return "Bronze"
        return pd.NA

    def _round_half_up(series: pd.Series, decimals: int = 0) -> pd.Series:
        factor = 10 ** decimals
        values = series.to_numpy(dtype="float64", copy=True)
        mask = np.isfinite(values)
        values[mask] = (
            np.sign(values[mask])
            * np.floor(np.abs(values[mask]) * factor + 0.5)
            / factor
        )
        return pd.Series(values, index=series.index, dtype="float64")

    def _complete_calendar(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        date_series = df[date_col].dropna()
        if date_series.empty:
            return df
        full_range = pd.date_range(
            date_series.min().normalize(),
            date_series.max().normalize(),
            freq="D",
        )
        existing = pd.Index(date_series.dt.normalize().unique())
        missing = full_range.difference(existing)
        if missing.empty:
            return df
        filler = pd.DataFrame({date_col: missing})
        return pd.concat([df, filler], ignore_index=True, sort=False)

    transactions = pd.read_csv(inputs_dir / "input_03.csv")
    products = pd.read_csv(inputs_dir / "input_02.csv")
    loyalty = pd.read_csv(inputs_dir / "input_01.csv")

    transactions["Transaction_Date"] = _parse_transaction_dates(
        transactions["Transaction_Date"]
    )
    transactions = transactions[
        transactions["Transaction_Date"].dt.year.isin([2023, 2024])
    ].copy()
    transactions = _complete_calendar(transactions, "Transaction_Date")

    transactions["Transanction_Number"] = transactions["Transanction_Number"].apply(
        _normalize_identifier
    )
    transactions["Loyalty_Number"] = transactions["Loyalty_Number"].apply(
        _normalize_identifier
    )

    splits = transactions["Product_ID"].str.split("-", n=2, expand=True)
    transactions["Product_Type"] = splits[0]
    transactions["Product_Scent"] = splits[1]
    transactions["Product_Size"] = splits[2]
    transactions.drop(columns=["Product_ID"], inplace=True)

    transactions["Product_Type"] = transactions["Product_Type"].str.strip()
    transactions["Product_Scent"] = (
        transactions["Product_Scent"].str.replace("_", " ", regex=False).str.strip()
    )
    transactions["Product_Size"] = transactions["Product_Size"].str.strip()

    cash_map = {1: "Card", 2: "Cash", "1": "Card", "2": "Cash"}
    transactions["Cash_or_Card"] = transactions["Cash_or_Card"].map(cash_map)

    products["Product_Size"] = products["Product_Size"].replace("", pd.NA)
    products["Pack_Size"] = products["Pack_Size"].replace("", pd.NA)
    products["Product_Size"] = products["Product_Size"].fillna(products["Pack_Size"])
    products["Product_Size"] = products["Product_Size"].str.strip()
    products["Product_Scent"] = products["Product_Scent"].str.strip()
    products["Product_Type"] = products["Product_Type"].str.strip()
    products["Unit_Cost"] = pd.to_numeric(products["Unit_Cost"], errors="coerce")
    products["Selling_Price"] = pd.to_numeric(
        products["Selling_Price"], errors="coerce"
    )
    products = products[
        ["Product_Type", "Product_Scent", "Product_Size", "Unit_Cost", "Selling_Price"]
    ]

    transactions = transactions.merge(
        products,
        how="left",
        on=["Product_Type", "Product_Scent", "Product_Size"],
    )

    transactions["Sales_Before_Discount"] = pd.to_numeric(
        transactions["Sales_Before_Discount"], errors="coerce"
    )
    price = transactions["Selling_Price"]
    sbd = transactions["Sales_Before_Discount"]
    qty = pd.Series(np.nan, index=transactions.index, dtype="float64")
    valid_price = price.notna() & price.ne(0)
    qty.loc[valid_price] = np.floor((sbd / price).where(valid_price))
    transactions["Quantity"] = qty

    loyalty["Loyalty_Number"] = loyalty["Loyalty_Number"].apply(_normalize_identifier)
    name_parts = loyalty["Customer_Name"].str.split(",", n=1, expand=True)
    last = name_parts[0].fillna("").str.strip()
    first = name_parts[1].fillna("").str.strip()
    loyalty["Customer_Name"] = (
        first + " " + last
    ).str.strip().str.title().replace({"": pd.NA})
    loyalty["Loyalty_Tier"] = loyalty["Loyalty_Tier"].apply(_normalize_tier)
    loyalty["Loyalty_Discount"] = (
        loyalty["Loyalty_Discount"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    )
    loyalty["Loyalty_Discount"] = (
        pd.to_numeric(loyalty["Loyalty_Discount"], errors="coerce") / 100
    )

    loyalty = loyalty[
        ["Loyalty_Number", "Customer_Name", "Loyalty_Tier", "Loyalty_Discount"]
    ]

    transactions = transactions.merge(loyalty, on="Loyalty_Number", how="left")

    discount_mask = (
        transactions["Loyalty_Number"].notna()
        & transactions["Loyalty_Discount"].notna()
        & transactions["Sales_Before_Discount"].notna()
    )
    sales_after_values = (
        transactions.loc[discount_mask, "Sales_Before_Discount"]
        * (1 - transactions.loc[discount_mask, "Loyalty_Discount"])
    )
    transactions.loc[discount_mask, "_sales_after_raw"] = sales_after_values
    transactions.loc[discount_mask, "Sales_After_Discount"] = np.round(
        sales_after_values,
        4,
    )

    profit_mask = (
        transactions["_sales_after_raw"].notna()
        & transactions["Unit_Cost"].notna()
        & transactions["Quantity"].notna()
    )
    profit_values = (
        transactions.loc[profit_mask, "_sales_after_raw"]
        - transactions.loc[profit_mask, "Unit_Cost"]
        * transactions.loc[profit_mask, "Quantity"]
    )
    transactions.loc[profit_mask, "Profit"] = _round_half_up(
        profit_values, decimals=2
    )
    if "_sales_after_raw" in transactions.columns:
        transactions.drop(columns=["_sales_after_raw"], inplace=True)

    transactions["Transaction_Date"] = transactions["Transaction_Date"].dt.strftime(
        "%d/%m/%Y"
    )
    transactions["Transanction_Number"] = transactions["Transanction_Number"].astype(
        "string"
    )
    output_cols = [
        "Transaction_Date",
        "Transanction_Number",
        "Product_Type",
        "Product_Scent",
        "Product_Size",
        "Cash_or_Card",
        "Loyalty_Number",
        "Customer_Name",
        "Loyalty_Tier",
        "Loyalty_Discount",
        "Quantity",
        "Sales_Before_Discount",
        "Sales_After_Discount",
        "Profit",
    ]
    result = transactions[output_cols].copy()

    result["_date_sort"] = pd.to_datetime(
        result["Transaction_Date"], format="%d/%m/%Y", errors="coerce"
    )
    result["_trans_sort"] = pd.to_numeric(
        result["Transanction_Number"], errors="coerce"
    )
    result = (
        result.sort_values(
            by=[
                "_date_sort",
                "_trans_sort",
                "Product_Type",
                "Product_Scent",
                "Product_Size",
            ],
            kind="mergesort",
        )
        .drop(columns=["_date_sort", "_trans_sort"])
    )

    result = result.drop_duplicates()

    rename_map = {
        "Transaction_Date": "Transaction Date",
        "Transanction_Number": "Transanction Number",
        "Product_Type": "Product Type",
        "Product_Scent": "Product Scent",
        "Product_Size": "Product Size",
        "Cash_or_Card": "Cash or Card",
        "Loyalty_Number": "Loyalty Number",
        "Customer_Name": "Customer Name",
        "Loyalty_Tier": "Loyalty Tier",
        "Loyalty_Discount": "Loyalty Discount",
        "Quantity": "Quantity",
        "Sales_Before_Discount": "Sales Before Discount",
        "Sales_After_Discount": "Sales After Discount",
        "Profit": "Profit",
    }
    result = result.rename(columns=rename_map)

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


