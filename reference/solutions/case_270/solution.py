from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def solve() -> Dict[str, pd.DataFrame]:
    task_dir = Path(__file__).parent

    RECALL_DATE = pd.Timestamp("2025-05-13")
    DEADLINE_DATE = pd.Timestamp("2025-05-20")

    def _read_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
        inputs_dir = task_dir / "inputs"
        df_local = pd.read_csv(inputs_dir / "input_01.csv")
        recalled_local = pd.read_csv(inputs_dir / "input_02.csv")
        if "Date" in df_local.columns:
            df_local["Date"] = pd.to_datetime(df_local["Date"], errors="coerce")
        return df_local, recalled_local[["Category", "Product ID"]]


    def _compute_avg_removal(df_recalled: pd.DataFrame) -> pd.DataFrame:
        df_done = df_recalled.dropna(subset=["Date"]).copy()
        df_done["days_to_removal"] = (df_done["Date"] - RECALL_DATE).dt.total_seconds() / 86400.0

        grp = df_done.groupby("Store", as_index=False)["days_to_removal"].mean()

        days = grp["days_to_removal"].floordiv(1).astype(int)
        hours = ((grp["days_to_removal"] - days) * 24).round().astype(int)

        hours_overflow = hours == 24
        if hours_overflow.any():
            days.loc[hours_overflow] = days.loc[hours_overflow] + 1
            hours.loc[hours_overflow] = 0

        out = pd.DataFrame(
            {
                "Store": grp["Store"],
                "Days to Removal": days,
                "Hours to Removal": hours,
            }
        )

        out = out.merge(grp[["Store", "days_to_removal"]], on="Store", how="left")
        out = out.sort_values(["days_to_removal", "Store"], ascending=[True, True], kind="mergesort").reset_index(drop=True)
        out.insert(0, "Rank", out.index + 1)
        out = out.drop(columns=["days_to_removal"])
        return out


    def _compute_overdue_summary(df_recalled: pd.DataFrame) -> pd.DataFrame:
        df2 = df_recalled.copy()

        store_max_date = (
            df2.groupby("Store")["Date"].max().rename("store_max_date")
        )
        df2 = df2.merge(store_max_date, on="Store", how="left")

        def status_for(row) -> str:
            if pd.isna(row["Date"]):
                return "Incomplete"
            if row["Date"] <= DEADLINE_DATE:
                return "On Target"
            return "Overdue"

        df2["Status"] = df2.apply(status_for, axis=1)

        overdue_mask = df2["Status"].isin(["Overdue", "Incomplete"])
        df_over = df2.loc[overdue_mask].copy()

        overdue_days_overdue = (df_over.loc[df_over["Status"] == "Overdue", "Date"] - DEADLINE_DATE).dt.total_seconds() / 86400.0
        snap = df_over.loc[df_over["Status"] == "Incomplete", "store_max_date"].copy()
        snap = snap.fillna(DEADLINE_DATE)
        snap = snap.mask(snap < DEADLINE_DATE, DEADLINE_DATE)
        overdue_days_incomplete = (snap - DEADLINE_DATE).dt.total_seconds() / 86400.0

        df_over.loc[df_over["Status"] == "Overdue", "days_overdue"] = overdue_days_overdue
        df_over.loc[df_over["Status"] == "Incomplete", "days_overdue"] = overdue_days_incomplete

        def round_half_up(x: float) -> int:
            import math
            return int(math.floor(x + 0.5))

        if "Quantity" in df_over.columns:
            df_over["Quantity"] = pd.to_numeric(df_over["Quantity"], errors="coerce").fillna(0)

        agg = (
            df_over.groupby("Store")
            .agg(
                **{
                    "Avg Days Overdue": ("days_overdue", lambda s: round_half_up(float(pd.Series(s).mean())) if len(s) else 0),
                    "Quantity": ("Quantity", "sum"),
                }
            )
            .reset_index()
        )

        agg["Avg Days Overdue"] = agg["Avg Days Overdue"].astype(int)
        agg["Quantity"] = agg["Quantity"].astype(int)
        return agg

    df, recalled = _read_inputs()
    df_recalled = df.merge(recalled, on=["Category", "Product ID"], how="inner")
    out1 = _compute_avg_removal(df_recalled)
    out2 = _compute_overdue_summary(df_recalled)
    return {"output_01.csv": out1, "output_02.csv": out2}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve()
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


