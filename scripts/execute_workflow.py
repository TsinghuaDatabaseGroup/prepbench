from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from evaluate.core import evaluate
from prepbench.case_ids import normalize_case_id
from py2flow.exec_flow import exec_flow


def infer_case_id(*paths: Path) -> str | None:
    for path in paths:
        for part in [path.name, *[parent.name for parent in path.parents]]:
            if part.startswith("case_") or part.startswith("case"):
                try:
                    return normalize_case_id(part)
                except Exception:
                    continue
    return None


def resolve_repo_path(path: str | Path) -> Path:
    path_obj = Path(path).expanduser()
    if path_obj.is_absolute():
        return path_obj.resolve()
    return (REPO_ROOT / path_obj).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute a PrepBench workflow JSON against one case's input tables, "
            "write candidate output CSVs, and optionally evaluate them against GT."
        )
    )
    parser.add_argument("--flow-path", required=True, help="Path to flow.json or flow_compressed.json.")
    parser.add_argument("--input-root", required=True, help="Directory containing input_*.csv files.")
    parser.add_argument(
        "--output-root",
        default="",
        help=(
            "Directory for generated output_*.csv files. Defaults to "
            "@output/workflow_execution/<case_id>/workflow/cand when a case id can be inferred."
        ),
    )
    parser.add_argument("--case-id", default="", help="Optional case id used for default output and GT paths.")
    parser.add_argument("--evaluate", action="store_true", help="Compare generated outputs with GT after execution.")
    parser.add_argument("--gt-root", default="src/evaluate/gt", help="Root containing GT case directories.")
    parser.add_argument("--gt-dir", default="", help="Explicit GT directory. Overrides --gt-root/--case-id.")
    parser.add_argument("--clean-output", action="store_true", help="Remove --output-root before execution.")
    parser.add_argument("--trace", action="store_true", help="Log per-node row/column traces.")
    parser.add_argument("--explain", action="store_true", help="Validate and print node summary without executing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    flow_path = resolve_repo_path(args.flow_path)
    input_root = resolve_repo_path(args.input_root)

    case_id = normalize_case_id(args.case_id) if args.case_id else infer_case_id(input_root, flow_path)
    if args.output_root:
        output_root = resolve_repo_path(args.output_root)
    else:
        output_case = case_id or "unknown_case"
        output_root = (REPO_ROOT / "@output" / "workflow_execution" / output_case / "workflow" / "cand").resolve()

    if args.clean_output and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    exec_flow(
        flow_path=flow_path,
        input_root=input_root,
        output_root=output_root,
        trace=bool(args.trace),
        explain=bool(args.explain),
    )

    output_files = sorted(path.name for path in output_root.glob("output_*.csv"))
    summary: dict[str, Any] = {
        "flow_path": str(flow_path),
        "input_root": str(input_root),
        "output_root": str(output_root),
        "case_id": case_id or "",
        "output_files": output_files,
        "evaluated": False,
        "passed": None,
        "first_error": None,
    }

    if args.evaluate:
        if args.gt_dir:
            gt_dir = resolve_repo_path(args.gt_dir)
        elif case_id:
            gt_dir = resolve_repo_path(Path(args.gt_root) / case_id)
        else:
            raise ValueError("--evaluate requires --gt-dir or an inferable/explicit --case-id")
        passed, first_error = evaluate(str(gt_dir), str(output_root))
        summary.update(
            {
                "gt_dir": str(gt_dir),
                "evaluated": True,
                "passed": passed,
                "first_error": first_error,
            }
        )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed"] is not False else 1


if __name__ == "__main__":
    raise SystemExit(main())
