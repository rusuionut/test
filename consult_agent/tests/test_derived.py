"""Teste pentru distinctia observat / dedus.

Miza: continutul dedus (directii de lucru, consecinte) trebuie sa fie permis si
marcat, fara ca asta sa slabeasca verificarea pe observatiile clinice.
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
from consult_agent.schema import build_extraction_schema, load_template  # noqa: E402
from consult_agent.validate import validate  # noqa: E402

TEMPLATE = ROOT / "templates" / "terapie_craniosacrala.yaml"
TRANSCRIPT = ROOT / "samples" / "craniosacrala_01.txt"
EXTRACTION = ROOT / "samples" / "craniosacrala_01.extraction.json"


def _template():
    return load_template(TEMPLATE)


def _extraction() -> dict:
    return json.loads(EXTRACTION.read_text(encoding="utf-8"))


def _transcript() -> str:
    return TRANSCRIPT.read_text(encoding="utf-8")


def test_section_mode_is_inherited_by_fields():
    template = _template()
    assert template.field("prioritati").is_derived
    assert template.field("consecinte_posibile").is_derived
    # Observatiile raman in modul strict.
    assert not template.field("tonus_general").is_derived
    assert not template.field("fascia_plantara").is_derived


def test_derived_fields_get_a_different_prompt_contract():
    template = _template()
    schema = build_extraction_schema(template)
    derived = schema["properties"]["prioritati"]["properties"]["evidence"]["description"]
    observed = schema["properties"]["tonus_general"]["properties"]["evidence"]["description"]
    assert "Justificarea deductiei" in derived
    assert "Citat literal" in observed


def test_derived_content_is_not_checked_against_the_transcript():
    """Continutul dedus nu are corespondent literal in dictare — si e in regula."""
    template = _template()
    issues = validate(_extraction(), template, _transcript())
    derived_errors = [
        i for i in issues if i.field_id == "prioritati" and i.severity == "error"
    ]
    assert derived_errors == []
    assert any(
        i.field_id == "prioritati" and "dedus" in i.message for i in issues
    )


def test_observed_fields_still_reject_fabrication():
    """Modul derived nu trebuie sa deschida o portita pentru observatii inventate."""
    template = _template()
    data = _extraction()
    data["tonus_general"] = {
        "value": "Tonus scazut, cu hiperlaxitate ligamentara",
        "evidence": "s-a observat hiperlaxitate ligamentara generalizata",
    }
    issues = validate(data, template, _transcript())
    assert any(
        i.field_id == "tonus_general" and i.severity == "error" and "inventat" in i.message
        for i in issues
    )


def test_derived_without_justification_is_flagged():
    template = _template()
    data = _extraction()
    data["prioritati"]["evidence"] = None
    issues = validate(data, template, _transcript())
    assert any(
        i.field_id == "prioritati" and i.severity == "warning" for i in issues
    )


def test_report_marks_derived_sections():
    template = _template()
    result = run(
        TRANSCRIPT,
        template=template,
        asr=get_asr("text-file"),
        extractor=get_extractor("offline", path=EXTRACTION),
    )
    assert result.issue_counts["error"] == 0
    assert "Direcții de lucru terapeutic" in result.report_markdown
    # Cititorul trebuie sa vada ce e constatat si ce e interpretat.
    assert "nu constatată direct în timpul ședinței" in result.report_markdown
    assert "terapeutului" in result.report_markdown  # disclaimer din template
