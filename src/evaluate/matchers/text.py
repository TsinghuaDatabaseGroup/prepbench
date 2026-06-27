from typing import Any, List
from .base import register, is_empty_token
import re

_WHITESPACE_RE = re.compile(r"\s+")

def _remove_quotes(s: str) -> str:
    """Remove leading and trailing quotes if present"""
    s = s.strip()
    if len(s) >= 2:
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
    return s


def _normalize_empty(value: str) -> Any:
    v = value
    if v is None:
        return None
    s = str(v)
    s = _remove_quotes(s)
    if is_empty_token(s):
        return None
    return s


def _text_exact(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if v is None:
            out.append(None)
            continue
        v2 = _normalize_empty(v)
        out.append(v2)
    return out


def _text_norm(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if v is None:
            out.append(None)
            continue
        s = str(v)
        s = _remove_quotes(s)
        if is_empty_token(s):
            out.append(None)
            continue
        s = s.strip().lower()
        s = _WHITESPACE_RE.sub(" ", s)
        out.append(s)
    return out


# register on import
register("text_exact", _text_exact)
register("text_norm", _text_norm)
