from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from prepbench.workspaces import prepare_case_workspace


REPO_ROOT = Path(__file__).resolve().parents[1]


class PrepareRunTest(unittest.TestCase):
    def test_clarified_workspace_uses_full_query_and_file_symlinked_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "clarified"
            workspace = prepare_case_workspace(
                case_id="case_001",
                mode="clarified",
                run_root=run_root,
                force=True,
            )

            self.assertEqual((workspace / "query.md").resolve(), (REPO_ROOT / "data" / "case_001" / "query_full.md").resolve())
            self.assertTrue((workspace / "inputs").is_dir())
            self.assertFalse((workspace / "inputs").is_symlink())
            input_files = sorted((workspace / "inputs").glob("input_*.csv"))
            self.assertTrue(input_files)
            self.assertTrue(all(path.is_symlink() for path in input_files))
            self.assertTrue((workspace / "result").is_dir())
            self.assertFalse((workspace / "clarification_guide.md").exists())
            self.assertFalse((workspace / "workflow_prompt.md").exists())

    def test_interactive_workspace_uses_original_query_and_clarification_guide(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "interactive"
            workspace = prepare_case_workspace(
                case_id="1",
                mode="interactive",
                run_root=run_root,
                force=True,
            )

            self.assertEqual((workspace / "query.md").resolve(), (REPO_ROOT / "data" / "case_001" / "query.md").resolve())
            clarification_guide = workspace / "clarification_guide.md"
            self.assertTrue(clarification_guide.is_file())
            guide_text = clarification_guide.read_text(encoding="utf-8")
            self.assertIn("LocalUserSimulatorAPI", guide_text)
            self.assertIn("may refuse questions", guide_text)
            self.assertFalse((workspace / "workflow_prompt.md").exists())

    def test_workflow_workspace_adds_operator_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "workflow"
            workspace = prepare_case_workspace(
                case_id="case_001",
                mode="workflow",
                run_root=run_root,
                force=True,
            )

            prompt = workspace / "workflow_prompt.md"
            self.assertTrue(prompt.is_symlink())
            self.assertEqual(prompt.resolve(), (REPO_ROOT / "src" / "agents" / "prompts" / "workflow_operators.md").resolve())

    def test_refuses_existing_workspace_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "clarified"
            prepare_case_workspace(case_id="case_001", mode="clarified", run_root=run_root)
            with self.assertRaises(FileExistsError):
                prepare_case_workspace(case_id="case_001", mode="clarified", run_root=run_root)

    def test_refuses_run_root_mode_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_root = Path(tmp) / "agent" / "clarified"
            with self.assertRaisesRegex(ValueError, "does not match run-root mode segment"):
                prepare_case_workspace(case_id="case_001", mode="workflow", run_root=run_root)

    def test_prepare_run_all_uses_gt_case_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            gt_root = tmp_path / "gt"
            (gt_root / "case_001").mkdir(parents=True)
            (gt_root / "case_002").mkdir(parents=True)
            run_root = tmp_path / "agent" / "clarified"

            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "prepare_run.py"),
                    "--mode",
                    "clarified",
                    "--all",
                    "--run-root",
                    str(run_root),
                    "--gt-root",
                    str(gt_root),
                ],
                cwd=REPO_ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            summary = json.loads(completed.stdout)
            self.assertEqual(summary["total"], 2)
            self.assertEqual(summary["cases"], ["case_001", "case_002"])
            self.assertTrue((run_root / "case_001" / "query.md").exists())
            self.assertTrue((run_root / "case_002" / "query.md").exists())


if __name__ == "__main__":
    unittest.main()
