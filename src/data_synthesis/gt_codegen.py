from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from agents.code_agent import CodeAgent
from core.case_assets import preferred_reference_solution_write_path

from .pipeline_common import (
    RepoPaths,
    evaluate_candidate,
    execute_solve_code,
    extract_solve_code,
    normalize_model_dir,
    profile_summary_text,
    read_text,
    summarize_eval_error,
    write_json,
)


@dataclass(frozen=True)
class GTCodeBuildOptions:
    model_name: str
    max_rounds: int = 5
    timeout_sec: int = 120
    publish_solution: bool = False
    force: bool = False


class GTCodeBuilder:
    def __init__(self, repo_paths: RepoPaths, options: GTCodeBuildOptions):
        self.repo_paths = repo_paths
        self.options = options
        self.code_agent = CodeAgent(options.model_name)
        self.model_dir = normalize_model_dir(options.model_name)

    def _case_output_root(self, case_name: str) -> Path:
        return self.repo_paths.output_root / "gt_codegen" / self.model_dir / case_name

    def _publish_solution(self, case_name: str, solve_code: str) -> None:
        target = preferred_reference_solution_write_path(case_name, root=self.repo_paths.solutions_root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(solve_code.rstrip() + "\n", encoding="utf-8")

    def build_case(self, case_name: str) -> dict[str, Any]:
        case_dir = self.repo_paths.data_root / case_name
        if not case_dir.is_dir():
            return {"case": case_name, "passed": False, "reason": f"case_not_found: {case_dir}"}

        query_path = case_dir / "query.md"
        input_dir = case_dir / "inputs"
        if not query_path.exists() or not input_dir.is_dir():
            return {
                "case": case_name,
                "passed": False,
                "reason": "missing_query_or_inputs",
            }

        output_root = self._case_output_root(case_name)
        if output_root.exists() and self.options.force:
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True, exist_ok=True)

        query_text = read_text(query_path)
        profile_summary = profile_summary_text(input_dir)
        session_state = {
            "task_dir": str(case_dir),
            "input_dir": str(input_dir),
            "model_name": self.options.model_name,
            "run_mode": "orig",
            "output_root": str(output_root),
            "query": query_text,
            "profile_summary": profile_summary,
        }

        passed = False
        reason = "max_rounds_reached"
        final_code = ""
        last_eval_error: Optional[dict[str, Any]] = None
        feedback: Optional[dict[str, Any]] = None
        rounds: list[dict[str, Any]] = []

        for round_idx in range(1, self.options.max_rounds + 1):
            round_root = output_root / "rounds" / f"round-{round_idx}"
            round_root.mkdir(parents=True, exist_ok=True)

            solve_code = ""
            raw_response = ""
            messages: list[dict[str, Any]] = []
            code_error: Optional[str] = None

            try:
                solve_code, raw_response, messages = self.code_agent.generate_code(session_state, feedback=feedback)
                if not solve_code.strip():
                    solve_code = extract_solve_code(raw_response)
                if not solve_code.strip():
                    code_error = "no_solve_code_generated"
            except Exception as exc:
                code_error = f"codegen_failed: {exc}"

            if raw_response:
                (round_root / "raw_response.txt").write_text(raw_response, encoding="utf-8")
            if messages:
                write_json(round_root / "messages.json", {"messages": messages})

            if code_error is not None:
                round_record = {
                    "round": round_idx,
                    "passed": False,
                    "reason": code_error,
                }
                rounds.append(round_record)
                write_json(round_root / "round_summary.json", round_record)
                feedback = {
                    "prev_code": final_code or "",
                    "execution": {"ok": False, "stderr": code_error},
                }
                reason = code_error
                continue

            final_code = solve_code
            exec_result = execute_solve_code(
                solve_code,
                input_dir=input_dir,
                work_dir=round_root,
                timeout=self.options.timeout_sec,
            )
            write_json(round_root / "execution.json", exec_result)

            exec_ok = bool(exec_result.get("ok"))
            eval_passed = False
            eval_error: Optional[dict[str, Any]] = None

            cand_dir = Path(str(exec_result.get("cand_dir", "")))
            if exec_ok and cand_dir.is_dir() and any(cand_dir.glob("*.csv")):
                eval_passed, eval_error = evaluate_candidate(case_name, cand_dir, self.repo_paths.gt_root)
                eval_payload = {
                    "passed": eval_passed,
                    "first_error": eval_error,
                }
                write_json(round_root / "evaluation.json", eval_payload)
                last_eval_error = eval_error
            elif exec_ok:
                eval_error = {
                    "error_type": "NO_OUTPUTS",
                    "message": "Execution succeeded but produced no output CSV files.",
                }
                write_json(round_root / "evaluation.json", {"passed": False, "first_error": eval_error})
                last_eval_error = eval_error

            if exec_ok and eval_passed:
                passed = True
                reason = "passed"
                round_record = {"round": round_idx, "passed": True, "reason": "passed"}
                rounds.append(round_record)
                write_json(round_root / "round_summary.json", round_record)
                break

            if not exec_ok:
                reason = str(exec_result.get("stderr") or "execution_failed")
                repair_message = f"Execution failed:\n{reason}"
            else:
                mismatch_text = summarize_eval_error(eval_error)
                reason = mismatch_text
                repair_message = (
                    "Execution succeeded, but output mismatched ground truth.\n"
                    f"{mismatch_text}\n"
                    "Revise solve() to match the expected output exactly."
                )

            feedback = {
                "prev_code": solve_code,
                "execution": {
                    "ok": False,
                    "stderr": repair_message,
                },
            }

            round_record = {
                "round": round_idx,
                "passed": False,
                "reason": reason,
            }
            rounds.append(round_record)
            write_json(round_root / "round_summary.json", round_record)

        final_payload = {
            "case": case_name,
            "passed": passed,
            "reason": reason,
            "rounds_used": len(rounds),
            "model": self.options.model_name,
            "last_eval_error": last_eval_error,
        }
        write_json(output_root / "final_status.json", final_payload)

        if final_code.strip():
            (output_root / "solution.py").write_text(final_code.rstrip() + "\n", encoding="utf-8")
        (output_root / "rounds.json").write_text(
            json.dumps(rounds, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        if passed and self.options.publish_solution and final_code.strip():
            self._publish_solution(case_name, final_code)
            final_payload["published"] = True
            write_json(output_root / "final_status.json", final_payload)

        return final_payload
