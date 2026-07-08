from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_customers = pd.read_csv(inputs_dir / "input_01.csv")
    df_loyalty = pd.read_csv(inputs_dir / "input_02.csv")
    df_stores = pd.read_csv(inputs_dir / "input_03.csv")

    def extract_points(s: pd.Series) -> pd.Series:
        return (
            s.astype(str)
            .str.extract(r"([0-9]+(?:\.[0-9]+)?)", expand=False)
            .astype(float)
        )

    df_loyalty["Loyalty Points"] = extract_points(df_loyalty["Loyalty Points"])
    df_loyalty["Date"] = pd.to_datetime(
        df_loyalty["DateTime_Out"], dayfirst=False, errors="coerce").dt.strftime("%d/%m/%Y")

    def split_email(email: str) -> tuple[str, str]:
        local = str(email).split("@")[0]
        parts = local.split(".")
        first = parts[0].capitalize() if parts else ""
        last_initial = parts[1][0].upper() if len(
            parts) > 1 and parts[1] else ""
        return first, last_initial

    first_last = df_loyalty["Email Address"].apply(split_email)
    df_loyalty["First Name"] = first_last.apply(lambda x: x[0])
    df_loyalty["Last Name"] = first_last.apply(lambda x: x[1])

    df_customers["Last Initial"] = df_customers["Last Name"].astype(
        str).str[:1].str.upper()
    df_customers["First Key"] = df_customers["First Name"].astype(
        str).str.strip().str.capitalize()

    df_loyalty["First Key"] = df_loyalty["First Name"].astype(str)
    df_loyalty["Last Initial"] = df_loyalty["Last Name"].astype(str)

    merged = df_loyalty.merge(
        df_customers[["First Key", "Last Initial",
                      "First Name", "Last Name", "Postcode", "address"]],
        on=["First Key", "Last Initial"],
        how="left",
    )

    merged = merged.copy()

    merged = merged.merge(df_stores, on="Store ID", how="left")

    merged = merged[merged["Postcode"].notna() & (
        merged["Postcode"].astype(str).str.strip() != "")]

    merged["Rank"] = merged.groupby(["City", "Store"], dropna=False)[
        "Loyalty Points"].rank(method="dense", ascending=False).astype(int)

    merged = merged[merged["Rank"] <= 5]

    if "First Name_y" in merged.columns:
        merged["First Name"] = merged["First Name_y"].fillna(
            merged.get("First Name_x"))
    else:
        merged["First Name"] = merged["First Name_x"]
    if "Last Name_y" in merged.columns:
        merged["Last Name"] = merged["Last Name_y"].fillna(
            merged.get("Last Name_x"))
    else:
        merged["Last Name"] = merged["Last Name_x"]

    out = merged[[
        "City",
        "Store",
        "Rank",
        "Email Address",
        "First Name",
        "Last Name",
        "Loyalty Points",
        "Date",
        "Postcode",
        "address",
    ]].copy()

    out["Rank"] = out["Rank"].astype(int)
    out["Loyalty Points"] = out["Loyalty Points"].astype(float)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False)
