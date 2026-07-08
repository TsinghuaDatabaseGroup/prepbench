from __future__ import annotations
from pathlib import Path
import pandas as pd
import math


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    frames = []
    for p in sorted(inputs_dir.glob("*.csv")):
        df = pd.read_csv(p)
        cols = {c.strip() for c in df.columns}
        if {"Email", "Order Total", "Order Date"}.issubset(cols):
            frames.append(
                df[["Email", "Order Total", "Order Date"]].copy())

    sales = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["Email", "Order Total", "Order Date"])

    sales["Order Date"] = pd.to_datetime(
        sales["Order Date"], format="%d-%b-%Y", errors="coerce")
    end_date = pd.Timestamp(2019, 5, 24)
    start_date = pd.Timestamp(2018, 11, 24)
    sales = sales[(sales["Order Date"] >= start_date) &
                  (sales["Order Date"] <= end_date)].copy()
    sales["Order Total"] = pd.to_numeric(sales["Order Total"], errors="coerce")

    agg = sales.groupby("Email", as_index=False)["Order Total"].sum()

    total_customers = len(agg)
    top_n = max(1, math.floor(total_customers * 0.08)
                ) if total_customers > 0 else 0

    agg = agg.sort_values(["Order Total", "Email"], ascending=[
                          False, True]).reset_index(drop=True)
    agg["Last 6 Months Rank"] = agg["Order Total"].rank(
        method="min", ascending=False).astype(int)
    top = agg[agg["Last 6 Months Rank"] <=
              top_n].copy() if top_n > 0 else agg.copy()

    out = top[["Last 6 Months Rank", "Email", "Order Total"]].copy()
    out["Order Total"] = out["Order Total"].round(1)
    out = out.sort_values(["Last 6 Months Rank", "Email", "Order Total"], ascending=[
                          True, True, True]).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        out_path = cand_dir / fname
        df.to_csv(out_path, index=False, encoding="utf-8")
