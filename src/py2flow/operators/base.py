from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Mapping, List, Protocol, runtime_checkable

import logging
import pandas as pd


@runtime_checkable
class IOAdapter(Protocol):

    def read_df(self, path: Path, fmt: str, options: Mapping[str, Any]) -> pd.DataFrame:
        ...

    def write_df(self, df: pd.DataFrame, path: Path, fmt: str, options: Mapping[str, Any]) -> None:
        ...


class FileIO(IOAdapter):

    def read_df(self, path: Path, fmt: str, options: Mapping[str, Any]) -> pd.DataFrame:
        if fmt == "csv":
            return pd.read_csv(path, **options)
        raise ValueError(f"Unsupported format: {fmt}")

    def write_df(self, df: pd.DataFrame, path: Path, fmt: str, options: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "csv":
            opts = {"index": False}
            opts.update(dict(options))
            df.to_csv(path, **opts)
        else:
            raise ValueError(f"Unsupported format: {fmt}")


class ExecutionContext:

    def __init__(
        self,
        base_path: Path | None = None,
        io: IOAdapter | None = None,
        logger: logging.Logger | None = None,
        input_tables: Mapping[str, pd.DataFrame] | None = None,
    ):
        self.base_path = base_path
        self.io: IOAdapter = io or FileIO()
        self.logger = logger or logging.getLogger("py2flow")
        self.executor: object | None = None
        self.input_tables = input_tables

    def resolve_path(self, path_str: str) -> Path:
        p = Path(path_str)
        if not p.is_absolute() and self.base_path is not None:
            candidate = (self.base_path / p)
            try:
                normalized = candidate.resolve()
                base_resolved = self.base_path.resolve()
                first_component = self.base_path / p.parts[0] if p.parts else candidate
                if first_component.is_symlink():
                    return candidate
                normalized.relative_to(base_resolved)
            except Exception:
                from py2flow.errors import FlowValidationError
                raise FlowValidationError(
                    f"Path escapes base_path: {path_str}", error_code="path_escape"
                )
            return candidate
        return p


class Operator(ABC):

    @abstractmethod
    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> Any:
        raise NotImplementedError
