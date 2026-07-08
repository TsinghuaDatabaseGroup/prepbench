from __future__ import annotations

import argparse
import contextlib
import csv
import inspect
import json
import os
import shutil
import subprocess
import sys
import time
import types
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluate.core import evaluate
from prepbench.case_ids import normalize_case_id


def parse_case_selectors(values: list[str]) -> set[str]:
    selected: set[str] = set()
    for value in values:
        for token in str(value).split(","):
            token = token.strip()
            if not token:
                continue
            if "-" in token and not token.lower().startswith("case-"):
                left, right = token.split("-", 1)
                start = int(normalize_case_id(left).split("_", 1)[1])
                end = int(normalize_case_id(right).split("_", 1)[1])
                if start > end:
                    start, end = end, start
                selected.update(f"case_{idx:03d}" for idx in range(start, end + 1))
            else:
                selected.add(normalize_case_id(token))
    return selected


def case_sort_key(path: Path) -> int:
    try:
        return int(path.name.split("_", 1)[1])
    except Exception:
        return 10**9


def default_solutions_root() -> Path:
    env_root = os.getenv("PREPBENCH_SOLUTIONS_ROOT", "").strip()
    if env_root:
        return Path(env_root).expanduser().resolve()
    public_root = REPO_ROOT / "reference" / "solutions"
    if public_root.is_dir():
        return public_root.resolve()
    return (REPO_ROOT / "src" / "simulator" / "assets" / "solutions").resolve()


def solution_candidates(case_name: str) -> list[Path]:
    idx = int(case_name.split("_", 1)[1])
    return [
        Path(f"case_{idx:03d}") / "solution.py",
        Path(f"case{idx:03d}") / "solution.py",
        Path(f"case_{idx:03d}.py"),
        Path(f"case{idx:03d}.py"),
    ]


def resolve_solution_path(solutions_root: Path, case_name: str) -> Path | None:
    for rel in solution_candidates(case_name):
        path = solutions_root / rel
        if path.is_file():
            return path
    return None


def load_solution_globals(solution_path: Path, case_dir: Path) -> dict[str, Any]:
    # Present __file__ as if the solution lived beside data/case_xxx/inputs.
    # This keeps legacy zero-argument solve() functions working without copying
    # reference solution files into the public data tree.
    module_name = f"prepbench_reference_{case_dir.name}"
    module = types.ModuleType(module_name)
    module.__file__ = str(case_dir / "solution.py")
    module.__package__ = ""
    sys.modules[module_name] = module
    source = solution_path.read_text(encoding="utf-8")
    code = compile(source, str(solution_path), "exec")
    exec(code, module.__dict__)
    return module.__dict__


def run_solution(solution_path: Path, case_dir: Path) -> dict[str, Any]:
    globals_dict = load_solution_globals(solution_path, case_dir)
    solve = globals_dict.get("solve")
    if solve is None or not callable(solve):
        raise RuntimeError("solution has no callable solve")

    signature = inspect.signature(solve)
    required_positional = [
        param
        for param in signature.parameters.values()
        if param.default is inspect.Parameter.empty
        and param.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    if len(required_positional) == 0:
        outputs = solve()
    elif len(required_positional) == 1:
        outputs = solve(case_dir / "inputs")
    else:
        raise RuntimeError(f"unsupported solve signature: {signature}")

    if not isinstance(outputs, dict):
        raise RuntimeError(f"solve returned {type(outputs).__name__}, expected dict")
    return outputs


def write_outputs(outputs: dict[str, Any], cand_dir: Path) -> None:
    cand_dir.mkdir(parents=True, exist_ok=True)
    for filename, table in outputs.items():
        if not isinstance(filename, str) or not filename.endswith(".csv"):
            raise RuntimeError(f"invalid output filename: {filename!r}")
        if "/" in filename or "\\" in filename:
            raise RuntimeError(f"output filename must not contain path separators: {filename!r}")
        if not hasattr(table, "to_csv"):
            raise RuntimeError(f"{filename}: output object has no to_csv method")
        table.to_csv(cand_dir / filename, index=False, encoding="utf-8")


def check_case(case_dir: Path, gt_root: Path, solutions_root: Path, output_root: Path) -> dict[str, str]:
    case_name = case_dir.name
    started = time.perf_counter()
    gt_dir = gt_root / case_name
    case_output_dir = output_root / case_name
    cand_dir = case_output_dir / "result"

    row = {
        "case_name": case_name,
        "status": "OK",
        "passed": "false",
        "solution_path": "",
        "candidate_dir": str(cand_dir),
        "error_type": "",
        "error_message": "",
        "seconds": "0.000",
    }

    try:
        solution_path = resolve_solution_path(solutions_root, case_name)
        if solution_path is None:
            row["status"] = "SOLUTION_NOT_FOUND"
            row["error_type"] = "SOLUTION_NOT_FOUND"
            row["error_message"] = f"No reference solution found under {solutions_root}"
            return row
        row["solution_path"] = str(solution_path)

        if case_output_dir.exists():
            shutil.rmtree(case_output_dir)
        outputs = run_solution(solution_path, case_dir)
        write_outputs(outputs, cand_dir)

        passed, first_error = evaluate(str(gt_dir), str(cand_dir))
        row["passed"] = "true" if passed else "false"
        if not passed:
            row["status"] = "EVAL_FAIL"
            row["error_type"] = str((first_error or {}).get("error_type") or "EVAL_FAIL")
            row["error_message"] = str((first_error or {}).get("message") or "")
    except Exception as exc:
        row["status"] = "ERROR"
        row["error_type"] = type(exc).__name__
        row["error_message"] = str(exc)
    finally:
        row["seconds"] = f"{time.perf_counter() - started:.3f}"

    return row


def _truncate(text: str, limit: int = 1000) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def check_case_in_subprocess(
    case_dir: Path,
    gt_root: Path,
    solutions_root: Path,
    output_root: Path,
    timeout_seconds: int,
) -> dict[str, str]:
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--worker-case",
        case_dir.name,
        "--data-root",
        str(case_dir.parent),
        "--gt-root",
        str(gt_root),
        "--solutions-root",
        str(solutions_root),
        "--output-root",
        str(output_root),
    ]
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "case_name": case_dir.name,
            "status": "TIMEOUT",
            "passed": "false",
            "solution_path": str(resolve_solution_path(solutions_root, case_dir.name) or ""),
            "candidate_dir": str(output_root / case_dir.name / "result"),
            "error_type": "TIMEOUT",
            "error_message": f"Timed out after {timeout_seconds}s",
            "seconds": f"{time.perf_counter() - started:.3f}",
        }

    try:
        row = json.loads(completed.stdout.strip())
    except Exception:
        row = {
            "case_name": case_dir.name,
            "status": "WORKER_ERROR",
            "passed": "false",
            "solution_path": str(resolve_solution_path(solutions_root, case_dir.name) or ""),
            "candidate_dir": str(output_root / case_dir.name / "result"),
            "error_type": "WORKER_ERROR",
            "error_message": _truncate((completed.stdout or "") + "\n" + (completed.stderr or "")),
            "seconds": f"{time.perf_counter() - started:.3f}",
        }
    if completed.returncode != 0 and row.get("passed") == "true":
        row["status"] = "WORKER_ERROR"
        row["passed"] = "false"
        row["error_type"] = "WORKER_ERROR"
        row["error_message"] = _truncate(completed.stderr or completed.stdout or f"returncode={completed.returncode}")
    return {key: str(value) for key, value in row.items()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run PrepBench reference solutions, write their outputs under "
            "@runs/reference_check, and verify them with the evaluator."
        )
    )
    parser.add_argument("--data-root", default="data", help="Path to data/case_xxx directories.")
    parser.add_argument("--gt-root", default="src/evaluate/gt", help="Path to evaluator GT directories.")
    parser.add_argument(
        "--solutions-root",
        default=str(default_solutions_root()),
        help="Reference-solution root. Defaults to PREPBENCH_SOLUTIONS_ROOT or reference/solutions.",
    )
    parser.add_argument(
        "--output-root",
        default="@runs/reference_check",
        help="Where generated reference outputs and the verification report are written.",
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="Optional case selector, e.g. --case 176 --case case_203 or --case 1-10.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=120,
        help="Per-case timeout for reference execution plus evaluator comparison.",
    )
    parser.add_argument("--worker-case", default="", help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_root = (REPO_ROOT / args.data_root).resolve()
    gt_root = (REPO_ROOT / args.gt_root).resolve()
    solutions_root = Path(args.solutions_root).expanduser().resolve()
    output_root = (REPO_ROOT / args.output_root).resolve()

    if args.worker_case:
        case_name = normalize_case_id(args.worker_case)
        case_dir = data_root / case_name
        with contextlib.redirect_stdout(sys.stderr):
            row = check_case(case_dir, gt_root, solutions_root, output_root)
        print(json.dumps(row, ensure_ascii=False))
        return 0

    selected = parse_case_selectors(args.case)
    case_dirs = sorted([path for path in data_root.glob("case_*") if path.is_dir()], key=case_sort_key)
    if selected:
        case_dirs = [path for path in case_dirs if path.name in selected]

    if not case_dirs:
        print("No cases selected.", file=sys.stderr)
        return 2

    if args.timeout_seconds <= 0:
        print("--timeout-seconds must be positive.", file=sys.stderr)
        return 2

    output_root.mkdir(parents=True, exist_ok=True)
    report_path = output_root / "reference_output_verification.csv"
    fieldnames = [
        "case_name",
        "status",
        "passed",
        "solution_path",
        "candidate_dir",
        "error_type",
        "error_message",
        "seconds",
    ]

    rows: list[dict[str, str]] = []
    with report_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, case_dir in enumerate(case_dirs, 1):
            row = check_case_in_subprocess(
                case_dir,
                gt_root,
                solutions_root,
                output_root,
                args.timeout_seconds,
            )
            rows.append(row)
            writer.writerow({key: row.get(key, "") for key in fieldnames})
            f.flush()
            if row.get("passed") != "true":
                print(f"FAIL {row['case_name']} {row['error_type']}: {row['error_message']}")
            elif idx % 25 == 0 or idx == len(case_dirs):
                print(f"[verify_reference_outputs] progress={idx}/{len(case_dirs)}")

    passed = sum(1 for row in rows if row["passed"] == "true")
    failed_rows = [row for row in rows if row["passed"] != "true"]
    print(
        f"[verify_reference_outputs] cases={len(rows)} passed={passed} "
        f"failed={len(failed_rows)} report={report_path}"
    )
    for row in failed_rows[:20]:
        print(f"FAIL {row['case_name']} {row['error_type']}: {row['error_message']}")
    if len(failed_rows) > 20:
        print(f"... {len(failed_rows) - 20} more failures in {report_path}")

    return 1 if failed_rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
