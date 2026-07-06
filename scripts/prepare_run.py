from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from prepbench.workspaces import MODES, prepare_case_workspace, workspace_summary_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare one PrepBench case workspace under a run root.")
    parser.add_argument("--mode", required=True, choices=MODES, help="Public mode: clarified, interactive, or workflow.")
    parser.add_argument("--case", required=True, dest="case_id", help="Case id, for example case_001 or 1.")
    parser.add_argument(
        "--run-root",
        required=True,
        help="Run root like @runs/<agent>/<mode>. The case workspace is created under this directory.",
    )
    parser.add_argument("--data-root", default="data", help="Dataset root containing data/case_xxx directories.")
    parser.add_argument(
        "--workflow-prompt",
        default="src/agents/prompts/flow_agent.yaml",
        help="Workflow prompt to symlink in workflow mode.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing case workspace.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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
    raise SystemExit(main())
