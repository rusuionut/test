"""Modelul template-ului de raport.

Un template este un fisier YAML care descrie sectiunile si campurile raportului.
Din el se genereaza automat *si* schema JSON folosita la extragere, *si* randarea
raportului final. Ca sa schimbi raportul, editezi YAML-ul -- nu codul.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any

import yaml

# Tipurile de camp suportate si maparea lor in JSON Schema.
SCALAR_TYPES = {
    "string": {"type": "string"},
    "text": {"type": "string"},
    "integer": {"type": "integer"},
    "number": {"type": "number"},
    "boolean": {"type": "boolean"},
    "date": {"type": "string", "description": "Data in format ISO 8601 (AAAA-LL-ZZ)."},
}


class TemplateError(ValueError):
    """Template YAML invalid."""


@dataclass
class Column:
    """O coloana dintr-un camp de tip `table`."""

    id: str
    label: str
    type: str = "string"
    description: str = ""

    def json_schema(self) -> dict[str, Any]:
        if self.type not in SCALAR_TYPES:
            raise TemplateError(
                f"Coloana '{self.id}': tip '{self.type}' nesuportat intr-un tabel."
            )
        schema = dict(SCALAR_TYPES[self.type])
        desc = self.description or self.label
        if desc:
            schema["description"] = desc
        # Coloanele pot lipsi din ce a dictat medicul.
        return {"anyOf": [schema, {"type": "null"}]}


@dataclass
class Field:
    id: str
    label: str
    type: str = "string"
    required: bool = False
    description: str = ""
    options: list[str] = dc_field(default_factory=list)
    columns: list[Column] = dc_field(default_factory=list)
    unit: str = ""

    def prompt_hint(self) -> str:
        """Descrierea trimisa modelului pentru acest camp."""
        bits = [self.description or self.label]
        if self.options:
            bits.append("Valori permise: " + ", ".join(self.options) + ".")
        if self.unit:
            bits.append(f"Unitate de masura: {self.unit}.")
        if self.type == "list":
            bits.append("Lista de siruri de caractere.")
        if self.type == "table":
            cols = ", ".join(f"{c.id} ({c.label})" for c in self.columns)
            bits.append(f"Lista de obiecte cu cheile: {cols}.")
        if self.required:
            bits.append("Camp obligatoriu in raport.")
        return " ".join(b for b in bits if b)

    def value_schema(self) -> dict[str, Any]:
        """Schema JSON pentru *valoarea* campului (fara wrapper-ul de evidenta)."""
        if self.type in SCALAR_TYPES:
            base: dict[str, Any] = dict(SCALAR_TYPES[self.type])
            if self.options:
                base = {"type": "string", "enum": self.options}
        elif self.type == "list":
            base = {"type": "array", "items": {"type": "string"}}
        elif self.type == "table":
            if not self.columns:
                raise TemplateError(f"Campul '{self.id}' de tip table nu are coloane.")
            base = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {c.id: c.json_schema() for c in self.columns},
                    "required": [c.id for c in self.columns],
                    "additionalProperties": False,
                },
            }
        else:
            raise TemplateError(f"Campul '{self.id}': tip necunoscut '{self.type}'.")
        # Orice camp poate lipsi din inregistrare -> null. Modelul NU inventeaza.
        return {"anyOf": [base, {"type": "null"}]}


@dataclass
class Section:
    id: str
    title: str
    description: str = ""
    fields: list[Field] = dc_field(default_factory=list)


@dataclass
class Template:
    name: str
    language: str
    sections: list[Section]
    specialty: str = ""
    footer: str = ""
    version: str = "1"

    @property
    def all_fields(self) -> list[Field]:
        return [f for s in self.sections for f in s.fields]

    def field(self, field_id: str) -> Field | None:
        for f in self.all_fields:
            if f.id == field_id:
                return f
        return None


def _parse_field(raw: dict[str, Any], section_id: str) -> Field:
    if "id" not in raw:
        raise TemplateError(f"Sectiunea '{section_id}': un camp nu are 'id'.")
    columns = [
        Column(
            id=c["id"],
            label=c.get("label", c["id"]),
            type=c.get("type", "string"),
            description=c.get("description", ""),
        )
        for c in raw.get("columns", [])
    ]
    return Field(
        id=raw["id"],
        label=raw.get("label", raw["id"]),
        type=raw.get("type", "string"),
        required=bool(raw.get("required", False)),
        description=raw.get("description", ""),
        options=list(raw.get("options", [])),
        columns=columns,
        unit=raw.get("unit", ""),
    )


def load_template(path: str | Path) -> Template:
    """Incarca si valideaza un template YAML."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TemplateError(f"{path}: continutul nu este un obiect YAML.")

    sections: list[Section] = []
    for s in raw.get("sections", []):
        if "id" not in s:
            raise TemplateError("O sectiune nu are 'id'.")
        sections.append(
            Section(
                id=s["id"],
                title=s.get("title", s["id"]),
                description=s.get("description", ""),
                fields=[_parse_field(f, s["id"]) for f in s.get("fields", [])],
            )
        )
    if not sections:
        raise TemplateError(f"{path}: template-ul nu contine nicio sectiune.")

    template = Template(
        name=raw.get("name", "Raport"),
        language=raw.get("language", "ro"),
        specialty=raw.get("specialty", ""),
        footer=raw.get("footer", ""),
        version=str(raw.get("version", "1")),
        sections=sections,
    )

    ids = [f.id for f in template.all_fields]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise TemplateError(f"ID-uri de camp duplicate: {sorted(duplicates)}")
    # Validare timpurie a tipurilor: mai bine acum decat la runtime.
    for f in template.all_fields:
        f.value_schema()
    return template


def build_extraction_schema(template: Template) -> dict[str, Any]:
    """Construieste schema JSON pe care modelul trebuie sa o respecte.

    Fiecare camp devine `{"value": ..., "evidence": ...}`. `evidence` este citatul
    exact din transcriere care justifica valoarea -- il folosim ulterior ca sa
    verificam ca modelul nu a inventat informatie (vezi validate.verify_evidence).
    """
    properties: dict[str, Any] = {}
    for f in template.all_fields:
        properties[f.id] = {
            "type": "object",
            "description": f.prompt_hint(),
            "properties": {
                "value": f.value_schema(),
                "evidence": {
                    "anyOf": [{"type": "string"}, {"type": "null"}],
                    "description": (
                        "Citat literal si scurt din transcriere care sustine valoarea. "
                        "null daca informatia nu apare in transcriere."
                    ),
                },
            },
            "required": ["value", "evidence"],
            "additionalProperties": False,
        }

    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }
