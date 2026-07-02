import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    TODAY = pd.Timestamp(2024, 1, 31)

    flights = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    customers = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)
    bookings = pd.read_csv(inputs_dir / "input_03.csv", dtype=str)

    flights["Date"] = pd.to_datetime(flights["Date"], format="%Y-%m-%d", errors="coerce")
    bookings["Date"] = pd.to_datetime(bookings["Date"], format="%Y-%m-%d", errors="coerce")

    f2024 = flights[flights["Date"].dt.year == 2024].copy()
    b2024 = bookings[bookings["Date"].dt.year == 2024].copy()

    out1 = (
        b2024.merge(customers, on="Customer ID", how="inner", validate="many_to_one")
             .merge(f2024, on=["Date", "Flight Number"], how="inner", validate="many_to_one")
             [[
                 "Date", "From", "To", "Flight Number", "Customer ID", "Last Date Flown",
                 "first_name", "last_name", "email", "gender", "Ticket Price"
             ]]
    )
    out1 = out1.sort_values(["Date", "Flight Number", "Customer ID"])\
               .reset_index(drop=True)

    booked_keys = b2024.drop_duplicates(["Date", "Flight Number"])[["Date", "Flight Number"]]
    out2 = (
        f2024.merge(booked_keys, on=["Date", "Flight Number"], how="left", indicator=True)
             .query("_merge == 'left_only'")
             .drop(columns="_merge")
             .assign(**{"Flights unbooked as of": TODAY.strftime("%Y-%m-%d")})
             [["Flights unbooked as of", "Date", "Flight Number", "From", "To"]]
             .sort_values(["Date", "Flight Number", "From", "To"])\
             .reset_index(drop=True)
    )

    customers_latest = customers.copy()
    customers_latest["Last Date Flown"] = pd.to_datetime(
        customers_latest["Last Date Flown"], format="%Y-%m-%d", errors="coerce"
    )
    not_booked = customers_latest[~customers_latest["Customer ID"].isin(b2024["Customer ID"])].copy()
    not_booked["Days Since Last Flown"] = (TODAY - customers_latest.loc[not_booked.index, "Last Date Flown"]).dt.days

    not_booked["Days Since Last Flown"] = not_booked["Days Since Last Flown"].fillna(-1).astype(int)

    def _bucket(days: int) -> str:
        if days is None or days < 0:
            return "Recent Fliers (less than 3 months since last flight)"
        if days > 270:
            return "Lapsed (over 9 months since last flight)"
        if days > 180:
            return "Been away a while (6-9 months since last flight)"
        if days > 90:
            return "Taking a break (3-6 months since last flight)"
        return "Recent Fliers (less than 3 months since last flight)"

    not_booked["Customer Category"] = not_booked["Days Since Last Flown"].map(_bucket)

    out3 = not_booked[[
        "Customer ID", "Customer Category", "Days Since Last Flown", "Last Date Flown",
        "first_name", "last_name", "email", "gender"
    ]].copy()

    out1["Date"] = pd.to_datetime(out1["Date"]).dt.strftime("%Y-%m-%d")
    out3["Last Date Flown"] = pd.to_datetime(out3["Last Date Flown"]).dt.strftime("%Y-%m-%d")

    for df, cols in [(out1, ["Customer ID", "Ticket Price"]), (out3, ["Customer ID"])]:
        for col in cols:
            if col in df.columns:
                if col == "Ticket Price":
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                else:
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype('Int64')
                    df[col] = df[col].astype('Int64')

    out1 = out1.sort_values(["Date", "Customer ID", "Flight Number", "Ticket Price"]).reset_index(drop=True)
    out2 = out2.sort_values(["Date", "Flight Number", "From", "To"]).reset_index(drop=True)
    out3 = out3.sort_values(["Customer ID", "Last Date Flown"]).reset_index(drop=True)

    for df, col in [(out1, "Customer ID"), (out3, "Customer ID")]:
        if df[col].isna().sum() == 0:
            df[col] = df[col].astype(int)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
        "output_03.csv": out3,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("") if df is None else None
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
