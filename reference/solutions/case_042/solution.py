from __future__ import annotations
from pathlib import Path
import pandas as pd
import re


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    in1 = pd.read_csv(inputs_dir / "input_01.csv")
    rates = pd.read_csv(inputs_dir / "input_02.csv")

    def split_location(loc: str):
        parts = [p.strip() for p in str(loc).split(",", 1)]
        if len(parts) == 2:
            return parts[0], parts[1]
        return str(loc), None

    city_country = in1["Location"].apply(split_location)
    in1["City"] = city_country.apply(lambda x: x[0])
    in1["Country"] = city_country.apply(lambda x: x[1])

    def parse_amount_currency(s: str):
        s = str(s).strip()
        m = re.match(r"^([0-9,]+)\s+([A-Z]{3})$", s)
        if not m:
            m2 = re.match(r"^([0-9,]+)$", s)
            if m2:
                return int(m2.group(1).replace(",", "")), None
            return None, None
        num = int(m.group(1).replace(",", ""))
        cur = m.group(2)
        return num, cur

    in1[["Store Potential Sales", "Currency"]] = in1["Store Potential Sales"].apply(lambda s: pd.Series(parse_amount_currency(s)))
    in1[["Store Cost", "Currency_cost"]] = in1["Store Cost"].apply(lambda s: pd.Series(parse_amount_currency(s)))

    in1["Currency"] = in1["Currency"].fillna(in1["Currency_cost"])

    in1 = in1.rename(columns={
        "Potential Store Location": "Zip Code",
    })

    valid_pairs = {
        ("New York", "United States"),
        ("San Francisco", "United States"),
        ("Miami", "United States"),
        ("Monterrey", "Mexico"),
    }
    mask_valid = in1[["City", "Country"]].apply(tuple, axis=1).isin(valid_pairs)
    df = in1.loc[mask_valid].copy()

    df = df[df["Currency"].notna()]

    df["Zip Code"] = df["Zip Code"].astype(str)
    df["Store Potential Sales"] = pd.to_numeric(df["Store Potential Sales"], errors="coerce")
    df["Store Cost"] = pd.to_numeric(df["Store Cost"], errors="coerce")

    df = df[df["Store Cost"] <= df["Store Potential Sales"]]

    df["_row_id"] = range(len(df))
    max_sales = df.groupby("Zip Code")["Store Potential Sales"].transform("max")
    df = df[df["Store Potential Sales"] == max_sales]
    df = df.sort_values(["Zip Code", "_row_id"]).drop_duplicates(subset=["Zip Code"], keep="first")

    df = df.merge(rates, how="left", on="Currency")

    out_cols = [
        "City",
        "Country",
        "Zip Code",
        "Store Cost",
        "Store Potential Sales",
        "Currency",
        "Value in USD",
    ]
    out = df[out_cols].copy()

    out["Store Cost"] = out["Store Cost"].astype(int)
    out["Store Potential Sales"] = out["Store Potential Sales"].astype(int)

    out = out.sort_values(["City", "Country", "Zip Code"]).reset_index(drop=True)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    result = solve(inputs_dir)
    for fname, df in result.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
