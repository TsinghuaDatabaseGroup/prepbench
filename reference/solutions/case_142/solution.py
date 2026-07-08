from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np

QUARTER_START = pd.Timestamp(2021, 10, 1)


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    lookup_path = inputs_dir / "input_03.csv"
    df_lookup = pd.read_csv(lookup_path)
    df_lookup.columns = [c.strip() for c in df_lookup.columns]
    level_to_rating = dict(zip(df_lookup["Risk level"], df_lookup["Risk rating"]))

    a_path = inputs_dir / "input_01.csv"
    df_a = pd.read_csv(a_path)
    df_a.columns = [c.strip() for c in df_a.columns]
    df_a["Date Lodged"] = pd.to_datetime(
        dict(year=df_a["Year"], month=df_a["Month"], day=df_a["Date"]), errors="coerce"
    )
    df_a["Rating"] = pd.to_numeric(df_a["Rating"], errors="coerce").map(level_to_rating)
    df_a["Business Unit"] = df_a.get("Business Unit", df_a.get("Business Unit ", "A")).astype(str).str.strip()
    df_a = df_a[["Ticket ID", "Business Unit", "Date Lodged", "Status", "Rating"]].copy()

    b_path = inputs_dir / "input_02.csv"
    with open(b_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("Ticket ID,Unit,Owner,Issue ") or line.startswith("Ticket ID,Unit,Owner,Issue"):
            header_idx = i
            break
    if header_idx is None:
        for i, line in enumerate(lines):
            if line.split(",")[0].strip() == "Ticket ID":
                header_idx = i
                break
    df_b = pd.read_csv(b_path, skiprows=header_idx)
    df_b.columns = [c.strip() for c in df_b.columns]
    df_b["Date Lodged"] = pd.to_datetime(df_b["Date lodged"], dayfirst=True, errors="coerce")
    df_b["Business Unit"] = df_b["Unit"].astype(str).str.strip()
    df_b = df_b[["Ticket ID", "Business Unit", "Date Lodged", "Status", "Rating"]].copy()

    df = pd.concat([df_a, df_b], ignore_index=True)

    opening = (
        df[df["Date Lodged"] < QUARTER_START]
        .groupby("Rating", dropna=False)
        .size()
        .rename("Cases")
        .to_frame()
    )
    new_cases = (
        df[df["Date Lodged"] >= QUARTER_START]
        .groupby("Rating", dropna=False)
        .size()
        .rename("Cases")
        .to_frame()
    )
    completed = (
        df[df["Status"].str.strip().eq("Completed")]
        .groupby("Rating", dropna=False)
        .size()
        .rename("Cases")
        .to_frame()
    )
    deferred = (
        df[df["Status"].str.strip().eq("Deferred")]
        .groupby("Rating", dropna=False)
        .size()
        .rename("Cases")
        .to_frame()
    )

    ratings = sorted(set(opening.index).union(new_cases.index).union(completed.index).union(deferred.index))

    def ensure_all(idx_values, name):
        s = pd.Series(0, index=ratings, name="Cases", dtype=int)
        if isinstance(idx_values, pd.DataFrame):
            base = idx_values["Cases"].reindex(ratings).fillna(0).astype(int)
        else:
            base = idx_values.reindex(ratings).fillna(0).astype(int)
        s.update(base)
        return s

    opening_s = ensure_all(opening, "Opening cases")
    new_s = ensure_all(new_cases, "New cases")
    completed_s = ensure_all(completed, "Completed")
    deferred_s = ensure_all(deferred, "Deferred")

    continuing_s = opening_s.add(new_s, fill_value=0).sub(completed_s, fill_value=0).sub(deferred_s, fill_value=0).astype(int)

    status_order = ["Completed", "Deferred", "New cases", "Opening cases", "Continuing"]
    rating_order = ["Medium", "Low", "High"]
    for r in ratings:
        if r not in rating_order:
            rating_order.append(r)
    rows = []
    for rating in rating_order:
        val_map = {
            "Completed": int(completed_s.get(rating, 0)),
            "Deferred": int(deferred_s.get(rating, 0)),
            "New cases": int(new_s.get(rating, 0)),
            "Opening cases": int(opening_s.get(rating, 0)),
            "Continuing": int(continuing_s.get(rating, 0)),
        }
        for status in status_order:
            rows.append({"Status": status, "Cases": val_map[status], "Rating": rating})
    out_df = pd.DataFrame(rows, columns=["Status", "Cases", "Rating"])

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).write_text("")
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

