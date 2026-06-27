from typing import Any, List
from .base import register, is_empty_token
import re

_CLEAN_RE = re.compile(r"[,$%]\s*")


def _num_norm(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if is_empty_token(v):
            out.append(None)
            continue
        s = str(v).strip().lower()
        s = _CLEAN_RE.sub("", s)
        try:
            n = float(s)
            out.append(n)
        except Exception:
            out.append(None)
    return out


register("number", _num_norm)
