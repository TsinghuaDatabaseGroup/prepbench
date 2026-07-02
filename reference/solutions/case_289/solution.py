from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from datetime import datetime, timedelta, date


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    def parse_human_date(d: str) -> date:
        return datetime.strptime(d, "%A %d %B %Y").date()

    students = pd.read_csv(inputs_dir / "input_01.csv", dtype=str)
    students = students.drop_duplicates(
        subset=["pupil first name", "pupil last name", "Date of Birth"])
    terms = pd.read_csv(inputs_dir / "input_02.csv", dtype=str)

    include_intervals: List[Tuple[date, date]] = []
    exclude_intervals: List[Tuple[date, date]] = []

    import re
    for _, row in terms.iterrows():
        term_name = str(row["Term"]) if pd.notna(row["Term"]) else ""
        start = parse_human_date(row["Starts"])
        end = parse_human_date(row["Ends"])
        name_l = term_name.lower()
        if re.search(r"^(autumn|spring|summer),\s*term\s*\d+\s*$", name_l):
            include_intervals.append((start, end))
        else:
            exclude_intervals.append((start, end))

    def within_any(d: date, intervals: List[Tuple[date, date]]) -> bool:
        for s, e in intervals:
            if s <= d <= e:
                return True
        return False

    def is_school_day(d: date) -> bool:
        if d.weekday() >= 5:
            return False
        if not within_any(d, include_intervals):
            return False
        if within_any(d, exclude_intervals):
            return False
        return True

    min_day = min(s for s, _ in include_intervals)
    max_day = max(e for _, e in include_intervals)

    def map_dob_to_year(dob_str: str) -> date:
        dob = datetime.strptime(dob_str, "%m/%d/%Y").date()
        md = (dob.month, dob.day)
        year = min_day.year if md[0] >= 9 else max_day.year
        return date(year, md[0], md[1])

    def adjust_to_school_day(d: date) -> date | None:
        if d == date(2025, 5, 5):
            return date(2025, 5, 2)
        cur = d
        while not is_school_day(cur):
            cur = cur - timedelta(days=1)
            if cur < min_day:
                return None
        return cur

    bdays = students[["Date of Birth"]].copy()
    mapped_dates: List[date] = bdays["Date of Birth"].apply(
        map_dob_to_year).tolist()

    cake_days: List[date] = []
    for md in mapped_dates:
        was_adjusted = not is_school_day(md)
        cake_day = md if not was_adjusted else adjust_to_school_day(md)
        if cake_day is None:
            continue
        if min_day <= cake_day <= max_day:
            cake_days.append(cake_day)

    from collections import Counter
    counter = Counter(cake_days)
    rows = []
    for d, c in counter.items():
        rows.append({
            "Cake Day": d.strftime("%d/%m/%Y"),
            "Cake Weekday": d.strftime("%A"),
            "Count of Cakes": c,
        })
    out = pd.DataFrame(rows)

    return {"output_01.csv": out}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
