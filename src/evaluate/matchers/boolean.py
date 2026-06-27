from typing import Any, List
from .base import register, is_empty_token

_TRUE_SET = {"true", "1", "yes", "y", "t", "是"}
_FALSE_SET = {"false", "0", "no", "n", "f", "否"}


def _bool_norm(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if is_empty_token(v):
            out.append(None)
            continue
        s = str(v).strip().lower()
        if s in _TRUE_SET:
            out.append(True)
        elif s in _FALSE_SET:
            out.append(False)
        else:
            raise ValueError(f"Unrecognized boolean value: {v!r}")
    return out


register("boolean", _bool_norm)
