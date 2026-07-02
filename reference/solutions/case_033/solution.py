from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np



def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    staff = pd.concat(
        [
            pd.read_csv(
                inputs_dir / "input_01.csv").assign(Store="Sheffield Store"),
            pd.read_csv(
                inputs_dir / "input_02.csv").assign(Store="Leeds Store"),
        ],
        ignore_index=True,
    )
    staff["Start Date"] = pd.to_datetime(
        staff["Start Date"], format="%Y-%m-%d")
    staff["End Date"] = pd.to_datetime(staff["End Date"], format="%Y-%m-%d")
    staff["Salary"] = staff["Salary"].astype(float)

    start_2019 = pd.Timestamp("2019-01-01")
    end_2019 = pd.Timestamp("2019-12-31")
    staff = staff.loc[
        (staff["Start Date"] <= end_2019)
        & (staff["End Date"].isna() | (staff["End Date"] >= start_2019))
    ].reset_index(drop=True)

    ranges = pd.read_csv(inputs_dir / "input_03.csv")
    bounds = (
        ranges["Range"]
        .str.replace("£", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.split("-", expand=True)
        .astype(float)
    )
    ranges = ranges.assign(min=bounds[0], max=bounds[1])
    ranges["Bonus amount"] = ranges["Bonus amount"].str.replace(
        "£", "", regex=False).str.replace(",", "", regex=False).astype(float)
    ranges["% above target for bonus"] = ranges["% above target for bonus"].astype(
        float)
    mins = ranges["min"].to_numpy()
    maxs = ranges["max"].to_numpy()

    def salary_to_range_idx(s: pd.Series) -> np.ndarray:
        salaries = s.to_numpy(dtype=float)
        hits = (salaries[:, None] >= mins) & (salaries[:, None] <= maxs)
        first_hit = hits.argmax(axis=1)
        return np.where(hits.any(axis=1), first_hit, -1)

    q_months = {
        "Q1": ["2019-01-01 00:00:00", "2019-02-01 00:00:00", "2019-03-01 00:00:00"],
        "Q2": ["2019-04-01 00:00:00", "2019-05-01 00:00:00", "2019-06-01 00:00:00"],
        "Q3": ["2019-07-01 00:00:00", "2019-08-01 00:00:00", "2019-09-01 00:00:00"],
    }
    q_final_month_date = {
        "Q1": pd.Timestamp("2019-03-01"),
        "Q2": pd.Timestamp("2019-06-01"),
        "Q3": pd.Timestamp("2019-09-01"),
    }

    sales = pd.read_csv(inputs_dir / "input_04.csv")
    for q, cols in q_months.items():
        sales[q] = sales[cols].astype(float).sum(
            axis=1) >= sales["Quarterly Target"]
    store_met = (
        sales[["Store", "Q1", "Q2", "Q3"]]
        .assign(Store=lambda df: df["Store"] + " Store")
        .set_index("Store")
    )

    employ_flags = {
        q: (staff["Start Date"] <= dt) & (
            staff["End Date"].fillna(pd.Timestamp.max) >= dt)
        for q, dt in q_final_month_date.items()
    }
    met_flags = {q: staff["Store"].map(store_met[q])
                 for q in q_final_month_date}
    eligible = pd.concat([(employ_flags[q] & met_flags[q]).rename(q)
                         for q in q_final_month_date], axis=1)
    eligible_count = eligible.sum(axis=1)

    range_idx = salary_to_range_idx(staff["Salary"])
    matched = ranges.reindex(range_idx).reset_index(drop=True)

    bonus_per_q = matched["Bonus amount"].fillna(0)
    bonus_amt = bonus_per_q * eligible_count
    pct_bonus = bonus_amt.div(staff["Salary"]).mul(100)
    pct_bonus = pct_bonus.where(
        pd.Series(range_idx, index=staff.index) >= 0).round(9)

    out1 = pd.DataFrame(
        {
            "% Bonus of Salary": pct_bonus,
            "Bonus amount": bonus_amt,
            "Store": staff["Store"],
            "Name": staff["Name"],
            "Total Salary": staff["Salary"],
        }
    )

    leeds = staff[staff["Store"] ==
                  "Leeds Store"].copy().reset_index(drop=True)
    leeds_idx = salary_to_range_idx(leeds["Salary"])
    leeds_match = ranges.reindex(leeds_idx).reset_index(drop=True)
    assumed_role = pd.Series(
        np.select(
            [leeds_match["min"] >= 40000, leeds_match["min"] >= 30000],
            ["Area Manager", "Manager"],
            default="Team Member",
        ),
        index=leeds.index,
    )
    mask_outside = pd.Series(leeds_idx < 0, index=leeds.index)
    mask_wrong = (assumed_role != leeds["Role"]) & ~mask_outside

    rows = []
    if mask_outside.any():
        rows.append(
            pd.DataFrame(
                {
                    "Correct Salary for Role?": False,
                    "Assumed Position based on Salary Range": "Team Member",
                    "Pay Status": "Incorrect Pay",
                    "End Date": pd.Timestamp("2019-10-01"),
                    "Salary Range Minimum": np.nan,
                    "Salary Range Maximum": np.nan,
                    "Bonus amount": np.nan,
                    "Range": "",
                    "% above target for bonus": np.nan,
                    "Role": leeds.loc[mask_outside, "Role"],
                    "Start Date": leeds.loc[mask_outside, "Start Date"],
                    "Salary": leeds.loc[mask_outside, "Salary"],
                    "Store": leeds.loc[mask_outside, "Store"],
                    "Name": leeds.loc[mask_outside, "Name"],
                }
            )
        )
    if mask_wrong.any():
        rows.append(
            pd.DataFrame(
                {
                    "Correct Salary for Role?": False,
                    "Assumed Position based on Salary Range": assumed_role.loc[mask_wrong],
                    "Pay Status": "Assumed Correct Pay",
                    "End Date": pd.Timestamp("2019-10-01"),
                    "Salary Range Minimum": leeds_match.loc[mask_wrong.to_numpy(), "min"],
                    "Salary Range Maximum": leeds_match.loc[mask_wrong.to_numpy(), "max"],
                    "Bonus amount": leeds_match.loc[mask_wrong.to_numpy(), "Bonus amount"],
                    "Range": leeds_match.loc[mask_wrong.to_numpy(), "Range"],
                    "% above target for bonus": leeds_match.loc[mask_wrong.to_numpy(), "% above target for bonus"],
                    "Role": leeds.loc[mask_wrong, "Role"],
                    "Start Date": leeds.loc[mask_wrong, "Start Date"],
                    "Salary": leeds.loc[mask_wrong, "Salary"],
                    "Store": leeds.loc[mask_wrong, "Store"],
                    "Name": leeds.loc[mask_wrong, "Name"],
                }
            )
        )

    out2_columns = [
        "Correct Salary for Role?",
        "Assumed Position based on Salary Range",
        "Pay Status",
        "End Date",
        "Salary Range Minimum",
        "Salary Range Maximum",
        "Bonus amount",
        "Range",
        "% above target for bonus",
        "Role",
        "Start Date",
        "Salary",
        "Store",
        "Name",
    ]
    out2 = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame(
        columns=out2_columns)

    if not out2.empty:
        out2["Start Date"] = pd.to_datetime(out2["Start Date"])
        out2["End Date"] = pd.to_datetime(out2["End Date"])
        out2["Start Date"] = out2["Start Date"].dt.strftime("%d/%m/%Y")
        out2["End Date"] = out2["End Date"].dt.strftime("%d/%m/%Y")

    for col in ["Salary Range Minimum", "Salary Range Maximum", "Bonus amount", "% above target for bonus", "Salary"]:
        if col in out2.columns:
            out2[col] = pd.to_numeric(out2[col], errors="coerce")

    out1["Bonus amount"] = pd.to_numeric(out1["Bonus amount"], errors="coerce")
    out1["Total Salary"] = pd.to_numeric(out1["Total Salary"], errors="coerce")
    out1["% Bonus of Salary"] = pd.to_numeric(
        out1["% Bonus of Salary"], errors="coerce")

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
