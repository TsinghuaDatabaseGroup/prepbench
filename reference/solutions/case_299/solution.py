from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file)

    df.columns = [c.strip() for c in df.columns]

    df["Date Sold"] = pd.to_datetime(df["Date Sold"], format="%d/%m/%Y", dayfirst=True, errors="coerce")
    df["Date Returned"] = pd.to_datetime(df["Date Returned"], format="%d/%m/%Y", dayfirst=True, errors="coerce")

    df["Price "] = pd.to_numeric(df["Price "] if "Price " in df.columns else df["Price"], errors="coerce")
    if "Price" not in df.columns:
        df = df.rename(columns={"Price ": "Price"})

    mask_swap = (~df["Date Returned"].isna()) & (~df["Date Sold"].isna()) & (df["Date Sold"] > df["Date Returned"])
    sold_orig = df.loc[mask_swap, "Date Sold"].copy()
    returned_orig = df.loc[mask_swap, "Date Returned"].copy()
    df.loc[mask_swap, "Date Sold"] = returned_orig.values
    df.loc[mask_swap, "Date Returned"] = sold_orig.values

    df["Days to Return"] = (df["Date Returned"] - df["Date Sold"]).dt.days

    def refund_amount(days: float, price: float) -> float:
        if pd.isna(days):
            return np.nan
        if days <= 60:
            return float(price)
        if days <= 100:
            return float(np.round(price * 0.5, 2))
        return 0.0

    df["Refund"] = [refund_amount(d, p) for d, p in zip(df["Days to Return"], df["Price"])]

    df["Sold Month"] = df["Date Sold"].dt.to_period("M").dt.to_timestamp()
    df["Returned Month"] = df["Date Returned"].dt.to_period("M").dt.to_timestamp()

    year = 2023
    months = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-01", freq="MS")
    out = pd.DataFrame({"Date": months})

    revenue = (
        df.dropna(subset=["Sold Month"]).groupby("Sold Month", as_index=False)["Price"].sum()
        .rename(columns={"Sold Month": "Date", "Price": "Revenue"})
    )
    out = out.merge(revenue, on="Date", how="left")

    returns = df.dropna(subset=["Returned Month"]).copy()

    total_returns = (
        returns.groupby("Returned Month", as_index=False)["Refund"].sum()
        .rename(columns={"Returned Month": "Date", "Refund": "Total Returns Value"})
    )

    num_returns = (
        returns.groupby("Returned Month", as_index=False)["Unique Sales ID"].count()
        .rename(columns={"Returned Month": "Date", "Unique Sales ID": "Number of Returns"})
    )

    avg_days = (
        returns.groupby("Returned Month", as_index=False)["Days to Return"].mean()
        .rename(columns={"Returned Month": "Date", "Days to Return": "Avg Days to Return"})
    )

    out = out.merge(total_returns, on="Date", how="left")
    out = out.merge(num_returns, on="Date", how="left")
    out = out.merge(avg_days, on="Date", how="left")

    no_returns_mask = out["Number of Returns"].isna()
    for col in ["Total Returns Value", "Number of Returns", "Avg Days to Return"]:
        out.loc[no_returns_mask, col] = np.nan

    if "Revenue" in out.columns:
        out["Revenue"] = out["Revenue"].round(2)
    if "Total Returns Value" in out.columns:
        out["Total Returns Value"] = out["Total Returns Value"].round(2)
    if "Avg Days to Return" in out.columns:
        out["Avg Days to Return"] = out["Avg Days to Return"].round(2)

    out["Date"] = out["Date"].dt.strftime("%d/%m/%Y")

    out = out[
        [
            "Date",
            "Revenue",
            "Total Returns Value",
            "Number of Returns",
            "Avg Days to Return",
        ]
    ]

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
