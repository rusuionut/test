#!/usr/bin/env python3
"""Afiseaza campurile pe care trebuie sa le completezi, citite din template.

Template-ul e sursa unica de adevar: daca terapeutul adauga o rubrica in YAML,
apare aici automat. De aceea lista nu e scrisa in SKILL.md — s-ar desincroniza.

    python scripts/fields.py [--template CALE] [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consult_agent.schema import build_extraction_schema, load_template  # noqa: E402

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "templates" / "terapie_craniosacrala.yaml"
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument(
        "--json", action="store_true", help="Afiseaza schema JSON completa, nu rezumatul."
    )
    args = ap.parse_args()

    template = load_template(args.template)

    if args.json:
        print(json.dumps(build_extraction_schema(template), ensure_ascii=False, indent=2))
        return 0

    print(f"# {template.name}")
    if template.specialty:
        print(f"Specialitate: {template.specialty}")
    print(f"Total campuri: {len(template.all_fields)}\n")

    for section in template.sections:
        marca = "  [SECTIUNE DEDUSA]" if section.is_derived else ""
        print(f"## {section.title}{marca}")
        if section.description:
            print(f"   {section.description.strip()}")
        for f in section.fields:
            bits = [f.type]
            if f.required:
                bits.append("obligatoriu")
            if f.is_derived and not section.is_derived:
                bits.append("DEDUS")
            if f.options:
                bits.append("una din: " + ", ".join(f.options))
            if f.columns:
                bits.append("coloane: " + ", ".join(c.id for c in f.columns))
            print(f"   - {f.id}  ({', '.join(bits)})")
            print(f"       {f.label} — {f.description.strip() or 'fara descriere'}")
        print()

    print("Fiecare camp se completeaza ca {\"value\": ..., \"evidence\": ...}.")
    print("Ruleaza cu --json daca vrei schema exacta a valorilor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
