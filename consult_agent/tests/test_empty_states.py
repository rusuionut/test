"""Teste pentru cele trei feluri de "gol".

Intr-un raport clinic ele nu sunt acelasi lucru:
  * nementionat        — nu s-a spus nimic despre asta
  * absent, consemnat  — specialistul a constatat explicit ca nu exista
  * neevaluat          — zona nu a fost abordata deloc in sedinta

"Neevaluat" nu inseamna "normal", deci nu poate fi nici omis in tacere, nici
confundat cu o constatare negativa.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from consult_agent.asr import get_asr  # noqa: E402
from consult_agent.extract import get_extractor  # noqa: E402
from consult_agent.pipeline import run  # noqa: E402
from consult_agent.render import section_is_unassessed  # noqa: E402
from consult_agent.schema import load_template  # noqa: E402
from consult_agent.validate import validate  # noqa: E402

TEMPLATE = ROOT / "templates" / "terapie_craniosacrala.yaml"
TRANSCRIPT = ROOT / "samples" / "craniosacrala_02.txt"
EXTRACTION = ROOT / "samples" / "craniosacrala_02.extraction.json"


def _run():
    return run(
        TRANSCRIPT,
        template=load_template(TEMPLATE),
        asr=get_asr("text-file"),
        extractor=get_extractor("offline", path=EXTRACTION),
    )


def test_second_session_extracts_cleanly():
    result = _run()
    assert result.issue_counts["error"] == 0
    assert "A.P." in result.report_markdown


def test_explicit_absence_differs_from_missing():
    """«Fără cicatrici» este o constatare, nu o lipsă de informație."""
    result = _run()
    assert "**Cicatrici:** _(fără elemente de consemnat)_" in result.report_markdown
    assert "**Traseul colonului:** _(nemenționat)_" in result.report_markdown

    issues = validate(
        json.loads(EXTRACTION.read_text(encoding="utf-8")),
        load_template(TEMPLATE),
        TRANSCRIPT.read_text(encoding="utf-8"),
    )
    assert any(
        i.field_id == "cicatrici" and "absent" in i.message for i in issues
    )


def test_unassessed_sections_collapse():
    """O secțiune fără nicio informație nu se randează ca un perete de câmpuri goale."""
    template = load_template(TEMPLATE)
    extraction = json.loads(EXTRACTION.read_text(encoding="utf-8"))

    bazin = next(s for s in template.sections if s.id == "bazin")
    fascial = next(s for s in template.sections if s.id == "fascial")
    assert section_is_unassessed(bazin, extraction)
    assert not section_is_unassessed(fascial, extraction)

    report = _run().report_markdown
    assert "Neevaluat în această ședință." in report
    # Câmpurile secțiunii neevaluate nu mai apar individual.
    assert "**Mobilitatea bazinului:**" not in report
    # Dar secțiunea rămâne vizibilă: neevaluat nu se omite în tăcere.
    assert "## Bazin" in report


def test_a_section_with_only_an_explicit_absence_is_not_unassessed():
    """O singură constatare negativă înseamnă că zona *a fost* evaluată."""
    template = load_template(TEMPLATE)
    extraction = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    visceral = next(s for s in template.sections if s.id == "visceral")
    stripped = dict(extraction)
    for f in visceral.fields:
        stripped[f.id] = {"value": None, "evidence": None}
    stripped["cicatrici"] = {"value": [], "evidence": "Fara cicatrici."}
    assert not section_is_unassessed(visceral, stripped)
