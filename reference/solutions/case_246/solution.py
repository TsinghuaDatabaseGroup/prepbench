from pathlib import Path
from typing import Dict

import pandas as pd


def _read_term(path: Path, has_first_name: bool) -> pd.DataFrame:
    df = pd.read_csv(path)
    if not has_first_name:
        first_col = df.columns[0]
        df = df.rename(columns={first_col: "First Name"})
    df = df.rename(columns={
        "First Name": "First Name",
        "Last Name": "Last Name",
        "Days Present": "Days Present",
        "Days Absent": "Days Absent",
    })
    df["Days Present"] = pd.to_numeric(df["Days Present"], errors="coerce").fillna(0)
    df["Days Absent"] = pd.to_numeric(df["Days Absent"], errors="coerce").fillna(0)
    return df[["First Name", "Last Name", "Days Present", "Days Absent"]]


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    t1 = _read_term(inputs_dir / "input_01.csv", has_first_name=True)
    t2 = _read_term(inputs_dir / "input_02.csv", has_first_name=False)
    t3 = _read_term(inputs_dir / "input_03.csv", has_first_name=False)
    year_group = pd.read_csv(inputs_dir / "input_04.csv")
    year_group = year_group.rename(columns={"Year Group ": "Year Group"})

    all_terms = pd.concat([t1, t2, t3], ignore_index=True)
    all_terms["First Name"] = all_terms["First Name"].astype(str).str.strip()
    all_terms["Last Name"] = all_terms["Last Name"].astype(str).str.strip()

    name_order = (
        all_terms.assign(name_order=range(len(all_terms)))
        .drop_duplicates(["First Name", "Last Name"], keep="first")
        [["First Name", "Last Name", "name_order"]]
    )

    agg = (
        all_terms.groupby(["First Name", "Last Name"], as_index=False)
        .agg({"Days Present": "sum", "Days Absent": "sum"})
    )
    agg["Total Days"] = agg["Days Present"] + agg["Days Absent"]
    agg["Year Attendance Rate"] = (agg["Days Present"] / agg["Total Days"] * 100).round(2)
    agg = agg.merge(name_order, on=["First Name", "Last Name"], how="left")
    agg["Full Name"] = agg["First Name"] + " " + agg["Last Name"]

    max_rate = agg["Year Attendance Rate"].max()
    best = agg[agg["Year Attendance Rate"] == max_rate].copy()
    best = best.sort_values(by=["name_order"], ascending=True, kind="mergesort").reset_index(drop=True)
    best["Rank"] = 1
    out1 = best[["Full Name", "Year Attendance Rate", "Rank"]]

    yg = year_group.copy()
    yg["First Name"] = yg["First Name"].astype(str).str.strip()
    yg["Last Name"] = yg["Last Name"].astype(str).str.strip()
    yg = yg.reset_index().rename(columns={"index": "yg_order"})

    yg = yg.merge(
        agg[["First Name", "Last Name", "Full Name", "Year Attendance Rate"]],
        on=["First Name", "Last Name"],
        how="left",
    )

    def select_top(g: pd.DataFrame) -> pd.DataFrame:
        g = g.sort_values(by=["Year Attendance Rate", "yg_order"], ascending=[False, True], kind="mergesort")
        thr = g["Year Attendance Rate"].quantile(0.95, interpolation="linear")
        sel = g[g["Year Attendance Rate"] >= thr]
        if sel.empty:
            sel = g.head(1)
        sel = sel.sort_values(by=["Year Attendance Rate", "yg_order"], ascending=[False, True], kind="mergesort")
        return sel

    top_by_group = (
        yg.groupby("Year Group", sort=True, group_keys=False)
        .apply(select_top)
        .reset_index(drop=True)
    )

    out2 = top_by_group[["Year Group", "Full Name", "Year Attendance Rate"]]

    return {
        "output_01.csv": out1,
        "output_02.csv": out2,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)).to_csv(
            cand_dir / fname, index=False, encoding="utf-8"
        )
