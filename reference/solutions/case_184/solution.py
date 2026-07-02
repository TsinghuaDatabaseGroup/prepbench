import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    instore_sales = pd.read_csv(inputs_dir / "input_01.csv")
    online_sales = pd.read_csv(inputs_dir / "input_02.csv")
    product_lookup = pd.read_csv(inputs_dir / "input_03.csv")

    online_sales = online_sales.rename(columns={"Sales Timestamp": "Sales Date"})

    online_sales["Store"] = "Online"

    combined = pd.concat([instore_sales, online_sales], ignore_index=True)

    product_lookup = product_lookup.rename(columns={"Product ID": "Product"})
    combined = combined.merge(product_lookup, on="Product", how="left")
    combined["Product Type"] = combined["Product Name"].str.split().str[0]

    combined["Sales Date"] = pd.to_datetime(combined["Sales Date"], format="%d/%m/%Y %H:%M:%S")

    instore = combined[combined["Store"] != "Online"].copy()
    online = combined[combined["Store"] == "Online"].copy()

    instore = (
        instore.sort_values(["Store", "Product Type", "Sales Date"])\
        .drop_duplicates(subset=["Store", "Product Type", "Sales Date"], keep="first")
    )

    combined2 = pd.concat([instore, online], ignore_index=True)

    sort_cols = ["Store", "Product Type", "Sales Date"]
    if "ID" in combined2.columns:
        sort_cols.append("ID")
    combined2 = combined2.sort_values(sort_cols).reset_index(drop=True)

    combined2["Next Sale Date"] = combined2.groupby(["Store", "Product Type"])['Sales Date'].shift(-1)
    combined2["Time Diff Minutes"] = (combined2["Next Sale Date"] - combined2["Sales Date"]).dt.total_seconds() / 60

    combined2 = combined2[combined2["Time Diff Minutes"].notna()]
    combined2 = combined2[combined2["Time Diff Minutes"] >= 0]

    result = (
        combined2.groupby(["Store", "Product Type"], as_index=False)["Time Diff Minutes"].mean()
        .rename(columns={"Time Diff Minutes": "Average mins to next sale"})
    )

    result["Average mins to next sale"] = result["Average mins to next sale"].round(1)

    result = result[["Average mins to next sale", "Product Type", "Store"]]
    result = result.sort_values(["Store", "Product Type"]).reset_index(drop=True)

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
