"""Randarea raportului final din template + extragere."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .schema import Field, Section, Template
from .validate import Issue

MISSING = "_(nemenționat)_"
# Absenta constatata explicit ("fara cicatrici") difera de informatia care
# pur si simplu nu a fost dictata. In clinica, distinctia conteaza.
NONE_STATED = "_(fără elemente de consemnat)_"


UNASSESSED = "Neevaluat în această ședință."
# Un camp dedus asezat printre observatii ar arata ca o constatare. Sectiunile
# integral deduse au deja nota lor; campul izolat are nevoie de propriul marcaj.
DERIVED_MARK = " (interpretare)"


def field_label(field: Field, section: Section) -> str:
    if field.is_derived and not section.is_derived:
        return f"{field.label}{DERIVED_MARK}"
    return field.label


def empty_label(entry: dict[str, Any]) -> str:
    """Ce se afiseaza pentru un camp gol, dupa cum absenta a fost sau nu consemnata."""
    stated = entry.get("value") == [] and entry.get("evidence")
    return NONE_STATED if stated else MISSING


def field_has_content(entry: dict[str, Any]) -> bool:
    """Campul spune ceva: fie o valoare, fie o absenta constatata explicit."""
    value = (entry or {}).get("value")
    if value not in (None, "", [], {}):
        return True
    return value == [] and bool((entry or {}).get("evidence"))


def section_is_unassessed(section: Section, extraction: dict[str, Any]) -> bool:
    """Nicio informatie in toata sectiunea — zona nu a fost abordata in sedinta.

    O randam ca atare, in loc sa insiram zece campuri goale: un perete de
    "(nementionat)" nu ajuta pe nimeni, iar clinic "neevaluat" nu inseamna
    "normal", deci nici nu poate fi omis in tacere.
    """
    return bool(section.fields) and not any(
        field_has_content(extraction.get(f.id, {})) for f in section.fields
    )


def _format_scalar(field: Field, value: Any) -> str:
    if isinstance(value, bool):
        return "Da" if value else "Nu"
    text = str(value)
    if field.unit:
        text = f"{text} {field.unit}"
    return text


def _format_table(field: Field, rows: list[Any]) -> list[str]:
    header = [c.label for c in field.columns]
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in rows:
        cells = []
        for column in field.columns:
            cell = row.get(column.id) if isinstance(row, dict) else None
            cells.append("—" if cell in (None, "") else str(cell).replace("|", "\\|"))
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def _render_field(field: Field, entry: dict[str, Any], label: str | None = None) -> list[str]:
    value = (entry or {}).get("value")
    label = label if label is not None else field.label

    if value is None or value == "" or value == []:
        return [f"**{label}:** {empty_label(entry or {})}", ""]

    if field.type == "table":
        return [f"**{label}:**", "", *_format_table(field, value), ""]

    if field.type == "list":
        return [f"**{label}:**", "", *(f"- {item}" for item in value), ""]

    if field.type == "text":
        return [f"**{label}:**", "", str(value), ""]

    return [f"**{label}:** {_format_scalar(field, value)}", ""]


def render_markdown(
    template: Template,
    extraction: dict[str, Any],
    issues: list[Issue] | None = None,
    transcript: str | None = None,
    generated_at: datetime | None = None,
) -> str:
    """Produce raportul Markdown complet."""
    stamp = (generated_at or datetime.now()).strftime("%Y-%m-%d %H:%M")
    lines: list[str] = [f"# {template.name}", ""]
    if template.specialty:
        lines.append(f"**Specialitate:** {template.specialty}  ")
    lines += [f"**Generat:** {stamp}", "", "---", ""]

    for section in template.sections:
        lines.append(f"## {section.title}")
        lines.append("")
        if section.description:
            lines += [f"_{section.description}_", ""]
        if section.is_derived:
            # Cititorul trebuie sa distinga ce s-a constatat de ce s-a dedus.
            lines += [
                "> Secțiune formulată prin interpretarea observațiilor de mai sus, "
                "nu constatată direct în timpul ședinței.",
                "",
            ]
        if section_is_unassessed(section, extraction):
            lines += [f"_{UNASSESSED}_", ""]
        else:
            for field in section.fields:
                lines += _render_field(
                    field, extraction.get(field.id, {}), field_label(field, section)
                )
        lines.append("")

    blocking = [i for i in (issues or []) if i.severity in ("error", "warning")]
    if blocking:
        lines += ["---", "", "## De verificat", ""]
        lines += [f"- **{i.severity.upper()}** — {i.message}" for i in blocking]
        lines.append("")

    if template.footer:
        lines += ["---", "", template.footer, ""]

    if template.disclaimer:
        lines += ["---", "", f"> {template.disclaimer.strip()}", ""]

    if transcript:
        lines += [
            "<details>",
            "<summary>Transcrierea inregistrarii</summary>",
            "",
            transcript.strip(),
            "",
            "</details>",
            "",
        ]

    return "\n".join(lines)
