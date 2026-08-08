"""Backend-uri de transcriere audio."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class ASR(Protocol):
    name: str

    def transcribe(self, audio_path: str | Path) -> str: ...


def get_asr(name: str, **kwargs: Any) -> ASR:
    if name == "faster-whisper":
        from .faster_whisper_asr import FasterWhisperASR

        return FasterWhisperASR(**kwargs)
    if name == "text-file":
        from .text_file import TextFileASR

        return TextFileASR(**kwargs)
    raise ValueError(f"Backend ASR necunoscut: '{name}' (faster-whisper | text-file)")


__all__ = ["ASR", "get_asr"]
