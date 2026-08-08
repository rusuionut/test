"""Lantul complet: audio -> transcriere -> extragere -> validare -> raport."""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from datetime import datetime
from pathlib import Path
from typing import Any

from .asr import ASR
from .extract import Extractor
from .render import render_markdown
from .schema import Template
from .validate import Issue, has_errors, summarize, validate


@dataclass
class Result:
    transcript: str
    extraction: dict[str, Any]
    issues: list[Issue]
    report_markdown: str
    template: Template
    timings: dict[str, float] = dc_field(default_factory=dict)

    @property
    def has_errors(self) -> bool:
        return has_errors(self.issues)

    @property
    def issue_counts(self) -> dict[str, int]:
        return summarize(self.issues)


def run(
    audio_path: str | Path,
    template: Template,
    asr: ASR,
    extractor: Extractor,
    include_transcript: bool = True,
) -> Result:
    """Ruleaza pipeline-ul pe o inregistrare si intoarce raportul plus diagnosticele."""
    started = datetime.now()
    transcript = asr.transcribe(audio_path)
    if not transcript.strip():
        raise ValueError(f"Transcrierea pentru {audio_path} este goala.")
    after_asr = datetime.now()

    extraction = extractor.extract(transcript, template)
    after_extract = datetime.now()

    issues = validate(extraction, template, transcript)
    report = render_markdown(
        template,
        extraction,
        issues=issues,
        transcript=transcript if include_transcript else None,
    )

    return Result(
        transcript=transcript,
        extraction=extraction,
        issues=issues,
        report_markdown=report,
        template=template,
        timings={
            "asr_s": (after_asr - started).total_seconds(),
            "extract_s": (after_extract - after_asr).total_seconds(),
            "total_s": (datetime.now() - started).total_seconds(),
        },
    )
