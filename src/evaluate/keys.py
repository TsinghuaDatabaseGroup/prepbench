from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, Set
from bisect import bisect_left, bisect_right

import pandas as pd

from .matchers.base import normalize_vector


KeyTuple = Tuple[Any, ...]


def normalize_key_row(row: pd.Series, key_cols: Sequence[str], key_types: Sequence[str]) -> KeyTuple:
    normalized_parts: List[Any] = []
    for col, t in zip(key_cols, key_types):
        raw_val = row.get(col)
        norm = normalize_vector([raw_val], t)
        part = norm[0] if norm else None
        normalized_parts.append(part)
    return tuple(normalized_parts)


def build_unique_index(
    df: pd.DataFrame,
    key_cols: Sequence[str],
    key_types: Sequence[str],
    allow_empty: bool = False,
) -> Tuple[Optional[Dict[KeyTuple, int]], Optional[Tuple[int, KeyTuple]], Optional[KeyTuple]]:
    index: Dict[KeyTuple, int] = {}
    for i, row in df.iterrows():
        k = normalize_key_row(row, key_cols, key_types)
        if not allow_empty and any(part is None for part in k):
            return None, (int(i), k), None
        if k in index:
            return None, None, k
        index[k] = int(i)
    return index, None, None


# Reuse _numbers_equal from matchers.base for consistent tolerance behavior
from .matchers.base import _numbers_equal as _numbers_close


def key_matches_with_tolerance(
    key_a: KeyTuple, 
    key_b: KeyTuple, 
    key_types: Sequence[str],
    tolerance: float = 0.02
) -> bool:
    """
    Compare two keys using type-aware tolerance.
    For 'number' type columns, uses relative tolerance.
    For other types, uses exact equality.
    """
    if len(key_a) != len(key_b):
        return False
    for a, b, t in zip(key_a, key_b, key_types):
        if a is None and b is None:
            continue
        if a is None or b is None:
            return False
        if t == "number":
            if not _numbers_close(a, b, tolerance):
                return False
        else:
            if a != b:
                return False
    return True


class TolerantKeyIndex:
    def __init__(
        self,
        cand_index: Dict[KeyTuple, int],
        key_types: Sequence[str],
        tolerance: float = 0.02,
    ) -> None:
        self.cand_index = cand_index
        self.key_types = list(key_types)
        self.tolerance = tolerance
        self.idx_to_key = {idx: key for key, idx in cand_index.items()}
        self.col_indexes: List[Dict[str, Any]] = []
        self._build_indexes()

    def _build_indexes(self) -> None:
        for col_idx, t in enumerate(self.key_types):
            if t == "number":
                values: List[Tuple[float, int]] = []
                none_set: Set[int] = set()
                for key, idx in self.cand_index.items():
                    v = key[col_idx]
                    if v is None:
                        none_set.add(idx)
                    else:
                        values.append((float(v), idx))
                values.sort(key=lambda x: x[0])
                self.col_indexes.append(
                    {
                        "type": "number",
                        "values": [v for v, _ in values],
                        "indices": [idx for _, idx in values],
                        "none": none_set,
                    }
                )
            else:
                mapping: Dict[Any, Set[int]] = {}
                for key, idx in self.cand_index.items():
                    v = key[col_idx]
                    mapping.setdefault(v, set()).add(idx)
                self.col_indexes.append({"type": "exact", "map": mapping})

    def _numeric_candidates(self, col: Dict[str, Any], target_val: Any) -> set[int]:
        if target_val is None:
            return set(col["none"])
        values: List[float] = col["values"]
        if not values:
            return set()
        tol = self.tolerance
        try:
            v = float(target_val)
        except Exception:
            return set()
        if v == 0:
            # _numbers_equal uses absolute tolerance when either side is zero.
            low = -tol
            high = tol
        else:
            low = min(v * (1 - tol), v / (1 - tol))
            high = max(v * (1 - tol), v / (1 - tol))
        lo = bisect_left(values, low)
        hi = bisect_right(values, high)
        return set(col["indices"][lo:hi])

    def find_matches(self, target_key: KeyTuple, excluded_indices: set) -> List[Tuple[KeyTuple, int]]:
        if len(target_key) != len(self.key_types):
            return []
        candidate_sets: List[set[int]] = []
        for col_idx, t in enumerate(self.key_types):
            col = self.col_indexes[col_idx]
            v = target_key[col_idx]
            if col["type"] == "number":
                cand_set = self._numeric_candidates(col, v)
            else:
                cand_set = set(col["map"].get(v, set()))
            if not cand_set:
                return []
            candidate_sets.append(cand_set)

        candidate_sets.sort(key=len)
        candidates = set(candidate_sets[0])
        for s in candidate_sets[1:]:
            candidates.intersection_update(s)
            if not candidates:
                return []

        results: List[Tuple[KeyTuple, int]] = []
        for idx in candidates:
            if idx in excluded_indices:
                continue
            key = self.idx_to_key.get(idx)
            if key is None:
                continue
            if key_matches_with_tolerance(target_key, key, self.key_types, self.tolerance):
                results.append((key, idx))
        results.sort(key=lambda x: x[1])
        return results
