from __future__ import annotations
from pathlib import Path
from typing import Dict
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    inp_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp_path).rename(
        columns={
            "COCKTAILS": "Cocktails",
            "Unnamed: 1": "Ingredients",
            "Unnamed: 2": "Cocktail Price",
        }
    )

    df["Cocktail Price"] = pd.to_numeric(df["Cocktail Price"])
    df["_cocktail_order"] = df.index + 1

    out = (
        df.assign(Ingredients=lambda d: d["Ingredients"].str.split(","))
        .explode("Ingredients")
        .assign(
            Ingredients=lambda d: d["Ingredients"].str.strip(),
            **{
                "Ingredient Position": lambda d: d.groupby("_cocktail_order")
                .cumcount()
                .add(1)
            },
        )
    )

    out["Avg Ingredient Price"] = (
        out.groupby("Ingredients")["Cocktail Price"].transform("mean").round(9)
    )

    out = (
        out.sort_values(["Ingredient Position", "_cocktail_order"])
        .reset_index(drop=True)[
            [
                "Ingredient Position",
                "Ingredients",
                "Cocktail Price",
                "Cocktails",
                "Avg Ingredient Price",
            ]
        ]
        .rename(columns={"Ingredients": "Ingredients Split"})
    )

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
