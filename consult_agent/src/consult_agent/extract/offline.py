"""Extractor offline: citeste un JSON de extragere deja produs.

Doua utilizari:

* Replay determinist in teste si in CI -- fara apel de retea, fara cost.
* Rularea lantului complet in medii fara acces la API, unde pasul de "creier" e
  produs separat si injectat aici.

Validul JSON este verificat impotriva template-ului, deci un fisier care nu se
potriveste cu template-ul curent esueaza imediat, nu la randare.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..schema import Template


class OfflineExtractor:
    name = "offline"

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def extract(self, transcript: str, template: Template) -> dict[str, Any]:
        del transcript  # extragerea e deja facuta; transcrierea ramane pentru verificare
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{self.path}: se astepta un obiect JSON.")

        expected = {f.id for f in template.all_fields}
        missing = expected - set(data)
        unknown = set(data) - expected
        if missing:
            raise ValueError(
                f"{self.path}: lipsesc campurile {sorted(missing)} cerute de template."
            )
        if unknown:
            raise ValueError(
                f"{self.path}: campurile {sorted(unknown)} nu exista in template."
            )
        for field_id, entry in data.items():
            if not isinstance(entry, dict) or "value" not in entry or "evidence" not in entry:
                raise ValueError(
                    f"{self.path}: campul '{field_id}' trebuie sa fie "
                    "{'value': ..., 'evidence': ...}."
                )
        return data
