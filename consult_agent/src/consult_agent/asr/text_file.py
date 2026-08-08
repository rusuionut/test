"""ASR "fals": citeste o transcriere gata facuta dintr-un fisier text.

Il folosim ca sa rulam si sa testam restul lantului fara audio si fara model ASR
(teste, CI, medii fara acces la modele). Interfata este identica cu cea reala,
deci pipeline-ul nu stie diferenta.
"""

from __future__ import annotations

from pathlib import Path


class TextFileASR:
    name = "text-file"

    def transcribe(self, audio_path: str | Path) -> str:
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Fisierul de transcriere nu exista: {path}")
        return path.read_text(encoding="utf-8").strip()
