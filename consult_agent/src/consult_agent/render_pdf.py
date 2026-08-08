"""Randare PDF, direct din template + extragere.

Nu trecem prin Markdown: avem deja datele structurate, iar un parser de Markdown
ar fi o sursa in plus de erori intr-un document trimis clientului.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .fonts import resolve_fonts
from .render import MISSING
from .schema import Field, Template
from .validate import Issue

ACCENT = colors.HexColor("#2F5D62")
MUTED = colors.HexColor("#6B7280")
RULE = colors.HexColor("#D7DEE0")
NOTE_BG = colors.HexColor("#F4F6F6")

MARGIN = 20 * mm


def _styles(body: str, bold: str) -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            "title", fontName=bold, fontSize=17, leading=21, textColor=ACCENT, spaceAfter=2
        ),
        "subtitle": ParagraphStyle(
            "subtitle", fontName=body, fontSize=9.5, leading=13, textColor=MUTED
        ),
        "section": ParagraphStyle(
            "section",
            fontName=bold,
            fontSize=12,
            leading=15,
            textColor=ACCENT,
            spaceBefore=11,
            spaceAfter=5,
        ),
        "sectionnote": ParagraphStyle(
            "sectionnote", fontName=body, fontSize=8.5, leading=11.5, textColor=MUTED
        ),
        "label": ParagraphStyle("label", fontName=bold, fontSize=9.5, leading=13),
        "body": ParagraphStyle(
            "body", fontName=body, fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY
        ),
        "inline": ParagraphStyle("inline", fontName=body, fontSize=9.5, leading=13.5),
        "bullet": ParagraphStyle(
            "bullet", fontName=body, fontSize=9.5, leading=13.5, leftIndent=10, bulletIndent=2
        ),
        "cell": ParagraphStyle("cell", fontName=body, fontSize=8.5, leading=11.5),
        "cellhead": ParagraphStyle(
            "cellhead", fontName=bold, fontSize=8.5, leading=11.5, textColor=colors.white
        ),
        "missing": ParagraphStyle(
            "missing", fontName=body, fontSize=9.5, leading=13.5, textColor=MUTED
        ),
        "footer": ParagraphStyle(
            "footer", fontName=body, fontSize=8.5, leading=11.5, textColor=MUTED
        ),
    }


def _esc(value: Any) -> str:
    return escape(str(value))


def _field_flowables(field: Field, entry: dict[str, Any], st: dict) -> list:
    value = (entry or {}).get("value")
    label = _esc(field.label)

    if value is None or value == "" or value == []:
        # MISSING contine deja parantezele; sublinierile sunt sintaxa Markdown.
        text = MISSING.strip("_")
        return [Paragraph(f"<b>{label}:</b> <i>{_esc(text)}</i>", st["missing"]), Spacer(1, 3)]

    if field.type == "table":
        head = [Paragraph(_esc(c.label), st["cellhead"]) for c in field.columns]
        rows = [head]
        for row in value:
            rows.append(
                [
                    Paragraph(
                        _esc(row.get(c.id)) if isinstance(row, dict) and row.get(c.id) else "—",
                        st["cell"],
                    )
                    for c in field.columns
                ]
            )
        width = A4[0] - 2 * MARGIN
        table = Table(rows, colWidths=[width / len(field.columns)] * len(field.columns))
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                    ("GRID", (0, 0), (-1, -1), 0.4, RULE),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, NOTE_BG]),
                ]
            )
        )
        return [Paragraph(f"<b>{label}:</b>", st["label"]), Spacer(1, 3), table, Spacer(1, 6)]

    if field.type == "list":
        items = [
            Paragraph(_esc(item), st["bullet"], bulletText="•") for item in value
        ]
        return [Paragraph(f"<b>{label}:</b>", st["label"]), Spacer(1, 2), *items, Spacer(1, 5)]

    if field.type == "text":
        return [
            Paragraph(f"<b>{label}:</b>", st["label"]),
            Spacer(1, 2),
            Paragraph(_esc(value), st["body"]),
            Spacer(1, 5),
        ]

    shown = "Da" if value is True else "Nu" if value is False else str(value)
    if field.unit:
        shown = f"{shown} {field.unit}"
    return [Paragraph(f"<b>{label}:</b> {_esc(shown)}", st["inline"]), Spacer(1, 3)]


def _note_box(text: str, st: dict) -> Table:
    """Caseta gri folosita pentru avertismente si sectiuni deduse."""
    inner = Paragraph(text, st["sectionnote"])
    table = Table([[inner]], colWidths=[A4[0] - 2 * MARGIN])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NOTE_BG),
                ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def render_pdf(
    template: Template,
    extraction: dict[str, Any],
    output_path: str | Path,
    issues: list[Issue] | None = None,
    generated_at: datetime | None = None,
    font_path: str | Path | None = None,
) -> Path:
    """Scrie raportul ca PDF si intoarce calea fisierului."""
    body_font, bold_font = resolve_fonts(font_path)
    st = _styles(body_font, bold_font)
    stamp = (generated_at or datetime.now()).strftime("%d.%m.%Y, %H:%M")

    story: list = [Paragraph(_esc(template.name), st["title"])]
    meta = " · ".join(x for x in [template.specialty, f"Generat: {stamp}"] if x)
    story += [Paragraph(_esc(meta), st["subtitle"]), Spacer(1, 10)]

    for section in template.sections:
        head: list = [Paragraph(_esc(section.title), st["section"])]
        if section.is_derived:
            head.append(
                _note_box(
                    "Secțiune formulată prin interpretarea observațiilor de mai sus, "
                    "nu constatată direct în timpul ședinței.",
                    st,
                )
            )
            head.append(Spacer(1, 6))
        # Titlul nu trebuie sa ramana singur la baza paginii.
        story.append(KeepTogether(head))
        for field in section.fields:
            story += _field_flowables(field, extraction.get(field.id, {}), st)

    flagged = [i for i in (issues or []) if i.severity in ("error", "warning")]
    if flagged:
        story.append(Paragraph("De verificat", st["section"]))
        for issue in flagged:
            story.append(
                Paragraph(
                    f"<b>{_esc(issue.severity.upper())}</b> — {_esc(issue.message)}",
                    st["bullet"],
                    bulletText="•",
                )
            )
        story.append(Spacer(1, 6))

    if template.footer:
        story += [Spacer(1, 8), _note_box(_esc(template.footer.strip()), st)]

    def _decorate(canvas, doc) -> None:
        canvas.saveState()
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, MARGIN - 4 * mm, A4[0] - MARGIN, MARGIN - 4 * mm)
        canvas.setFont(body_font, 7.5)
        canvas.setFillColor(MUTED)
        baseline = MARGIN - 9 * mm
        page_label = f"Pagina {canvas.getPageNumber()}"
        canvas.drawRightString(A4[0] - MARGIN, baseline, page_label)

        if template.disclaimer:
            # Taiem disclaimerul la latimea ramasa, ca sa nu intre peste numarul
            # paginii; masuram efectiv, nu ghicim un numar de caractere.
            available = (
                A4[0]
                - 2 * MARGIN
                - canvas.stringWidth(page_label, body_font, 7.5)
                - 6 * mm
            )
            text = " ".join(template.disclaimer.split())
            while text and canvas.stringWidth(text, body_font, 7.5) > available:
                text = text[:-2]
            if text != " ".join(template.disclaimer.split()):
                text = text.rstrip(" .,") + "…"
            canvas.drawString(MARGIN, baseline, text)
        canvas.restoreState()

    output_path = Path(output_path)
    doc = BaseDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 6 * mm,
        title=template.name,
        author=template.specialty or "consult-agent",
    )
    frame = Frame(
        MARGIN, doc.bottomMargin, A4[0] - 2 * MARGIN, A4[1] - MARGIN - doc.bottomMargin
    )
    doc.addPageTemplates([PageTemplate(id="raport", frames=[frame], onPage=_decorate)])
    doc.build(story)
    return output_path
