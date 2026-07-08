
import pandas as pd
from pathlib import Path


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:

    src = inputs_dir / "input_01.csv"
    df = pd.read_csv(src)

    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

    def to_km(row):
        if str(row["Measure"]).strip().lower() == "min":
            return float(row["Value"]) * 0.5
        else:
            detail = row.get("Detail")
            if pd.isna(detail) or str(detail).strip() == "":
                return 0.0
            return float(row["Value"]) if pd.notna(row["Value"]) else 0.0

    df["km"] = df.apply(to_km, axis=1)

    df["category"] = df["Measure"].astype(str).str.strip().str.lower().map({
        "min": "Turbo Trainer",
        "km": "Outdoors"
    })

    def is_activity(row):
        m = str(row["Measure"]).strip().lower()
        if m == "min":
            return 1
        detail = row.get("Detail")
        return 1 if (pd.notna(detail) and str(detail).strip() != "") else 0

    df["activity"] = df.apply(is_activity, axis=1)

    agg = df.groupby(["Date", "category"], as_index=False).agg({
        "km": "sum",
        "activity": "sum"
    })

    pivot = agg.pivot_table(index="Date", columns="category",
                            values="km", aggfunc="sum", fill_value=0.0)
    pivot = pivot.rename_axis(None, axis=1)

    act = agg.groupby("Date", as_index=True)["activity"].sum()

    res = pivot.join(act, how="outer").fillna(0)

    full_range = pd.date_range(start="2021-01-01", end="2021-11-01", freq="D")
    res = res.reindex(full_range).fillna(0)
    res.index.name = "Date"

    if "Turbo Trainer" not in res.columns:
        res["Turbo Trainer"] = 0.0
    if "Outdoors" not in res.columns:
        res["Outdoors"] = 0.0

    out = res.reset_index()
    out = out.rename(columns={"activity": "Activities per day"})
    out = out[["Turbo Trainer", "Outdoors", "Date", "Activities per day"]]

    out["Turbo Trainer"] = out["Turbo Trainer"].astype(float)
    out["Outdoors"] = out["Outdoors"].astype(float)
    out["Activities per day"] = out["Activities per day"].astype(int)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"

    if not cand_dir.exists():
        cand_dir.mkdir()

    outputs = solve(inputs_dir)

    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, date_format="%d/%m/%Y")
