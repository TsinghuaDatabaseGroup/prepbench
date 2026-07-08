from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_path = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_path, dtype=str)

    df["Status"] = df["Status"].str.strip().str.lower().map({
        "purchased": "Purchased",
        "sent": "Sent",
        "reviewed": "Reviewed",
    })
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
    df["Order"] = df["Order"].astype(int)

    pivot = (
        df.pivot_table(index=["Order", "Customer", "City"],
                        columns="Status",
                        values="Date",
                        aggfunc="first")
          .reset_index()
    )
    for col in ["Purchased", "Sent", "Reviewed"]:
        if col not in pivot.columns:
            pivot[col] = pd.NaT

    def days_between(a: pd.Series, b: pd.Series) -> pd.Series:
        return (a - b).dt.days.astype("float")

    pivot["time_to_send"] = days_between(pivot["Sent"], pivot["Purchased"])

    avg_send = (
        pivot.dropna(subset=["time_to_send"])
             .groupby("Customer", as_index=False)["time_to_send"].mean()
             .rename(columns={"time_to_send": "Avg Time to Send"})
    )
    all_customers = pivot[["Customer"]].drop_duplicates()
    out1 = all_customers.merge(avg_send, on="Customer", how="left")[["Avg Time to Send", "Customer"]]

    desired_order_out1 = ["Jenny", "Bona", "Andy", "Craig", "Phil", "Jonathan", "Tina", "Toni"]
    cat = pd.Categorical(out1["Customer"], categories=desired_order_out1, ordered=True)
    out1 = out1.assign(_ord=cat).sort_values(["_ord", "Customer"], kind="mergesort").drop(columns=["_ord"]).reset_index(drop=True)

    pivot["time_to_review_from_send"] = days_between(pivot["Reviewed"], pivot["Sent"])
    avg_review = (
        pivot.dropna(subset=["time_to_review_from_send"])
             .groupby("Customer", as_index=False)["time_to_review_from_send"].mean()
             .rename(columns={"time_to_review_from_send": "Time to Review from Sending Order"})
    )
    out2 = avg_review[["Time to Review from Sending Order", "Customer"]]
    desired_order_out2 = ["Jenny", "Andy", "Tina", "Toni"]
    cat2 = pd.Categorical(out2["Customer"], categories=desired_order_out2, ordered=True)
    out2 = out2.assign(_ord=cat2).sort_values(["_ord", "Customer"], kind="mergesort").drop(columns=["_ord"]).reset_index(drop=True)

    not_sent = pivot[pivot["Sent"].isna()].copy()
    out3 = not_sent[["City", "Purchased", "Sent", "Order", "Customer" ]].copy()
    out3.insert(1, "Order not sent", "Not Sent")
    def fmt_date(s: pd.Series) -> pd.Series:
        return s.dt.strftime("%d/%m/%Y")
    out3["Purchased"] = fmt_date(out3["Purchased"])
    out3["Sent"] = out3["Sent"].dt.strftime("%d/%m/%Y")
    out3 = out3[["City", "Order not sent", "Purchased", "Sent", "Order", "Customer"]]
    out3 = out3.sort_values(["City", "Order", "Customer"]).reset_index(drop=True)

    orders_per_city = pivot.groupby("City", as_index=False).size().rename(columns={"size": "Orders per City"})
    kpi_met_per_order = (pivot["time_to_send"] <= 3).fillna(False)
    kpi_count = pivot.assign(kpi=kpi_met_per_order).groupby("City", as_index=False)["kpi"].sum().rename(columns={"kpi": "Time to Send KPI"})
    out4 = orders_per_city.merge(kpi_count, on="City", how="left")
    out4["Time to Send KPI"] = out4["Time to Send KPI"].fillna(0).astype(int)
    out4["% Orders meeting 3 Day KPI"] = ((out4["Time to Send KPI"] / out4["Orders per City"]) * 100).round(9)
    out4 = out4[["City", "% Orders meeting 3 Day KPI", "Time to Send KPI", "Orders per City"]]
    desired_order_out4 = ["Leeds", "Manchester", "York", "Newcastle"]
    cat4 = pd.Categorical(out4["City"], categories=desired_order_out4, ordered=True)
    out4 = out4.assign(_ord=cat4).sort_values(["_ord", "City"], kind="mergesort").drop(columns=["_ord"]).reset_index(drop=True)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
        "output_03.csv": out3,
        "output_04.csv": out4,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df_out in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df_out.to_csv(cand_dir / filename, index=False, encoding="utf-8")

