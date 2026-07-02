from __future__ import annotations

import pandas as pd
from pathlib import Path
from datetime import datetime
import re

YEAR = 2020
DAY_COUNT = 366


def _month_abbrev(month: int) -> str:
    return datetime(YEAR, month, 1).strftime("%b")


def _day_of_year(month: int, day: int) -> int:
    return datetime(YEAR, month, day).timetuple().tm_yday


def _range_contains(start_doy: int, end_doy: int, target_doy: int) -> bool:
    if start_doy <= end_doy:
        return start_doy <= target_doy <= end_doy
    return target_doy >= start_doy or target_doy <= end_doy


def _distance_from_start(start_doy: int, target_doy: int) -> int:
    return (target_doy - start_doy) % DAY_COUNT


def _parse_new_system(path: Path) -> list[dict]:
    rows = pd.read_csv(path, header=None, names=["text"])
    pattern = re.compile(r"([^:]+):\s*(\w+)\s+(\d+)\s*[–-]\s*(\w+)\s+(\d+)", re.IGNORECASE)
    signs: list[dict] = []
    for idx, raw in rows["text"].dropna().items():
        text = raw.strip()
        if not text:
            continue
        match = pattern.match(text)
        if not match:
            continue
        sign = match.group(1).strip()
        start_month = datetime.strptime(match.group(2)[:3], "%b").month
        start_day = int(match.group(3))
        end_month = datetime.strptime(match.group(4)[:3], "%b").month
        end_day = int(match.group(5))
        start_doy = _day_of_year(start_month, start_day)
        end_doy = _day_of_year(end_month, end_day)
        signs.append(
            {
                "name": sign,
                "start_month": start_month,
                "start_day": start_day,
                "end_month": end_month,
                "end_day": end_day,
                "start_doy": start_doy,
                "end_doy": end_doy,
                "order": idx,
                "range_str": f"{start_day} {_month_abbrev(start_month)} - {end_day} {_month_abbrev(end_month)}",
            }
        )
    return signs


def _parse_old_system(path: Path) -> list[dict]:
    df = pd.read_csv(path, header=None)
    entries: list[dict] = []
    order = 0
    for _, row in df.iterrows():
        values = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip()]
        if not values:
            continue
        for i in range(0, len(values), 2):
            if i + 1 >= len(values):
                continue
            sign = values[i]
            range_raw = values[i + 1]
            range_clean = range_raw.replace("-", "–")
            match = re.match(r"(\d{1,2})/(\d{1,2})[–](\d{1,2})/(\d{1,2})", range_clean)
            if not match:
                continue
            start_month = int(match.group(1))
            start_day = int(match.group(2))
            end_month = int(match.group(3))
            end_day = int(match.group(4))
            start_doy = _day_of_year(start_month, start_day)
            end_doy = _day_of_year(end_month, end_day)
            entries.append(
                {
                    "name": sign,
                    "start_month": start_month,
                    "start_day": start_day,
                    "end_month": end_month,
                    "end_day": end_day,
                    "start_doy": start_doy,
                    "end_doy": end_doy,
                    "order": order,
                }
            )
            order += 1
    return entries


def _signs_for_day(sign_defs: list[dict], target_doy: int) -> list[dict]:
    matched = []
    for entry in sign_defs:
        if _range_contains(entry["start_doy"], entry["end_doy"], target_doy):
            distance = _distance_from_start(entry["start_doy"], target_doy)
            matched.append((distance, entry["order"], entry))
    matched.sort(key=lambda item: (item[0], item[1]))
    return [entry for _, _, entry in matched]


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    dates_raw = pd.read_csv(inputs_dir / "input_03.csv")
    dates_raw["Date"] = pd.to_datetime(dates_raw["Date"], format="%d/%m/%Y", errors="coerce")
    dates_2020 = dates_raw[dates_raw["Date"].dt.year == YEAR]["Date"].dropna().sort_values()

    old_system = _parse_old_system(inputs_dir / "input_02.csv")
    new_system = _parse_new_system(inputs_dir / "input_01.csv")

    records: list[dict] = []

    for current_date in dates_2020:
        doy = current_date.timetuple().tm_yday
        if current_date.month == 6 and current_date.day == 21:
            continue

        old_matches = _signs_for_day(old_system, doy)
        new_matches = _signs_for_day(new_system, doy)

        if not old_matches or not new_matches:
            continue
        old_set = {e["name"] for e in old_matches}
        new_set = {e["name"] for e in new_matches}
        if (len(old_set) == 1 and old_set.issubset(new_set)) or (len(new_set) == 1 and new_set.issubset(old_set)):
            continue

        pair_len = min(len(old_matches), len(new_matches))
        birthday = f"{current_date.strftime('%b')} {current_date.day}"

        if pair_len == 1:
            if len(old_matches) == 2 and len(new_matches) == 1:
                new_sign = new_matches[0]
                for old_sign in old_matches:
                    if old_sign["name"] != new_sign["name"]:
                        records.append(
                            {
                                "Birthday": birthday,
                                "Old Star Sign": old_sign["name"],
                                "New Star Sign": new_sign["name"],
                                "Date Range": new_sign["range_str"],
                            }
                        )
                continue
            if len(old_matches) == 1 and len(new_matches) == 2:
                old_sign = old_matches[0]
                for new_sign in new_matches:
                    if old_sign["name"] != new_sign["name"]:
                        records.append(
                            {
                                "Birthday": birthday,
                                "Old Star Sign": old_sign["name"],
                                "New Star Sign": new_sign["name"],
                                "Date Range": new_sign["range_str"],
                            }
                        )
                continue

        for idx in range(pair_len):
            old_sign = old_matches[idx]
            new_sign = new_matches[idx]

            if old_sign["name"] == new_sign["name"]:
                continue

            records.append(
                {
                    "Birthday": birthday,
                    "Old Star Sign": old_sign["name"],
                    "New Star Sign": new_sign["name"],
                    "Date Range": new_sign["range_str"],
                }
            )

    output = pd.DataFrame(records).drop_duplicates().reset_index(drop=True)

    if not output.empty:
        month_lookup = {m: idx for idx, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}
        output["__month"] = output["Birthday"].str.split().str[0].map(month_lookup)
        output["__day"] = output["Birthday"].str.split().str[1].astype(int)
        output = output.sort_values(["__month", "__day", "Old Star Sign", "New Star Sign"]).drop(columns=["__month", "__day"]).reset_index(drop=True)

    return {"output_01.csv": output}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")

