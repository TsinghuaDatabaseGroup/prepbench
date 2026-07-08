from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_type = pd.read_csv(inputs_dir / "input_01.csv")
    df_price = pd.read_csv(inputs_dir / "input_02.csv")

    def normalise_type(x: str) -> str:
        x_norm = (x or "").strip()
        if x_norm.lower().replace("-", " ").replace("  ", " ") in {"meat based", "meatbased"}:
            return "Meat-based"
        if x_norm.lower() in {"veggie", "vegetarian"}:
            return "Vegetarian"
        if x_norm.lower() == "vegan":
            return "Vegan"
        return x

    df_type["Type"] = df_type["Type"].apply(normalise_type)

    df = df_type.merge(df_price, on="Meal Option", how="inner")

    total_count = float(len(df))
    agg = (
        df.groupby("Type", as_index=False)
        .agg(**{
            "Average Price": ("Price", "mean"),
            "Count": ("Meal Option", "count"),
        })
    )
    agg["Percent of Total"] = (agg["Count"] / total_count * 100).round(0).astype(int)
    agg["Average Price"] = agg["Average Price"].round(2)
    out = agg[["Type", "Average Price", "Percent of Total"]].copy()

    type_order = {"Meat-based": 0, "Vegan": 1, "Vegetarian": 2}
    out["_order"] = out["Type"].map(type_order)
    out = out.sort_values("_order").drop(columns=["_order"]).reset_index(drop=True)

    out["Average Price"] = pd.to_numeric(out["Average Price"])
    out["Percent of Total"] = pd.to_numeric(out["Percent of Total"])

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

