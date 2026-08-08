"""Validarea si randarea raportului de sedinta.

Nucleul deterministic al skill-ului: template-ul, verificarile si randarea.
Extragerea nu e aici — o face Claude, urmand regulile din SKILL.md.
"""

from .render import render_markdown
from .render_pdf import render_pdf
from .schema import Template, build_extraction_schema, load_template
from .validate import Issue, has_errors, summarize, validate

__all__ = [
    "Issue",
    "Template",
    "build_extraction_schema",
    "has_errors",
    "load_template",
    "render_markdown",
    "render_pdf",
    "summarize",
    "validate",
]
