from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

import pandas as pd
from dateutil import parser


ORDINAL_RE = re.compile(r"(\d+)(st|nd|rd|th)", flags=re.IGNORECASE)
MONTH_YEAR_ONLY_RE = re.compile(r"^[A-Za-z]+-\d{2}$", flags=re.IGNORECASE)
YEAR_TOKEN_RE = re.compile(r"(\d{2,4})(?!.*\d)")
PM_REMAP = {"Winston Churchill": "Sir Winston Churchill"}
MATCH_COMPETITIONS = {"League", "League Cup", "F.A. Cup", "Europe"}


def _strip_ordinals(value: str) -> str:
    return ORDINAL_RE.sub(r"\1", value)


def _split_duration(text: str) -> tuple[str, str]:
    normalized = (
        text.replace("–", "-")
        .replace("—", "-")
        .replace("  ", " ")
        .strip()
    )
    parts = normalized.split("-", 1)
    if len(parts) == 1:
        return parts[0].strip(), ""
    return parts[0].strip(), parts[1].strip()


def _parse_date(text: str, *, today: pd.Timestamp | None = None) -> pd.Timestamp | pd.NaT:
    if pd.isna(text):
        return pd.NaT
    stripped = _strip_ordinals(str(text)).strip()
    if not stripped:
        return pd.NaT
    if stripped.lower() == "present":
        return today
    parsed = pd.to_datetime(stripped, dayfirst=True, errors="coerce")
    if pd.isna(parsed):
        try:
            parsed = parser.parse(
                stripped, dayfirst=True, yearfirst=False, default=datetime(1900, 1, 1)
            )
        except (parser.ParserError, ValueError, TypeError, OverflowError):
            return pd.NaT
        return pd.Timestamp(parsed.date())
    return pd.Timestamp(parsed)


def _expand_ranges(rows: pd.DataFrame, start_col: str, end_col: str, new_col: str) -> pd.DataFrame:
    expanded_frames: list[pd.DataFrame] = []
    for _, record in rows.iterrows():
        start: pd.Timestamp = record[start_col]
        end: pd.Timestamp = record[end_col]
        if pd.isna(start) or pd.isna(end) or end < start:
            continue
        expanded = pd.DataFrame(
            {
                start_col: start,
                end_col: end,
                new_col: pd.date_range(start, end, freq="D"),
            }
        )
        for col in rows.columns:
            if col in (start_col, end_col):
                continue
            expanded[col] = record[col]
        expanded_frames.append(expanded)
    if not expanded_frames:
        return pd.DataFrame(columns=[*rows.columns, new_col])
    return pd.concat(expanded_frames, ignore_index=True)


def _prepare_matches(matches_path: Path) -> tuple[pd.DataFrame, pd.Timestamp]:
    matches = pd.read_csv(matches_path)
    matches = matches[matches["Comp"].isin(MATCH_COMPETITIONS)].copy()
    matches["Match Date"] = matches["Date"].apply(
        lambda x: pd.to_datetime(
            _strip_ordinals(str(x)).strip(), dayfirst=True, errors="coerce"
        )
    )
    matches = matches.dropna(subset=["Match Date"])
    max_date = matches["Match Date"].max()

    daily_counts = (
        matches.groupby(["Match Date", "Result"]).size().unstack(fill_value=0)
    )
    for col in ["Match Won", "Match Drawn", "Match Lost"]:
        if col not in daily_counts:
            daily_counts[col] = 0
    daily_counts = daily_counts[["Match Won", "Match Drawn", "Match Lost"]]
    daily_counts = daily_counts.rename(
        columns={
            "Match Won": "Matches Won",
            "Match Drawn": "Matches Drawn",
            "Match Lost": "Matches Lost",
        }
    )
    daily_counts["Matches"] = daily_counts.sum(axis=1)
    daily_counts = daily_counts.reset_index().rename(
        columns={"Match Date": "Date"})
    return daily_counts, max_date


def _extract_year_token(text: str) -> str | None:
    match = YEAR_TOKEN_RE.search(text)
    return match.group(1) if match else None


def _prepare_manager_date_text(text: str | float | None) -> str:
    if pd.isna(text):
        return ""
    cleaned = _strip_ordinals(str(text)).strip()
    cleaned = cleaned.replace("Sept", "Sep")
    if MONTH_YEAR_ONLY_RE.match(cleaned):
        cleaned = f"1-{cleaned}"
    return cleaned


def _resolve_start_year(
    token: str | None, current_century: int, last_year: int, fallback_year: int
) -> tuple[int, int]:
    if token is None:
        year_full = fallback_year
    elif len(token) == 4:
        year_full = int(token)
    else:
        year_two = int(token)
        candidate = current_century + year_two
        if last_year and candidate < last_year:
            candidate += 100
        year_full = candidate
    century = (year_full // 100) * 100
    return year_full, century


def _parse_manager_periods(managers_path: Path, today: pd.Timestamp) -> pd.DataFrame:
    managers = pd.read_csv(managers_path)
    managers["Chelsea Managers"] = managers["Name"].str.split(
        "[", n=1).str[0].str.strip()

    current_century = 1900
    last_start_year = 0
    start_dates: list[pd.Timestamp] = []
    end_dates: list[pd.Timestamp] = []

    for _, row in managers.iterrows():
        start_text = _prepare_manager_date_text(row["From"])
        end_text_raw = row["To"]

        start_dt = pd.to_datetime(start_text, dayfirst=True, errors="coerce")
        if pd.isna(start_dt):
            start_dates.append(pd.NaT)
            end_dates.append(pd.NaT)
            continue
        start_token = _extract_year_token(start_text)
        start_year, current_century = _resolve_start_year(
            start_token, current_century, last_start_year, start_dt.year
        )
        start_dt = start_dt.replace(year=start_year)
        last_start_year = start_year

        if isinstance(end_text_raw, str) and end_text_raw.strip().lower() == "present":
            end_dt = today
        elif pd.isna(end_text_raw):
            end_dt = today
        else:
            end_text = _prepare_manager_date_text(end_text_raw)
            end_token = _extract_year_token(end_text)
            end_dt = pd.to_datetime(end_text, dayfirst=True, errors="coerce")
            if pd.isna(end_dt):
                end_dt = today
            else:
                if end_token and len(end_token) == 2:
                    base_century = (start_year // 100) * 100
                    year_full = base_century + int(end_token)
                    if year_full < start_year:
                        year_full += 100
                elif end_token:
                    year_full = int(end_token)
                else:
                    year_full = end_dt.year
                end_dt = end_dt.replace(year=year_full)

        start_dates.append(pd.Timestamp(start_dt))
        end_dates.append(pd.Timestamp(end_dt))

    managers["Start Date CM"] = start_dates
    managers["End Date CM"] = end_dates
    return managers[["Chelsea Managers", "Start Date CM", "End Date CM"]]


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    matches_daily, max_match_date = _prepare_matches(
        inputs_dir / "input_03.csv")
    today = max_match_date + pd.Timedelta(days=1)

    prime_ministers = pd.read_csv(inputs_dir / "input_01.csv")
    prime_ministers["Prime Ministers"] = prime_ministers["Prime Ministers"].replace(
        PM_REMAP)
    start_text, end_text = zip(
        *prime_ministers["Duration"].map(_split_duration))
    prime_ministers["Start Date PM"] = [
        _parse_date(value, today=today) for value in start_text
    ]
    prime_ministers["End Date PM"] = [
        _parse_date(value, today=today) for value in end_text
    ]
    prime_ministers["End Date PM"] = prime_ministers["End Date PM"].fillna(
        today)

    pm_days = _expand_ranges(
        prime_ministers[["Prime Ministers", "Start Date PM", "End Date PM"]],
        "Start Date PM",
        "End Date PM",
        "Date",
    )

    managers = _parse_manager_periods(inputs_dir / "input_02.csv", today)
    manager_days = _expand_ranges(
        managers[["Chelsea Managers", "Start Date CM", "End Date CM"]],
        "Start Date CM",
        "End Date CM",
        "Date",
    )[["Chelsea Managers", "Date"]]

    manager_match_days = manager_days.merge(
        matches_daily, on="Date", how="left")
    match_cols = ["Matches", "Matches Won", "Matches Drawn", "Matches Lost"]
    manager_match_days[match_cols] = manager_match_days[match_cols].fillna(0)

    combined = pm_days.merge(
        manager_match_days[["Date", "Chelsea Managers", *match_cols]],
        on="Date",
        how="inner",
    )
    grouped = (
        combined.groupby(["Prime Ministers", "Start Date PM", "End Date PM"], as_index=False).agg(
            Chelsea_Managers=("Chelsea Managers", "nunique"),
            Matches=("Matches", "sum"),
            Matches_Won=("Matches Won", "sum"),
            Matches_Drawn=("Matches Drawn", "sum"),
            Matches_Lost=("Matches Lost", "sum"),
        )
    )

    result = grouped.rename(
        columns={
            "Chelsea_Managers": "Chelsea Managers",
            "Matches_Won": "Matches Won",
            "Matches_Drawn": "Matches Drawn",
            "Matches_Lost": "Matches Lost",
        }
    )
    result[["Matches Drawn", "Matches Lost"]] = result[[
        "Matches Lost", "Matches Drawn"]].to_numpy()
    for col in ["Chelsea Managers", *match_cols]:
        result[col] = result[col].fillna(0).astype(int)
    win_pct = (result["Matches Won"] / result["Matches"]).round(2)
    win_pct = win_pct.where(result["Matches"] > 0)
    result["Win %"] = win_pct

    result = result[
        [
            "Prime Ministers",
            "Start Date PM",
            "End Date PM",
            "Chelsea Managers",
            "Matches",
            "Matches Won",
            "Matches Drawn",
            "Matches Lost",
            "Win %",
        ]
    ]
    result = result.sort_values(["Start Date PM", "Prime Ministers"], ascending=[
                                True, True]).reset_index(drop=True)
    for col in ["Start Date PM", "End Date PM"]:
        result[col] = pd.to_datetime(result[col]).dt.strftime("%d/%m/%Y")

    return {"output_01.csv": result}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        (cand_dir / filename).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(cand_dir / filename, index=False, encoding="utf-8")
