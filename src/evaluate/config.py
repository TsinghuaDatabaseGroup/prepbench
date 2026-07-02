import json
from pathlib import Path
from typing import Any, Dict


def load_config(path: str) -> Dict[str, Any]:
    """
    Load config.json and apply defaults per spec.
    Structure:
    {
      "files": {
        "<gt_filename>.csv": {
          "key": ["col1", "col2"],
          "columns": { "<gt_col>": "<type>", ... }
        }
      }
    }
    - key is required (non-empty list)
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
        columns = spec.get("columns") or {}
        key = spec.get("key") or []
        # validate key
        if not isinstance(key, list) or not key or not all(isinstance(k, str) and k.strip() for k in key):
            # invalid: return empty to let caller treat as failure
            return {}
        # columns is expected to be mapping of gt_col -> type string
        normalized["files"][fname] = {
            "key": key,
            "columns": columns,
        }

    return normalized
