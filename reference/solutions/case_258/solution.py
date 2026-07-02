from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    target_names = ["input_01.csv", "input_02.csv", "input_03.csv", "input_04.csv"]
    target_frames: list[pd.DataFrame] = []
    for name in target_names:
        df = pd.read_csv(inputs_dir / name)
        df["Month"] = pd.to_numeric(df["Month"], errors="coerce").astype("Int64")
        df["Class"] = df["Class"].astype(str).str.strip()
        df["Target"] = pd.to_numeric(df["Target"], errors="coerce")
        target_frames.append(df[["Month", "Class", "Target"]])
    targets_all = pd.concat(target_frames, ignore_index=True)

    sales_names = ["input_05.csv", "input_06.csv"]

    def normalize_sales_class_to_code(s: pd.Series) -> pd.Series:
        s = s.replace({
            "Economy": "First Class",
            "First Class": "Economy",
        })
        mapping = {
            "First Class": "FC",
            "Business Class": "BC",
            "Premium Economy": "PE",
            "Economy": "E",
        }
        return s.map(mapping)

    sales_frames: list[pd.DataFrame] = []
    for name in sales_names:
        df = pd.read_csv(inputs_dir / name)
        dt = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
        df["Month"] = dt.dt.month
        df["Class"] = normalize_sales_class_to_code(df["Class"])
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        sales_frames.append(df[["Month", "Class", "Price"]])
    sales_all = pd.concat(sales_frames, ignore_index=True)

    sales_agg = (
        sales_all.dropna(subset=["Month", "Class"]).groupby(["Month", "Class"], as_index=False)["Price"].sum()
    )

    merged = pd.merge(
        sales_agg,
        targets_all,
        how="inner",
        on=["Month", "Class"],
        validate="one_to_one",
    )

    merged["Difference to Target"] = merged["Price"] - merged["Target"]

    class_order = ["FC", "BC", "PE", "E"]
    merged["Class"] = pd.Categorical(merged["Class"], categories=class_order, ordered=True)
    merged = merged.sort_values(["Month", "Class"]).reset_index(drop=True)

    merged["Date"] = merged["Month"].astype(int)

    out = merged[[
        "Difference to Target",
        "Date",
        "Price",
        "Class",
        "Target",
    ]].copy()

    for col in ["Price", "Target", "Difference to Target"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    out["Date"] = pd.to_numeric(out["Date"], errors="coerce").astype(int)

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
