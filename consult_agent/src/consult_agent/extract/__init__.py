"""Backend-uri de extragere structurata."""

from __future__ import annotations

from typing import Any

from .base import Extractor


def get_extractor(name: str, **kwargs: Any) -> Extractor:
    if name == "claude":
        from .claude import ClaudeExtractor

        return ClaudeExtractor(**kwargs)
    if name == "offline":
        from .offline import OfflineExtractor

        return OfflineExtractor(**kwargs)
    raise ValueError(f"Backend de extragere necunoscut: '{name}' (claude | offline)")


__all__ = ["Extractor", "get_extractor"]
