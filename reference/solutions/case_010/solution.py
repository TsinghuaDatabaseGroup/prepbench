from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    ml = pd.read_csv(inputs_dir / "input_01.csv")
    un = pd.read_csv(inputs_dir / "input_02.csv")
    sales = pd.read_csv(inputs_dir / "input_03.csv")

    ml["Sign-up Date"] = pd.to_datetime(ml["Sign-up Date"], format="%Y-%m-%d")

    un_date = pd.to_datetime(un["Date"], format="%d.%m.%Y")

    un_initial = un["first_name"].str[0].str.lower()
    un_last = un["last_name"].astype(
        str).str.lower().str.replace(r"[^a-z]", "", regex=True)
    un_key = un_initial + un_last

    ml_local = ml["email"].str.split("@").str[0]
    ml_base = ml_local.str.extract(r"^([^0-9]*)", expand=False)
    ml_key = ml_base.str.lower().str.replace(r"[^a-z]", "", regex=True)

    un_df = pd.DataFrame({
        "un_key": un_key,
        "Unsubscribe Date": un_date
    }).groupby("un_key", as_index=False)["Unsubscribe Date"].max()

    ml2 = ml.copy()
    ml2["_key"] = ml_key

    ml2["_tmp"] = 1
    un_df["_tmp"] = 1
    cand = ml2[["email", "_key", "_tmp"]].merge(un_df, on="_tmp", how="left")
    cand = cand[cand.apply(lambda r: str(
        r["_key"]).startswith(str(r["un_key"])), axis=1)]
    cand["un_len"] = cand["un_key"].str.len()
    cand = cand.sort_values(["email", "un_len"], ascending=[
                            True, False]).drop_duplicates("email", keep="first")

    ml2 = ml2.merge(cand[["email", "Unsubscribe Date"]],
                    on="email", how="left").drop(columns=["_tmp"])

    ml2["Status"] = np.where(
        ml2["Unsubscribe Date"].isna(),
        "Subscribed",
        np.where(ml2["Unsubscribe Date"] < ml2["Sign-up Date"],
                 "Resubscribed", "Unsubscribed")
    )

    ml2["Interested in Liquid Soap"] = ml2["Liquid"].astype(bool)
    ml2["Interested In Soap Bars"] = ml2["Bar"].astype(bool)

    ml2 = ml2.merge(sales, on="email", how="left")

    out02_cols = [
        "Status",
        "email",
        "Interested in Liquid Soap",
        "Interested In Soap Bars",
        "Sign-up Date",
        "Unsubscribe Date",
        "Liquid Sales to Date",
        "Bar Sales to Date",
    ]

    ml2["_orig_order"] = np.arange(len(ml2))

    resub = ml2[ml2["Status"] == "Resubscribed"].copy()
    sub = ml2[ml2["Status"] == "Subscribed"].copy()

    resub["Sign-up Date"] = resub["Sign-up Date"].dt.strftime("%d/%m/%Y")
    resub["Unsubscribe Date"] = resub["Unsubscribe Date"].dt.strftime(
        "%d/%m/%Y")
    sub["Sign-up Date"] = sub["Sign-up Date"].dt.strftime("%d/%m/%Y")
    sub["Unsubscribe Date"] = ""

    out02 = pd.concat([
        resub.sort_values("_orig_order"),
        sub.sort_values("_orig_order"),
    ], ignore_index=True)[out02_cols]

    unsub = ml2[ml2["Status"] == "Unsubscribed"].copy()
    unsub["months"] = (unsub["Unsubscribe Date"].dt.year - unsub["Sign-up Date"].dt.year) * 12 + \
                      (unsub["Unsubscribe Date"].dt.month -
                       unsub["Sign-up Date"].dt.month)

    unsub["Months before Unsubscribed group"] = pd.cut(
        unsub["months"],
        bins=[-np.inf, 3, 6, 12, 24, np.inf],
        labels=["0-3", "3-6", "6-12", "12-24", "24+"],
        right=False
    ).astype(str)

    grp_cols_unsub = [
        "Months before Unsubscribed group",
        "Status",
        "Interested in Liquid Soap",
        "Interested In Soap Bars",
    ]
    agg_map = {
        "email": "count",
        "Liquid Sales to Date": "sum",
        "Bar Sales to Date": "sum",
    }
    unsub_g = unsub.groupby(grp_cols_unsub, as_index=False).agg(agg_map)

    t02_sr = pd.concat([resub, sub], ignore_index=True)[[
        "Status",
        "Interested in Liquid Soap",
        "Interested In Soap Bars",
        "email",
        "Liquid Sales to Date",
        "Bar Sales to Date",
    ]].copy()
    t02_sr["Months before Unsubscribed group"] = ""
    sr_g = t02_sr.groupby([
        "Months before Unsubscribed group",
        "Status",
        "Interested in Liquid Soap",
        "Interested In Soap Bars",
    ], as_index=False).agg(agg_map)

    out01 = pd.concat([unsub_g, sr_g], ignore_index=True)

    out01["_bo"] = out01["Months before Unsubscribed group"].map(
        {"0-3": 0, "3-6": 1, "6-12": 2, "12-24": 3, "24+": 4, "": 5})
    out01["_so"] = out01["Status"].map(
        {"Unsubscribed": 0, "Resubscribed": 1, "Subscribed": 2})
    out01 = out01.sort_values(["_bo", "_so", "Interested in Liquid Soap", "Interested In Soap Bars"]).drop(
        columns=["_bo", "_so"]).reset_index(drop=True)

    out01 = out01[[
        "Months before Unsubscribed group",
        "Status",
        "Interested in Liquid Soap",
        "Interested In Soap Bars",
        "email",
        "Liquid Sales to Date",
        "Bar Sales to Date",
    ]]

    return {
        "output_01.csv": out01,
        "output_02.csv": out02,
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    dfs = solve(inputs_dir)
    for fname, df in dfs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
