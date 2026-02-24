from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal

QuerySource = Literal["query", "query_full", "solution_only"]


@dataclass(frozen=True)
class ModeSpec:
    name: str
    query_source: QuerySource
    allow_profile: bool
    allow_clarify: bool
    allow_flow: bool


_CANONICAL_MODE_SPECS: Dict[str, ModeSpec] = {
    "orig": ModeSpec(
        name="orig",
        query_source="query",
        allow_profile=True,
        allow_clarify=False,
        allow_flow=False,
    ),
    "disamb": ModeSpec(
        name="disamb",
        query_source="query_full",
        allow_profile=True,
        allow_clarify=False,
        allow_flow=False,
    ),
    "interact": ModeSpec(
        name="interact",
        query_source="query",
        allow_profile=True,
        allow_clarify=True,
        allow_flow=False,
    ),
    "disamb_only": ModeSpec(
        name="disamb_only",
        query_source="query_full",
        allow_profile=False,
        allow_clarify=False,
        allow_flow=False,
    ),
    "e2e": ModeSpec(
        name="e2e",
        query_source="query",
        allow_profile=True,
        allow_clarify=True,
        allow_flow=True,
    ),
    "flow": ModeSpec(
        name="flow",
        # Mode 3 (code-to-workflow) translates reference solution code directly.
        query_source="solution_only",
        allow_profile=False,
        allow_clarify=False,
        allow_flow=True,
    ),
}

def get_mode_spec(run_mode: str) -> ModeSpec:
    mode = (run_mode or "").strip().lower()
    if mode in _CANONICAL_MODE_SPECS:
        return _CANONICAL_MODE_SPECS[mode]
    raise ValueError(
        f"Unsupported run_mode '{run_mode}'. Allowed: {sorted(_CANONICAL_MODE_SPECS.keys())}"
    )


def allowed_run_modes() -> tuple[str, ...]:
    return tuple(_CANONICAL_MODE_SPECS.keys())
