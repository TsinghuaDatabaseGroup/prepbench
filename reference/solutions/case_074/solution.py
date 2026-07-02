import pandas as pd
from pathlib import Path


def roman_to_int(roman: str) -> int:
    roman_dict = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }

    result = 0
    prev_value = 0

    for char in reversed(roman):
        value = roman_dict.get(char, 0)
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value

    return result


def parse_dates(date_str: str, year: int) -> tuple[str, str]:
    if pd.isna(date_str):
        return None, None

    date_str = date_str.strip()
    if not date_str:
        return None, None

    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12,
    }

    if '–' not in date_str:
        return None, None

    start_part, end_part = [p.strip() for p in date_str.split('–', 1)]

    if ' ' in start_part:
        start_day_str, start_month_name = start_part.split(None, 1)
        start_day = int(start_day_str)
    else:
        start_day = int(start_part)
        start_month_name = end_part.split()[-1]

    start_month = month_map[start_month_name]

    end_day_str, end_month_name = end_part.split(None, 1)
    end_day = int(end_day_str)
    end_month = month_map[end_month_name]

    start_date = f"{start_month}/{start_day}/{year}"
    end_date = f"{end_month}/{end_day}/{year}"

    return start_date, end_date


def solve(inputs_dir: Path) -> dict[str, pd.DataFrame]:
    df = pd.read_csv(inputs_dir / "input_01.csv")

    df['Game_Number'] = df['Games'].apply(roman_to_int)

    df['Year'] = 1896 + (df['Game_Number'] - 1) * 4

    date_results = df.apply(lambda row: parse_dates(
        row['Dates'], row['Year']), axis=1)
    df['Start Date'] = date_results.apply(lambda x: x[0] if x[0] else None)
    df['End Date'] = date_results.apply(lambda x: x[1] if x[1] else None)

    df = df[df['Start Date'].notna() & df['End Date'].notna()].copy()

    result = df[[
        'Start Date', 'End Date', 'Games', 'Host', 'Nations', 'Sports', 'Events'
    ]].copy()

    result['Nations'] = result['Nations'].astype(float).astype(int)
    result['Sports'] = result['Sports'].astype(float).astype(int)
    result['Events'] = result['Events'].astype(float).astype(int)

    result = result.reset_index(drop=True)

    return {
        "output_01.csv": result
    }


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(parents=True, exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False, encoding='utf-8')
