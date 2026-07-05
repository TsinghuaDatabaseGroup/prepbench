from __future__ import annotations

import json
import unittest
from pathlib import Path

from py2flow.api import execute_flow_dict
from py2flow.errors import FlowValidationError


ROOT = Path(__file__).resolve().parents[1]


def run_target(nodes: dict[str, object], target: str):
    flow = {"id": "test_flow", "name": "Test flow", "nodes": nodes}
    return execute_flow_dict(flow, keep="targets", targets=[target])[target]


class Py2FlowContractTest(unittest.TestCase):
    def test_expand_is_schema_object_and_executes(self) -> None:
        schema = json.loads((ROOT / "src/py2flow/flow.schema.json").read_text(encoding="utf-8"))
        expand_schema = schema["$defs"]["project_params"]["properties"]["expand"]
        self.assertEqual(expand_schema["type"], "object")

        out = run_target(
            {
                "src": {
                    "kind": "input",
                    "params": {"data": [{"grp": "a", "start": 1}, {"grp": "b", "start": 2}]},
                },
                "expanded": {
                    "kind": "project",
                    "inputs": {"in": "src"},
                    "params": {
                        "expand": {
                            "keys": ["grp"],
                            "from_col": "start",
                            "to_value": 3,
                            "expand_col": "step",
                        }
                    },
                },
            },
            "expanded",
        )

        self.assertEqual(out[["grp", "step"]].to_dict(orient="records"), [
            {"grp": "a", "step": 1},
            {"grp": "a", "step": 2},
            {"grp": "a", "step": 3},
            {"grp": "b", "step": 2},
            {"grp": "b", "step": 3},
        ])

    def test_map_top_level_when_controls_rows(self) -> None:
        out = run_target(
            {
                "src": {
                    "kind": "input",
                    "params": {
                        "data": [
                            {"name": "alice", "flag": True},
                            {"name": "Bob", "flag": False},
                        ]
                    },
                },
                "mapped": {
                    "kind": "project",
                    "inputs": {"in": "src"},
                    "params": {"map": [{"col": "name", "op": "upper", "when": "flag"}]},
                },
            },
            "mapped",
        )

        self.assertEqual(out["name"].tolist(), ["ALICE", "Bob"])

    def test_map_when_conflict_fails_validation(self) -> None:
        with self.assertRaises(FlowValidationError):
            run_target(
                {
                    "src": {
                        "kind": "input",
                        "params": {"data": [{"name": "alice", "flag": True}]},
                    },
                    "mapped": {
                        "kind": "project",
                        "inputs": {"in": "src"},
                        "params": {
                            "map": [
                                {
                                    "col": "name",
                                    "op": "upper",
                                    "when": "flag",
                                    "args": {"when": "not flag"},
                                }
                            ]
                        },
                    },
                },
                "mapped",
            )

    def test_script_metadata_defaults(self) -> None:
        out = run_target(
            {
                "src": {"kind": "input", "params": {"data": [{"x": 1}, {"x": 2}]}},
                "scripted": {
                    "kind": "script",
                    "inputs": {"in": "src"},
                    "params": {
                        "inline_code": "def transform(df, pd, np):\n    return df.assign(y=df['x'] + 1)"
                    },
                },
            },
            "scripted",
        )

        self.assertEqual(out["y"].tolist(), [2, 3])


if __name__ == "__main__":
    unittest.main()
