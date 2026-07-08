from __future__ import annotations

import json
import argparse
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_ROOT = REPO_ROOT / "examples"
if str(EXAMPLES_ROOT) not in sys.path:
    sys.path.insert(0, str(EXAMPLES_ROOT))

import run_workflow_agent as workflow_example


class FakeChatClient:
    def __init__(self, responses: list[str]) -> None:
        self.responses = responses
        self.prompts: list[str] = []

    def generate(self, messages: list[dict[str, str]], *, temperature: float, max_tokens: int) -> str:
        self.prompts.append(messages[-1]["content"])
        if not self.responses:
            raise AssertionError("FakeChatClient has no remaining responses")
        return self.responses.pop(0)


class FakeSimulatorAPI:
    def start_session(self, *, case_id: str, run_id: str) -> dict[str, Any]:
        return {
            "session_id": "sess_fake",
            "case_id": case_id,
            "run_id": run_id,
            "max_rounds": 1,
            "max_questions": 5,
            "max_questions_per_ask": 5,
            "ambiguity_count": 1,
        }

    def ask(self, *, session_id: str, questions: list[str], round: int | None = None) -> dict[str, Any]:
        return {
            "session_id": session_id,
            "case_id": "case_001",
            "run_id": "fake",
            "round": 1,
            "answers": [
                {
                    "sub_question": questions[0],
                    "classification": "hit",
                    "source": "lib",
                    "answer": "Use the input as-is.",
                    "ref": "fake_ref",
                }
            ],
            "budget": {"max_rounds": 1, "used_rounds": 1, "max_questions": 5, "used_questions": 1, "remaining_questions": 4},
            "done": True,
            "next_round": None,
            "parse_error": None,
        }


class WorkflowAgentTest(unittest.TestCase):
    def test_extract_json_object_accepts_fenced_json(self) -> None:
        parsed = workflow_example.extract_json('before\n```json\n{"x": 1}\n```\nafter')
        self.assertEqual(parsed, {"x": 1})

    def test_build_input_profile_includes_shape_columns_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_root = Path(tmp)
            (input_root / "input_01.csv").write_text("a,b\n1,2\n3,4\n", encoding="utf-8")

            profile = workflow_example.input_profile(input_root, rows=1)

            self.assertIn("input_01.csv", profile)
            self.assertIn("shape: 2 rows x 2 columns", profile)
            self.assertIn('"a"', profile)
            self.assertIn("a,b\n1,2", profile)

    def test_run_workflow_agent_retries_with_executor_error_feedback(self) -> None:
        bad_flow = {
            "id": "bad",
            "name": "Bad",
            "nodes": {
                "a": {"kind": "input", "params": {"data": [{"x": 1}]}},
                "b": {"kind": "input", "params": {"data": [{"x": 2}]}},
                "u": {"kind": "union", "inputs": {"items": ["a", "b"]}, "params": {}},
                "out": {"kind": "output", "inputs": {"in": "u"}, "params": {"path": "output_01.csv"}},
            },
        }
        good_flow = {
            "id": "good",
            "name": "Good",
            "nodes": {
                "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}},
                "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "output_01.csv"}},
            },
        }
        client = FakeChatClient(
            [
                json.dumps({"questions": ["Should the output preserve input rows?"]}),
                json.dumps(bad_flow),
                json.dumps(good_flow),
            ]
        )

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "case_001"
            (workspace / "inputs").mkdir(parents=True)
            (workspace / "result").mkdir()
            (workspace / "query.md").write_text("Output the input table.", encoding="utf-8")
            (workspace / "workflow_prompt.md").write_text("Use valid PrepBench workflow JSON.", encoding="utf-8")
            (workspace / "inputs" / "input_01.csv").write_text("x\n1\n", encoding="utf-8")

            args = argparse.Namespace(
                workspace=str(workspace),
                case="",
                run_id="fake",
                max_questions=5,
                max_attempts=2,
                evaluate=False,
                gt_root="",
                clean_result=True,
                input_preview_rows=5,
            )
            with (
                patch.object(workflow_example, "agent_client", return_value=(client, 0.0, 8192, {"model": "fake"})),
                patch.object(workflow_example, "LocalUserSimulatorAPI", return_value=FakeSimulatorAPI()),
            ):
                result = workflow_example.run(args)

            trace = json.loads((workspace / "workflow_agent_trace.json").read_text(encoding="utf-8"))
            self.assertTrue(result["ok"])
            self.assertEqual(len(trace["attempts"]), 2)
            self.assertEqual(trace["attempts"][0]["error"]["error_code"], "union_distinct_required")
            self.assertTrue((workspace / "result" / "output_01.csv").is_file())
            self.assertIn("Previous attempt failed", client.prompts[-1])
            self.assertIn("union_distinct_required", client.prompts[-1])


if __name__ == "__main__":
    unittest.main()
