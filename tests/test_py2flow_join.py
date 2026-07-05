from __future__ import annotations

import unittest

import pandas as pd

from py2flow.api import execute_flow_dict
from py2flow.errors import FlowValidationError


def run_join(
    params: dict[str, object],
    *,
    left_data: list[dict[str, object]] | None = None,
    right_data: list[dict[str, object]] | None = None,
):
    if left_data is None:
        left_data = [
            {"needle": "abc", "left_id": 1},
            {"needle": "zzz", "left_id": 2},
        ]
    if right_data is None:
        right_data = [
            {"hay": "prefix abc suffix", "label": "long"},
            {"hay": "abc", "label": "short"},
            {"hay": "abc", "label": "tie"},
        ]
    flow = {
        "id": "join_flow",
        "name": "Join flow",
        "nodes": {
            "left": {
                "kind": "input",
                "params": {"data": left_data},
            },
            "right": {
                "kind": "input",
                "params": {"data": right_data},
            },
            "joined": {
                "kind": "join",
                "inputs": {"left": "left", "right": "right"},
                "params": params,
            },
        },
    }
    return execute_flow_dict(flow, keep="targets", targets=["joined"])["joined"]


class Py2FlowJoinTest(unittest.TestCase):
    def test_fuzzy_match_uses_specific_match_and_stable_tie(self) -> None:
        out = run_join(
            {
                "left_on": ["needle"],
                "right_on": ["hay"],
                "how": "left",
                "fuzzy_match": True,
                "select_left": ["needle", "left_id"],
                "select_right": ["label", "hay"],
            }
        )

        self.assertEqual(out.loc[0, "label"], "short")
        self.assertEqual(out.loc[0, "hay"], "abc")
        self.assertTrue(pd.isna(out.loc[1, "label"]))

    def test_fuzzy_inner_skips_unmatched_rows(self) -> None:
        out = run_join(
            {
                "left_on": ["needle"],
                "right_on": ["hay"],
                "how": "inner",
                "fuzzy_match": True,
            }
        )

        self.assertEqual(out["left_id"].tolist(), [1])

    def test_fuzzy_inner_no_match_keeps_columns(self) -> None:
        out = run_join(
            {
                "left_on": ["needle"],
                "right_on": ["hay"],
                "how": "inner",
                "fuzzy_match": True,
                "select_left": ["needle", "left_id"],
                "select_right": ["label", "hay"],
            },
            left_data=[{"needle": "never", "left_id": 1}],
        )

        self.assertEqual(out.columns.tolist(), ["needle", "left_id", "label", "hay"])
        self.assertTrue(out.empty)

    def test_fuzzy_match_survives_non_default_right_index(self) -> None:
        # A right table filtered upstream carries a non-default index. The fuzzy
        # matcher must key off positional offsets, not index labels, so that its
        # .iloc lookup stays correct (regression: IndexError / wrong-row merge).
        flow = {
            "id": "join_flow",
            "name": "Join flow",
            "nodes": {
                "left": {
                    "kind": "input",
                    "params": {"data": [{"needle": "abc", "left_id": 1}]},
                },
                "right_raw": {
                    "kind": "input",
                    "params": {
                        "data": [
                            {"hay": "drop me", "label": "drop", "keep": False},
                            {"hay": "prefix abc suffix", "label": "long", "keep": True},
                            {"hay": "abc", "label": "short", "keep": True},
                        ]
                    },
                },
                "right": {
                    "kind": "filter",
                    "inputs": {"in": "right_raw"},
                    "params": {"predicate": "keep"},
                },
                "joined": {
                    "kind": "join",
                    "inputs": {"left": "left", "right": "right"},
                    "params": {
                        "left_on": ["needle"],
                        "right_on": ["hay"],
                        "how": "left",
                        "fuzzy_match": True,
                        "select_left": ["needle", "left_id"],
                        "select_right": ["label", "hay"],
                    },
                },
            },
        }
        out = execute_flow_dict(flow, keep="targets", targets=["joined"])["joined"]
        self.assertEqual(out.loc[0, "label"], "short")
        self.assertEqual(out.loc[0, "hay"], "abc")

    def test_fuzzy_invalid_how_fails_validation(self) -> None:
        with self.assertRaises(FlowValidationError):
            run_join(
                {
                    "left_on": ["needle"],
                    "right_on": ["hay"],
                    "how": "full",
                    "fuzzy_match": True,
                }
            )


if __name__ == "__main__":
    unittest.main()
