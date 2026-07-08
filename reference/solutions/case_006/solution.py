from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input1_path = inputs_dir / "input_01.csv"
    input2_path = inputs_dir / "input_02.csv"
    input3_path = inputs_dir / "input_03.csv"

    df1 = pd.read_csv(input1_path)

    base = df1.rename(columns={"Category": "Product"})[
        ["Country", "Month", "Product", "Profit"]].copy()

    df2 = pd.read_csv(input2_path)
    df3 = pd.read_csv(input3_path)

    units_by_cat = (
        df2[df2["Country"] == "England"]
        .groupby("Category", as_index=False)["Units Sold"].sum()
        .rename(columns={"Category": "Product"})
    )

    type_map = {"Bar": "Bar Soap", "Liquid": "Liquid Soap"}
    ppu = (
        df3.assign(profit_per_unit=df3["Selling Price per Unit"] - df3["Manufacturing Cost per Unit"],
                   Product=df3["Type of Soap"].map(type_map))
        [["Product", "profit_per_unit"]]
    )

    march = units_by_cat.merge(ppu, on="Product", how="inner")
    march["Profit"] = (march["Units Sold"] *
                       march["profit_per_unit"]).round().astype(int)
    march["Country"] = "England"
    march["Month"] = "2019-03-19"
    df_march = march[["Country", "Month", "Product", "Profit"]]

    order = {"Bar Soap": 0, "Liquid Soap": 1}
    df_march = df_march.sort_values(
        by="Product", key=lambda s: s.map(order)).reset_index(drop=True)

    out_df = pd.concat([base, df_march], ignore_index=True)

    out_df["Profit"] = out_df["Profit"].astype(int)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")
