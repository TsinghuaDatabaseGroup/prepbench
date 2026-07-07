from __future__ import annotations

import unittest
from unittest.mock import patch

from simulator.user_simulator import OpenAICompatibleClient, _default_thinking_type, _validate_parsed_answers


class UserSimulatorConfigTest(unittest.TestCase):
    def test_official_deepseek_v4_defaults_to_non_thinking(self) -> None:
        with patch.dict("os.environ", {"PREPBENCH_SIMULATOR_THINKING": ""}):
            thinking_type = _default_thinking_type("https://api.deepseek.com", "deepseek-v4-flash")
        client = OpenAICompatibleClient(
            api_key="dummy",
            model_name="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
            timeout=120,
            thinking_type=thinking_type,
        )

        self.assertEqual(thinking_type, "disabled")
        payload = client._build_payload(
            [{"role": "user", "content": "hello"}],
            temperature=0,
            max_tokens=16,
        )
        self.assertEqual(payload["thinking"], {"type": "disabled"})
        self.assertNotIn("reasoning_effort", payload)

    def test_non_deepseek_backend_does_not_send_thinking_by_default(self) -> None:
        with patch.dict("os.environ", {"PREPBENCH_SIMULATOR_THINKING": ""}):
            thinking_type = _default_thinking_type("https://api.openai.com/v1", "gpt-4.1-mini")
        client = OpenAICompatibleClient(
            api_key="dummy",
            model_name="gpt-4.1-mini",
            base_url="https://api.openai.com/v1",
            timeout=120,
            thinking_type=thinking_type,
        )

        payload = client._build_payload(
            [{"role": "user", "content": "hello"}],
            temperature=0,
            max_tokens=16,
        )
        self.assertIsNone(thinking_type)
        self.assertNotIn("thinking", payload)

    def test_explicit_thinking_enabled_adds_reasoning_effort(self) -> None:
        client = OpenAICompatibleClient(
            api_key="dummy",
            model_name="deepseek-v4-flash",
            base_url="https://api.deepseek.com",
            timeout=120,
            thinking_type="enabled",
            reasoning_effort="high",
        )

        payload = client._build_payload(
            [{"role": "user", "content": "hello"}],
            temperature=0,
            max_tokens=16,
        )
        self.assertEqual(payload["thinking"], {"type": "enabled"})
        self.assertEqual(payload["reasoning_effort"], "high")

    def test_missing_simulator_config_errors_point_to_env_example(self) -> None:
        with self.assertRaisesRegex(RuntimeError, ".env.example"):
            OpenAICompatibleClient(
                api_key="",
                model_name="deepseek-v4-flash",
                base_url="https://api.deepseek.com",
                timeout=120,
            )
        with self.assertRaisesRegex(RuntimeError, ".env.example"):
            OpenAICompatibleClient(
                api_key="dummy",
                model_name="",
                base_url="https://api.deepseek.com",
                timeout=120,
            )

    def test_answer_validation_rejects_invalid_classification(self) -> None:
        payload = {
            "answers": [
                {
                    "sub_question": "q",
                    "classification": "illegal",
                    "answer": "No.",
                    "ref": None,
                }
            ]
        }

        self.assertEqual(
            _validate_parsed_answers(payload, ["q"]),
            "classification_invalid: index=0 got='illegal'",
        )

    def test_answer_validation_requires_ref_field(self) -> None:
        payload = {
            "answers": [
                {
                    "sub_question": "q",
                    "classification": "fallback",
                    "answer": "Use sum.",
                }
            ]
        }

        self.assertEqual(_validate_parsed_answers(payload, ["q"]), "answer_missing_fields: index=0 missing=['ref']")

    def test_answer_validation_requires_hit_ref(self) -> None:
        payload = {
            "answers": [
                {
                    "sub_question": "q",
                    "classification": "hit",
                    "answer": "Use sum.",
                    "ref": None,
                }
            ]
        }

        self.assertEqual(_validate_parsed_answers(payload, ["q"]), "hit_ref_missing: index=0")


if __name__ == "__main__":
    unittest.main()
