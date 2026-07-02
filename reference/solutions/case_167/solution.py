from __future__ import annotations

from pathlib import Path

import pandas as pd

TICK = "🗸"


def _normalize_course(value: str) -> str | None:
    cleaned = value.strip().lower()
    if cleaned.startswith("starter"):
        return "Starters"
    if cleaned.startswith("main"):
        return "Mains"
    if cleaned.startswith("dessert"):
        return "Dessert"
    return None


def _reshape_orders(orders_df: pd.DataFrame) -> pd.DataFrame:
    name_row = orders_df.iloc[0]
    guest_mask = name_row.notna() & (name_row.astype("string").str.strip() != "")
    guest_cols = name_row.index[guest_mask].tolist()

    records = [
        pd.DataFrame({
            "Guest": name_row[col].strip(),
            "value": orders_df.loc[1:, col],
            "selection": orders_df.loc[1:, col + 1],
        })
        for col in guest_cols
    ]

    combined = pd.concat(records, ignore_index=True)
    combined["value"] = combined["value"].astype("string").str.strip()
    combined["selection"] = combined["selection"].astype("string").str.strip()

    combined["course_marker"] = combined["value"].apply(_normalize_course)
    combined["Course"] = combined.groupby(
        "Guest")["course_marker"].transform("ffill")

    dishes = combined[combined["course_marker"].isna() & (
        combined["selection"] == TICK) & combined["value"].notna()].copy()
    dishes = dishes.rename(columns={"value": "Dish"}).drop(
        columns=["course_marker"])
    return dishes


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    orders_path = inputs_dir / "input_01.csv"
    lookup_path = inputs_dir / "input_02.csv"

    orders_df = pd.read_csv(orders_path, header=None, dtype=str)
    lookup_df = pd.read_csv(lookup_path, dtype={"Recipe ID": int, "Dish": str})
    lookup_df["Dish"] = lookup_df["Dish"].str.strip()

    dishes = _reshape_orders(orders_df)
    result = dishes.merge(lookup_df, on="Dish", how="left")
    result["Recipe ID"] = result["Recipe ID"].astype(int)
    result["Dish"] = result["Dish"].str.replace("'", "’", regex=False)

    output_df = result[["Guest", "Course", "Recipe ID", "Dish"]].sort_values(
        by=["Guest", "Course", "Recipe ID"]
    ).reset_index(drop=True)

    return {"output_01.csv": output_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        output_path = cand_dir / filename
        df.to_csv(output_path, index=False, encoding="utf-8")
