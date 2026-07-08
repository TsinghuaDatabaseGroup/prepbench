from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    cocktails = pd.read_csv(inputs_dir / "input_01.csv")
    sourcing = pd.read_csv(inputs_dir / "input_02.csv")
    rates = pd.read_csv(inputs_dir / "input_03.csv")

    rate_map = dict(zip(rates["Currency"], rates["Conversion Rate £"]))

    sourcing = sourcing.copy()
    sourcing["rate"] = sourcing["Currency"].map(rate_map)
    sourcing["price_gbp_per_bottle"] = sourcing["Price"] / sourcing["rate"]
    sourcing["price_gbp_per_ml"] = sourcing["price_gbp_per_bottle"] / \
        sourcing["ml per Bottle"]
    sourcing = sourcing[["Ingredient", "price_gbp_per_ml"]]

    def parse_recipe(recipe: str) -> list[tuple[str, float]]:
        items = []
        if pd.isna(recipe) or not str(recipe).strip():
            return items
        for part in str(recipe).split(";"):
            part = part.strip()
            if not part:
                continue
            if ":" not in part:
                continue
            name, qty = part.split(":", 1)
            name = name.strip()
            qty = qty.strip()
            qty = qty.lower().replace("ml", "").strip()
            try:
                ml = float(qty)
            except ValueError:
                continue
            items.append((name, ml))
        return items

    rows = []
    for _, r in cocktails.iterrows():
        cocktail = r["Cocktail"]
        price = float(r["Price (£)"])
        recipe = r["Recipe (ml)"]
        for ing, ml in parse_recipe(recipe):
            rows.append({
                "Cocktail": cocktail,
                "Price": price,
                "Ingredient": ing,
                "ml_needed": ml,
            })
    long_df = pd.DataFrame(rows)

    long_df = long_df.merge(sourcing, on="Ingredient", how="left")

    long_df["cost_component"] = long_df["price_gbp_per_ml"] * \
        long_df["ml_needed"]
    cost_df = long_df.groupby(["Cocktail", "Price"], as_index=False)[
        "cost_component"].sum()
    cost_df.rename(columns={"cost_component": "Cost"}, inplace=True)

    cost_df["Cost"] = cost_df["Cost"].round(2)
    cost_df["Price"] = cost_df["Price"].round(2)
    cost_df["Margin"] = (cost_df["Price"] - cost_df["Cost"]).round(2)

    out_df = cost_df[["Margin", "Cost", "Cocktail", "Price"]]

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
