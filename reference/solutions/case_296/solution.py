from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import re
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def read_source(url_path: Path) -> str:
        src_df = pd.read_csv(url_path)
        vals = src_df.iloc[:, 0].dropna().tolist()
        return vals[1] if len(vals) > 1 else (vals[0] if vals else "")

    def parse_money(text: str) -> float:
        if pd.isna(text):
            return None
        s = str(text)
        s = s.replace(",", "")
        s = s.replace("*", "").strip()
        if s.startswith("$"):
            s = s[1:]
        s = s.strip()
        m = re.match(r"^([0-9]+(?:\.[0-9]+)?)\s*million\s*$", s, re.IGNORECASE)
        if m:
            return float(m.group(1)) * 1_000_000
        try:
            return float(s)
        except ValueError:
            return None

    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        rename_map = {}
        for col in df.columns:
            lc = col.lower().strip()
            if lc == "rank":
                rename_map[col] = "Rank"
            elif lc == "name":
                rename_map[col] = "Name"
            elif lc == "sport":
                rename_map[col] = "Sport"
            elif lc in ("nation", "nationality", "country"):
                rename_map[col] = "Country"
            elif lc in ("total", "total earnings"):
                rename_map[col] = "Total earnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings",):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings (usd)", "salary/winnings "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings usd"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings usd"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings  "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary\u200b/winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings", "salary/winnings", "salary/winnings* "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary/winnings "):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("salary/winnings", "salary\nwinnings", "salary / winnings"):
                rename_map[col] = "Salary/Winnings"
            elif lc in ("endorsements",):
                rename_map[col] = "Endorsements"
        df = df.rename(columns=rename_map)
        if "Salary/Winnings" not in df.columns and "Salary/winnings" in df.columns:
            df = df.rename(columns={"Salary/winnings": "Salary/Winnings"})
        if "Total earnings" not in df.columns and "Total" in df.columns:
            df = df.rename(columns={"Total": "Total earnings"})
        if "Country" not in df.columns and "Nation" in df.columns:
            df = df.rename(columns={"Nation": "Country"})
        if "Country" not in df.columns and "Nationality" in df.columns:
            df = df.rename(columns={"Nationality": "Country"})
        return df

    source_url = read_source(inputs_dir / "input_14.csv")

    frames: List[pd.DataFrame] = []
    for idx in range(1, 14):
        year = 2011 + idx
        path = inputs_dir / f"input_{idx:02d}.csv"
        df = pd.read_csv(path)
        df = normalize_columns(df)

        for col in ["Total earnings", "Salary/Winnings", "Endorsements"]:
            df[col] = df[col].map(parse_money)

        df["Year"] = year
        df["Source"] = source_url

        frames.append(df[[
            "Year",
            "Rank",
            "Name",
            "Sport",
            "Country",
            "Total earnings",
            "Salary/Winnings",
            "Endorsements",
            "Source",
        ]])

    out = pd.concat(frames, ignore_index=True)

    out["Year"] = pd.to_numeric(out["Year"], errors="coerce")
    out["Rank"] = pd.to_numeric(out["Rank"], errors="coerce")
    for col in ["Total earnings", "Salary/Winnings", "Endorsements"]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, data in outputs.items():
        out_path = cand_dir / filename
        data.to_csv(out_path, index=False, encoding="utf-8")


