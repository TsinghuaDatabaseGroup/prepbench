from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .ir import StepKind


class FlowError(Exception):
    pass


def _kind_value(kind: Any) -> Any:
    return getattr(kind, "value", kind)


def error_to_dict(exc: BaseException) -> dict[str, Any]:
    if hasattr(exc, "to_dict"):
        payload = getattr(exc, "to_dict")()
        if isinstance(payload, dict):
            return payload
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "node_id": None,
        "step_kind": None,
        "field": None,
        "error_code": None,
        "help": getattr(exc, "help", None),
    }


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "validation_error",
            "message": self.message,
            "node_id": self.node_id,
            "step_kind": _kind_value(self.step_kind),
            "field": self.field,
            "error_code": self.error_code,
            "help": self.help,
        }


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "execution_error",
            "message": self.message or str(self.cause),
            "node_id": self.node_id,
            "step_kind": _kind_value(self.kind),
            "field": None,
            "error_code": self.error_code,
            "help": self.help,
        }
