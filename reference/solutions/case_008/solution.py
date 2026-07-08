from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    def ddmmyyyy(dt: pd.Series) -> pd.Series:
        return dt.dt.strftime("%d/%m/%Y")

    f1 = inputs_dir / "input_01.csv"
    f2 = inputs_dir / "input_02.csv"

    df = pd.read_csv(f1)

    def clean_type(x: str) -> str:
        return "Bar" if "bar" in x.lower() else "Liquid"

    df["Type"] = df["Type"].apply(clean_type)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    with open(f2, "r", encoding="utf-8") as fh:
        lines = [ln.strip() for ln in fh if ln.strip()]
    mapping: dict[str, str] = {}
    for ln in lines[1:]:
        if " - " in ln:
            sid, name = ln.split(" - ", 1)
            mapping[sid.strip()] = name.strip()

    df["Branch Name"] = df["Store ID"].map(mapping)

    theft = df[df["Action"] == "Theft"].copy()
    adj = df[df["Action"] == "Stock Adjusted"].copy()

    theft_grp = (
        theft.groupby("Crime Ref Number").agg(
            {
                "Quantity": "sum",
                "Date": "min",
                "Type": "first",
                "Branch Name": "first",
            }
        )
        .rename(columns={"Quantity": "Stolen volume", "Date": "Theft"})
    )

    adj_grp = (
        adj.groupby("Crime Ref Number").agg(
            {
                "Quantity": "sum",
                "Date": "min",
                "Type": "first",
                "Branch Name": "first",
            }
        )
        .rename(columns={"Quantity": "AdjQty", "Date": "Stock Adjusted"})
    )

    num_records = theft.groupby("Crime Ref Number").size().rename(
        "Number of Records").to_frame()

    out = theft_grp.join(adj_grp[["AdjQty", "Stock Adjusted"]], how="left")
    out = out.join(num_records, how="left")

    out["Stock Variance"] = out["Stolen volume"] - \
        out["AdjQty"].abs().fillna(0)
    out["Days to complete adjustment"] = (
        out["Stock Adjusted"] - out["Theft"]).dt.days

    out = out.reset_index()

    out = out.sort_values(
        by=["Stock Adjusted", "Theft", "Crime Ref Number"], na_position="first")

    out["Theft"] = ddmmyyyy(out["Theft"])
    out["Stock Adjusted"] = ddmmyyyy(out["Stock Adjusted"])

    out = out[
        [
            "Branch Name",
            "Crime Ref Number",
            "Days to complete adjustment",
            "Number of Records",
            "Stock Adjusted",
            "Stock Variance",
            "Stolen volume",
            "Theft",
            "Type",
        ]
    ]

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
