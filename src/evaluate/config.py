import json
from pathlib import Path
from typing import Any, Dict

from . import matchers  # noqa: F401 - import registers built-in matcher types
from .matchers.base import registered_type_names


class ConfigError(ValueError):
    """Raised when an evaluator config file cannot be loaded or normalized."""


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
    - parsing or shape errors raise ConfigError with the concrete reason
    """
    config_path = Path(path)
    try:
        with config_path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"invalid JSON in {config_path}: {exc}") from exc
    except OSError as exc:
        raise ConfigError(f"cannot read {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"config must be a JSON object: {config_path}")

    files = raw.get("files") or {}
    if not isinstance(files, dict):
        raise ConfigError(f"config field 'files' must be an object: {config_path}")
    normalized: Dict[str, Any] = {"files": {}}
    known_types = registered_type_names()

    for fname, spec in files.items():
        spec = spec or {}
        if not isinstance(spec, dict):
            raise ConfigError(f"config for {fname!r} must be an object")
        columns = spec.get("columns") or {}
        key = spec.get("key") or []
        if not isinstance(columns, dict):
            raise ConfigError(f"columns for {fname!r} must be an object")
        for col, type_name in columns.items():
            if not isinstance(col, str) or not col.strip():
                raise ConfigError(f"columns for {fname!r} must use non-empty string column names")
            if not isinstance(type_name, str) or type_name not in known_types:
                allowed = ", ".join(sorted(known_types))
                raise ConfigError(
                    f"unknown type for {fname!r}.{col!r}: {type_name!r}; allowed types: {allowed}"
                )
        if not isinstance(key, list) or not key or not all(isinstance(k, str) and k.strip() for k in key):
            raise ConfigError(f"key for {fname!r} must be a non-empty list of column names")
        missing_key_cols = [k for k in key if k not in columns]
        if missing_key_cols:
            raise ConfigError(f"key columns for {fname!r} are missing from columns: {missing_key_cols}")
        normalized["files"][fname] = {
            "key": key,
            "columns": columns,
        }

    return normalized
