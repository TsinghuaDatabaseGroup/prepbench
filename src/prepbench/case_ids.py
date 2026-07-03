from __future__ import annotations

import re


_CASE_ID_RE = re.compile(r"case[_-]?(\d+)")


def case_index(value: str) -> int | None:
    token = str(value or "").strip().lower()
    if not token:
        return None
    match = _CASE_ID_RE.fullmatch(token)
    if match:
        return int(match.group(1))
    if token.isdigit():
        return int(token)
    return None


def case_index_text(value: str) -> str | None:
    idx = case_index(value)
    if idx is None:
        return None
    return f"{idx:03d}"


def normalize_case_id(value: str, *, passthrough: bool = False) -> str:
    token = str(value or "").strip().lower()
    if not token:
        raise ValueError("case_id must be a non-empty string")
    idx = case_index(token)
    if idx is None:
        if passthrough:
            return token
        raise ValueError(f"invalid case id: {value!r}")
    return f"case_{idx:03d}"
