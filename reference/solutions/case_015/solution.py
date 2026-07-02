from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    pattern = re.compile(r"input_(\d+)\.csv")
    region_mapping = {
        1: "Central",
        2: "East",
        3: "North",
        4: "South",
        5: "West",
    }
    region_sort_order = ["South", "Central", "North", "West", "East"]

    input_frames = [
        pd.read_csv(csv_path).assign(
            Region=region_mapping[int(pattern.fullmatch(csv_path.name).group(1))])
        for csv_path in sorted(inputs_dir.glob("input_*.csv"))
    ]
    combined = pd.concat(input_frames, ignore_index=True)
    combined["Order Date"] = pd.to_datetime(
        combined["Order Date"], format="%d/%m/%Y", dayfirst=True
    )

    regional_totals = (
        combined.groupby(["Region", "Stock"], as_index=False)["Sales"]
        .sum()
        .rename(columns={"Sales": "Total Regional Sales"})
    )

    stock_totals = (
        regional_totals.groupby("Stock", as_index=False)[
            "Total Regional Sales"]
        .sum()
        .rename(columns={"Total Regional Sales": "Total Sales"})
    )

    enriched = (
        combined.merge(regional_totals, on=["Region", "Stock"], how="left")
        .merge(stock_totals, on="Stock", how="left")
        .assign(
            **{
                "% of Total Sales": lambda x: x["Sales"] / x["Total Sales"] * 100,
                "% of Regional Sales": lambda x: x["Sales"] / x["Total Regional Sales"] * 100,
            }
        )
    )

    filtered = (
        enriched[enriched["Sales"] != enriched["Total Regional Sales"]]
        .assign(
            **{
                "% of Total Sales": lambda x: x["% of Total Sales"].round(12),
                "% of Regional Sales": lambda x: x["% of Regional Sales"].round(12),
                "Sales": lambda x: x["Sales"].round(2),
                "Total Regional Sales": lambda x: x["Total Regional Sales"].round(2),
                "Total Sales": lambda x: x["Total Sales"].round(2),
            }
        )
    )

    final_df = (
        filtered.assign(Region=pd.Categorical(
            filtered["Region"], categories=region_sort_order, ordered=True))
        .sort_values(["Region", "Customer ID", "Stock"])
        .assign(
            Region=lambda x: x["Region"].astype(str),
            **{"Order Date": lambda x: x["Order Date"].dt.strftime("%d/%m/%Y")}
        )
        .reset_index(drop=True)
        [[
            "% of Regional Sales",
            "% of Total Sales",
            "Region",
            "Customer ID",
            "First Name",
            "Last Name",
            "Sales",
            "Order Date",
            "Stock",
            "Total Regional Sales",
            "Total Sales",
        ]]
    )

    return {"output_01.csv": final_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False)
