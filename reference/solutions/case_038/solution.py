from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    fp = inputs_dir / "input_01.csv"
    df = pd.read_csv(fp, dtype={
        "VisitID": int,
        "PatientID": int,
        "Visit Type": str,
        "Doctor": str,
        "Date of Servce": str,
    })

    visit_dt = pd.to_datetime(df["Date of Servce"], errors="coerce", dayfirst=False)

    df_sorted = df.copy()
    df_sorted["_visit_dt"] = visit_dt
    df_sorted = df_sorted.sort_values(["PatientID", "_visit_dt", "VisitID"], ascending=[True, True, True])

    total_visits = df_sorted.groupby("PatientID").size().rename("Total Patient visits")

    first_visit_dt = df_sorted.groupby("PatientID")["_visit_dt"].min().rename("_first_dt")

    df_sorted["Patient visit number"] = (
        df_sorted.groupby("PatientID").cumcount() + 1
    )

    df_out = df_sorted.merge(total_visits, left_on="PatientID", right_index=True, how="left")
    df_out = df_out.merge(first_visit_dt, left_on="PatientID", right_index=True, how="left")

    df_out["New Patient Flag"] = np.where(
        df_out["Patient visit number"] == 1, "New patient", "Returning patient"
    )

    df_out["Date of Servce"] = df_out["_visit_dt"].dt.strftime("%d/%m/%Y")
    df_out["First visit date"] = df_out["_first_dt"].dt.strftime("%d/%m/%Y")

    cols = [
        "Date of Servce",
        "VisitID",
        "PatientID",
        "Visit Type",
        "Doctor",
        "Patient visit number",
        "First visit date",
        "Total Patient visits",
        "New Patient Flag",
    ]
    out = df_out[cols].copy()

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)
    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")

