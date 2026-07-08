from __future__ import annotations

import hashlib
import traceback
from typing import Any, Callable, Dict, List, Mapping, cast

import numpy as np
import pandas as pd

from py2flow.errors import FlowExecutionError
from py2flow.ir import StepKind
from .base import ExecutionContext, Operator
from .expr import TRUSTED_IMPORTS, exec_code


def _ensure_dataframe(obj: Any, context: str) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj
    raise TypeError(f"Expected pandas DataFrame for {context}, got {type(obj)}")


class Script(Operator):
    def __init__(self) -> None:
        self._local_cache: Dict[str, Callable[[pd.DataFrame, Any, Any], pd.DataFrame]] = {}

    def execute(self, node_id: str, inputs: List[pd.DataFrame], params: Mapping[str, Any], ctx: ExecutionContext) -> pd.DataFrame:
        if len(inputs) != 1:
            raise ValueError("script expects exactly 1 input")
        df = inputs[0]
        func = self._get_transform(node_id, params, ctx)
        try:
            out = func(df, pd, np)
        except Exception as exc:
            help_text = _format_script_exception(node_id, params.get("inline_code"), exc)
            raise FlowExecutionError(
                node_id,
                StepKind.SCRIPT,
                params,
                exc,
                message=f"script transform failed: {exc}",
                error_code="script_error",
                help=help_text,
            ) from exc
        return _ensure_dataframe(out, "script-result")

    def _get_cache(self, ctx: ExecutionContext) -> Dict[str, Callable[[pd.DataFrame, Any, Any], pd.DataFrame]]:
        exec_inst = getattr(ctx, "executor", None)
        if exec_inst is not None and hasattr(exec_inst, "_script_cache"):
            return cast(Dict[str, Callable[[pd.DataFrame, Any, Any], pd.DataFrame]], getattr(exec_inst, "_script_cache"))
        return self._local_cache

    def _get_transform(self, node_id: str, params: Mapping[str, Any], ctx: ExecutionContext) -> Callable[[pd.DataFrame, Any, Any], pd.DataFrame]:
        cache = self._get_cache(ctx)

        deterministic = params.get("deterministic", True)
        side_effects = params.get("side_effects", False)
        code = params.get("inline_code")
        if not isinstance(deterministic, bool) or not isinstance(side_effects, bool):
            raise ValueError("script requires boolean deterministic/side_effects")
        if not isinstance(code, str) or not code.strip():
            raise ValueError("script requires non-empty inline_code")

        code_hash = hashlib.sha256(code.encode("utf-8")).hexdigest()
        cache_key = f"{node_id}:{code_hash}"
        if cache_key in cache:
            return cache[cache_key]

        env: Dict[str, Any] = {}
        exec_code(
            code,
            env,
            filename=f"<py2flow:script:{node_id}>",
            allow_imports=TRUSTED_IMPORTS,
        )
        transform = env.get("transform")
        if not callable(transform):
            raise ValueError("script inline_code must define function transform(df, pd, np) -> df")
        cache[cache_key] = cast(Callable[[pd.DataFrame, Any, Any], pd.DataFrame], transform)
        return cache[cache_key]


def _format_script_exception(node_id: str, code: Any, exc: BaseException) -> str | None:
    if not isinstance(code, str) or not code:
        return None
    lines = code.splitlines()
    tb = exc.__traceback__
    if tb is None:
        return None

    frames = traceback.extract_tb(tb)
    target = None
    script_filename = f"<py2flow:script:{node_id}>"
    for fr in reversed(frames):
        if fr.filename == script_filename:
            target = fr
            break
    if target is None:
        return None
    lineno = int(target.lineno)
    if lineno < 1 or lineno > len(lines):
        return f"Script error at {script_filename}:{lineno}"
    snippet = lines[lineno - 1].rstrip()
    return f"Script error at {script_filename}:{lineno}: {snippet}"
