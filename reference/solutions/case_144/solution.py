from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Dict, List, Tuple


def _parse_time_to_minutes(t: str) -> int:
    t = str(t).strip()
    if t.isdigit():
        return int(t) * 60
    parts = t.split(":")
    if len(parts) >= 2:
        try:
            h = int(parts[0])
            m = int(parts[1])
            return h * 60 + m
        except ValueError:
            pass
    try:
        dt = pd.to_datetime(t, errors="coerce")
        if pd.isna(dt):
            return 0
        return dt.hour * 60 + dt.minute
    except Exception:
        return 0


def _explode_attendees(df: pd.DataFrame) -> pd.DataFrame:
    def split_ids(s: str) -> List[int]:
        if pd.isna(s):
            return []
        return [int(x.strip()) for x in str(s).split(',') if str(x).strip()]

    df = df.copy()
    df["AttendeeList"] = df["Attendee IDs"].apply(split_ids)
    df = df.explode("AttendeeList")
    df = df.rename(columns={"AttendeeList": "AttendeeID"})
    df["AttendeeID"] = df["AttendeeID"].astype(int)
    return df


def _session_pairs(att_ids: List[int]) -> List[Tuple[int, int]]:
    pairs = []
    n = len(att_ids)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a = att_ids[i]
            b = att_ids[j]
            if a != b:
                pairs.append((a, b))
    return pairs


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    input_files = [
        inputs_dir / "input_01.csv",
        inputs_dir / "input_02.csv",
        inputs_dir / "input_03.csv",
    ]
    sessions = []
    for day_idx, f in enumerate(input_files, start=1):
        df = pd.read_csv(f)
        df = df.rename(columns={
            "Session ID": "SessionID",
            "Session Time": "SessionTime",
        })
        df["Day"] = day_idx
        df["TimeMinutes"] = df["SessionTime"].apply(_parse_time_to_minutes)
        sessions.append(df)
    sessions_df = pd.concat(sessions, ignore_index=True)

    lookup = pd.read_csv(inputs_dir / "input_04.csv")
    lookup = lookup.rename(columns={"Attendee ID": "AttendeeID"})

    sessions_df["OrderKey"] = list(zip(sessions_df["Day"], sessions_df["TimeMinutes"], sessions_df["SessionID"]))
    sessions_df = sessions_df.sort_values(["Day", "TimeMinutes", "SessionID"]).reset_index(drop=True)

    results_rows: List[Tuple[str, int, str, int]] = []

    for subject, sub_df in sessions_df.groupby("Subject", sort=False):
        prior_direct: dict[int, set[int]] = {}
        final_direct: dict[int, set[int]] = {}
        final_indirect: dict[int, set[int]] = {}

        sub_df = sub_df.sort_values(["Day", "TimeMinutes", "SessionID"])
        for _, row in sub_df.iterrows():
            att_ids = [int(x.strip()) for x in str(row["Attendee IDs"]).split(',') if str(x).strip()]

            direct_add_for: dict[int, set[int]] = {}
            for a, b in _session_pairs(att_ids):
                direct_add_for.setdefault(a, set()).add(b)

            indirect_add_for: dict[int, set[int]] = {}
            for a in att_ids:
                candidates: set[int] = set()
                for other in direct_add_for.get(a, set()):
                    candidates |= prior_direct.get(other, set())
                candidates.discard(a)
                candidates -= direct_add_for.get(a, set())
                candidates -= final_direct.get(a, set())
                if candidates:
                    indirect_add_for.setdefault(a, set()).update(candidates)

            for a, ds in direct_add_for.items():
                if not ds:
                    continue
                final_direct.setdefault(a, set()).update(ds)
            for a, inds in indirect_add_for.items():
                if not inds:
                    continue
                inds = inds - final_direct.get(a, set())
                if inds:
                    final_indirect.setdefault(a, set()).update(inds)

            for a, ds in direct_add_for.items():
                if not ds:
                    continue
                prior_direct.setdefault(a, set()).update(ds)

        for a, ds in final_direct.items():
            for b in sorted(ds):
                results_rows.append((subject, a, "Direct Contact", b))
        for a, inds in final_indirect.items():
            remain = inds - final_direct.get(a, set())
            for b in sorted(remain):
                results_rows.append((subject, a, "Indirect Contact", b))

    name_map = dict(zip(lookup["AttendeeID"], lookup["Attendee"]))
    out_df = pd.DataFrame(results_rows, columns=["Subject", "AttendeeID", "Contact Type", "ContactID"])
    out_df["Attendee"] = out_df["AttendeeID"].map(name_map)
    out_df["Contact"] = out_df["ContactID"].map(name_map)
    out_df = out_df.drop(columns=["AttendeeID", "ContactID"])

    out_df = out_df.dropna(subset=["Attendee", "Contact"]).copy()

    out_df = out_df[out_df["Attendee"] != out_df["Contact"]]
    out_df = out_df.drop_duplicates(subset=["Subject", "Attendee", "Contact Type", "Contact"], keep="first")

    out_df = out_df.sort_values(["Subject", "Attendee", "Contact Type", "Contact"]).reset_index(drop=True)

    return {"output_01.csv": out_df}


if __name__ == "__main__":
    import sys
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        out_path = cand_dir / filename
        df.to_csv(out_path, index=False, encoding="utf-8")
    for k, v in outputs.items():
        print(f"Wrote {k}: {len(v)} rows")

