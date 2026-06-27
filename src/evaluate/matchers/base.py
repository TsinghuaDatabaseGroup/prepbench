from typing import Any, Callable, Dict, List, Tuple

_NORMALIZERS: Dict[str, Callable[[List[str]], List[Any]]] = {}

# Unified empty tokens across all normalizers
EMPTY_TOKENS = {"", "none", "nan", "null", "n/a", "na"}


def is_empty_token(v: Any) -> bool:
    if v is None:
        return True
    s = str(v).strip().lower()
    return s in EMPTY_TOKENS


def register(type_name: str, normalizer: Callable[[List[str]], List[Any]]) -> None:
    _NORMALIZERS[type_name] = normalizer


def normalize_vector(values: List[str], type_name: str) -> List[Any]:
    normalizer = _NORMALIZERS.get(type_name)
    if not normalizer:
        # Unknown type: identity normalization (treat as text_exact behavior)
        return values
    return normalizer(values)


def _sort_key(v: Any) -> Tuple[int, str]:
    # Ensure stable comparable key across types
    if v is None:
        return (0, "")
    return (1, repr(v))


def _numbers_equal(a: Any, b: Any, tolerance: float = 0.02) -> bool:
    """Compare two numbers with relative tolerance (default 2%)"""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    
    # If both are numbers, use relative tolerance
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a == 0 and b == 0:
            return True
        if a == 0 or b == 0:
            return abs(a - b) < tolerance
        return abs(a - b) / max(abs(a), abs(b)) < tolerance
    
    # For non-numbers, use exact equality
    return a == b


def equals(vec_a: List[Any], vec_b: List[Any], ignore_order: bool, use_number_tolerance: bool = False) -> bool:
    if len(vec_a) != len(vec_b):
        return False
    
    # Choose comparison function based on whether to use number tolerance
    if use_number_tolerance:
        compare_fn = _numbers_equal
    else:
        compare_fn = lambda a, b: a == b
    
    if ignore_order:
        vec_a = sorted(vec_a, key=_sort_key)
        vec_b = sorted(vec_b, key=_sort_key)

    return all(compare_fn(x, y) for x, y in zip(vec_a, vec_b))
