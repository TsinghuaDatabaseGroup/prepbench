from __future__ import annotations

import logging
import unittest

import pandas as pd

from py2flow.api import execute_flow_dict
from py2flow.errors import FlowExecutionError
from py2flow.operators.expr import eval_expr


class Py2FlowSecurityTest(unittest.TestCase):
    def test_eval_expr_blocks_untrusted_imports(self) -> None:
        with self.assertRaises(ImportError):
            eval_expr("__import__('os').getcwd()", pd.DataFrame({"x": [1]}))

    def test_eval_expr_allows_trusted_imports(self) -> None:
        result = eval_expr("__import__('math').sqrt(9)", pd.DataFrame({"x": [1]}))
        self.assertEqual(result, 3.0)

    def test_script_blocks_untrusted_imports(self) -> None:
        flow = {
            "id": "bad_script",
            "name": "Bad script",
            "nodes": {
                "src": {"kind": "input", "params": {"data": [{"x": 1}]}},
                "scripted": {
                    "kind": "script",
                    "inputs": {"in": "src"},
                    "params": {
                        "inline_code": "import os\n\ndef transform(df, pd, np):\n    return df"
                    },
                },
            },
        }

        logging.disable(logging.CRITICAL)
        try:
            with self.assertRaises(FlowExecutionError):
                execute_flow_dict(flow, keep="targets", targets=["scripted"])
        finally:
            logging.disable(logging.NOTSET)


if __name__ == "__main__":
    unittest.main()
