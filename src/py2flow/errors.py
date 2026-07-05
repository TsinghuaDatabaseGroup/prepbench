from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .ir import StepKind


class FlowError(Exception):
    pass


@dataclass
class FlowValidationError(FlowError):

    message: str
    node_id: Optional[str] = None
    step_kind: Optional["StepKind"] = None
    error_code: Optional[str] = None  # e.g. "cycle", "unreachable_nodes", "node_validation"
    field: Optional[str] = None  # optional field name for faster debugging, e.g. "distinct"
    help: Optional[str] = None  # human-friendly fix suggestion (kept out of __str__ for compatibility)

    def __str__(self) -> str:
        return self.message

    @property
    def kind(self) -> Optional["StepKind"]:
        return self.step_kind


@dataclass
class FlowExecutionError(FlowError):

    node_id: str
    kind: "StepKind"
    params: Mapping[str, Any]
    cause: BaseException
    message: Optional[str] = None
    error_code: Optional[str] = None  # e.g. "operator_error"
    help: Optional[str] = None  # human-friendly fix suggestion (kept out of __str__ for compatibility)

    def __str__(self) -> str:
        m = self.message or str(self.cause)
        return f"Execution failed at node '{self.node_id}' ({self.kind.value}): {m}"
