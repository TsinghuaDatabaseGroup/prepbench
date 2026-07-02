from __future__ import annotations
from pathlib import Path
import pandas as pd


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    booking_files = [
        inputs_dir / "input_01.csv",
        inputs_dir / "input_02.csv",
        inputs_dir / "input_03.csv",
    ]
    bookings_list = []
    for fp in booking_files:
        if fp.exists():
            df = pd.read_csv(fp)
            df = df[["Class", "Seat", "Row"]].copy()
            df["Seat"] = pd.to_numeric(df["Seat"], errors="coerce").astype("Int64")
            df["Row"] = pd.to_numeric(df["Row"], errors="coerce").astype("Int64")
            df["Class"] = df["Class"].astype(str)
            bookings_list.append(df)
    bookings = pd.concat(bookings_list, ignore_index=True) if bookings_list else pd.DataFrame(columns=["Class","Seat","Row"]) 

    plan_fp = inputs_dir / "input_04.csv"
    plan = pd.read_csv(plan_fp)
    plan = plan[["Class", "Seat", "Row"]].copy()
    plan["Seat"] = pd.to_numeric(plan["Seat"], errors="coerce").astype("Int64")
    plan["Row"] = pd.to_numeric(plan["Row"], errors="coerce").astype("Int64")
    plan["Class"] = plan["Class"].astype(str)

    booked_keys = bookings.drop_duplicates(subset=["Class", "Seat", "Row"]) if not bookings.empty else bookings

    merged = plan.merge(booked_keys, on=["Class", "Seat", "Row"], how="left", indicator=True)
    unbooked = merged[merged["_merge"] == "left_only"][ ["Class", "Seat", "Row"] ].copy()

    unbooked_sorted = unbooked.sort_values(by=["Class", "Seat", "Row"], kind="mergesort").reset_index(drop=True)

    return {
        "output_01.csv": unbooked_sorted.astype({"Class": "string", "Seat": "Int64", "Row": "Int64"})
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

