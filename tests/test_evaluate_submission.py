from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from prepbench.submission_eval import evaluate_submission


REPO_ROOT = Path(__file__).resolve().parents[1]


class EvaluateSubmissionTest(unittest.TestCase):
    def test_evaluates_result_directory_and_writes_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "clarified"
            result_dir = run_root / "case_001" / "result"
            result_dir.mkdir(parents=True)
            shutil.copy2(REPO_ROOT / "src" / "evaluate" / "gt" / "case_001" / "output_01.csv", result_dir / "output_01.csv")

            summary = evaluate_submission(run_root=run_root, mode="clarified", case_id="case_001")

            self.assertTrue(summary["aggregate"]["passed"])
            summary_json = run_root / "evaluation" / "summary.json"
            summary_csv = run_root / "evaluation" / "summary.csv"
            self.assertTrue(summary_json.is_file())
            self.assertTrue(summary_csv.is_file())
            loaded = json.loads(summary_json.read_text(encoding="utf-8"))
            self.assertEqual(loaded["aggregate"]["correct"], 1)

    def test_missing_outputs_are_not_found_and_not_passed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "workflow"
            (run_root / "case_001" / "result").mkdir(parents=True)

            summary = evaluate_submission(run_root=run_root, mode="workflow", case_id="case_001")

            self.assertFalse(summary["aggregate"]["passed"])
            self.assertEqual(summary["cases"][0]["error_type"], "NOT_FOUND")

    def test_default_evaluation_counts_gt_cases_not_only_present_workspaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            gt_root = tmp_path / "gt"
            shutil.copytree(REPO_ROOT / "src" / "evaluate" / "gt" / "case_001", gt_root / "case_001")
            shutil.copytree(REPO_ROOT / "src" / "evaluate" / "gt" / "case_002", gt_root / "case_002")

            run_root = tmp_path / "agent" / "clarified"
            result_dir = run_root / "case_001" / "result"
            result_dir.mkdir(parents=True)
            shutil.copy2(gt_root / "case_001" / "output_01.csv", result_dir / "output_01.csv")

            summary = evaluate_submission(run_root=run_root, mode="clarified", gt_root=gt_root)

            self.assertFalse(summary["aggregate"]["passed"])
            self.assertEqual(summary["aggregate"]["total"], 2)
            self.assertEqual(summary["aggregate"]["correct"], 1)
            self.assertEqual(summary["aggregate"]["missing"], 1)
            self.assertEqual(summary["cases"][1]["case_name"], "case_002")
            self.assertEqual(summary["cases"][1]["error_type"], "NOT_FOUND")

    def test_mode_must_match_run_root_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "clarified"
            (run_root / "case_001" / "result").mkdir(parents=True)

            with self.assertRaises(ValueError):
                evaluate_submission(run_root=run_root, mode="workflow", case_id="case_001")


if __name__ == "__main__":
    unittest.main()
