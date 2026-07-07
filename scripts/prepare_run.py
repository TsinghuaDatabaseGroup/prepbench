from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from prepbench.workspaces import MODES, discover_case_ids, prepare_case_workspace, resolve_repo_path, workspace_summary_json


EXPECTED_CLI_ERRORS = (FileExistsError, FileNotFoundError, RuntimeError, ValueError)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare PrepBench case workspaces under a run root.")
    parser.add_argument("--mode", required=True, choices=MODES, help="Public mode: clarified, interactive, or workflow.")
    case_group = parser.add_mutually_exclusive_group(required=True)
    case_group.add_argument("--case", dest="case_id", help="Case id, for example case_001 or 1.")
    case_group.add_argument("--all", action="store_true", help="Prepare all GT cases for this mode.")
    parser.add_argument(
        "--run-root",
        required=True,
        help="Run root like @runs/<agent>/<mode>. The case workspace is created under this directory.",
    )
    parser.add_argument("--data-root", default="data", help="Dataset root containing data/case_xxx directories.")
    parser.add_argument("--gt-root", default="src/evaluate/gt", help="GT case root used by --all.")
    parser.add_argument(
        "--workflow-prompt",
        default="src/agents/prompts/flow_agent.yaml",
        help="Workflow prompt to symlink in workflow mode.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing case workspace.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.all:
        case_ids = discover_case_ids(args.gt_root)
        if not case_ids:
            raise ValueError(f"No GT case_* directories found under {resolve_repo_path(args.gt_root)}")
        workspaces = [
            prepare_case_workspace(
                case_id=case_id,
                mode=args.mode,
                run_root=args.run_root,
                data_root=args.data_root,
                workflow_prompt=args.workflow_prompt,
                force=bool(args.force),
            )
            for case_id in case_ids
        ]
        summary = {
            "mode": args.mode,
            "run_root": str(resolve_repo_path(args.run_root)),
            "total": len(workspaces),
            "cases": case_ids,
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    workspace = prepare_case_workspace(
        case_id=args.case_id,
        mode=args.mode,
        run_root=args.run_root,
        data_root=args.data_root,
        workflow_prompt=args.workflow_prompt,
        force=bool(args.force),
    )
    print(workspace_summary_json(workspace, case_id=args.case_id, mode=args.mode))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EXPECTED_CLI_ERRORS as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
