"""Interfata pasului de extragere structurata."""

from __future__ import annotations

from typing import Any, Protocol

from ..schema import Template


class Extractor(Protocol):
    """Transforma o transcriere in dictionarul `{field_id: {value, evidence}}`."""

    name: str

    def extract(self, transcript: str, template: Template) -> dict[str, Any]: ...
