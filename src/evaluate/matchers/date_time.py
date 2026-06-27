from typing import Any, List
from .base import register
from datetime import datetime

_EMPTY_VALUES = {"", "na", "n/a", "null"}
_DATE_FORMATS = [
    "%Y-%m-%d",      
    "%Y/%m/%d",      
    "%d/%m/%Y",      
]
_DATETIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  
    "%Y-%m-%d %H:%M",     
    "%Y/%m/%d %H:%M:%S",  
    "%d/%m/%Y %H:%M:%S",  
]


def _parse_any(s: str, fmts: List[str]) -> Any:
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            continue
    # Try to handle 3-digit years by padding with leading zero
    # This handles cases like "01/01/991" -> "01/01/0991"
    if "/" in s:
        parts = s.split("/")
        if len(parts) == 3:
            day, month, year = parts
            # If year is 3 digits, pad with leading zero
            if len(year) == 3 and year.isdigit():
                padded_s = f"{day}/{month}/0{year}"
                for fmt in fmts:
                    try:
                        return datetime.strptime(padded_s, fmt)
                    except Exception:
                        continue
    return None


def _date_norm(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if v is None:
            out.append(None)
            continue
        s = str(v).strip()
        if s.lower() in _EMPTY_VALUES:
            out.append(None)
            continue
        dt = _parse_any(s, _DATE_FORMATS)
        if dt is None:
            out.append(s)
        else:
            out.append(dt.strftime("%Y-%m-%d"))
    return out


def _dt_norm(values: List[str]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if v is None:
            out.append(None)
            continue
        s = str(v).strip()
        if s.lower() in _EMPTY_VALUES:
            out.append(None)
            continue
        dt = _parse_any(s, _DATETIME_FORMATS)
        if dt is None:
            out.append(s)
        else:
            out.append(dt.strftime("%Y-%m-%d %H:%M:%S"))
    return out


register("date", _date_norm)
register("datetime", _dt_norm)
