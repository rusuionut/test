"""Interfata de linie de comanda."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .asr import get_asr
from .extract import get_extractor
from .pipeline import run
from .schema import load_template

DEFAULT_TEMPLATE = (
    Path(__file__).resolve().parents[2] / "templates" / "terapie_craniosacrala.yaml"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="consult-agent",
        description="Transforma inregistrarea audio a unui consult intr-un raport structurat.",
    )
    parser.add_argument(
        "input",
        help="Fisierul audio (.mp3/.wav/.m4a...) sau, cu --asr text-file, o transcriere .txt",
    )
    parser.add_argument(
        "-t", "--template", default=str(DEFAULT_TEMPLATE), help="Template-ul YAML de raport."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Fisierul de raport. Extensia decide formatul: .pdf sau .md (implicit: stdout).",
    )
    parser.add_argument(
        "--format",
        choices=["md", "pdf"],
        help="Forteaza formatul, ignorand extensia fisierului de iesire.",
    )
    parser.add_argument(
        "--font",
        help="Font TTF pentru PDF. Implicit se cauta unul de sistem cu diacritice romanesti.",
    )
    parser.add_argument(
        "--asr",
        default="faster-whisper",
        choices=["faster-whisper", "text-file"],
        help="Backend de transcriere.",
    )
    parser.add_argument("--asr-model", default="large-v3", help="Model faster-whisper.")
    parser.add_argument("--language", default="ro", help="Limba inregistrarii.")
    parser.add_argument(
        "--extractor",
        default="claude",
        choices=["claude", "offline"],
        help="Backend de extragere structurata.",
    )
    parser.add_argument("--model", default="claude-opus-5", help="Modelul Claude.")
    parser.add_argument(
        "--effort",
        default="high",
        choices=["low", "medium", "high", "xhigh", "max"],
        help="Nivelul de efort al modelului.",
    )
    parser.add_argument(
        "--extraction-json",
        help="Cu --extractor offline: fisierul JSON cu extragerea deja facuta.",
    )
    parser.add_argument(
        "--save-extraction", help="Salveaza extragerea bruta (JSON) in acest fisier."
    )
    parser.add_argument(
        "--no-transcript",
        action="store_true",
        help="Nu include transcrierea la finalul raportului.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Iesire cu cod 1 daca validarea gaseste erori.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    template = load_template(args.template)

    if args.asr == "faster-whisper":
        asr = get_asr("faster-whisper", model_size=args.asr_model, language=args.language)
    else:
        asr = get_asr("text-file")

    if args.extractor == "claude":
        extractor = get_extractor("claude", model=args.model, effort=args.effort)
    else:
        if not args.extraction_json:
            print(
                "Eroare: --extractor offline necesita --extraction-json.", file=sys.stderr
            )
            return 2
        extractor = get_extractor("offline", path=args.extraction_json)

    result = run(
        args.input,
        template=template,
        asr=asr,
        extractor=extractor,
        include_transcript=not args.no_transcript,
    )

    if args.save_extraction:
        Path(args.save_extraction).write_text(
            json.dumps(result.extraction, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    output_format = args.format
    if output_format is None:
        output_format = (
            "pdf" if args.output and Path(args.output).suffix.lower() == ".pdf" else "md"
        )

    if output_format == "pdf":
        if not args.output:
            print("Eroare: PDF-ul are nevoie de --output.", file=sys.stderr)
            return 2
        from .fonts import FontError
        from .render_pdf import render_pdf

        try:
            render_pdf(
                template,
                result.extraction,
                args.output,
                issues=result.issues,
                font_path=args.font,
            )
        except FontError as exc:
            print(f"Eroare de font:\n{exc}", file=sys.stderr)
            return 3
        print(f"Raport PDF scris in {args.output}", file=sys.stderr)
    elif args.output:
        Path(args.output).write_text(result.report_markdown, encoding="utf-8")
        print(f"Raport scris in {args.output}", file=sys.stderr)
    else:
        print(result.report_markdown)

    counts = result.issue_counts
    print(
        f"\nValidare: {counts['error']} erori, {counts['warning']} avertismente, "
        f"{counts['info']} câmpuri nemenționate "
        f"(ASR {result.timings['asr_s']:.1f}s, extragere {result.timings['extract_s']:.1f}s)",
        file=sys.stderr,
    )
    for issue in result.issues:
        if issue.severity != "info":
            print(f"  {issue}", file=sys.stderr)

    return 1 if (args.strict and result.has_errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())
