from __future__ import annotations

from typing import Dict, Mapping, Optional

from .base import Operator
from .input import Input
from .output import Output
from .project import Project
from .filter import Filter
from .dedup import Dedup
from .join import Join
from .union import Union
from .aggregate import Aggregate
from .pivot import Pivot
from .script import Script
from .sort import Sort

from py2flow.ir import StepKind


class OperatorRegistry:

    def __init__(self, initial: Optional[Mapping[StepKind, Operator]] = None) -> None:
        self._ops: Dict[StepKind, Operator] = dict(initial or {})

    @classmethod
    def with_builtins(cls) -> "OperatorRegistry":
        reg = cls()
        reg._register_builtins()
        return reg

    def _register_builtins(self) -> None:
        self._ops.update(
            {
                StepKind.INPUT: Input(),
                StepKind.OUTPUT: Output(),
                StepKind.PROJECT: Project(),
                StepKind.FILTER: Filter(),
                StepKind.DEDUP: Dedup(),
                StepKind.JOIN: Join(),
                StepKind.UNION: Union(),
                StepKind.AGGREGATE: Aggregate(),
                StepKind.PIVOT: Pivot(),
                StepKind.SCRIPT: Script(),
                StepKind.SORT: Sort(),
            }
        )

    def register(self, kind: StepKind, operator: Operator) -> None:
        self._ops[kind] = operator

    def get(self, kind: StepKind) -> Optional[Operator]:
        return self._ops.get(kind)

    def as_mapping(self) -> Mapping[StepKind, Operator]:
        return dict(self._ops)


_GLOBAL_REGISTRY = OperatorRegistry.with_builtins()


def get_global_operator_registry() -> OperatorRegistry:
    return _GLOBAL_REGISTRY


def register_operator(kind: StepKind, operator: Operator) -> None:
    _GLOBAL_REGISTRY.register(kind, operator)



def default_operator_registry() -> Dict[StepKind, Operator]:
    return dict(_GLOBAL_REGISTRY.as_mapping())
