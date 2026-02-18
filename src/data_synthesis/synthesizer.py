#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Optional, Dict, Any
from pathlib import Path
import yaml
from string import Template

from llm_connect.openrouter_client import OpenRouterLLMClient
from data_synthesis import config as ds_config


PROMPT_DIR = Path(__file__).parent / "prompt"
PROMPT_REWRITER_FULL_PATH = PROMPT_DIR / "rewriter.yaml"
PROMPT_AMBIGUITY_PATH = PROMPT_DIR / "amb_kb.yaml"


class Synthesizer:

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_full: Optional[str] = None,
        model_amb: Optional[str] = None,
        temperature_full: Optional[float] = None,
        temperature_amb: Optional[float] = None,
        max_tokens_full: Optional[int] = None,
        max_tokens_amb: Optional[int] = None,
        timeout_full: Optional[int] = None,
        timeout_amb: Optional[int] = None,
    ) -> None:
        key = api_key or ds_config.get_api_key()
        if not key:
            raise ValueError("API Key not set. Please set API_KEY in data_synthesis/config.py or pass api_key parameter")

        default_full_model = ds_config.get_full_default_model()
        selected_full_model = model_full or default_full_model
        if not isinstance(selected_full_model, str) or not selected_full_model.strip():
            raise ValueError("model_full must be a non-empty string")
        self.full_cfg = {
            "model": selected_full_model,
            "temperature": temperature_full if temperature_full is not None else ds_config.FULL["temperature"],
            "max_tokens": max_tokens_full if max_tokens_full is not None else ds_config.FULL["max_tokens"],
            "timeout": timeout_full if timeout_full is not None else ds_config.FULL["timeout"],
        }
        self.amb_cfg = {
            "model": model_amb or ds_config.AMB["model"],
            "temperature": temperature_amb if temperature_amb is not None else ds_config.AMB["temperature"],
            "max_tokens": max_tokens_amb if max_tokens_amb is not None else ds_config.AMB["max_tokens"],
            "timeout": timeout_amb if timeout_amb is not None else ds_config.AMB["timeout"],
        }

        self.client_full = OpenRouterLLMClient(
            api_key=key,
            model_name=self.full_cfg["model"],
            http_referer=ds_config.HTTP_REFERER,
            x_title=ds_config.X_TITLE,
        )
        self.client_amb = OpenRouterLLMClient(
            api_key=key,
            model_name=self.amb_cfg["model"],
            http_referer=ds_config.HTTP_REFERER,
            x_title=ds_config.X_TITLE,
        )

        self.rewriter_system_prompt = self._load_text(PROMPT_REWRITER_FULL_PATH)
        self.prompts_ambiguity = self._load_prompt(PROMPT_AMBIGUITY_PATH)

    def _load_prompt(self, path: Path) -> Dict[str, str]:
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")

        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt {path}: {e}") from e

        if not isinstance(data, dict):
            raise ValueError(f"Prompt file content must be a dict: {path}")

        if "system_prompt" not in data or "user_prompt" not in data:
            raise ValueError(f"Prompt file missing required fields system_prompt or user_prompt: {path}")

        return {
            "system_prompt": data["system_prompt"],
            "user_prompt": data["user_prompt"],
        }

    def _load_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        return path.read_text(encoding="utf-8")

    @staticmethod
    def _call_llm(client: OpenRouterLLMClient, system_prompt: str, user_prompt: str, *, temperature: float, max_tokens: int, timeout: int) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return client.generate(messages, temperature=temperature, max_tokens=max_tokens, timeout=timeout)

    def generate_query_full(self, query: str, code: str, flow: str, *, feedback: str = "") -> str:
        user_prompt = (
            "[query_raw]\n" + query + "\n\n" +
            "[solution.py]\n```python\n" + code + "\n```\n\n" +
            "[flow.json]\n```json\n" + flow + "\n```\n\n" +
            "Task: Follow the system instructions to decide whether the original query is clear enough. "
            "Return either 'no ambiguity' or the rewritten query_full starting with '## Context'. "
            "Do not add any commentary or code fences around the output."
        )
        if feedback.strip():
            user_prompt += "\n\n[revision_feedback]\n" + feedback.strip() + "\n"
        final_full = self._call_llm(
            self.client_full,
            self.rewriter_system_prompt,
            user_prompt,
            temperature=self.full_cfg["temperature"],
            max_tokens=self.full_cfg["max_tokens"],
            timeout=self.full_cfg["timeout"],
        ).strip()

        return final_full

    def classify_disamb_failure(
        self,
        *,
        query: str,
        query_full: str,
        failure_context: str,
    ) -> Dict[str, Any]:
        system_prompt = (
            "You classify failure root causes for disambiguated request validation.\n"
            "Return strict JSON with keys: category, reason.\n"
            "Allowed category values only: ambiguity, data_irregular, coder_fail."
        )
        user_prompt = (
            "[query_raw]\n" + query + "\n\n"
            "[query_full_candidate]\n" + query_full + "\n\n"
            "[failure_context]\n" + failure_context + "\n\n"
            "Task: choose one category. Use 'ambiguity' only when query_full still allows multiple reasonable interpretations. "
            "Use 'data_irregular' when input data pathology is primary. Otherwise use 'coder_fail'. "
            "Output JSON only."
        )
        response = self._call_llm(
            self.client_full,
            system_prompt,
            user_prompt,
            temperature=0.0,
            max_tokens=500,
            timeout=self.full_cfg["timeout"],
        )
        parsed = json.loads(response)
        if not isinstance(parsed, dict):
            raise ValueError("classification response must be JSON object")
        category = str(parsed.get("category", "")).strip()
        if category not in {"ambiguity", "data_irregular", "coder_fail"}:
            raise ValueError(f"invalid category: {category}")
        if "reason" not in parsed:
            parsed["reason"] = ""
        return parsed

    def generate_ambiguities_raw(self, query: str, code: str, query_full: str, flow: str) -> str:
        """Generate ambiguity base as raw text (no JSON parsing)."""
        system_prompt = self.prompts_ambiguity["system_prompt"]
        user_template = self.prompts_ambiguity["user_prompt"]
        user_prompt = Template(user_template).safe_substitute(query=query, code=code, query_full=query_full, flow=flow)
        return self._call_llm(
            self.client_amb,
            system_prompt,
            user_prompt,
            temperature=self.amb_cfg["temperature"],
            max_tokens=self.amb_cfg["max_tokens"],
            timeout=self.amb_cfg["timeout"],
        )
