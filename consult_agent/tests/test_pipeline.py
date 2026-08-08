"""Teste pentru lantul de procesare, rulate fara audio si fara apel de retea."""

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

TEMPLATE = ROOT / "templates" / "consult_medical.yaml"
TRANSCRIPT = ROOT / "samples" / "consult_01.txt"
EXTRACTION = ROOT / "samples" / "consult_01.extraction.json"


def _load():
    return load_template(TEMPLATE)


def test_schema_covers_every_field():
    template = _load()
    schema = build_extraction_schema(template)
    assert set(schema["properties"]) == {f.id for f in template.all_fields}
    assert schema["additionalProperties"] is False


def test_pipeline_end_to_end():
    template = _load()
    result = run(
        TRANSCRIPT,
        template=template,
        asr=get_asr("text-file"),
        extractor=get_extractor("offline", path=EXTRACTION),
    )
    assert "Maria Ionescu" in result.report_markdown
    assert result.issue_counts["error"] == 0
    # Campurile nementionate trebuie marcate, nu completate.
    assert "_(nementionat)_" in result.report_markdown


def test_missing_required_field_is_an_error():
    template = _load()
    data = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    data["nume_pacient"] = {"value": None, "evidence": None}
    issues = validate(data, template, TRANSCRIPT.read_text(encoding="utf-8"))
    assert any(i.severity == "error" and i.field_id == "nume_pacient" for i in issues)


def test_fabricated_value_is_caught():
    """Un citat care nu exista in transcriere trebuie semnalat ca eroare."""
    template = _load()
    data = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    data["alergii"] = {
        "value": ["penicilina"],
        "evidence": "pacienta este alergica la penicilina",
    }
    issues = validate(data, template, TRANSCRIPT.read_text(encoding="utf-8"))
    assert any(
        i.severity == "error" and i.field_id == "alergii" and "inventata" in i.message
        for i in issues
    )


def test_enum_and_date_are_enforced():
    template = _load()
    data = json.loads(EXTRACTION.read_text(encoding="utf-8"))
    data["sex"]["value"] = "F"
    data["data_consultului"]["value"] = "08.08.2026"
    issues = validate(data, template, TRANSCRIPT.read_text(encoding="utf-8"))
    assert any(i.field_id == "sex" and i.severity == "error" for i in issues)
    assert any(i.field_id == "data_consultului" and i.severity == "error" for i in issues)
