from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    inp = inputs_dir / "input_01.csv"
    df = pd.read_csv(inp)

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

    def compute_dest_rolling(g: pd.DataFrame) -> pd.DataFrame:
        g = g.sort_values("Date").copy()
        roll_sum = (
            g["Revenue"].rolling(window=7, center=True, min_periods=1).sum()
        )
        roll_avg = (
            g["Revenue"].rolling(window=7, center=True, min_periods=1).mean()
        )
        out = pd.DataFrame({
            "Destination": g["Destination"].values,
            "Date": g["Date"].values,
            "Rolling Week Avg": roll_avg.values,
            "Rolling Week Total": roll_sum.values,
        })
        return out

    dest_out = df.groupby("Destination", group_keys=False).apply(
        compute_dest_rolling)

    daily = (
        df.groupby("Date", as_index=False)
        .agg(**{"Daily Total": ("Revenue", "sum"), "Daily Count": ("Revenue", "size")})
        .sort_values("Date")
    )
    daily["Rolling Total Sum"] = daily["Daily Total"].rolling(
        window=7, center=True, min_periods=1).sum()
    daily["Rolling Count Sum"] = daily["Daily Count"].rolling(
        window=7, center=True, min_periods=1).sum()
    daily["Rolling Week Avg"] = daily["Rolling Total Sum"] / \
        daily["Rolling Count Sum"]
    daily["Rolling Week Total"] = daily["Rolling Total Sum"]

    all_out = daily[["Date", "Rolling Week Avg", "Rolling Week Total"]].copy()
    all_out.insert(0, "Destination", "All")

    out = pd.concat([dest_out, all_out], ignore_index=True)

    out["Rolling Week Avg"] = out["Rolling Week Avg"].round(9)
    out["Rolling Week Total"] = out["Rolling Week Total"].round(0).astype(int)

    out["Date"] = out["Date"].dt.strftime("%d/%m/%Y")

    out = out[["Destination", "Date", "Rolling Week Avg", "Rolling Week Total"]]

    return {"output_01.csv": out}


if __name__ == "__main__":
    import sys

    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
