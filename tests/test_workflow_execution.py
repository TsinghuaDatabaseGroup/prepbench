from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from py2flow.api import execute_flow_file
from py2flow.exec_flow import exec_flow


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


if __name__ == "__main__":
    unittest.main()
