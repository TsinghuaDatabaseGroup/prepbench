from pathlib import Path
from typing import Dict
import pandas as pd
import numpy as np
import re


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    doubles = pd.read_csv(inputs_dir / "input_01.csv")
    mixed = pd.read_csv(inputs_dir / "input_02.csv")
    singles = pd.read_csv(inputs_dir / "input_03.csv")

    def normalize_year_col(df: pd.DataFrame, year_col: str = "year") -> pd.DataFrame:
        df = df.copy()
        df[year_col] = df[year_col].astype(str)
        notheld_mask = df.apply(lambda r: any(isinstance(
            v, str) and "not held" in v.lower() for v in r), axis=1)
        df = df[~notheld_mask].copy()
        year_extracted = df[year_col].str.extract(r"(\d{4})")[0]
        df["__year_tmp__"] = pd.to_numeric(year_extracted, errors="coerce")
        df = df[df["__year_tmp__"].notna()].copy()
        df[year_col] = df["__year_tmp__"].astype(int)
        df = df.drop(columns=["__year_tmp__"])
        return df

    doubles = normalize_year_col(doubles, "year")
    singles = normalize_year_col(singles, "year")

    mixed = mixed.copy()
    mixed = mixed[~mixed["Year"].astype(str).str.contains(
        "No competition", case=False, na=False)]
    mixed["Year"] = pd.to_numeric(mixed["Year"], errors="coerce")
    mixed = mixed[mixed["Year"].notna()].copy()
    mixed["Year"] = mixed["Year"].astype(int)

    def clean_person_name(name: str) -> str:
        s = str(name).strip()
        s = re.sub(r"\s*\([^)]*\)", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        s = s.strip(", ")
        return s

    def split_names(cell: str) -> list[str]:
        if pd.isna(cell):
            return []
        s = str(cell)
        s = s.replace("\n", ",")
        parts = [p.strip() for p in s.split(",") if p.strip()]
        cleaned = [clean_person_name(p) for p in parts]
        return cleaned

    rows = []
    for _, r in singles.iterrows():
        y = int(r["year"])
        for name in split_names(r.get("men", "")):
            if name:
                rows.append((y, name, "Men's Singles", "Men"))
        for name in split_names(r.get("women", "")):
            if name:
                rows.append((y, name, "Women's Singles", "Women"))

    for _, r in doubles.iterrows():
        y = int(r["year"])
        for name in split_names(r.get("men", "")):
            if name:
                rows.append((y, name, "Men's Doubles", "Men"))
        for name in split_names(r.get("women", "")):
            if name:
                rows.append((y, name, "Women's Doubles", "Women"))

    for _, r in mixed.iterrows():
        y = int(r["Year"])
        for name in split_names(r.get("Champions", "")):
            if name:
                rows.append((y, name, "Mixed Doubles", None))

    long_df = pd.DataFrame(rows, columns=[
                           "Year", "Champion", "Tournament", "Gender_hint"]).dropna(subset=["Champion"])

    gender_map = (
        long_df.dropna(subset=["Gender_hint"]).drop_duplicates(
            subset=["Champion", "Gender_hint"]).set_index("Champion")["Gender_hint"].to_dict()
    )
    long_df["Gender"] = long_df["Champion"].map(gender_map)
    long_df["Gender"] = long_df["Gender"].map({"Men": "Man", "Women": "Woman"})

    long_df["count"] = 1
    pivot = long_df.pivot_table(
        index=["Champion", "Gender"],
        columns="Tournament",
        values="count",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()

    for col in ["Women's Singles", "Men's Singles", "Women's Doubles", "Mixed Doubles", "Men's Doubles"]:
        if col not in pivot.columns:
            pivot[col] = 0

    singles_total = pivot["Women's Singles"] + pivot["Men's Singles"]
    doubles_total = pivot["Women's Doubles"] + \
        pivot["Men's Doubles"] + pivot["Mixed Doubles"]
    pivot = pivot[(singles_total > 0) & (doubles_total > 0)].copy()

    pivot["Total Championships"] = (
        pivot["Women's Singles"] + pivot["Men's Singles"] +
        pivot["Women's Doubles"] +
        pivot["Mixed Doubles"] + pivot["Men's Doubles"]
    )

    most_recent = long_df.groupby("Champion")["Year"].max().rename(
        "Most Recent Win").reset_index()
    out = pivot.merge(most_recent, on="Champion", how="left")

    out = out.sort_values(["Total Championships", "Most Recent Win"], ascending=[
                          False, False]).reset_index(drop=True)
    out["Rank"] = out["Total Championships"].rank(
        method='min', ascending=False).astype(int)

    out = out[[
        "Rank",
        "Champion",
        "Gender",
        "Total Championships",
        "Women's Singles",
        "Men's Singles",
        "Women's Doubles",
        "Mixed Doubles",
        "Men's Doubles",
        "Most Recent Win",
    ]]

    num_cols = [c for c in out.columns if c not in ["Champion", "Gender"]]
    for c in num_cols:
        out[c] = out[c].astype(int)

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
