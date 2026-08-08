"""Transcriere locala cu faster-whisper.

Ruleaza complet offline dupa prima descarcare a modelului: audio-ul cu date
medicale nu paraseste masina.
"""

from __future__ import annotations

from pathlib import Path


class FasterWhisperASR:
    name = "faster-whisper"

    def __init__(
        self,
        model_size: str = "large-v3",
        device: str = "auto",
        compute_type: str = "auto",
        language: str = "ro",
        beam_size: int = 5,
        vad_filter: bool = True,
    ) -> None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:  # pragma: no cover - depinde de mediu
            raise RuntimeError(
                "faster-whisper nu este instalat. Ruleaza: pip install faster-whisper"
            ) from exc

        self.language = language
        self.beam_size = beam_size
        self.vad_filter = vad_filter
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe(self, audio_path: str | Path) -> str:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Fisierul audio nu exista: {path}")

        segments, _info = self.model.transcribe(
            str(path),
            language=self.language,
            beam_size=self.beam_size,
            vad_filter=self.vad_filter,
            # Reduce halucinatiile Whisper pe tacere si pe zgomot de fundal.
            condition_on_previous_text=False,
        )
        return " ".join(segment.text.strip() for segment in segments).strip()
