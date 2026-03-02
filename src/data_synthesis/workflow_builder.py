from __future__ import annotations

import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from agents.flow_agent import FlowAgent
from core.case_assets import require_reference_solution_path
from py2flow.errors import FlowExecutionError, FlowValidationError
from py2flow.executor import DAGExecutor, DebugConfig
from py2flow.flow_constraints import validate_script_constraints
from py2flow.ir import DAG

from .pipeline_common import (
    RepoPaths,
    evaluate_candidate,
    normalize_model_dir,
    read_text,
    summarize_eval_error,
    write_json,
)


@dataclass(frozen=True)
class WorkflowBuildOptions:
    model_name: str
    max_rounds: int = 5
    publish_flow: bool = False
    force: bool = False


class WorkflowBuilder:
    def __init__(self, repo_paths: RepoPaths, options: WorkflowBuildOptions):
        self.repo_paths = repo_paths
        self.options = options
        self.flow_agent = FlowAgent(model_name=options.model_name)
        self.model_dir = normalize_model_dir(options.model_name)

    def _case_output_root(self, case_name: str) -> Path:
        return self.repo_paths.output_root / "workflow" / self.model_dir / case_name

    def _solution_path(self, case_name: str) -> Path:
        case_dir = self.repo_paths.data_root / case_name
        return require_reference_solution_path(case_dir, root=self.repo_paths.solutions_root)

    def _execute_flow_once(
        self,
        *,
        case_name: str,
        case_dir: Path,
        round_root: Path,
        flow_dict: dict[str, Any],
    ) -> tuple[bool, dict[str, Any], Optional[dict[str, Any]]]:
        solution_dir = round_root / "solution"
        solution_dir.mkdir(parents=True, exist_ok=True)
        write_json(solution_dir / "flow.json", flow_dict)

        try:
            dag = DAG.from_dict(flow_dict)
        except FlowValidationError as exc:
            info = {
                "ok": False,
                "error_type": "validation",
                "message": str(exc),
                "details": {
                    "error_code": getattr(exc, "error_code", None),
                    "node_id": getattr(exc, "node_id", None),
                    "field": getattr(exc, "field", None),
                },
            }
            return False, info, None

        ok_constraints, constraint_msg, constraint_details = validate_script_constraints(flow_dict)
        if not ok_constraints:
            info = {
                "ok": False,
                "error_type": "validation",
                "message": constraint_msg,
                "details": constraint_details,
            }
            return False, info, None

        inputs_src = case_dir / "inputs"
        inputs_dst = solution_dir / "inputs"
        if inputs_dst.exists() or inputs_dst.is_symlink():
            if inputs_dst.is_symlink() or inputs_dst.is_file():
                inputs_dst.unlink()
            else:
                shutil.rmtree(inputs_dst)
        try:
            inputs_dst.symlink_to(inputs_src)
        except OSError:
            shutil.copytree(inputs_src, inputs_dst)

        try:
            executor = DAGExecutor(dag, base_path=solution_dir, debug=DebugConfig(on_fail_dump=True))
            start = time.time()
            executor.run(keep="none")
            elapsed = time.time() - start
        except FlowExecutionError as exc:
            info = {
                "ok": False,
                "error_type": "execution",
                "message": str(exc),
                "details": {"node_id": getattr(exc, "node_id", None)},
            }
            return False, info, None
        except Exception as exc:
            info = {
                "ok": False,
                "error_type": "execution",
                "message": str(exc),
                "details": {},
            }
            return False, info, None

        cand_dir = solution_dir / "flow_cand"
        if not cand_dir.is_dir() or not any(cand_dir.glob("*.csv")):
            info = {
                "ok": False,
                "error_type": "no_outputs",
                "message": "No output CSV files found under flow_cand.",
                "details": {},
            }
            return False, info, None

        eval_passed, eval_error = evaluate_candidate(case_name, cand_dir, self.repo_paths.gt_root)
        eval_payload = {
            "passed": eval_passed,
            "first_error": eval_error,
            "elapsed_sec": elapsed,
        }
        write_json(solution_dir / "evaluation.json", eval_payload)

        if eval_passed:
            info = {
                "ok": True,
                "error_type": "",
                "message": "passed",
                "details": {"elapsed_sec": elapsed},
            }
            return True, info, None

        mismatch = summarize_eval_error(eval_error)
        info = {
            "ok": False,
            "error_type": "evaluation",
            "message": mismatch,
            "details": {},
        }
        return False, info, eval_error

    def _publish_flow(self, case_dir: Path, flow_dict: dict[str, Any]) -> None:
        write_json(case_dir / "flow.json", flow_dict)

    def build_case(self, case_name: str) -> dict[str, Any]:
        case_dir = self.repo_paths.data_root / case_name
        if not case_dir.is_dir():
            return {"case": case_name, "passed": False, "reason": "case_not_found"}

        try:
            solution_path = self._solution_path(case_name)
        except FileNotFoundError as exc:
            return {"case": case_name, "passed": False, "reason": f"solution_not_found: {exc}"}

        output_root = self._case_output_root(case_name)
        if output_root.exists() and self.options.force:
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True, exist_ok=True)

        session_state = {
            "task_dir": str(case_dir),
            "case_name": case_name,
            "solution_text": read_text(solution_path),
        }

        feedback: Optional[dict[str, Any]] = None
        passed = False
        reason = "max_rounds_reached"
        rounds: list[dict[str, Any]] = []
        final_flow: dict[str, Any] = {}
        last_eval_error: Optional[dict[str, Any]] = None

        for round_idx in range(1, self.options.max_rounds + 1):
            round_root = output_root / "rounds" / f"round-{round_idx}"
            round_root.mkdir(parents=True, exist_ok=True)

            flow_dict, raw_response, messages, parse_error = self.flow_agent.generate_flow(
                session_state, feedback=feedback
            )
            if raw_response:
                (round_root / "raw_response.txt").write_text(raw_response, encoding="utf-8")
            if messages:
                write_json(round_root / "messages.json", {"messages": messages})

            if parse_error:
                write_json(round_root / "parse_error.json", parse_error)
                reason = str(parse_error.get("message") or "flow_parse_failed")
                rounds.append({"round": round_idx, "passed": False, "reason": reason})
                feedback = {
                    "type": parse_error.get("type", "json_parse"),
                    "message": reason,
                    "details": parse_error.get("details", {}),
                }
                continue

            write_json(round_root / "flow.json", flow_dict)
            final_flow = flow_dict

            exec_ok, exec_info, eval_error = self._execute_flow_once(
                case_name=case_name,
                case_dir=case_dir,
                round_root=round_root,
                flow_dict=flow_dict,
            )
            write_json(round_root / "execution_summary.json", exec_info)
            if eval_error is not None:
                last_eval_error = eval_error

            if exec_ok:
                passed = True
                reason = "passed"
                rounds.append({"round": round_idx, "passed": True, "reason": "passed"})
                break

            reason = str(exec_info.get("message") or "flow_round_failed")
            rounds.append({"round": round_idx, "passed": False, "reason": reason})
            feedback = {
                "type": str(exec_info.get("error_type") or "execution"),
                "message": reason,
                "details": exec_info.get("details") or {},
            }

        if final_flow:
            write_json(output_root / "flow.json", final_flow)
            if passed and self.options.publish_flow:
                self._publish_flow(case_dir, final_flow)

        write_json(output_root / "rounds.json", {"rounds": rounds})
        final_status = {
            "case": case_name,
            "passed": passed,
            "reason": reason,
            "rounds_used": len(rounds),
            "model": self.options.model_name,
            "last_eval_error": last_eval_error,
        }
        write_json(output_root / "final_status.json", final_status)
        return final_status
