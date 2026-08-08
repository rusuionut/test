"""Rezolvarea unui font capabil de diacritice romanesti pentru export PDF.

Fonturile PDF standard (Helvetica, Times) sunt Latin-1 si nu contin ă, ș, ț.
Fontul Vera livrat cu reportlab la fel. Un raport clinic cu glife lipsa e mai
rau decat o eroare clara, asa ca aici cautam un font potrivit pe sistem si
*verificam* acoperirea, in loc sa o presupunem.
"""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Diacriticele romanesti, inclusiv variantele cu sedila folosite de fonturi vechi.
REQUIRED_GLYPHS = "ăĂâÂîÎșȘțȚ"

ENV_VAR = "CONSULT_AGENT_FONT"

# Perechi (regular, bold) incercate in ordine. Acopera Linux, macOS si Windows.
FONT_CANDIDATES: list[tuple[str, str]] = [
    (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ),
    ("/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"),
    (
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ),
    (
        "/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf",
        "/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf",
    ),
    ("/Library/Fonts/Arial Unicode.ttf", "/Library/Fonts/Arial Unicode.ttf"),
    (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ("C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/calibrib.ttf"),
]


class FontError(RuntimeError):
    """Niciun font disponibil nu poate reda diacriticele romanesti."""


def missing_glyphs(font_path: str | Path) -> list[str]:
    """Caracterele din REQUIRED_GLYPHS pe care fontul nu le contine."""
    face = TTFont("probe", str(font_path)).face
    return [c for c in REQUIRED_GLYPHS if ord(c) not in face.charToGlyph]


def _usable(path: str | Path) -> bool:
    if not Path(path).exists():
        return False
    try:
        return not missing_glyphs(path)
    except Exception:
        return False


def resolve_fonts(explicit: str | Path | None = None) -> tuple[str, str]:
    """Inregistreaza si intoarce numele (regular, bold) de folosit in reportlab.

    Ordinea: argument explicit -> variabila de mediu -> fonturi de sistem.
    """
    candidates: list[tuple[str, str]] = []

    override = explicit or os.environ.get(ENV_VAR)
    if override:
        override = str(override)
        if not Path(override).exists():
            raise FontError(f"Fontul indicat nu exista: {override}")
        lipsa = missing_glyphs(override)
        if lipsa:
            raise FontError(
                f"Fontul {override} nu contine diacriticele romanesti: {''.join(lipsa)}"
            )
        # Cautam un Bold alaturat; daca nu exista, folosim acelasi fisier.
        stem = Path(override)
        bold_guess = stem.with_name(stem.stem.replace("Regular", "Bold") + stem.suffix)
        candidates = [(override, str(bold_guess) if bold_guess.exists() else override)]
    else:
        candidates = [(r, b) for r, b in FONT_CANDIDATES if _usable(r)]

    if not candidates:
        raise FontError(
            "Nu am gasit pe acest sistem un font care sa contina diacriticele "
            "romanesti (ă, ș, ț).\n"
            "Solutii:\n"
            "  Linux : sudo apt install fonts-dejavu-core\n"
            "  macOS : fontul Arial Unicode este de obicei prezent; altfel instaleaza DejaVu\n"
            f"  oricand: --font /cale/catre/font.ttf sau {ENV_VAR}=/cale/catre/font.ttf\n"
            "Alternativ, exporta in Markdown (-o raport.md), care nu depinde de fonturi."
        )

    regular_path, bold_path = candidates[0]
    if not Path(bold_path).exists() or missing_glyphs(bold_path):
        bold_path = regular_path

    pdfmetrics.registerFont(TTFont("ReportBody", regular_path))
    pdfmetrics.registerFont(TTFont("ReportBody-Bold", bold_path))
    pdfmetrics.registerFontFamily(
        "ReportBody", normal="ReportBody", bold="ReportBody-Bold"
    )
    return "ReportBody", "ReportBody-Bold"
