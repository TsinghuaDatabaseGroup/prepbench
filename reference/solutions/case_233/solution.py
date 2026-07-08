import pandas as pd
from pathlib import Path
from typing import Dict


def _build_lookup(dim_df: pd.DataFrame, monthly_df: pd.DataFrame) -> pd.DataFrame:
    a = dim_df[["employee_id", "guid"]].copy()
    b = monthly_df[["employee_id", "guid"]].copy()
    lookup = pd.concat([a, b], ignore_index=True)
    lookup = lookup[(lookup["employee_id"].notna()) | (lookup["guid"].notna())]
    lookup = lookup[lookup["employee_id"].notna() & lookup["guid"].notna()]
    lookup = lookup.drop_duplicates(subset=["employee_id", "guid"]).reset_index(drop=True)
    return lookup


def _fill_ids(df: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.merge(lookup.rename(columns={"guid": "guid_lu"}), how="left", on="employee_id")
    out["guid"] = out["guid"].where(out["guid"].notna(), out["guid_lu"])
    out = out.drop(columns=["guid_lu"]) if "guid_lu" in out.columns else out

    out = out.merge(lookup.rename(columns={"employee_id": "employee_id_lu"}), how="left", on="guid")
    out["employee_id"] = out["employee_id"].where(out["employee_id"].notna(), out["employee_id_lu"])
    out = out.drop(columns=["employee_id_lu"]) if "employee_id_lu" in out.columns else out

    return out


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    dim_path = inputs_dir / "input_01.csv"
    monthly_path = inputs_dir / "input_02.csv"
    dim_df = pd.read_csv(dim_path, dtype=str)
    monthly_df = pd.read_csv(monthly_path, dtype=str)

    lookup = _build_lookup(dim_df, monthly_df)

    dim_filled = _fill_ids(dim_df, lookup)
    monthly_filled = _fill_ids(monthly_df, lookup)

    assert dim_filled["employee_id"].notna().all() and dim_filled["guid"].notna().all()
    assert monthly_filled["employee_id"].notna().all() and monthly_filled["guid"].notna().all()

    dim_cols = [
        "employee_id",
        "guid",
        "first_name",
        "last_name",
        "date_of_birth",
        "nationality",
        "gender",
        "email",
        "hire_date",
        "leave_date",
    ]
    monthly_cols = [
        "employee_id",
        "guid",
        "dc_nbr",
        "month_end_date",
        "hire_date",
        "leave_date",
    ]

    dim_out = dim_filled.loc[:, dim_cols].copy()
    monthly_out = monthly_filled.loc[:, monthly_cols].copy()

    return {
        "output_01.csv": dim_out,
        "output_02.csv": monthly_out,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for name, df in outputs.items():
        (cand_dir / name).write_text("", encoding="utf-8")
        df.to_csv(cand_dir / name, index=False, encoding="utf-8")
        
















