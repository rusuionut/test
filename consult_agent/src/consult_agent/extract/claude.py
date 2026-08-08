"""Extragere structurata cu Claude (Anthropic API)."""

from __future__ import annotations

import json
from typing import Any

import anthropic

from ..prompts import SYSTEM_PROMPT, build_extraction_prompt
from ..schema import Template, build_extraction_schema

DEFAULT_MODEL = "claude-opus-5"


class ClaudeExtractor:
    """Trimite transcrierea la Claude si primeste JSON validat pe schema template-ului.

    Foloseste structured outputs (`output_config.format`), deci raspunsul respecta
    garantat forma ceruta -- nu e nevoie de parsare defensiva sau retry pe JSON rupt.
    """

    name = "claude"

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        effort: str = "high",
        max_tokens: int = 16000,
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        # Fara api_key explicit, SDK-ul rezolva singur credentialele din mediu.
        self.client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

    def extract(self, transcript: str, template: Template) -> dict[str, Any]:
        schema = build_extraction_schema(template)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    # Prompt-ul de sistem e identic intre consulturi: il cache-uim.
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            thinking={"type": "adaptive"},
            output_config={
                "effort": self.effort,
                "format": {"type": "json_schema", "schema": schema},
            },
            messages=[
                {
                    "role": "user",
                    "content": build_extraction_prompt(template, transcript),
                }
            ],
        )

        if response.stop_reason == "refusal":
            detail = getattr(response, "stop_details", None)
            category = getattr(detail, "category", None)
            raise RuntimeError(
                f"Modelul a refuzat procesarea acestei inregistrari (categorie: {category})."
            )
        if response.stop_reason == "max_tokens":
            raise RuntimeError(
                "Raspunsul a fost trunchiat (max_tokens). Creste max_tokens sau "
                "imparte consultul in bucati mai mici."
            )

        text = next((b.text for b in response.content if b.type == "text"), None)
        if text is None:
            raise RuntimeError("Raspunsul modelului nu contine text.")
        return json.loads(text)
