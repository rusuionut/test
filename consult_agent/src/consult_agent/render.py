"""Randarea raportului final din template + extragere."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .schema import Field, Template
from .validate import Issue

MISSING = "_(nementionat)_"


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


def _render_field(field: Field, entry: dict[str, Any]) -> list[str]:
    value = (entry or {}).get("value")

    if value is None or value == "" or value == []:
        return [f"**{field.label}:** {MISSING}", ""]

    if field.type == "table":
        return [f"**{field.label}:**", "", *_format_table(field, value), ""]

    if field.type == "list":
        return [f"**{field.label}:**", "", *(f"- {item}" for item in value), ""]

    if field.type == "text":
        return [f"**{field.label}:**", "", str(value), ""]

    return [f"**{field.label}:** {_format_scalar(field, value)}", ""]


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
        for field in section.fields:
            lines += _render_field(field, extraction.get(field.id, {}))
        lines.append("")

    blocking = [i for i in (issues or []) if i.severity in ("error", "warning")]
    if blocking:
        lines += ["---", "", "## De verificat de catre medic", ""]
        lines += [f"- **{i.severity.upper()}** — {i.message}" for i in blocking]
        lines.append("")

    if template.footer:
        lines += ["---", "", template.footer, ""]

    lines += [
        "---",
        "",
        "> Raport generat automat dintr-o inregistrare audio. Necesita verificare "
        "si semnatura medicului inainte de a fi folosit ca document clinic.",
        "",
    ]

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
