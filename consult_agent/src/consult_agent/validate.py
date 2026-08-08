"""Verificari pe extragere, inainte de randarea raportului.

Scopul nu e sa blocheze raportul, ci sa spuna medicului exact ce lipseste si ce
nu se poate justifica din inregistrare. Un raport medical incomplet dar marcat
corect e util; unul complet dar inventat pe alocuri e periculos.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from typing import Any

from .schema import Template

# Sub acest prag, citatul returnat de model nu se regaseste in transcriere.
EVIDENCE_MATCH_THRESHOLD = 0.80

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Issue:
    severity: str  # "error" | "warning" | "info"
    field_id: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.field_id}: {self.message}"


def _normalize(text: str) -> str:
    """Minuscule, fara diacritice, fara punctuatie, spatii colapsate."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]+", " ", stripped).strip()


def _match_ratio(needle: str, haystack: str) -> float:
    """Cat de mult din `needle` se regaseste, contiguu, in `haystack` (0..1)."""
    if not needle:
        return 0.0
    if needle in haystack:
        return 1.0
    matcher = SequenceMatcher(None, needle, haystack, autojunk=False)
    match = matcher.find_longest_match(0, len(needle), 0, len(haystack))
    return match.size / len(needle)


def _is_empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def validate(
    extraction: dict[str, Any], template: Template, transcript: str
) -> list[Issue]:
    """Verifica extragerea si intoarce lista de probleme gasite."""
    issues: list[Issue] = []
    normalized_transcript = _normalize(transcript)
    today = date.today().isoformat()

    for field in template.all_fields:
        entry = extraction.get(field.id) or {}
        value = entry.get("value")
        evidence = entry.get("evidence")
        empty = _is_empty(value)

        if field.required and empty:
            issues.append(
                Issue("error", field.id, f"Câmp obligatoriu necompletat ({field.label}).")
            )
            continue
        if empty:
            issues.append(Issue("info", field.id, "Nemenționat în înregistrare."))
            continue

        if field.is_derived:
            # Continut dedus: nu are corespondent literal in transcriere, deci
            # verificarea prin potrivire nu se aplica. Cerem doar justificarea,
            # iar raportul il marcheaza vizibil ca dedus.
            if not evidence:
                issues.append(
                    Issue("warning", field.id, "Conținut dedus, fără justificare atașată.")
                )
            issues.append(
                Issue("info", field.id, "Conținut dedus — de confirmat de specialist.")
            )
        elif not evidence:
            # Valoare fara citat: nu putem urmari de unde vine.
            issues.append(
                Issue("warning", field.id, "Valoare completată fără citat justificativ.")
            )
        else:
            ratio = _match_ratio(_normalize(evidence), normalized_transcript)
            if ratio < EVIDENCE_MATCH_THRESHOLD:
                issues.append(
                    Issue(
                        "error",
                        field.id,
                        "Citatul nu se regăsește în transcriere "
                        f"(potrivire {ratio:.0%}): {evidence!r}. Posibilă informație inventată.",
                    )
                )

        if field.options and isinstance(value, str) and value not in field.options:
            issues.append(
                Issue(
                    "error",
                    field.id,
                    f"Valoarea {value!r} nu este în lista permisă: {field.options}.",
                )
            )

        if field.type == "date" and isinstance(value, str):
            if not ISO_DATE.match(value):
                issues.append(
                    Issue("error", field.id, f"Data {value!r} nu e în format AAAA-LL-ZZ.")
                )
            elif value > today:
                issues.append(Issue("warning", field.id, f"Data {value} este în viitor."))

        if field.type == "table" and isinstance(value, list):
            allowed = {c.id for c in field.columns}
            for i, row in enumerate(value, start=1):
                if not isinstance(row, dict):
                    issues.append(Issue("error", field.id, f"Rândul {i} nu este un obiect."))
                    continue
                extra = set(row) - allowed
                if extra:
                    issues.append(
                        Issue("error", field.id, f"Rândul {i} are coloane necunoscute: {sorted(extra)}.")
                    )

    return issues


def has_errors(issues: list[Issue]) -> bool:
    return any(i.severity == "error" for i in issues)


def summarize(issues: list[Issue]) -> dict[str, int]:
    counts = {"error": 0, "warning": 0, "info": 0}
    for issue in issues:
        counts[issue.severity] = counts.get(issue.severity, 0) + 1
    return counts
