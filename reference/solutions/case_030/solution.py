from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

import pandas as pd


WATER_F_RE = re.compile(r"Water\s*-\s*([-\d.]+)F", re.IGNORECASE | re.DOTALL)
WATER_C_RE = re.compile(
    r"Water\s*-\s*[-\d.]+F\s*/\s*([-\d.]+)C", re.IGNORECASE | re.DOTALL
)
AIR_F_RE = re.compile(r"Air\s*-\s*([-\d.]+)F", re.IGNORECASE | re.DOTALL)
AIR_C_RE = re.compile(
    r"Air\s*-\s*[-\d.]+F\s*/\s*([-\d.]+)C", re.IGNORECASE | re.DOTALL
)
COMMENT_PREFIX_RE = re.compile(r"^.*?C\.(?:\s+|$)", re.IGNORECASE | re.DOTALL)
NON_WORD_PATTERN = r"[^\w\s]+"
NON_WORD_RE = re.compile(NON_WORD_PATTERN)
MAX_TOKENS = 25


def _read_common_words(path: Path) -> set[str]:
    common_df = pd.read_csv(path, dtype={"Rank": "Int64", "Word": "string"})
    cleaned = (
        common_df["Word"]
        .fillna("")
        .str.lower()
        .str.replace(NON_WORD_PATTERN, "", regex=True)
        .str.strip()
    )
    return {word for word in cleaned.tolist() if word}


def _clean_comment(text: str) -> tuple[str, list[str]]:
    normalized = text.replace("\r", " ").replace("\n", " ")
    match = COMMENT_PREFIX_RE.match(normalized)
    comment_body = normalized[match.end():] if match else normalized
    comment_body = comment_body.strip()

    lowercase = comment_body.lower()
    tokens = NON_WORD_RE.sub(" ", lowercase).split()
    return comment_body, tokens


def _extract_temperature(pattern: re.Pattern, text: str) -> float | None:
    match = pattern.search(text)
    if not match:
        return None
    return float(match.group(1))


def _parse_temperatures(text: str) -> dict[str, float | None]:
    return {
        "Water TempF": _extract_temperature(WATER_F_RE, text),
        "Water TempC": _extract_temperature(WATER_C_RE, text),
        "Air TempF": _extract_temperature(AIR_F_RE, text),
        "Air TempC": _extract_temperature(AIR_C_RE, text),
    }


def _filter_tokens(tokens: list[str], stopwords: set[str]) -> list[str]:
    filtered: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        if token in stopwords or not token or token in seen:
            continue
        seen.add(token)
        filtered.append(token)
        if len(filtered) >= MAX_TOKENS:
            break
    return filtered


def solve(inputs_dir: Path) -> Dict[str, pd.DataFrame]:
    tweets_path = inputs_dir / "input_02.csv"
    common_words_path = inputs_dir / "input_01.csv"

    common_words = _read_common_words(common_words_path)

    tweets = pd.read_csv(
        tweets_path,
        usecols=["Tweet Id", "Text", "Created At"],
        dtype=str,
        keep_default_na=False,
    )
    has_water = tweets["Text"].str.contains(
        r"Water\s*-\s*\d", case=False, na=False, regex=True)
    has_air = tweets["Text"].str.contains(
        r"Air\s*-\s*\d", case=False, na=False, regex=True)
    tweets = tweets.loc[has_water & has_air].reset_index(drop=True)

    temperature_data = tweets["Text"].apply(
        _parse_temperatures).apply(pd.Series)
    tweets = (
        pd.concat([tweets, temperature_data], axis=1)
        .dropna(subset=["Water TempF", "Water TempC", "Air TempF", "Air TempC"])
    )

    tweets["Created At"] = (
        pd.to_datetime(
            tweets["Created At"],
            format="%a %b %d %H:%M:%S %z %Y",
            utc=True,
            errors="coerce",
        )
        .dt.tz_convert(None)
        .dt.strftime("%d/%m/%Y %H:%M:%S")
    )

    comment_token_df = pd.DataFrame(
        tweets["Text"].apply(_clean_comment).tolist(),
        columns=["Comment", "Tokens"],
    )
    comment_token_df["Tokens"] = comment_token_df["Tokens"].apply(
        lambda tokens: _filter_tokens(tokens, common_words)
    )
    tweets = tweets.join(comment_token_df)
    tweets = tweets.loc[tweets["Tokens"].apply(len) > 0]

    exploded = tweets.explode("Tokens")
    stacked = pd.concat(
        [
            exploded.assign(
                Category="Water",
                TempF=exploded["Water TempF"],
                TempC=exploded["Water TempC"],
            ),
            exploded.assign(
                Category="Air",
                TempF=exploded["Air TempF"],
                TempC=exploded["Air TempC"],
            ),
        ],
        ignore_index=True,
    )

    result_df = stacked.rename(columns={"Tokens": "Comment Split"})[
        [
            "Comment Split",
            "Category",
            "TempF",
            "TempC",
            "Comment",
            "Tweet Id",
            "Created At",
        ]
    ]

    return {"output_01.csv": result_df}


if __name__ == "__main__":
    task_dir = Path(__file__).parent
    inputs_dir = task_dir / "inputs"
    cand_dir = task_dir / "cand"
    cand_dir.mkdir(exist_ok=True)

    outputs = solve(inputs_dir)
    for filename, df in outputs.items():
        df.to_csv(cand_dir / filename, index=False)
