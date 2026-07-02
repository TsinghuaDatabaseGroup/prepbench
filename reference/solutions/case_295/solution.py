from __future__ import annotations

from pathlib import Path
from typing import Dict

import math
import pandas as pd


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    df_ads = pd.read_csv(inputs_dir / "input_01.csv")
    df_users_raw = pd.read_csv(inputs_dir / "input_02.csv")

    users_line = df_users_raw.iloc[0, 0]
    user_tokens = [tok.strip() for tok in str(
        users_line).split(",") if tok.strip()]

    def parse_user(token: str) -> dict:
        user_id = token[:7]
        user_type = token[-1]
        dealership_id = ""
        if user_type == "D":
            dealership_id = token[7:10]
        return {
            "user_id": user_id,
            "user_type": user_type,
            "Dealership ID": dealership_id,
        }

    df_users = pd.DataFrame([parse_user(t) for t in user_tokens])
    df_users["user_id"] = df_users["user_id"].astype(str)

    ads = df_ads.copy()
    ads["user_id"] = ads["user_id"].astype(str)
    ads = ads[ads["sale_date"].notna() & (
        ads["sale_date"].astype(str).str.strip() != "")].copy()

    ads["publish_ts"] = pd.to_datetime(
        ads["publish_ts"], format="%d/%m/%Y %H:%M:%S", errors="coerce")
    ads["sale_date_dt"] = pd.to_datetime(ads["sale_date"], errors="coerce")

    ads = ads.merge(df_users, how="left", on="user_id")

    ads = ads[ads["user_type"] == "D"].copy()

    first_pub = ads.groupby("registration_number", as_index=False)[
        "publish_ts"].min().rename(columns={"publish_ts": "first_publish"})
    ads = ads.merge(first_pub, on="registration_number", how="left")
    ads = ads[ads["publish_ts"] == ads["first_publish"]].copy()

    delta_days = (ads["sale_date_dt"] - ads["first_publish"]
                  ).dt.total_seconds() / (24 * 3600)
    ads["Days to Sell"] = delta_days.apply(
        lambda x: math.ceil(x) if pd.notna(x) else pd.NA)

    result = (
        ads.groupby("Dealership ID", as_index=False)["Days to Sell"].mean().rename(
            columns={"Days to Sell": "Dealership Avg Days to Sell"})
    )

    result["Dealership Avg Days to Sell"] = result["Dealership Avg Days to Sell"].apply(
        lambda x: math.ceil(x) if pd.notna(x) else pd.NA)
    result["Dealership Avg Days to Sell"] = result["Dealership Avg Days to Sell"].astype(
        int)

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False)
