from __future__ import annotations
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dateutil import parser


def _clean_country(x: str) -> str:
    if pd.isna(x):
        return x
    s = str(x).strip()
    s_low = s.lower()
    if s_low in {"england", "ingland", "egland", "3ngland", "eggland", "enGLAND".lower()}:
        return "England"
    if s_low in {"scotland", "sc0tland", "scottish"}:
        return "Scotland"
    if s_low in {"united states", "united state", "usa", "u.s.a."}:
        return "United States"
    if s_low in {"the netherlands", "netherlands", "holland"}:
        return "Netherlands"
    return s.title()


def _clean_store(country: str, store: str) -> str:
    if pd.isna(store):
        return store
    s = str(store).strip()
    if _clean_country(country) == "Netherlands" and s.lower() == "amstelveen":
        return "Amsterdam"
    return s


def _parse_date(date_str: str) -> datetime | pd.NaT:
    if pd.isna(date_str) or str(date_str).strip() == "":
        return pd.NaT
    s = str(date_str).strip()
    s_low = s.lower()
    if any(w in s_low for w in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]):
        if not any(len(tok) == 4 and tok.isdigit() for tok in s_low.replace("/", " ").replace("-", " ").split()):
            return pd.NaT
    for suf in ["st", "nd", "rd", "th"]:
        s = s.replace(f"{suf} ", " ")
    try:
        if pd.notna(s) and len(s) == 10 and s[4] == '-' and s[7] == '-':
            y, m, d = s.split('-')
            return datetime(int(y), int(m), int(d))
    except Exception:
        pass
    try:
        if "/" in s and len(s.split("/")) == 3:
            a, b, c = s.split("/")
            if a.isdigit() and b.isdigit() and int(b) > 12:
                return parser.parse(s, dayfirst=False)
    except Exception:
        pass
    try:
        return parser.parse(s, dayfirst=True)
    except Exception:
        try:
            return parser.parse(s, dayfirst=False)
        except Exception:
            return pd.NaT


def _parse_time(tstr: str) -> tuple[datetime | pd.NaT, bool]:
    if pd.isna(tstr) or str(tstr).strip() == "":
        return (pd.NaT, False)
    s = str(tstr).strip().lower()
    s = s.replace(".", ":").replace(" ", "")
    if s == "2400":
        return (datetime(2000, 1, 1, 0, 0, 0), True)
    if s.isdigit() and len(s) in (3, 4):
        if len(s) == 3:
            h = int(s[0])
            m = int(s[1:])
        else:
            h = int(s[:2])
            m = int(s[2:])
        h = h % 24
        m = m % 60
        return (datetime(2000, 1, 1, h, m, 0), False)
    try:
        dt = parser.parse(s)
        return (datetime(2000, 1, 1, dt.hour, dt.minute, dt.second), False)
    except Exception:
        try:
            parts = s.split(":")
            h = int(parts[0])
            m = int(parts[1]) if len(parts) > 1 else 0
            return (datetime(2000, 1, 1, h % 24, m % 60, 0), False)
        except Exception:
            return (pd.NaT, False)


def _calc_age(dob_str: str) -> float | None:
    if pd.isna(dob_str) or str(dob_str).strip() == "":
        return None
    dob = _parse_date(dob_str)
    if pd.isna(dob):
        return None
    ref = datetime(2020, 1, 22)
    years = ref.year - dob.year
    return years


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    src = pd.read_csv(inputs_dir / "input_01.csv")

    src["Question Number"] = src["Question Number"].astype(str)

    keep_cols = ["Country", "Store", "Name", "DoB", "Response"]
    base = src.sort_values(["Response"]).drop_duplicates(
        ["Response"], keep="first")[keep_cols]

    qm = src.pivot_table(
        index="Response", columns="Question Number", values="Answer", aggfunc="first")
    qm = qm.rename(columns={
        "1": "date_str",
        "2": "time_str",
        "3": "nps",
        "3a": "pos_reason",
        "3b": "neg_reason",
    })

    df = base.set_index("Response").join(qm, how="left").reset_index()

    df["Country"] = df["Country"].apply(_clean_country)
    df["Store"] = df.apply(lambda r: _clean_store(
        r["Country"], r["Store"]), axis=1)

    parsed_dates = df["date_str"].apply(_parse_date)
    times_parsed = df["time_str"].apply(_parse_time)
    time_vals = [tp[0] for tp in times_parsed]
    rolled_flags = [tp[1] for tp in times_parsed]

    comp_dt = []
    for d, t, rolled in zip(parsed_dates, time_vals, rolled_flags):
        if pd.isna(d) or pd.isna(t):
            comp_dt.append(pd.NaT)
            continue
        combined = datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
        if rolled:
            combined = combined + timedelta(days=1)
        comp_dt.append(combined)
    df["CompletionDT"] = comp_dt

    def to_int_safe(x):
        try:
            return int(float(x))
        except Exception:
            return np.nan
    df["NPS"] = df["nps"].apply(to_int_safe)

    df["Age"] = df["DoB"].apply(_calc_age)

    df["Promoter"] = np.where(df["NPS"].between(
        9, 10, inclusive="both"), 1, np.nan)
    df["Passive"] = np.where(df["NPS"].between(
        7, 8, inclusive="both"), 1, np.nan)
    df["Detractor"] = np.where(df["NPS"].between(
        0, 6, inclusive="both"), 1, np.nan)

    grp_keys = ["Country", "Store", "Name"]
    df_valid = df.dropna(subset=["CompletionDT"]).copy()

    grp = df_valid.groupby(grp_keys)
    first_idx = grp["CompletionDT"].idxmin()
    latest_idx = grp["CompletionDT"].idxmax()

    sel_set = set(first_idx.tolist()) | set(latest_idx.tolist())

    out = df_valid.loc[sorted(sel_set)].copy()

    out["Result (First / Latest)"] = "First"
    kept_grp = out.groupby(grp_keys).apply(lambda x: x.index.tolist())
    for key, idxs in kept_grp.items():
        if len(idxs) >= 2:
            idx_latest_kept = out.loc[idxs, "CompletionDT"].idxmax()
            out.loc[idx_latest_kept, "Result (First / Latest)"] = "Latest"

    out_sorted = out.copy()

    out_sorted["Completion Date (Date Time stamp)"] = out_sorted["CompletionDT"].dt.strftime(
        "%d/%m/%Y %H:%M:%S")

    out_sorted["Would you recommend C&BS Co to your friends and family?"] = out_sorted["NPS"].astype(
        "Int64")

    out_sorted["Age of Customer"] = out_sorted["Age"].astype("Int64")

    final_cols = [
        "Country",
        "Store",
        "Name",
        "Completion Date (Date Time stamp)",
        "Result (First / Latest)",
        "Would you recommend C&BS Co to your friends and family?",
        "Promoter",
        "Passive",
        "Detractor",
        "Age of Customer",
        "pos_reason",
        "neg_reason",
    ]
    out_sorted = out_sorted.rename(columns={
        "pos_reason": "If you would, why?",
        "neg_reason": "If you wouldn't, why?",
    })

    final_cols = [
        "Country",
        "Store",
        "Name",
        "Completion Date (Date Time stamp)",
        "Result (First / Latest)",
        "Would you recommend C&BS Co to your friends and family?",
        "Promoter",
        "Passive",
        "Detractor",
        "Age of Customer",
        "If you would, why?",
        "If you wouldn't, why?",
    ]

    out_sorted = out_sorted.sort_values(
        ["Country", "Store", "Name", "CompletionDT", "Result (First / Latest)"]).reset_index(drop=True)

    for col in ["Promoter", "Passive", "Detractor"]:
        out_sorted[col] = out_sorted[col].astype("Int64")

    result = out_sorted[final_cols].copy()

    return {"output_01.csv": result}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for fname, df in outputs.items():
        (cand_dir / fname).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / fname, index=False, encoding="utf-8")
