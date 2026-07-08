from __future__ import annotations

from pathlib import Path
import re
from typing import Dict

import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_money_to_float(s: str) -> float | None:
        if s is None:
            return None
        txt = str(s).strip()
        if txt.lower() in {"", "n/a", "na", "none", "null"}:
            return None
        txt = txt.replace("$", "").replace(",", "").strip()
        if not txt:
            return None
        multiplier = 1.0
        if txt.endswith(("M", "m")):
            multiplier = 1_000_000.0
            txt = txt[:-1]
        elif txt.endswith(("B", "b")):
            multiplier = 1_000_000_000.0
            txt = txt[:-1]
        txt = txt.strip()
        try:
            val = float(txt)
        except Exception:
            return None
        return round(val * multiplier, 2)

    def categorize_purchase(price: float) -> str:
        if price < 25000:
            return "Small"
        if price < 50000:
            return "Medium"
        if price < 75000:
            return "Large"
        return "Very Large"

    def categorize_market_cap(market_cap: float) -> str:
        if market_cap < 100_000_000:
            return "Small"
        if market_cap < 1_000_000_000:
            return "Medium"
        if market_cap < 100_000_000_000:
            return "Large"
        return "Huge"

    def extract_month_from_filename(path: Path) -> int:
        m = re.search(r"_(\d+)\.csv$", path.name)
        if m:
            try:
                month = int(m.group(1))
                if 1 <= month <= 12:
                    return month
            except Exception:
                pass
        return 1

    all_frames: list[pd.DataFrame] = []
    if inputs_dir.exists():
        for p in sorted(inputs_dir.glob("*.csv")):
            month = extract_month_from_filename(p)
            df = pd.read_csv(p, dtype=str)
            if "Ticker" in df.columns:
                df["Ticker"] = df["Ticker"].fillna("").astype(str).str.strip()
            if "Sector" in df.columns:
                df["Sector"] = df["Sector"].fillna("").astype(str).str.strip()
            if "Market" in df.columns:
                df["Market"] = df["Market"].fillna("").astype(str).str.strip()
            if "Stock Name" in df.columns:
                df["Stock Name"] = df["Stock Name"].fillna(
                    "").astype(str).str.strip()
            df["Market Capitalisation"] = df["Market Cap"].map(
                parse_money_to_float)
            df["Purchase Price"] = df["Purchase Price"].map(
                parse_money_to_float)
            df = df[df["Market Capitalisation"].notna()].copy()
            file_date = f"2023-{month:02d}-01"
            df["File Date"] = file_date
            df["Purchase Price Categorisation"] = df["Purchase Price"].astype(
                float).map(categorize_purchase)
            df["Market Capitalisation Categorisation"] = df["Market Capitalisation"].astype(
                float).map(categorize_market_cap)
            group_keys = ["File Date", "Purchase Price Categorisation",
                          "Market Capitalisation Categorisation"]
            df = df.sort_values(
                by=group_keys + ["Purchase Price", "Ticker"], ascending=[True, True, True, False, True])
            df["Rank"] = df.groupby(group_keys).cumcount() + 1
            df = df[df["Rank"] <= 5].copy()
            out_cols = [
                "Market Capitalisation Categorisation",
                "Purchase Price Categorisation",
                "File Date",
                "Ticker",
                "Sector",
                "Market",
                "Stock Name",
                "Market Capitalisation",
                "Purchase Price",
                "Rank",
            ]
            df = df[out_cols]
            all_frames.append(df)

    result_df = pd.concat(all_frames, ignore_index=True) if all_frames else pd.DataFrame(
        columns=[
            "Market Capitalisation Categorisation",
            "Purchase Price Categorisation",
            "File Date",
            "Ticker",
            "Sector",
            "Market",
            "Stock Name",
            "Market Capitalisation",
            "Purchase Price",
            "Rank",
        ]
    )

    return {
        "output_01.csv": result_df
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    out_map = solve(inputs_dir)
    for fname, df in out_map.items():
        if df is None:
            df = pd.DataFrame()
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
