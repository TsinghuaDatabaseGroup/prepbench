from pathlib import Path
from typing import Dict
import pandas as pd


def _parse_date_series(date_s: pd.Series) -> pd.Series:
    return pd.to_datetime(date_s.replace({"": pd.NA}), format="%d/%m/%Y", errors="coerce", dayfirst=True)


def _format_date_series(dt_s: pd.Series) -> pd.Series:
    out = dt_s.dt.strftime("%d/%m/%Y")
    return out.fillna("")


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    dim_path = inputs_dir / "input_01.csv"
    monthly_path = inputs_dir / "input_02.csv"
    ee_dim = pd.read_csv(dim_path, dtype=str)
    monthly = pd.read_csv(monthly_path, dtype=str)


    monthly_dt = monthly.copy()
    monthly_dt["month_end_date_dt"] = _parse_date_series(monthly_dt["month_end_date"])
    monthly_dt["hire_date_dt"] = _parse_date_series(monthly_dt["hire_date"])
    monthly_dt["leave_date_dt"] = _parse_date_series(monthly_dt["leave_date"])
    monthly_dt["tenure_end_dt"] = monthly_dt[["month_end_date_dt", "leave_date_dt"]].min(axis=1)
    start = monthly_dt["hire_date_dt"]
    end = monthly_dt["tenure_end_dt"]
    months_diff = (end.dt.year - start.dt.year) * 12 + (end.dt.month - start.dt.month)
    is_month_end = end.dt.is_month_end
    needs_subtract = (end.dt.day < start.dt.day) & (~is_month_end)
    months_full = (months_diff - needs_subtract.astype("Int64")).fillna(0).astype(int)
    months_full = months_full.clip(lower=0)
    monthly_dt["tenure_months"] = months_full
    monthly_dt["tenure_years"] = (monthly_dt["tenure_months"] // 12).astype(int)

    out1_cols = [
        "dc_nbr",
        "month_end_date",
        "employee_id",
        "guid",
        "hire_date",
        "leave_date",
        "tenure_months",
        "tenure_years",
        "age_range",
    ]
    out1 = monthly_dt.copy()
    out1["month_end_date"] = _format_date_series(out1["month_end_date_dt"])
    out1["hire_date"] = _format_date_series(out1["hire_date_dt"])
    out1["leave_date"] = _format_date_series(out1["leave_date_dt"])
    out1["dc_nbr"] = out1["dc_nbr"].astype(int)
    out1["tenure_months"] = out1["tenure_months"].astype(int)
    out1["tenure_years"] = out1["tenure_years"].astype(int)
    out1 = out1[out1_cols].copy()
    out1 = out1.sort_values(["dc_nbr", "month_end_date", "employee_id", "guid", "hire_date", "leave_date", "tenure_months", "tenure_years", "age_range"], kind="mergesort").reset_index(drop=True)

    dim_keep = ee_dim[["employee_id", "guid", "nationality", "gender", "generation_name"]].copy()
    monthly_enriched = monthly_dt.merge(dim_keep, on=["employee_id", "guid"], how="left")

    base_keys = ["dc_nbr", "month_end_date"]
    def build_summary(df: pd.DataFrame, demographic_type: str, detail_col: str) -> pd.DataFrame:
        tmp = df.copy()
        tmp["demographic_type"] = demographic_type
        detail = tmp[detail_col].astype(str)
        tmp["demographic_detail"] = detail
        grp = (
            tmp.groupby(base_keys + ["demographic_type", "demographic_detail"], dropna=False)
            .size()
            .rename("ee_count")
            .reset_index()
        )
        return grp

    dc_month = monthly_enriched[base_keys].copy()
    dc_month["dc_nbr"] = dc_month["dc_nbr"].astype(int)
    dc_month = dc_month.drop_duplicates().reset_index(drop=True)

    gen_all = (
        monthly_enriched["generation_name"].dropna().astype(str).sort_values().drop_duplicates().tolist()
    )
    gender_all = (
        monthly_enriched["gender"].dropna().astype(str).sort_values().drop_duplicates().tolist()
    )
    nationality_all = (
        monthly_enriched["nationality"].dropna().astype(str).sort_values().drop_duplicates().tolist()
    )
    age_range_all = (
        monthly_enriched["age_range"].dropna().astype(str).sort_values().drop_duplicates().tolist()
    )
    tenure_years_all = (
        monthly_enriched["tenure_years"].dropna().astype(int).sort_values().drop_duplicates().astype(str).tolist()
    )

    sum_gen = build_summary(monthly_enriched, "Generation Name", "generation_name")
    sum_gender = build_summary(monthly_enriched, "Gender", "gender")
    sum_nat = build_summary(monthly_enriched, "Nationality", "nationality")
    sum_age = build_summary(monthly_enriched, "Age Range", "age_range")
    sum_tenure = build_summary(monthly_enriched, "Tenure", "tenure_years")
    sum_tenure["demographic_detail"] = sum_tenure["demographic_detail"].astype(str)

    summary_all = pd.concat([sum_gen, sum_gender, sum_nat, sum_age, sum_tenure], ignore_index=True)

    type_to_details = {
        "Generation Name": gen_all,
        "Gender": gender_all,
        "Nationality": nationality_all,
        "Age Range": age_range_all,
        "Tenure": tenure_years_all,
    }
    type_detail_rows: list[pd.DataFrame] = []
    for t, details in type_to_details.items():
        if not details:
            continue
        base = dc_month.copy()
        base["demographic_type"] = t
        cross = base.merge(pd.DataFrame({"demographic_detail": details}), how="cross")
        type_detail_rows.append(cross)
    all_combos = pd.concat(type_detail_rows, ignore_index=True)

    all_combos["dc_nbr"] = all_combos["dc_nbr"].astype(int)
    all_combos["month_end_date"] = all_combos["month_end_date"].astype(str)
    summary_all["dc_nbr"] = summary_all["dc_nbr"].astype(int)
    summary_all["month_end_date"] = summary_all["month_end_date"].astype(str)

    out2 = all_combos.merge(
        summary_all,
        on=base_keys + ["demographic_type", "demographic_detail"],
        how="left",
    )
    out2["ee_count"] = out2["ee_count"].fillna(0).astype(int)
    out2 = out2.sort_values(
        ["dc_nbr", "month_end_date", "demographic_type", "demographic_detail"],
        kind="mergesort",
    ).reset_index(drop=True)

    out2["dc_nbr"] = out2["dc_nbr"].astype(int)

    return {
        "output_01.csv": out1,
        "output_02.csv": out2[["dc_nbr", "month_end_date", "demographic_type", "demographic_detail", "ee_count"]],
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).write_text("")
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")


