from __future__ import annotations

import keyword
import re
from typing import Any, Dict, Mapping, MutableMapping, Optional, Set

import numpy as np
import pandas as pd


TRUSTED_IMPORTS: Set[str] = {
    "calendar",
    "collections",
    "datetime",
    "decimal",
    "functools",
    "itertools",
    "json",
    "locale",
    "math",
    "numpy",
    "pandas",
    "re",
    "time",
    "_strptime",
    "statistics",
    "string",
    "typing",
}


def safe_builtins(*, allow_imports: Optional[Set[str]] = None) -> Dict[str, Any]:
    def restricted_import(name: str, globals: Any = None, locals: Any = None, fromlist: Any = (), level: int = 0) -> Any:
        if allow_imports is None:
            return __import__(name, globals, locals, fromlist, level)
        root = name.split(".", 1)[0]
        if root not in allow_imports:
            raise ImportError(f"import of {root!r} is not allowed")
        return __import__(name, globals, locals, fromlist, level)

    return {
        "len": len,
        "range": range,
        "min": min,
        "max": max,
        "sum": sum,
        "enumerate": enumerate,
        "map": map,
        "filter": filter,
        "zip": zip,
        "iter": iter,
        "next": next,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "abs": abs,
        "round": round,
        "any": any,
        "all": all,
        "sorted": sorted,
        "isinstance": isinstance,
        "issubclass": issubclass,
        "__import__": restricted_import,
        "BaseException": BaseException,
        "Exception": Exception,
        "RuntimeError": RuntimeError,
        "ValueError": ValueError,
        "TypeError": TypeError,
        "NameError": NameError,
        "AssertionError": AssertionError,
    }

def _is_safe_identifier(name: str) -> bool:
    if not name.isidentifier():
        return False
    if keyword.iskeyword(name):
        return False
    return True


def _rewrite_backtick_columns(expr: str) -> str:
    # Rewrite `Column Name` -> df['Column Name'].
    # Quote-aware to avoid rewriting inside string literals.
    out: list[str] = []
    i = 0
    n = len(expr)
    quote: str | None = None
    triple = False

    while i < n:
        ch = expr[i]
        if quote is None:
            if ch in ("'", '"'):
                if expr[i: i + 3] == ch * 3:
                    quote = ch
                    triple = True
                    out.append(ch * 3)
                    i += 3
                    continue
                quote = ch
                triple = False
                out.append(ch)
                i += 1
                continue
            if ch == "`":
                j = expr.find("`", i + 1)
                if j == -1:
                    out.append(ch)
                    i += 1
                    continue
                col = expr[i + 1: j]
                out.append(f"df[{col!r}]")
                i = j + 1
                continue
            out.append(ch)
            i += 1
            continue

        # inside a string literal
        if ch == "\\" and not triple:
            if i + 1 < n:
                out.append(expr[i: i + 2])
                i += 2
                continue
        if triple:
            if expr[i: i + 3] == quote * 3:
                out.append(quote * 3)
                i += 3
                quote = None
                triple = False
                continue
            out.append(ch)
            i += 1
            continue
        if ch == quote:
            out.append(ch)
            i += 1
            quote = None
            continue
        out.append(ch)
        i += 1

    return "".join(out)

def expr_env(df: pd.DataFrame, extra: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    builtins = safe_builtins(allow_imports=TRUSTED_IMPORTS)
    env: Dict[str, Any] = {"df": df, "pd": pd,
                           "np": np, "__builtins__": builtins}
    env["__row_pos"] = pd.Series(range(len(df)), index=df.index)
    env["re"] = re
    reserved = set(env.keys()) | set(builtins.keys())
    for col in df.columns:
        name = str(col)
        if name in reserved:
            continue
        if not _is_safe_identifier(name):
            continue
        env[name] = df[name]
    if extra:
        env.update(dict(extra))
    return env


def eval_expr(expr: str, df: pd.DataFrame, extra: Optional[Mapping[str, Any]] = None) -> Any:
    env = expr_env(df, extra=extra)
    rewritten = _rewrite_backtick_columns(expr)
    try:
        return eval(rewritten, env, env)
    except NameError as exc:
        m = re.search(r"name '([^']+)' is not defined", str(exc))
        if m:
            missing = m.group(1)
            if missing in {str(c) for c in df.columns}:
                hint = f"Unknown name {missing!r}. If you meant the column, use df[{missing!r}] or `{missing}`."
                raise NameError(hint) from exc
        raise


def exec_code(code: str, env: MutableMapping[str, Any], *, filename: str = "<py2flow:exec>", allow_imports: Optional[Set[str]] = None) -> None:
    env.setdefault("pd", pd)
    env.setdefault("np", np)
    env.setdefault("re", re)
    env.setdefault("__builtins__", safe_builtins(allow_imports=allow_imports))
    compiled = compile(code, filename, "exec")
    exec(compiled, env, env)
