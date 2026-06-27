from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set

import pandas as pd

from .config import load_config
from .io_utils import list_csvs, read_csv
from .keys import build_unique_index
from .matchers.base import normalize_vector, equals


class Evaluator:
    def __init__(self, gt_dir: str, cand_dir: str, config_path: Optional[str] = None):
        self.gt_dir = gt_dir
        self.cand_dir = cand_dir
        self.config_path = config_path
        self.report: Dict[str, Any] = {"passed": False, "errors": [], "diff_summary": {}}
        self.cfg = {"files": {}}
        self.any_error = False

    def run(self) -> Dict[str, Any]:
        try:
            self._load_config()
            self._check_files()

            if self.any_error:
                self.report["passed"] = False
                return self.report

            gt_paths = list_csvs(self.gt_dir)
            cand_by_name = {p.name: p for p in list_csvs(self.cand_dir)}

            for gt_path in gt_paths:
                self._evaluate_file(gt_path, cand_by_name[gt_path.name])
                if self.any_error:
                    break

            self.report["passed"] = not self.any_error

        except Exception as e:
            self._add_error("EXCEPTION", repr(e))

        return self.report

    def _load_config(self):
        if self.config_path:
            self.cfg = load_config(self.config_path)
            if not self.cfg or "files" not in self.cfg:
                self._add_error("CONFIG_MISSING", f"Cannot parse or missing 'files' in config: {self.config_path}")

    def _add_error(self, error_type: str, message: str, file: Optional[str] = None, detail: Optional[Dict[str, Any]] = None):
        if self.any_error:
            return
        entry: Dict[str, Any] = {"error_type": error_type, "message": message}
        if file:
            entry["file"] = file
        if detail:
            entry["detail"] = detail
        self.report["errors"].append(entry)
        self.any_error = True

    def _check_files(self):
        gt_paths = list_csvs(self.gt_dir)
        cand_paths = list_csvs(self.cand_dir)

        if not gt_paths or not cand_paths:
            self._add_error("FILE_COUNT_MISMATCH", f"gold={len(gt_paths)}, cand={len(cand_paths)}")
            self.report["diff_summary"]["file_count_mismatch"] = {"gold": len(gt_paths), "cand": len(cand_paths)}
            return

        if len(gt_paths) != len(cand_paths):
            self._add_error("FILE_COUNT_MISMATCH", f"gold={len(gt_paths)}, cand={len(cand_paths)}")
            self.report["diff_summary"]["file_count_mismatch"] = {"gold": len(gt_paths), "cand": len(cand_paths)}

        gt_names = {p.name for p in gt_paths}
        cand_names = {p.name for p in cand_paths}
        missing_files = sorted(list(gt_names - cand_names))
        if missing_files:
            self.report["diff_summary"]["missing_files"] = missing_files
            self._add_error(
                "MISSING_FILE",
                f"Candidate directory is missing file: {missing_files[0]}",
                file=missing_files[0],
                detail={"file": missing_files[0]},
            )

    def _evaluate_file(self, gt_path: Path, cand_path: Path):

        gt_df = read_csv(gt_path)
        cand_df = read_csv(cand_path)

        filename = gt_path.name

        if gt_df is None or cand_df is None:
            self._add_error("READ_ERROR", f"Failed to read CSV: {gt_path.name} or {cand_path.name}", file=filename)
            return

        file_cfg = self.cfg.get("files", {}).get(gt_path.name)
        if not file_cfg:
            self._add_error("CONFIG_MISSING", f"No config found for file: {gt_path.name}", file=filename)
            return

        key_cols: List[str] = file_cfg.get("key", [])
        columns_spec: Dict[str, str] = file_cfg.get("columns", {})
        ignore_order: bool = bool(file_cfg.get("ignore_order", True))

        if not self._validate_columns(gt_path.name, gt_df, cand_df, columns_spec):
            return
        
        if len(gt_df) != len(cand_df):
            delta = len(cand_df) - len(gt_df)
            self._add_error("ROW_COUNT_MISMATCH", f"File {gt_path.name}: gold={len(gt_df)}, cand={len(cand_df)}", file=filename)
            self.report["diff_summary"].setdefault("row_count_delta", {})[filename] = delta
            return

        self._compare_data(gt_path.name, gt_df, cand_df, key_cols, columns_spec, ignore_order)

    def _validate_columns(self, filename: str, gt_df: pd.DataFrame, cand_df: pd.DataFrame, columns_spec: Dict[str, str]) -> bool:
        required_cols = set(columns_spec.keys())
        cand_cols = set(cand_df.columns)
        if not required_cols.issubset(cand_cols):
            missing = sorted(list(required_cols - cand_cols))
            self._add_error("MISSING_COLUMNS", f"File {filename} is missing columns: {missing}", file=filename, detail={"columns": missing})
            self.report["diff_summary"].setdefault("missing_columns", []).append({"file": filename, "columns": missing})
            return False
        return True

    def _compare_data(self, filename: str, gt_df: pd.DataFrame, cand_df: pd.DataFrame, key_cols: List[str], columns_spec: Dict[str, str], ignore_order: bool):
        """
        Tolerant key matching with fail-fast behavior.
        - Key matching is tolerant (e.g., numeric tolerance).
        - Multiple candidate matches for a key are treated as an error.
        - Stops at the first mismatch.
        """
        from .keys import TolerantKeyIndex
        
        if not key_cols:
            self._add_error("CONFIG_MISSING", f"Key columns not specified for {filename}", file=filename)
            return

        key_types = [columns_spec[c] for c in key_cols]
        compare_cols = [c for c in columns_spec if c not in key_cols]
        
        gt_k_index, _, gt_dup = build_unique_index(gt_df, key_cols, key_types, allow_empty=True)
        cand_k_index, _, cand_dup = build_unique_index(cand_df, key_cols, key_types, allow_empty=True)

        if gt_dup or cand_dup:
            side = "GT" if gt_dup else "CAND"
            dup_key = gt_dup or cand_dup
            self._add_error("NON_UNIQUE_KEY", f"Duplicate keys in {side} for file {filename}: {dup_key}", file=filename)
            self.report["diff_summary"].setdefault("non_unique_key", {})[filename] = {"side": side, "key_tuple": dup_key}
            return

        matched_cand_indices: Set[int] = set()
        matched_pairs: List[Tuple[int, int, Tuple[Any, ...]]] = []

        cand_indexer = TolerantKeyIndex(cand_k_index, key_types)

        for gt_key in gt_k_index.keys():
            gt_idx = gt_k_index[gt_key]
            candidates = cand_indexer.find_matches(gt_key, matched_cand_indices)

            if not candidates:
                self.report["diff_summary"].setdefault("missing_keys", {})[filename] = {
                    "count": 1,
                    "sample": [gt_key],
                }
                self._add_error(
                    "KEY_MISMATCH",
                    f"Missing key in candidate for file {filename}: {gt_key!r}",
                    file=filename,
                    detail={"reason": "missing_key", "key": gt_key},
                )
                return

            if len(candidates) > 1:
                sample_keys = [k for k, _ in candidates[:3]]
                self.report["diff_summary"].setdefault("multiple_key_matches", {})[filename] = {
                    "key": gt_key,
                    "candidate_count": len(candidates),
                    "sample": sample_keys,
                }
                self._add_error(
                    "KEY_MISMATCH",
                    f"Multiple candidate matches for key in {filename}: {gt_key!r}",
                    file=filename,
                    detail={
                        "reason": "multiple_matches",
                        "key": gt_key,
                        "candidate_count": len(candidates),
                        "candidate_sample": sample_keys,
                    },
                )
                return

            _, cand_idx = candidates[0]
            matched_cand_indices.add(cand_idx)
            matched_pairs.append((gt_idx, cand_idx, gt_key))

        all_cand_indices = set(cand_k_index.values())
        unmatched_cand_indices = all_cand_indices - matched_cand_indices
        if unmatched_cand_indices:
            extra_keys = [cand_indexer.idx_to_key[idx] for idx in sorted(unmatched_cand_indices)]
            sample_keys = extra_keys[:3]
            self.report["diff_summary"].setdefault("extra_keys", {})[filename] = {
                "count": len(extra_keys),
                "sample": sample_keys,
            }
            self._add_error(
                "KEY_MISMATCH",
                f"Extra keys in candidate for file {filename}: {sample_keys[0]!r}",
                file=filename,
                detail={
                    "reason": "extra_keys",
                    "key": sample_keys[0],
                    "extra_count": len(extra_keys),
                    "extra_sample": sample_keys,
                },
            )
            return

        # Value comparison for matched pairs
        if not compare_cols:
            return

        try:
            for gt_idx, cand_idx, gt_key in matched_pairs:
                for col in compare_cols:
                    type_name = columns_spec[col]
                    gt_val = gt_df.loc[gt_idx, col]
                    cand_val = cand_df.loc[cand_idx, col]
                    gt_vec = normalize_vector([gt_val], type_name)
                    cand_vec = normalize_vector([cand_val], type_name)
                    use_tol = (type_name == "number")

                    if not equals(gt_vec, cand_vec, ignore_order=ignore_order, use_number_tolerance=use_tol):
                        sample = {
                            "file": filename,
                            "col": col,
                            "key": gt_key,
                            "gold": gt_val,
                            "cand": cand_val,
                        }
                        self.report["diff_summary"].setdefault("value_mismatch_samples", []).append(sample)
                        self._add_error(
                            "VALUE_MISMATCH",
                            f"Mismatch in {filename}, col '{col}', key={gt_key!r}",
                            file=filename,
                            detail={"col": col, "key": gt_key},
                        )
                        return
        except Exception as e:
            self._add_error("ALIGNMENT_ERROR", f"Failed to compare data for {filename}: {e}", file=filename)
            return
