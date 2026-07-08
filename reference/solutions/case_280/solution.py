from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
import re


def solve() -> Dict[str, pd.DataFrame]:
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"

    df_lookup = pd.read_csv(inputs_dir / "input_01.csv")
    df = pd.read_csv(inputs_dir / "input_02.csv")

    def parse_mixed(s: str) -> pd.Timestamp | pd.NaT:
        if not isinstance(s, str):
            return pd.NaT
        s_strip = s.strip()
        if "/" in s_strip:
            return pd.to_datetime(s_strip, errors="coerce", dayfirst=False)
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", s_strip)
        if m:
            y, mm, dd = m.group(1), m.group(2), m.group(3)
            swapped = f"{y}-{dd}-{mm}"
            ts = pd.to_datetime(swapped, errors="coerce", dayfirst=False)
            if pd.notna(ts):
                return ts
        return pd.to_datetime(s_strip, errors="coerce", dayfirst=False)

    rec_parsed = df["Date Received"].apply(parse_mixed)
    res_parsed = df["Date Resolved"].apply(parse_mixed)
    df["Date Received"] = rec_parsed
    df["Date Resolved"] = res_parsed

    if df["Timely Response"].dtype != bool:
        df["Timely Response"] = df["Timely Response"].astype(
            str).str.strip().str.lower().map({"true": True, "false": False})

    pat = re.compile(r"^\s*([A-Z]{2}\d{4})\s*-\s*([^:]+):\s*(.*)\s*$")

    def parse_description(text: str) -> tuple[str | None, str | None, str | None]:
        if not isinstance(text, str):
            return None, None, None
        m = pat.match(text)
        if not m:
            return None, None, text.strip()
        product_id, issue_type, desc = m.group(
            1), m.group(2).strip(), m.group(3).strip()
        if len(desc) >= 2 and ((desc[0] == desc[-1] == '"') or (desc[0] == desc[-1] == "'")):
            desc = desc[1:-1]
        return product_id, issue_type, desc

    parsed = df["Complaint Description"].apply(parse_description)
    df["Product ID"] = parsed.map(lambda x: x[0])
    df["Issue Type"] = parsed.map(lambda x: x[1])
    df["Complaint Description"] = parsed.map(lambda x: x[2])

    code_to_category = {
        "BE": "Beauty",
        "CL": "Clothes",
        "EL": "Electronic",
        "GR": "Groceries",
        "HO": "Home",
    }
    df["Category Code"] = df["Product ID"].astype(str).str[:2]
    df["Product Category"] = df["Category Code"].map(code_to_category)

    mask_after = res_parsed > rec_parsed
    df = df[mask_after].copy()

    out_cols = [
        "Complaint ID",
        "Receipt Number",
        "Customer ID",
        "Date Received",
        "Date Resolved",
        "Timely Response",
        "Response to Consumer",
        "Issue Type",
        "Product Category",
        "Product ID",
        "Complaint Description",
    ]
    out = df[out_cols].copy()

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve()
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
