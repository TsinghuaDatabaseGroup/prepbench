from pathlib import Path
from typing import Dict
import pandas as pd
import re


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_file = inputs_dir / "input_01.csv"
    df = pd.read_csv(input_file, dtype=str)

    first_col = df.columns[0]
    project_col = df.columns[1]

    date_cols = [c for c in df.columns if re.fullmatch(
        r"\d{4}/\d{1,2}/\d{1,2}", str(c))]

    df = df[df[project_col].fillna("").str.startswith(
        "Overall Total for ") == False]

    long_df = df.melt(id_vars=[first_col, project_col],
                      value_vars=date_cols, var_name="Date", value_name="Hours")

    long_df["Hours"] = long_df["Hours"].astype(str).str.strip()
    long_df = long_df[(long_df["Hours"].notna()) & (long_df["Hours"] != "")]
    long_df = long_df[long_df["Hours"].str.lower() != "annual leave".lower()]

    long_df["Hours"] = pd.to_numeric(long_df["Hours"], errors="coerce")
    long_df = long_df[long_df["Hours"].notna()]

    def parse_name_area(s: str):
        s = s if isinstance(s, str) else ""
        m = re.match(r"^(.*?),\s*\d+:\s*(.*)$", s)
        if m:
            name = m.group(1).strip()
            area = m.group(2).strip()
            return pd.Series([name, area])
        else:
            if ":" in s:
                left, right = s.split(":", 1)
                area = right.strip()
                if "," in left:
                    name = left.rsplit(",", 1)[0].strip()
                else:
                    name = left.strip()
                return pd.Series([name, area])
            return pd.Series([s.strip(), ""])

    long_df[["Name", "Area of Work"]
            ] = long_df[first_col].apply(parse_name_area)

    nd = long_df.groupby(["Name", "Date"], as_index=False)["Hours"].sum()

    nd_positive = nd[nd["Hours"] > 0]
    per_person = nd_positive.groupby("Name", as_index=False).agg(
        {"Hours": "sum", "Date": "nunique"})
    per_person = per_person.rename(
        columns={"Hours": "TotalHours_All", "Date": "DaysWorked"})
    per_person["Avg Number of Hours worked per day"] = per_person["TotalHours_All"] / \
        per_person["DaysWorked"]

    no_chats = long_df[long_df["Area of Work"].str.strip().str.lower()
                       != "chats"]

    by_area = no_chats.groupby(["Name", "Area of Work"], as_index=False)[
        "Hours"].sum()
    by_area = by_area.rename(columns={"Hours": "AreaHours"})

    total_non_chats = no_chats.groupby("Name", as_index=False)[
        "Hours"].sum().rename(columns={"Hours": "TotalHours_NonChats"})

    area_with_tot = by_area.merge(total_non_chats, on="Name", how="left")
    area_with_tot["% of Total"] = (
        area_with_tot["AreaHours"] / area_with_tot["TotalHours_NonChats"]) * 100.0
    area_with_tot["% of Total"] = area_with_tot["% of Total"].round(
        0).astype(int).astype(str) + "%"

    client_only = area_with_tot[area_with_tot["Area of Work"].str.strip(
    ).str.lower() == "client"].copy()

    out = client_only.merge(
        per_person[["Name", "Avg Number of Hours worked per day"]], on="Name", how="left")

    out = out[["Name", "Area of Work", "% of Total",
               "Avg Number of Hours worked per day"]].copy()

    out["Avg Number of Hours worked per day"] = pd.to_numeric(
        out["Avg Number of Hours worked per day"]).round(9)

    out = out.sort_values(by=["Avg Number of Hours worked per day", "Name"], ascending=[
                          True, True]).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
