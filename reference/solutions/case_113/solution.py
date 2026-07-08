from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    p1 = inputs_dir / "input_01.csv"
    p2 = inputs_dir / "input_02.csv"
    p3 = inputs_dir / "input_03.csv"
    p4 = inputs_dir / "input_04.csv"

    df_pass = pd.read_csv(p1)
    df_pass = df_pass[["first_name", "last_name",
                       "passenger_number", "flight_number", "purchase_amount"]]
    df_pass["passenger_number"] = pd.to_numeric(
        df_pass["passenger_number"], errors="coerce").astype("Int64")
    df_pass["flight_number"] = pd.to_numeric(
        df_pass["flight_number"], errors="coerce").astype("Int64")
    df_pass["purchase_amount"] = pd.to_numeric(
        df_pass["purchase_amount"], errors="coerce").fillna(0.0)
    df_pass = df_pass.dropna(
        subset=["passenger_number", "flight_number"]).copy()
    df_pass["passenger_number"] = df_pass["passenger_number"].astype(int)
    df_pass["flight_number"] = df_pass["flight_number"].astype(int)

    df_seat = pd.read_csv(p2)
    seat_long = df_seat.melt(
        id_vars=["Row"], var_name="SeatLetter", value_name="passenger_number")
    seat_long["passenger_number"] = pd.to_numeric(
        seat_long["passenger_number"], errors="coerce").astype("Int64")
    seat_long = seat_long.dropna(subset=["passenger_number"]).copy()
    seat_long["passenger_number"] = seat_long["passenger_number"].astype(int)

    def seat_position(letter: str) -> str:
        if letter in ("A", "F"):
            return "Window"
        if letter in ("B", "E"):
            return "Middle"
        return "Aisle"

    seat_long["Seat Position"] = seat_long["SeatLetter"].map(seat_position)

    df_ps = df_pass.merge(seat_long, on="passenger_number", how="left")

    lines = p3.read_text(encoding="utf-8").strip().splitlines()
    rows = []
    cols = None
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("[") and s.endswith("]"):
            inner = s[1:-1]
            parts = inner.split("|")
            if cols is None:
                cols = parts
            else:
                rows.append(parts)
    df_f = pd.DataFrame(rows, columns=cols)
    df_f["FlightID"] = pd.to_numeric(
        df_f["FlightID"], errors="coerce").astype(int)
    dep_dt = pd.to_datetime(
        df_f["DepDate"] + " " + df_f["DepTime"], errors="coerce")
    hours = dep_dt.dt.hour.fillna(0).astype(int)

    def time_of_day(h: int) -> str:
        if h < 12:
            return "Morning"
        if 12 <= h <= 18:
            return "Afternoon"
        return "Evening"

    df_f["Depart Time of Day"] = hours.map(time_of_day)

    df_plane = pd.read_csv(p4)
    df_plane = df_plane.rename(columns={"FlightNo.": "FlightID"})
    df_plane["FlightID"] = pd.to_numeric(
        df_plane["FlightID"], errors="coerce").astype(int)

    def parse_range(r: str) -> tuple[int, int]:
        if pd.isna(r):
            return (0, -1)
        r = str(r)
        if "-" in r:
            a, b = r.split("-", 1)
            try:
                return (int(a), int(b))
            except Exception:
                return (0, -1)
        try:
            v = int(r)
            return (v, v)
        except Exception:
            return (0, -1)

    bc_bounds = df_plane["Business Class"].map(parse_range)
    df_plane["bc_start"] = bc_bounds.map(lambda t: t[0])
    df_plane["bc_end"] = bc_bounds.map(lambda t: t[1])

    df_ps = df_ps.merge(df_f[["FlightID", "Depart Time of Day"]],
                        left_on="flight_number", right_on="FlightID", how="left")
    df_ps = df_ps.merge(
        df_plane[["FlightID", "bc_start", "bc_end"]], on="FlightID", how="left")

    df_ps["Row"] = pd.to_numeric(df_ps["Row"], errors="coerce")
    is_bc = (df_ps["Row"].notna()) & (df_ps["bc_start"].notna()) & (
        df_ps["Row"] >= df_ps["bc_start"]) & (df_ps["Row"] <= df_ps["bc_end"])
    df_ps["Business Class"] = np.where(is_bc, "Business Class", "Economy")

    df_ps_econ = df_ps[df_ps["Business Class"] == "Economy"].copy()
    flight_totals = df_ps_econ.groupby("flight_number", as_index=False)[
        "purchase_amount"].sum().rename(columns={"purchase_amount": "total_purchase"})
    flight_time = df_f[["FlightID", "Depart Time of Day"]].rename(
        columns={"FlightID": "flight_number"})
    flight_totals = flight_totals.merge(
        flight_time, on="flight_number", how="left")
    avg_per_flight = flight_totals.groupby("Depart Time of Day", as_index=False)[
        "total_purchase"].mean()
    avg_per_flight = avg_per_flight.rename(
        columns={"total_purchase": "Avg per Flight"})
    avg_per_flight["Avg per Flight"] = avg_per_flight["Avg per Flight"].round(
        2)
    avg_per_flight = avg_per_flight.sort_values(["Avg per Flight", "Depart Time of Day"], ascending=[
                                                False, True], kind="mergesort").reset_index(drop=True)
    avg_per_flight.insert(0, "Rank", range(1, len(avg_per_flight) + 1))
    out1 = avg_per_flight[["Rank", "Depart Time of Day", "Avg per Flight"]]

    seat_totals = df_ps_econ.groupby("Seat Position", as_index=False)[
        "purchase_amount"].sum()
    seat_totals = seat_totals.rename(
        columns={"purchase_amount": "Purchase Amount"})
    seat_totals["Purchase Amount"] = seat_totals["Purchase Amount"].round(2)
    seat_totals = seat_totals.sort_values(["Purchase Amount", "Seat Position"], ascending=[
                                          False, True], kind="mergesort").reset_index(drop=True)
    seat_totals.insert(0, "Rank", range(1, len(seat_totals) + 1))
    out2 = seat_totals[["Rank", "Seat Position", "Purchase Amount"]]

    class_totals = df_ps.groupby("Business Class", as_index=False)[
        "purchase_amount"].sum()
    class_totals = class_totals.rename(
        columns={"purchase_amount": "Purchase Amount"})
    class_totals["Purchase Amount"] = class_totals["Purchase Amount"].round(2)
    class_totals = class_totals.sort_values(["Purchase Amount", "Business Class"], ascending=[
                                            False, True], kind="mergesort").reset_index(drop=True)
    class_totals.insert(0, "Rank", range(1, len(class_totals) + 1))
    out3 = class_totals[["Rank", "Business Class", "Purchase Amount"]]

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
        "output_03.csv": out3,
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True, parents=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
