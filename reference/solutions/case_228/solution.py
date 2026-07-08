from pathlib import Path
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    part1 = pd.read_csv(inputs_dir / "input_01.csv")
    addl = pd.read_csv(inputs_dir / "input_02.csv")

    part1["_dob"] = pd.to_datetime(part1["Date of Birth"], format="%Y-%m-%d", errors="coerce")
    addl["_dob"] = pd.to_datetime(addl["Date of Birth"], format="%d/%m/%Y", errors="coerce")

    for df in (part1, addl):
        for col in ["English", "Maths", "Science", "School Name"]:
            df[col] = df[col].astype(str).str.strip()

    part1["_key"] = (
        part1["_dob"].astype("int64").astype(str)
        + "||" + part1["School Name"]
        + "||" + part1["English"]
        + "||" + part1["Maths"]
        + "||" + part1["Science"]
    )
    addl["_key"] = (
        addl["_dob"].astype("int64").astype(str)
        + "||" + addl["School Name"]
        + "||" + addl["English"]
        + "||" + addl["Maths"]
        + "||" + addl["Science"]
    )
    def compute_initials(full_name: str) -> str:
        if not isinstance(full_name, str):
            return ""
        parts = [p for p in full_name.strip().split() if p]
        if not parts:
            return ""
        first = parts[0][0]
        second = ""
        if len(parts) >= 2:
            second_token = parts[1]
            second = second_token.split("-")[0][0]
        return (first + second).upper()

    addl["Initials_calc"] = addl["Full Name"].apply(compute_initials)
    part1["Initials"] = part1["Initials"].astype(str).str.strip().str.upper()

    part1["_key2"] = part1["_key"] + "||" + part1["Initials"]
    addl["_key2"] = addl["_key"] + "||" + addl["Initials_calc"]

    part1_dedup = (
        part1.sort_values("Distance From School (Miles)", ascending=True)
        .drop_duplicates(subset=["_key2"], keep="first")
    )

    merged = addl.merge(
        part1_dedup[
            [
                "_key2",
                "Subject Selection",
                "Distance From School (Miles)",
            ]
        ],
        left_on="_key2",
        right_on="_key2",
        how="left",
        validate="many_to_one",
    )

    if merged["Subject Selection"].isna().any():
        part1_dedup_key = (
            part1.sort_values("Distance From School (Miles)", ascending=True)
            .drop_duplicates(subset=["_key"], keep="first")
        )[["_key", "Subject Selection", "Distance From School (Miles)"]]
        fallback = addl.merge(
            part1_dedup_key,
            left_on="_key",
            right_on="_key",
            how="left",
            validate="many_to_one",
            suffixes=("", "_fb"),
        )[["Subject Selection", "Distance From School (Miles)"]].rename(
            columns={
                "Subject Selection": "Subject Selection_fb",
                "Distance From School (Miles)": "Distance From School (Miles)_fb",
            }
        )
        merged = pd.concat([merged, fallback], axis=1)
        merged["Subject Selection"] = merged["Subject Selection"].fillna(merged["Subject Selection_fb"])
        merged["Distance From School (Miles)"] = merged["Distance From School (Miles)"].fillna(
            merged["Distance From School (Miles)_fb"]
        )
        merged = merged.drop(columns=["Subject Selection_fb", "Distance From School (Miles)_fb"])

    assert len(merged) == len(addl)
    assert merged["Subject Selection"].notna().all(), "Join failed for some rows even after fallback"

    merged["Distance From School (Miles)"] = pd.to_numeric(
        merged["Distance From School (Miles)"], errors="coerce"
    )
    merged["Grade Score"] = pd.to_numeric(merged["Grade Score"], errors="coerce")

    merged = merged.sort_values(
        by=["Subject Selection", "Region", "Grade Score", "Distance From School (Miles)"],
        ascending=[True, True, False, True],
    )

    def pick_top(group: pd.DataFrame) -> pd.DataFrame:
        east = group[group["Region"].str.upper() == "EAST"].head(15)
        west = group[group["Region"].str.upper() == "WEST"].head(5)
        return pd.concat([east, west], ignore_index=True)

    selected = merged.groupby("Subject Selection", group_keys=False).apply(pick_top)

    counts = (
        selected.groupby(["Region", "School Name"], as_index=False)
        .size()
        .rename(columns={"size": "Accepted Count"})
    )
    region_total = pd.DataFrame({"Region": ["EAST", "WEST"], "Total Seats": [75, 25]})
    counts = counts.merge(region_total, on="Region", how="left")
    counts["Acceptance %"] = (counts["Accepted Count"] / counts["Total Seats"]) * 100

    def label_status(region_df: pd.DataFrame) -> pd.DataFrame:
        if region_df.empty:
            return region_df.assign(**{"School Status": pd.Series(dtype=str)})
        max_val = region_df["Acceptance %"].max()
        min_val = region_df["Acceptance %"].min()
        region_df["School Status"] = "Average Performing"
        region_df.loc[region_df["Acceptance %"] == max_val, "School Status"] = "High Performing"
        region_df.loc[region_df["Acceptance %"] == min_val, "School Status"] = "Low Performing"
        return region_df

    counts = counts.groupby("Region", group_keys=False).apply(label_status)
    counts = counts[["Region", "School Name", "School Status"]]

    selected = selected.merge(counts, on=["Region", "School Name"], how="left")

    out = selected.copy()
    out = out[[
        "Student ID",
        "Full Name",
        "Date of Birth",
        "Region",
        "School Name",
        "School Status",
        "Subject Selection",
        "English",
        "Maths",
        "Science",
        "Grade Score",
    ]].copy()

    out["Student ID"] = pd.to_numeric(out["Student ID"])
    out["Grade Score"] = pd.to_numeric(out["Grade Score"])
    out["Date of Birth"] = pd.to_datetime(out["Date of Birth"], errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")

    out = out.merge(
        selected[["Student ID", "Subject Selection", "Region", "Grade Score", "Distance From School (Miles)"]],
        on=["Student ID", "Subject Selection", "Region", "Grade Score"],
        how="left",
    ).sort_values(
        by=["Subject Selection", "Region", "Grade Score", "Distance From School (Miles)"],
        ascending=[True, True, False, True],
    ).drop(columns=["Distance From School (Miles)"]).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

