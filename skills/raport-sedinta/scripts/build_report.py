#!/usr/bin/env python3
"""Valideaza extragerea si scrie raportul.

    python scripts/build_report.py TRANSCRIERE.txt EXTRAGERE.json -o raport.pdf

Verificarile ruleaza ca *cod*, nu ca instructiune in prompt: fiecare citat dintr-un
camp observat e cautat efectiv in transcriere. Un camp completat fara suport in
inregistrare iese la iveala aici, indiferent cat de plauzibil suna.

Iesirea pe stdout e un raport de validare de citit inainte de a livra PDF-ul.
Cod de iesire 1 daca exista erori — atunci extragerea trebuie corectata, nu raportul
livrat asa cum e.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consult_agent.render import render_markdown  # noqa: E402
from consult_agent.schema import load_template  # noqa: E402
from consult_agent.validate import summarize, validate  # noqa: E402

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "templates" / "terapie_craniosacrala.yaml"
)


def _check_shape(extraction: dict, template) -> list[str]:
    """Campurile lipsa sau in plus sunt greseli de completare, nu de continut."""
    problems: list[str] = []
    expected = {f.id for f in template.all_fields}
    for missing in sorted(expected - set(extraction)):
        problems.append(f"Campul '{missing}' lipseste din extragere.")
    for unknown in sorted(set(extraction) - expected):
        problems.append(f"Campul '{unknown}' nu exista in template.")
    for fid, entry in extraction.items():
        if fid in expected and (
            not isinstance(entry, dict) or "value" not in entry or "evidence" not in entry
        ):
            problems.append(
                f"Campul '{fid}' trebuie sa fie un obiect cu cheile 'value' si 'evidence'."
            )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("transcript", help="Fisierul cu transcrierea dictarii.")
    ap.add_argument("extraction", help="Fisierul JSON cu extragerea.")
    ap.add_argument("-o", "--output", default="raport.pdf", help="Fisierul de iesire.")
    ap.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    ap.add_argument("--font", help="Font TTF pentru PDF, daca cel gasit automat nu convine.")
    args = ap.parse_args()

    template = load_template(args.template)
    transcript = Path(args.transcript).read_text(encoding="utf-8")
    extraction = json.loads(Path(args.extraction).read_text(encoding="utf-8"))

    shape_problems = _check_shape(extraction, template)
    if shape_problems:
        print("EXTRAGERE INVALIDA — corecteaza fisierul JSON:\n")
        for p in shape_problems:
            print(f"  {p}")
        return 1

    issues = validate(extraction, template, transcript)
    counts = summarize(issues)

    out = Path(args.output)
    markdown = render_markdown(template, extraction, issues=issues, transcript=None)
    md_path = out.with_suffix(".md")
    md_path.write_text(markdown, encoding="utf-8")

    written = [str(md_path)]
    if out.suffix.lower() == ".pdf":
        try:
            from consult_agent.fonts import FontError
            from consult_agent.render_pdf import render_pdf

            render_pdf(template, extraction, out, issues=issues, font_path=args.font)
            written.append(str(out))
        except ImportError:
            print(
                "NOTA: reportlab nu este instalat, deci PDF-ul nu s-a generat.\n"
                "      Instaleaza cu 'pip install reportlab' si ruleaza din nou.\n"
                f"      Varianta Markdown a fost scrisa in {md_path}.\n"
            )
        except FontError as exc:
            print(f"NOTA: PDF-ul nu s-a generat.\n{exc}\n")

    print(f"Scris: {', '.join(written)}")
    print(
        f"\nValidare: {counts['error']} erori, {counts['warning']} avertismente, "
        f"{counts['info']} campuri fara continut\n"
    )

    for severity in ("error", "warning"):
        rows = [i for i in issues if i.severity == severity]
        if rows:
            print(f"{severity.upper()}:")
            for i in rows:
                print(f"  {i.field_id}: {i.message}")
            print()

    empty = [i for i in issues if i.severity == "info" and "Nemention" in i.message]
    if empty:
        print(f"Fara continut ({len(empty)}): {', '.join(i.field_id for i in empty)}\n")

    if counts["error"]:
        print(
            "Exista erori. Un citat care nu se regaseste in transcriere inseamna, de\n"
            "regula, ca valoarea a fost completata din presupuneri: sterge-o sau\n"
            "inlocuieste citatul cu unul real, apoi ruleaza din nou."
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
