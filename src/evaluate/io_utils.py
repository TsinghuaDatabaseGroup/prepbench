from pathlib import Path
from typing import List, Optional
import pandas as pd


def list_csvs(dir_path: str) -> List[Path]:
    p = Path(dir_path)
    if not p.exists() or not p.is_dir():
        return []
    return sorted([f for f in p.iterdir() if f.is_file() and f.suffix.lower() == ".csv"])


def _detect_sep(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".tsv", ".tab"}:
        return "\t"
    return ","


def read_csv(path: Path) -> Optional[pd.DataFrame]:
    sep = _detect_sep(path)
    # Try utf-8 then latin-1; fall back to python engine
    for enc in ("utf-8", "latin-1"):
        try:
            # Read everything as string to keep comparisons consistent
            return pd.read_csv(
                path,
                sep=sep,
                dtype=str,
                keep_default_na=False,
                na_filter=False,
                encoding=enc,
            )
        except Exception:
            try:
                return pd.read_csv(
                    path,
                    sep=sep,
                    dtype=str,
                    keep_default_na=False,
                    na_filter=False,
                    encoding=enc,
                    engine="python",
                    on_bad_lines="skip",
                )
            except Exception:
                continue
    return None

