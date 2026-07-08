from __future__ import annotations
from pathlib import Path
from typing import Dict, List
import pandas as pd
import numpy as np


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    guests = pd.read_csv(inputs_dir / "input_01.csv")
    rooms = pd.read_csv(inputs_dir / "input_02.csv")

    guests = guests.copy()
    guests["Additional Requests"] = guests["Additional Requests"].replace({"N/A": np.nan})

    guests["Adults"] = guests["Adults"].fillna(0).astype(int)
    guests["Children"] = guests["Children"].fillna(0).astype(int)

    def map_bool(x: str) -> bool:
        if pd.isna(x):
            return False
        s = str(x).strip().upper()
        if s in ("Y", "YES", "TRUE", "T", "1"):
            return True
        return False

    guests["Requires Accessible Room?"] = guests["Requires Accessible Room?"].map(map_bool)

    def parse_requests(val: object) -> List[str]:
        if pd.isna(val) or str(val).strip() == "":
            return []
        parts = [p.strip() for p in str(val).split(",")]
        parts = [p for p in parts if p != ""]
        return parts

    guests["_requests_list"] = guests["Additional Requests"].apply(parse_requests)
    guests["_requests_cnt"] = guests["_requests_list"].apply(len)

    rooms = rooms.copy()
    rooms["Adults"] = rooms["Adults"].fillna(0).astype(int)
    rooms["Children"] = rooms["Children"].fillna(0).astype(int)
    rooms["_features_text"] = rooms["Features"].astype(str)

    def parse_features(val: object) -> set:
        if pd.isna(val) or str(val).strip() == "":
            return set()
        return set([p.strip() for p in str(val).split(",")])

    rooms["_features_set"] = rooms["Features"].apply(parse_features)

    def bed_ok(guest_bed: str, features: set) -> bool:
        gb = str(guest_bed).strip()
        return gb in features

    def accessible_ok(need_access: bool, features: set) -> bool:
        if not need_access:
            return True
        return "Accessible" in features

    def capacity_ok(g_adults: int, g_children: int, r_adults: int, r_children: int) -> bool:
        return (r_adults >= g_adults) and (r_children >= g_children)

    def satisfied_requests(reqs: List[str], features: set) -> int:
        sat = 0
        for r in reqs:
            if r == "Bath":
                if "Bath" in features:
                    sat += 1
            elif r == "High Floor":
                if "High Floor" in features:
                    sat += 1
            elif r == "Near to lift":
                if "Near to lift" in features:
                    sat += 1
            elif r == "NOT Near to lift":
                if "Near to lift" not in features:
                    sat += 1
            else:
                pass
        return sat

    guests_exp = guests.assign(_tmp=1)
    rooms_exp = rooms.assign(_tmp=1)
    cross = guests_exp.merge(rooms_exp, on="_tmp", suffixes=("_g", "_r"))

    mask_capacity = cross.apply(
        lambda x: capacity_ok(x["Adults_g"], x["Children_g"], x["Adults_r"], x["Children_r"]), axis=1
    )
    mask_bed = cross.apply(lambda x: bed_ok(x["Double/Twin"], x["_features_set"]), axis=1)
    mask_access = cross.apply(lambda x: accessible_ok(x["Requires Accessible Room?"], x["_features_set"]), axis=1)

    filt = cross[mask_capacity & mask_bed & mask_access].copy()

    sats = filt.apply(lambda x: satisfied_requests(x["_requests_list"], x["_features_set"]), axis=1)
    total = filt["_requests_cnt"]
    pct = np.where(total == 0, 100, (sats / total * 100))
    filt["Request Satisfaction %"] = np.round(pct, 0).astype(int)

    filt["_max_pct"] = filt.groupby(["Party"])['Request Satisfaction %'].transform('max')
    filt = filt[filt["Request Satisfaction %"] == filt["_max_pct"]].copy()

    filt = filt[~((filt["Adults_r"] >= 4) & (filt["Adults_g"] <= 2))].copy()

    out = pd.DataFrame({
        "Party": filt["Party"],
        "Adults in Party": filt["Adults_g"].astype(int),
        "Children in Party": filt["Children_g"].astype(int),
        "Double/Twin": filt["Double/Twin"].astype(str),
        "Requires Accessible Room?": filt["Requires Accessible Room?"].astype(bool),
        "Additional Requests": filt["Additional Requests"],
        "Request Satisfaction %": filt["Request Satisfaction %"].astype(int),
        "Room": filt["Room"].astype(int),
        "Adults": filt["Adults_r"].astype(int),
        "Children": filt["Children_r"].astype(int),
        "Features": filt["_features_text"].astype(str),
    })

    out = out.sort_values(["Party", "Room"]).reset_index(drop=True)

    return {"output_01.csv": out}


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
