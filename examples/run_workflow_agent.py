"""Minimal reference harness for PrepBench workflow mode.

This is an example, not a required agent framework.
It sends CSV column names and preview rows to the configured agent endpoint.
For brevity it asks the model for workflow JSON directly; replace that step
with your own code-to-workflow logic if that is the agent you want to evaluate.
By default it clears the workspace result/ directory before each workflow attempt.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from prepbench.case_ids import normalize_case_id
from prepbench.submission_eval import evaluate_submission
from py2flow.api import run_flow_file
from simulator import LocalUserSimulatorAPI
from simulator.user_simulator import OpenAICompatibleClient


JSON_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)```", re.MULTILINE)


def load_repo_dotenv() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        if stripped.startswith("export "):
            stripped = stripped[len("export ") :].strip()
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def agent_client() -> tuple[OpenAICompatibleClient, float, int, dict[str, Any]]:
    load_repo_dotenv()
    model = os.getenv("PREPBENCH_AGENT_MODEL") or os.getenv("LLM_MODEL")
    base_url = os.getenv("PREPBENCH_AGENT_BASE_URL") or os.getenv("OPENAI_BASE_URL")
    api_key = os.getenv("PREPBENCH_AGENT_API_KEY") or os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not base_url:
        raise RuntimeError("Set PREPBENCH_AGENT_BASE_URL or OPENAI_BASE_URL for this example agent.")
    client = OpenAICompatibleClient(
        api_key=api_key or "",
        model_name=model or "",
        base_url=base_url,
        timeout=int(os.getenv("PREPBENCH_AGENT_TIMEOUT") or "120"),
        thinking_type=os.getenv("PREPBENCH_AGENT_THINKING") or None,
        reasoning_effort=os.getenv("PREPBENCH_AGENT_REASONING_EFFORT") or None,
    )
    temperature = float(os.getenv("PREPBENCH_AGENT_TEMPERATURE") or "0")
    max_tokens = int(os.getenv("PREPBENCH_AGENT_MAX_TOKENS") or "8192")
    return client, temperature, max_tokens, {"model": model, "base_url": base_url}


def messages(prompt: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "Return exactly the requested JSON. No markdown."},
        {"role": "user", "content": prompt},
    ]


def extract_json(text: str) -> dict[str, Any]:
    for candidate in [text.strip(), *(m.group(1).strip() for m in JSON_FENCE_RE.finditer(text))]:
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        try:
            parsed = json.loads(text[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
    raise ValueError(f"LLM response did not contain a JSON object: {text[:500]}")


def infer_case_id(workspace: Path) -> str:
    for part in [workspace.name, *[parent.name for parent in workspace.parents]]:
        if part.startswith("case"):
            return normalize_case_id(part)
    raise ValueError(f"Could not infer case id from workspace path: {workspace}")


def input_profile(input_root: Path, rows: int) -> str:
    chunks: list[str] = []
    for csv_path in sorted(input_root.glob("*.csv")):
        df = pd.read_csv(csv_path)
        chunks.append(
            "\n".join(
                [
                    f"### {csv_path.name}",
                    f"shape: {df.shape[0]} rows x {df.shape[1]} columns",
                    f"columns: {json.dumps(list(df.columns), ensure_ascii=False)}",
                    "preview_csv:",
                    df.head(rows).to_csv(index=False).strip(),
                ]
            )
        )
    if not chunks:
        raise FileNotFoundError(f"No CSV inputs found under {input_root}")
    return "\n\n".join(chunks)


def ask_clarifications(
    *,
    client: OpenAICompatibleClient,
    temperature: float,
    max_tokens: int,
    case_id: str,
    run_id: str,
    query: str,
    profile: str,
    max_questions: int,
) -> list[dict[str, Any]]:
    prompt = f"""Decide which requirement clarifications to ask before generating a PrepBench workflow.
Return ONLY JSON: {{"questions": ["atomic clarification question", "..."]}}
Ask at most {max_questions} questions. Do not ask for hidden outputs, code, full hidden specs, or raw data inspection.

Case id: {case_id}

Query:
{query}

Input profile:
{profile}
"""
    parsed = extract_json(client.generate(messages(prompt), temperature=temperature, max_tokens=max_tokens))
    questions = [str(q).strip() for q in parsed.get("questions", []) if str(q).strip()][:max_questions]
    if not questions:
        return []
    api = LocalUserSimulatorAPI(max_rounds=1, max_questions=max_questions, max_questions_per_ask=max_questions)
    session = api.start_session(case_id=case_id, run_id=run_id)
    return list(api.ask(session_id=session["session_id"], questions=questions).get("answers") or [])


def generate_workflow(
    *,
    client: OpenAICompatibleClient,
    temperature: float,
    max_tokens: int,
    case_id: str,
    query: str,
    profile: str,
    operator_guide: str,
    clarifications: list[dict[str, Any]],
    feedback: str,
) -> dict[str, Any]:
    feedback_text = f"\nPrevious attempt failed. Fix this feedback:\n{feedback}\n" if feedback else ""
    prompt = f"""Generate one valid PrepBench workflow JSON object. Return ONLY the JSON object.

Requirements:
- read only files under inputs/
- write final scored tables as output_*.csv, for example "output_01.csv"
- never write output paths with a result/ prefix
- prefer standard operators; use script nodes only when necessary
- keep every script.inline_code <= 1500 characters

Case id: {case_id}

Query:
{query}

Input profile:
{profile}

Clarification answers:
{json.dumps(clarifications, ensure_ascii=False, indent=2)}

Workflow operator guide:
{operator_guide}
{feedback_text}
"""
    return extract_json(client.generate(messages(prompt), temperature=temperature, max_tokens=max_tokens))


def run(args: argparse.Namespace) -> dict[str, Any]:
    workspace = Path(args.workspace).expanduser().resolve()
    case_id = normalize_case_id(args.case) if args.case else infer_case_id(workspace)
    query = (workspace / "query.md").read_text(encoding="utf-8")
    operator_guide = (workspace / "workflow_prompt.md").read_text(encoding="utf-8")
    input_root = workspace / "inputs"
    result_root = workspace / "result"
    profile = input_profile(input_root, args.input_preview_rows)
    client, temperature, max_tokens, backend = agent_client()

    trace: dict[str, Any] = {"workspace": str(workspace), "case_id": case_id, "backend": backend, "attempts": []}
    clarifications = ask_clarifications(
        client=client,
        temperature=temperature,
        max_tokens=max_tokens,
        case_id=case_id,
        run_id=args.run_id,
        query=query,
        profile=profile,
        max_questions=args.max_questions,
    )
    trace["clarifications"] = clarifications

    feedback = ""
    for attempt in range(1, args.max_attempts + 1):
        workflow = generate_workflow(
            client=client,
            temperature=temperature,
            max_tokens=max_tokens,
            case_id=case_id,
            query=query,
            profile=profile,
            operator_guide=operator_guide,
            clarifications=clarifications,
            feedback=feedback,
        )
        attempt_path = workspace / f"workflow_attempt_{attempt}.json"
        attempt_path.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (workspace / "workflow.json").write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if args.clean_result and result_root.exists():
            shutil.rmtree(result_root)
        result_root.mkdir(parents=True, exist_ok=True)
        exec_result = run_flow_file(workspace / "workflow.json", input_root=input_root, output_root=result_root, require_outputs=True)
        output_files = sorted(path.name for path in result_root.glob("output_*.csv"))
        evaluation = None
        ok = bool(exec_result.get("ok"))
        error = exec_result.get("error")
        if ok and args.evaluate:
            evaluation = evaluate_submission(run_root=workspace.parent, mode="workflow", case_id=case_id, gt_root=args.gt_root or None)
            aggregate = evaluation.get("aggregate") if isinstance(evaluation, dict) else None
            ok = isinstance(aggregate, dict) and bool(aggregate.get("passed"))
            if not ok:
                error = {"error_code": "evaluation_failed", "aggregate": aggregate, "first_case": (evaluation.get("cases") or [{}])[0]}

        record = {"attempt": attempt, "flow_path": str(attempt_path), "ok": ok, "error": error, "output_files": output_files, "evaluation": evaluation}
        trace["attempts"].append(record)
        (workspace / "workflow_agent_trace.json").write_text(json.dumps(trace, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if ok:
            return {"ok": True, "workspace": str(workspace), "case_id": case_id, "output_files": output_files, "evaluation": evaluation, "trace_path": str(workspace / "workflow_agent_trace.json")}
        feedback = json.dumps(error, ensure_ascii=False, indent=2)
    return {"ok": False, "workspace": str(workspace), "case_id": case_id, "error": trace["attempts"][-1]["error"], "trace_path": str(workspace / "workflow_agent_trace.json")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a minimal reference workflow agent on a prepared workflow workspace.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--case", default="")
    parser.add_argument("--run-id", default="workflow_agent")
    parser.add_argument("--max-questions", type=int, default=5)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--gt-root", default="")
    parser.add_argument(
        "--no-clean-result",
        dest="clean_result",
        action="store_false",
        help="Do not clear workspace result/ before each attempt.",
    )
    parser.add_argument(
        "--input-preview-rows",
        type=int,
        default=5,
        help="Number of input CSV rows included in prompts sent to the agent endpoint.",
    )
    parser.set_defaults(clean_result=True)
    return parser.parse_args()


def main() -> int:
    result = run(parse_args())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError, KeyError, pd.errors.ParserError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
