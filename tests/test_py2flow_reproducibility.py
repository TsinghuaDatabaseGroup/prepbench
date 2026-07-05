from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import pandas as pd

from py2flow.api import execute_flow_dict


class Py2FlowReproducibilityTest(unittest.TestCase):
    def test_aggregate_null_group_sentinel_does_not_collide(self) -> None:
        sentinel_like_value = "__PY2FLOW_NULL_GROUP__group__"
        flow = {
            "id": "agg_flow",
            "name": "Aggregate flow",
            "nodes": {
                "src": {
                    "kind": "input",
                    "params": {"data": [{"group": None}, {"group": sentinel_like_value}]},
                },
                "agg": {
                    "kind": "aggregate",
                    "inputs": {"in": "src"},
                    "params": {"group_keys": ["group"], "aggs": [{"as": "n", "func": "count"}]},
                },
            },
        }

        out = execute_flow_dict(flow, keep="targets", targets=["agg"])["agg"]
        self.assertEqual(len(out), 2)
        self.assertEqual(sorted(out["n"].tolist()), [1, 1])
        self.assertTrue(out["group"].isna().any())
        self.assertIn(sentinel_like_value, set(out["group"].dropna().tolist()))

    def test_output_write_order_reorders_without_schema_enforce(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            flow = {
                "id": "output_flow",
                "name": "Output flow",
                "nodes": {
                    "src": {
                        "kind": "input",
                        "params": {"data": [{"b": 2, "a": 1, "c": 3}]},
                    },
                    "out": {
                        "kind": "output",
                        "inputs": {"in": "src"},
                        "params": {
                            "path": "ordered.csv",
                            "schema": {"order": ["a", "b"]},
                            "write_order": True,
                        },
                    },
                },
            }

            execute_flow_dict(flow, base_path=base, keep="outputs")
            result = pd.read_csv(base / "ordered.csv")
            self.assertEqual(result.columns.tolist(), ["a", "b", "c"])


if __name__ == "__main__":
    unittest.main()
