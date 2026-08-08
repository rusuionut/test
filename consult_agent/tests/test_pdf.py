"""Teste pentru exportul PDF.

Verificarea importanta nu e ca fisierul exista, ci ca diacriticele romanesti
chiar ajung in el: fontul gresit produce un PDF cu glife lipsa, care trece
orice test superficial de tip "s-a scris ceva".
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from consult_agent.fonts import FontError, missing_glyphs, resolve_fonts  # noqa: E402
from consult_agent.render_pdf import render_pdf  # noqa: E402
from consult_agent.schema import load_template  # noqa: E402
from consult_agent.validate import validate  # noqa: E402

TEMPLATE = ROOT / "templates" / "terapie_craniosacrala.yaml"
TRANSCRIPT = ROOT / "samples" / "craniosacrala_01.txt"
EXTRACTION = ROOT / "samples" / "craniosacrala_01.extraction.json"


def _has_font() -> bool:
    try:
        resolve_fonts()
        return True
    except FontError:
        return False


needs_font = pytest.mark.skipif(
    not _has_font(), reason="Niciun font de sistem cu diacritice romanesti."
)


@needs_font
def test_pdf_is_created(tmp_path):
    template = load_template(TEMPLATE)
    extraction = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    out = render_pdf(template, extraction, tmp_path / "raport.pdf")
    assert out.exists()
    assert out.read_bytes().startswith(b"%PDF")


@needs_font
def test_pdf_contains_romanian_diacritics(tmp_path):
    pdfium = pytest.importorskip("pypdfium2", reason="pypdfium2 nu e instalat")
    template = load_template(TEMPLATE)
    extraction = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    transcript = TRANSCRIPT.read_text(encoding="utf-8")
    issues = validate(extraction, template, transcript)

    out = render_pdf(template, extraction, tmp_path / "raport.pdf", issues=issues)
    doc = pdfium.PdfDocument(str(out))
    text = "\n".join(
        doc[i].get_textpage().get_text_range() for i in range(len(doc))
    )

    # Titlul si etichetele vin din template, valorile din extragere: le vrem pe toate.
    assert "Terapie Craniosacrală" in text
    assert "Data ședinței" in text
    assert "Prăbușit" in text
    # Sectiunile deduse trebuie sa ramana marcate si in PDF.
    assert "nu constatată direct în timpul ședinței" in text


def test_font_probe_detects_incomplete_coverage():
    """Fontul livrat de reportlab nu acopera romana — sonda trebuie sa observe."""
    import os

    import reportlab

    vera = os.path.join(os.path.dirname(reportlab.__file__), "fonts", "Vera.ttf")
    assert set(missing_glyphs(vera)) >= {"ă", "ș", "ț"}


def test_explicit_font_that_cannot_render_romanian_is_rejected():
    import os

    import reportlab

    vera = os.path.join(os.path.dirname(reportlab.__file__), "fonts", "Vera.ttf")
    with pytest.raises(FontError, match="diacriticele"):
        resolve_fonts(vera)


def test_missing_font_path_is_rejected():
    with pytest.raises(FontError, match="nu exista"):
        resolve_fonts("/cale/inexistenta/font.ttf")
