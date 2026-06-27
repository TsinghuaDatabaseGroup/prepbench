import json
from pathlib import Path
from typing import Any, Dict


TRUE_STRINGS = {"true", "1", "yes"}
FALSE_STRINGS = {"false", "0", "no"}


def _to_bool(value: Any, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lower = value.strip().lower()
        if lower in TRUE_STRINGS:
            return True
        if lower in FALSE_STRINGS:
            return False
    return default


def load_config(path: str) -> Dict[str, Any]:
    """
    Load config.json and apply defaults per spec.
    Structure:
    {
      "files": {
        "<gt_filename>.csv": {
          "ignore_order": true,
          "key": ["col1", "col2"],
          "columns": { "<gt_col>": "<type>", ... }
        }
      }
    }
    - ignore_order default: True
    - key is required (non-empty list)
    - tolerate string booleans
    - if file entry missing, it's allowed (may lead to empty columns)
    - any parsing error returns empty config to let caller treat as failure
    """
    try:
        config_path = Path(path)
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return {}

    files = raw.get("files") or {}
    normalized: Dict[str, Any] = {"files": {}}

    for fname, spec in files.items():
        spec = spec or {}
        ignore_order = _to_bool(spec.get("ignore_order"), default=True)
        columns = spec.get("columns") or {}
        key = spec.get("key") or []
        # validate key
        if not isinstance(key, list) or not key or not all(isinstance(k, str) and k.strip() for k in key):
            # invalid: return empty to let caller treat as failure
            return {}
        # columns is expected to be mapping of gt_col -> type string
        normalized["files"][fname] = {
            "ignore_order": ignore_order,
            "key": key,
            "columns": columns,
        }

    return normalized
