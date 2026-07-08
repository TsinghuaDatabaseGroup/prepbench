from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from py2flow.api import execute_flow_file, run_flow_file
from py2flow.exec_flow import exec_flow

REPO_ROOT = Path(__file__).resolve().parents[1]


class WorkflowExecutionTest(unittest.TestCase):
    def test_exec_flow_maps_input_and_output_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            flow_dir = root / "workflow"
            input_root = root / "inputs"
            output_root = root / "cand"
            flow_dir.mkdir()
            input_root.mkdir()

            (input_root / "input_01.csv").write_text(
                "qty,price\n2,5\n3,7\n",
                encoding="utf-8",
            )
            flow_path = flow_dir / "flow.json"
            flow_path.write_text(
                """
{
  "id": "demo_flow",
  "name": "Demo flow",
  "nodes": {
    "orders": {
      "kind": "input",
      "params": {"path": "inputs/input_01.csv"}
    },
    "with_total": {
      "kind": "project",
      "inputs": {"in": "orders"},
      "params": {
        "compute": [{"as": "total", "expr": "qty * price"}],
        "select": ["qty", "price"]
      }
    },
    "final": {
      "kind": "project",
      "inputs": {"in": "with_total"},
      "params": {"select": ["qty", "price", "total"]}
    },
    "out": {
      "kind": "output",
      "inputs": {"in": "final"},
      "params": {"path": "output_01.csv"}
    }
  }
}
""".strip(),
                encoding="utf-8",
            )

            exec_flow(flow_path=flow_path, input_root=input_root, output_root=output_root)

            output = pd.read_csv(output_root / "output_01.csv")
            self.assertEqual(output.to_dict(orient="list"), {"qty": [2, 3], "price": [5, 7], "total": [10, 21]})

    def test_execute_flow_file_uses_workspace_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            input_root = workspace / "inputs"
            input_root.mkdir()
            (input_root / "input_01.csv").write_text(
                "qty,price\n2,5\n3,7\n",
                encoding="utf-8",
            )
            (workspace / "flow.json").write_text(
                """
{
  "id": "demo_flow",
  "name": "Demo flow",
  "nodes": {
    "orders": {
      "kind": "input",
      "params": {"path": "inputs/input_01.csv"}
    },
    "with_total": {
      "kind": "project",
      "inputs": {"in": "orders"},
      "params": {
        "compute": [{"as": "total", "expr": "qty * price"}],
        "select": ["qty", "price"]
      }
    },
    "final": {
      "kind": "project",
      "inputs": {"in": "with_total"},
      "params": {"select": ["qty", "price", "total"]}
    },
    "out": {
      "kind": "output",
      "inputs": {"in": "final"},
      "params": {"path": "output_01.csv"}
    }
  }
}
""".strip(),
                encoding="utf-8",
            )
            original_cwd = Path.cwd()
            try:
                os.chdir(workspace)
                execute_flow_file("flow.json")
            finally:
                os.chdir(original_cwd)

            output = pd.read_csv(workspace / "result" / "output_01.csv")
            self.assertEqual(output.to_dict(orient="list"), {"qty": [2, 3], "price": [5, 7], "total": [10, 21]})

    def test_run_flow_file_returns_success_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            input_root = workspace / "inputs"
            result_root = workspace / "result"
            input_root.mkdir()
            (input_root / "input_01.csv").write_text("x\n1\n", encoding="utf-8")
            flow_path = workspace / "flow.json"
            flow_path.write_text(
                """
{
  "id": "ok",
  "name": "OK",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}},
    "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            payload = run_flow_file(flow_path, input_root=input_root, output_root=result_root)

            self.assertTrue(payload["ok"])
            self.assertIsNone(payload["error"])
            self.assertTrue((result_root / "output_01.csv").is_file())

    def test_run_flow_file_returns_structured_error_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            input_root = workspace / "inputs"
            result_root = workspace / "result"
            input_root.mkdir()
            flow_path = workspace / "bad_union.json"
            flow_path.write_text(
                """
{
  "id": "bad_union",
  "name": "Bad union",
  "nodes": {
    "a": {"kind": "input", "params": {"data": [{"x": 1}]}},
    "b": {"kind": "input", "params": {"data": [{"x": 2}]}},
    "u": {"kind": "union", "inputs": {"items": ["a", "b"]}, "params": {}},
    "out": {"kind": "output", "inputs": {"in": "u"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            payload = run_flow_file(flow_path, input_root=input_root, output_root=result_root)

            self.assertFalse(payload["ok"])
            self.assertIsNone(payload["result"])
            error = payload["error"]
            self.assertIsInstance(error, dict)
            self.assertEqual(error["node_id"], "u")
            self.assertEqual(error["step_kind"], "union")
            self.assertEqual(error["field"], "distinct")
            self.assertEqual(error["error_code"], "union_distinct_required")

    def test_run_flow_file_can_require_scored_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            input_root = workspace / "inputs"
            result_root = workspace / "result"
            input_root.mkdir()
            (input_root / "input_01.csv").write_text("x\n1\n", encoding="utf-8")
            flow_path = workspace / "no_output.json"
            flow_path.write_text(
                """
{
  "id": "no_output",
  "name": "No output",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            payload = run_flow_file(flow_path, input_root=input_root, output_root=result_root, require_outputs=True)

            self.assertFalse(payload["ok"])
            self.assertIsNone(payload["result"])
            error = payload["error"]
            self.assertIsInstance(error, dict)
            self.assertEqual(error["error_code"], "missing_output_files")
            self.assertEqual(error["field"], "output_root")

    def test_exec_flow_rejects_input_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            flow_dir = root / "workflow"
            input_root = root / "inputs"
            output_root = root / "result"
            flow_dir.mkdir()
            input_root.mkdir()
            flow_path = flow_dir / "flow.json"
            flow_path.write_text(
                """
{
  "id": "bad_input",
  "name": "Bad input",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/../secret.csv"}},
    "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "input path escapes configured root"):
                exec_flow(flow_path=flow_path, input_root=input_root, output_root=output_root)

    def test_exec_flow_allows_input_symlink_inside_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            flow_dir = root / "workflow"
            input_root = root / "inputs"
            real_inputs = root / "real_inputs"
            output_root = root / "result"
            flow_dir.mkdir()
            input_root.mkdir()
            real_inputs.mkdir()
            (real_inputs / "input_01.csv").write_text("x\n1\n", encoding="utf-8")
            (input_root / "input_01.csv").symlink_to(real_inputs / "input_01.csv")
            flow_path = flow_dir / "flow.json"
            flow_path.write_text(
                """
{
  "id": "symlink_input",
  "name": "Symlink input",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}},
    "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            exec_flow(flow_path=flow_path, input_root=input_root, output_root=output_root)

            output = pd.read_csv(output_root / "output_01.csv")
            self.assertEqual(output.to_dict(orient="list"), {"x": [1]})

    def test_exec_flow_rejects_output_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            flow_dir = root / "workflow"
            input_root = root / "inputs"
            output_root = root / "result"
            flow_dir.mkdir()
            input_root.mkdir()
            (input_root / "input_01.csv").write_text("x\n1\n", encoding="utf-8")
            flow_path = flow_dir / "flow.json"
            flow_path.write_text(
                """
{
  "id": "bad_output",
  "name": "Bad output",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}},
    "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "../escaped.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "output path escapes configured root"):
                exec_flow(flow_path=flow_path, input_root=input_root, output_root=output_root)
            self.assertFalse((root / "escaped.csv").exists())

    def test_execute_workflow_cli_reports_flow_errors_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_root = root / "inputs"
            input_root.mkdir()
            flow_path = root / "bad_flow.json"
            flow_path.write_text(
                """
{
  "id": "bad",
  "name": "Bad",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/missing.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "execute_workflow.py"),
                    "--flow-path",
                    str(flow_path),
                    "--input-root",
                    str(input_root),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 2)
            self.assertIn("error:", completed.stderr)
            self.assertNotIn("Traceback", completed.stderr)

    def test_execute_workflow_cli_json_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_root = root / "inputs"
            output_root = root / "result"
            input_root.mkdir()
            flow_path = root / "bad_union.json"
            flow_path.write_text(
                """
{
  "id": "bad_union",
  "name": "Bad union",
  "nodes": {
    "a": {"kind": "input", "params": {"data": [{"x": 1}]}},
    "b": {"kind": "input", "params": {"data": [{"x": 2}]}},
    "u": {"kind": "union", "inputs": {"items": ["a", "b"]}, "params": {}},
    "out": {"kind": "output", "inputs": {"in": "u"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "execute_workflow.py"),
                    "--flow-path",
                    str(flow_path),
                    "--input-root",
                    str(input_root),
                    "--output-root",
                    str(output_root),
                    "--json-errors",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 1)
            payload = json.loads(completed.stderr)
            self.assertEqual(payload["node_id"], "u")
            self.assertEqual(payload["step_kind"], "union")
            self.assertEqual(payload["field"], "distinct")
            self.assertEqual(payload["error_code"], "union_distinct_required")
            self.assertIn("distinct", payload["help"])

    def test_execute_workflow_cli_requires_scored_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_root = root / "inputs"
            output_root = root / "result"
            input_root.mkdir()
            (input_root / "input_01.csv").write_text("x\n1\n", encoding="utf-8")
            flow_path = root / "no_output.json"
            flow_path.write_text(
                """
{
  "id": "no_output",
  "name": "No output",
  "nodes": {
    "src": {"kind": "input", "params": {"path": "inputs/input_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "execute_workflow.py"),
                    "--flow-path",
                    str(flow_path),
                    "--input-root",
                    str(input_root),
                    "--output-root",
                    str(output_root),
                    "--json-errors",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 1)
            payload = json.loads(completed.stderr)
            self.assertEqual(payload["error_code"], "missing_output_files")
            self.assertEqual(payload["field"], "output_root")

    def test_execute_workflow_cli_dry_run_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_root = root / "inputs"
            output_root = root / "result"
            input_root.mkdir()
            flow_path = root / "flow.json"
            flow_path.write_text(
                """
{
  "id": "dry_run",
  "name": "Dry run",
  "nodes": {
    "src": {"kind": "input", "params": {"data": [{"x": 1}]}},
    "out": {"kind": "output", "inputs": {"in": "src"}, "params": {"path": "output_01.csv"}}
  }
}
""".strip(),
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "execute_workflow.py"),
                    "--flow-path",
                    str(flow_path),
                    "--input-root",
                    str(input_root),
                    "--output-root",
                    str(output_root),
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(completed.returncode, 0)
            self.assertIn("node=src", completed.stdout)
            self.assertFalse((output_root / "output_01.csv").exists())


if __name__ == "__main__":
    unittest.main()
