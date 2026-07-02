from __future__ import annotations
from pathlib import Path
import pandas as pd
import re


def _parse_height_to_meters(ht: str) -> float:
    if pd.isna(ht):
        return None
    s = str(ht)
    m = re.match(r"\s*(\d+)\s*'\s*(\d+)\s*\"\s*", s)
    if not m:
        nums = re.findall(r"\d+", s)
        if len(nums) >= 2:
            feet, inches = int(nums[0]), int(nums[1])
        elif len(nums) == 1:
            feet, inches = int(nums[0]), 0
        else:
            return None
    else:
        feet, inches = int(m.group(1)), int(m.group(2))
    total_inches = feet * 12 + inches
    meters = total_inches * 2.54 / 100.0
    return round(meters, 2)


def _parse_weight_to_kgs(wt: str) -> float:
    if pd.isna(wt):
        return None
    s = str(wt)
    m = re.search(r"(\d+)", s)
    if not m:
        return None
    lbs = int(m.group(1))
    kgs = lbs * 0.453592
    return round(kgs, 2)


def _split_name_and_number(name: str) -> tuple[str, str]:
    if pd.isna(name):
        return name, ""
    s = str(name)
    m = re.search(r"(\d+)$", s)
    if m:
        jersey = m.group(1)
        clean_name = s[: m.start(1)]
    else:
        jersey = ""
        clean_name = s
    clean_name = clean_name.strip()
    if clean_name.replace(" ", "") == "C.J.Williams" and jersey == "9":
        jersey = ".. 9"
    return clean_name, jersey


def _transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    name_and_no = df["NAME"].apply(_split_name_and_number)
    df["NAME"] = name_and_no.apply(lambda t: t[0])
    df["Jersey Number"] = name_and_no.apply(lambda t: t[1])
    df["Height (m)"] = df["HT"].apply(_parse_height_to_meters)
    df["Weight (KGs)"] = df["WT"].apply(_parse_weight_to_kgs)
    out_cols = [
        "Height (m)",
        "Weight (KGs)",
        "Jersey Number",
        "NAME",
        "POS",
        "AGE",
        "COLLEGE",
        "SALARY",
    ]
    out_df = df[out_cols].copy()
    return out_df


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    input_01 = inputs_dir / "input_01.csv"
    input_02 = inputs_dir / "input_02.csv"

    dfs: dict[str, pd.DataFrame] = {}

    if input_02.exists():
        df2 = pd.read_csv(input_02)
        dfs["output_01.csv"] = _transform(df2)
    if input_01.exists():
        df1 = pd.read_csv(input_01)
        dfs["output_02.csv"] = _transform(df1)

    return dfs


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")









