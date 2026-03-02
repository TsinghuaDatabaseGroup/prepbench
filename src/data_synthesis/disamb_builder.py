from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from agents.code_agent import CodeAgent
from core.case_assets import require_reference_solution_path

from .json_valid import validate_case
from .pipeline_common import (
    RepoPaths,
    execute_solve_code,
    extract_solve_code,
    normalize_model_dir,
    read_text,
    summarize_eval_error,
    write_json,
    evaluate_candidate,
)
from .synthesizer import Synthesizer


def _looks_like_no_ambiguity(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return False
    words = ("no ambiguity", "no ambiguities", "no-ambiguity", "unchanged", "no change")
    return any(w in t for w in words) and len(t) <= 120


@dataclass(frozen=True)
class DisambBuildOptions:
    model_name: str
    max_rewrite_rounds: int = 3
    max_validation_rounds: int = 3
    timeout_sec: int = 120
    force: bool = False


class DisambBuilder:
    def __init__(self, repo_paths: RepoPaths, options: DisambBuildOptions):
        self.repo_paths = repo_paths
        self.options = options
        self.synth = Synthesizer(model_full=options.model_name)
        self.code_agent = CodeAgent(options.model_name)
        self.model_dir = normalize_model_dir(options.model_name)

    def _case_output_root(self, case_name: str) -> Path:
        return self.repo_paths.output_root / "disamb_build" / self.model_dir / case_name

    def _reference_solution_path(self, case_name: str) -> Path:
        case_dir = self.repo_paths.data_root / case_name
        return require_reference_solution_path(case_dir, root=self.repo_paths.solutions_root)

    def _resolve_flow_text(self, case_dir: Path, case_name: str) -> str:
        candidates = [
            case_dir / "flow.json",
            case_dir / "flow_compressed.json",
            self.repo_paths.output_root / "workflow" / self.model_dir / case_name / "flow.json",
        ]
        for path in candidates:
            if path.exists():
                return read_text(path)
        return "{}"

    def _validate_query_full(
        self,
        *,
        case_name: str,
        case_dir: Path,
        query_full: str,
        output_root: Path,
    ) -> dict[str, Any]:
        input_dir = case_dir / "inputs"
        session_state = {
            "task_dir": str(case_dir),
            "input_dir": str(input_dir),
            "model_name": self.options.model_name,
            "run_mode": "disamb_only",
            "output_root": str(output_root),
            "query": query_full,
        }
        feedback: Optional[dict[str, Any]] = None
        final_reason = "max_rounds_reached"
        final_error: Optional[dict[str, Any]] = None
        passed = False
        rounds: list[dict[str, Any]] = []

        for round_idx in range(1, self.options.max_validation_rounds + 1):
            round_root = output_root / "validate" / f"round-{round_idx}"
            round_root.mkdir(parents=True, exist_ok=True)

            code = ""
            raw_response = ""
            messages: list[dict[str, Any]] = []
            code_error: Optional[str] = None

            try:
                code, raw_response, messages = self.code_agent.generate_code(session_state, feedback=feedback)
                if not code.strip():
                    code = extract_solve_code(raw_response)
                if not code.strip():
                    code_error = "no_solve_code_generated"
            except Exception as exc:
                code_error = f"codegen_failed: {exc}"

            if raw_response:
                (round_root / "raw_response.txt").write_text(raw_response, encoding="utf-8")
            if messages:
                write_json(round_root / "messages.json", {"messages": messages})

            if code_error:
                final_reason = code_error
                rounds.append({"round": round_idx, "passed": False, "reason": code_error})
                write_json(round_root / "round_summary.json", rounds[-1])
                feedback = {
                    "prev_code": code,
                    "execution": {"ok": False, "stderr": code_error},
                }
                continue

            exec_result = execute_solve_code(
                code,
                input_dir=input_dir,
                work_dir=round_root,
                timeout=self.options.timeout_sec,
            )
            write_json(round_root / "execution.json", exec_result)

            if not exec_result.get("ok"):
                stderr = str(exec_result.get("stderr") or "execution_failed")
                final_reason = stderr
                rounds.append({"round": round_idx, "passed": False, "reason": stderr})
                write_json(round_root / "round_summary.json", rounds[-1])
                feedback = {
                    "prev_code": code,
                    "execution": {"ok": False, "stderr": stderr},
                }
                continue

            cand_dir = Path(str(exec_result.get("cand_dir", "")))
            if not cand_dir.is_dir() or not any(cand_dir.glob("*.csv")):
                no_output_err = "Execution succeeded but produced no output CSV files."
                final_reason = no_output_err
                rounds.append({"round": round_idx, "passed": False, "reason": no_output_err})
                write_json(round_root / "round_summary.json", rounds[-1])
                feedback = {
                    "prev_code": code,
                    "execution": {"ok": False, "stderr": no_output_err},
                }
                continue

            eval_passed, eval_error = evaluate_candidate(case_name, cand_dir, self.repo_paths.gt_root)
            write_json(round_root / "evaluation.json", {"passed": eval_passed, "first_error": eval_error})
            final_error = eval_error
            if eval_passed:
                passed = True
                final_reason = "passed"
                rounds.append({"round": round_idx, "passed": True, "reason": "passed"})
                write_json(round_root / "round_summary.json", rounds[-1])
                break

            mismatch = summarize_eval_error(eval_error)
            final_reason = mismatch
            rounds.append({"round": round_idx, "passed": False, "reason": mismatch})
            write_json(round_root / "round_summary.json", rounds[-1])
            feedback = {
                "prev_code": code,
                "execution": {
                    "ok": False,
                    "stderr": (
                        "Execution succeeded, but output mismatched ground truth.\n"
                        f"{mismatch}\n"
                        "Revise solve() based only on request text and inputs."
                    ),
                },
            }

        return {
            "passed": passed,
            "reason": final_reason,
            "rounds": rounds,
            "error": final_error,
        }

    def _classify_failure(
        self,
        *,
        query: str,
        query_full: str,
        validation_result: dict[str, Any],
    ) -> dict[str, Any]:
        context = {
            "validation_reason": validation_result.get("reason"),
            "validation_error": validation_result.get("error"),
        }
        context_text = json.dumps(context, ensure_ascii=False, indent=2)
        try:
            return self.synth.classify_disamb_failure(
                query=query,
                query_full=query_full,
                failure_context=context_text,
            )
        except Exception:
            reason = str(validation_result.get("reason") or "").lower()
            if any(k in reason for k in ("parser", "decode", "dtype", "date", "encoding")):
                return {"category": "data_irregular", "reason": "heuristic: data parsing related failure"}
            return {"category": "coder_fail", "reason": "heuristic fallback"}

    def build_case(self, case_name: str) -> dict[str, Any]:
        case_dir = self.repo_paths.data_root / case_name
        if not case_dir.is_dir():
            return {"case": case_name, "passed": False, "reason": "case_not_found"}

        query_path = case_dir / "query.md"
        input_dir = case_dir / "inputs"
        try:
            ref_solution_path = self._reference_solution_path(case_name)
        except FileNotFoundError as exc:
            return {"case": case_name, "passed": False, "reason": f"missing_query_inputs_or_solution: {exc}"}
        if not query_path.exists() or not input_dir.is_dir() or not ref_solution_path.exists():
            return {"case": case_name, "passed": False, "reason": "missing_query_inputs_or_solution"}

        output_root = self._case_output_root(case_name)
        if output_root.exists() and self.options.force:
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True, exist_ok=True)

        query_text = read_text(query_path)
        solution_text = read_text(ref_solution_path)
        flow_text = self._resolve_flow_text(case_dir, case_name)

        rewrite_feedback = ""
        final_query_full = query_text
        validate_result: dict[str, Any] = {"passed": False, "reason": "not_run"}
        classification: dict[str, Any] = {"category": "coder_fail", "reason": "not_run"}

        for rewrite_round in range(1, self.options.max_rewrite_rounds + 1):
            round_root = output_root / "rewrite" / f"round-{rewrite_round}"
            round_root.mkdir(parents=True, exist_ok=True)

            candidate = self.synth.generate_query_full(
                query_text,
                solution_text,
                flow_text,
                feedback=rewrite_feedback,
            )
            if _looks_like_no_ambiguity(candidate) or candidate.strip() == query_text.strip():
                candidate = query_text
            (round_root / "query_full_candidate.md").write_text(candidate, encoding="utf-8")

            validate_result = self._validate_query_full(
                case_name=case_name,
                case_dir=case_dir,
                query_full=candidate,
                output_root=round_root,
            )
            write_json(round_root / "validate_summary.json", validate_result)

            final_query_full = candidate
            if validate_result.get("passed"):
                classification = {"category": "accepted", "reason": "validation_passed"}
                write_json(round_root / "classification.json", classification)
                break

            classification = self._classify_failure(
                query=query_text,
                query_full=candidate,
                validation_result=validate_result,
            )
            write_json(round_root / "classification.json", classification)

            # Only ambiguity failures should trigger rewriting in the next round.
            if classification.get("category") != "ambiguity":
                break
            rewrite_feedback = (
                "The previous rewrite is still ambiguous.\n"
                f"Classifier reason: {classification.get('reason', '')}\n"
                f"Validation summary: {validate_result.get('reason', '')}\n"
                "Rewrite query_full to remove remaining ambiguity while preserving intent."
            )

        query_full_path = output_root / "query_full.md"
        query_full_path.write_text(final_query_full, encoding="utf-8")

        amb_raw = self.synth.generate_ambiguities_raw(
            query_text,
            solution_text,
            final_query_full,
            flow_text,
        )
        amb_path = output_root / "amb_kb.json"
        amb_parse_error: Optional[str] = None
        try:
            parsed_amb = json.loads(amb_raw)
            amb_text = json.dumps(parsed_amb, ensure_ascii=False, indent=2)
        except Exception as exc:
            amb_parse_error = f"amb_json_parse_failed: {exc}"
            amb_text = amb_raw
        amb_path.write_text(amb_text, encoding="utf-8")

        # Validate assets from output directory without mutating data/case_xxx.
        try:
            parsed_flow = json.loads(flow_text)
            if isinstance(parsed_flow, dict) and isinstance(parsed_flow.get("nodes"), dict):
                write_json(output_root / "flow.json", parsed_flow)
        except Exception:
            pass
        # flow.json may be absent in current dataset layout, so we allow validation without node checks.
        amb_issues = validate_case(output_root, check_ref_lines=True)
        query_full_validation_passed = bool(validate_result.get("passed"))
        classification_category = str(classification.get("category") or "")
        # Following the paper protocol: if validation fails but failure is not due to ambiguity,
        # query_full is still considered acceptable for downstream use.
        query_full_accepted = query_full_validation_passed or (
            classification_category in {"data_irregular", "coder_fail"}
        )
        build_ok = (
            query_full_accepted
            and classification_category != "ambiguity"
            and amb_parse_error is None
            and not amb_issues
        )
        if classification_category == "ambiguity":
            reason = "remaining_ambiguity"
        elif not query_full_accepted:
            reason = "query_full_validation_failed"
        elif amb_parse_error is not None:
            reason = "amb_json_parse_failed"
        elif amb_issues:
            reason = "amb_kb_validation_failed"
        else:
            reason = "passed"

        final_status = {
            "case": case_name,
            "passed": build_ok,
            "reason": reason,
            "query_full_validation_passed": query_full_validation_passed,
            "query_full_accepted": query_full_accepted,
            "classification": classification,
            "query_full_reason": validate_result.get("reason"),
            "amb_parse_error": amb_parse_error,
            "amb_kb_issues": amb_issues,
            "model": self.options.model_name,
        }
        write_json(output_root / "final_status.json", final_status)
        return final_status
