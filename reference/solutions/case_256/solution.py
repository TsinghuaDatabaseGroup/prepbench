from __future__ import annotations
import pandas as pd
from pathlib import Path
from decimal import Decimal, InvalidOperation


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_csv = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_csv, dtype=str)

    parts = df["Flight Details"].str.split("//", n=4, expand=True)
    parts.columns = ["Date", "Flight Number", "Route", "Class", "Price"]
    route = parts["Route"].str.split("-", n=1, expand=True)
    parts["From"] = route[0].str.strip()
    parts["To"] = route[1].str.strip()

    def normalize_price(x: str):
        try:
            d = Decimal(x)
        except (InvalidOperation, TypeError):
            return pd.NA
        if d == d.to_integral():
            return int(d)
        return float(d.quantize(Decimal("0.1")))

    date_series = pd.to_datetime(
        parts["Date"], format="%Y-%m-%d", errors="coerce").dt.strftime("%d/%m/%Y")

    out = pd.DataFrame({
        "Date": date_series,
        "Flight Number": parts["Flight Number"],
        "From": parts["From"],
        "To": parts["To"],
        "Class": parts["Class"],
        "Price": parts["Price"].apply(normalize_price),
        "Flow Card?": df["Flow Card?"].str.strip().map(lambda v: "Yes" if v == "1" else "No"),
        "Bags Checked": df["Bags Checked"].astype(int),
        "Meal Type": df["Meal Type"],
    })

    yes_df = out[out["Flow Card?"] == "Yes"].reset_index(drop=True)
    no_df = out[out["Flow Card?"] == "No"].reset_index(drop=True)

    return {
        "output_01.csv": yes_df,
        "output_02.csv": no_df,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    results = solve(inputs_dir)
    for fname, df in results.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
