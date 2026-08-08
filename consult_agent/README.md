# consult-agent

Transformă înregistrarea audio a unei ședințe într-un raport structurat,
completând un template predefinit.

```
audio  →  [ASR]  →  transcriere  →  [extragere LLM]  →  JSON  →  [validare]  →  raport Markdown
```

## Ideea centrală: template-ul este singura sursă de adevăr

Template-ul YAML descrie secțiunile și câmpurile raportului. Din același fișier
se generează automat **și** schema JSON trimisă modelului la extragere, **și**
documentul final. Ca să schimbi raportul — alte secțiuni, alte câmpuri, alt
domeniu — editezi YAML-ul; codul rămâne neatins.

Două template-uri livrate:

| Template | Domeniu |
|---|---|
| `templates/terapie_craniosacrala.yaml` | Evaluare posturală + ședință de Terapie Craniosacrală (implicit) |
| `templates/consult_medical.yaml` | Consult de medicină internă |

## Observat vs. dedus

Un raport de ședință conține două tipuri de conținut, cu reguli diferite:

- **Observat** (`mode: observed`, implicit) — ce a constatat terapeutul. Se extrage
  din dictare, cu citat literal obligatoriu, verificat mecanic.
- **Dedus** (`mode: derived`) — direcții de lucru, consecințe funcționale posibile.
  Nu apare în dictare; e formulat de model pe baza observațiilor și **marcat
  vizibil în raport** ca interpretare, nu constatare.

Modul se poate seta pe secțiune (moștenit de câmpuri) sau pe câmp individual.
Distincția e importantă: fără ea, ori pierzi secțiunile generate, ori slăbești
garanția pe observațiile clinice. Aici rămân separate.

## Instalare

```bash
pip install -r requirements.txt        # nucleu
pip install -r requirements-asr.txt    # transcriere locală (opțional, ~1.5 GB model)
export ANTHROPIC_API_KEY=...           # sau: ant auth login
```

## Utilizare

Rularea normală, cu audio real:

```bash
python -m consult_agent.cli sedinta.m4a \
  --template templates/terapie_craniosacrala.yaml \
  -o raport.md
```

Opțiuni utile:

| Flag | Ce face |
|---|---|
| `--asr-model medium` | Model Whisper mai mic/rapid (implicit `large-v3`) |
| `--effort medium` | Reduce costul extragerii (implicit `high`) |
| `--save-extraction x.json` | Salvează extragerea brută, cu citate |
| `--strict` | Cod de ieșire 1 dacă validarea găsește erori |
| `--no-transcript` | Nu atașa transcrierea la finalul raportului |

Rulare fără audio și fără rețea (teste, CI, replay determinist):

```bash
python -m consult_agent.cli samples/craniosacrala_01.txt \
  --template templates/terapie_craniosacrala.yaml --asr text-file \
  --extractor offline --extraction-json samples/craniosacrala_01.extraction.json
```

## Ce face agentul ca să nu inventeze

Într-un document clinic, un câmp completat din presupuneri e mai periculos decât
unul gol. Pe câmpurile **observate**, trei mecanisme:

1. **Prompt.** Modelul primește instrucțiunea explicită să lase câmpul `null`
   când informația nu apare, și să nu deducă diagnostice din semne.
2. **Citat obligatoriu.** Pentru fiecare câmp completat, modelul întoarce și un
   citat literal din transcriere.
3. **Verificare mecanică.** `validate.py` caută fiecare citat în transcriere.
   Sub 80% potrivire, câmpul e marcat ca posibilă informație inventată — nu
   depindem de auto-raportarea modelului.

Pe câmpurile **deduse**, verificarea prin potrivire nu se aplică (conținutul nu
există în dictare), dar modelul trebuie să atașeze justificarea deducției, iar
secțiunea e marcată în raport ca interpretare.

Exemplu de ieșire a validării pe o extragere cu date injectate:

```
[ERROR]   alergii: Citatul nu se regaseste in transcriere (potrivire 25%) ...
[WARNING] trimitere: Valoare completata fara citat justificativ.
```

Problemele găsite ajung și într-o secțiune „De verificat de către medic" la
finalul raportului, iar câmpurile fără informație apar explicit ca
`_(nementionat)_` — nu dispar tăcut.

Validarea verifică în plus: câmpurile obligatorii, valorile enum, formatul
datelor calendaristice (ISO, fără date în viitor) și coloanele tabelelor.

## Limbaj și terminologie

Dictarea e telegrafică și colocvială („gemenii", „sacroiliace"); raportul trebuie
să fie profesional. Prompt-ul cere completarea terminologiei anatomice
(„gemenii" → „gastrocnemian"), dar **numai când sensul reiese clar din context** —
altfel câmpul rămâne gol, în loc să fie ghicit. Ieșirea e în română cu diacritice,
indiferent cum arată transcrierea.

## Structură

```
src/consult_agent/
  schema.py      Template YAML → obiecte + generare schemă JSON de extragere
                 (inclusiv modul observed/derived per câmp)
  prompts.py     Prompt-ul de extragere, construit din template
  asr/           faster-whisper (local) | text-file (transcriere gata făcută)
  extract/       claude (API, structured outputs) | offline (JSON pre-existent)
  validate.py    Câmpuri obligatorii, citate, enum-uri, date, tabele
  render.py      Template + extragere → Markdown
  pipeline.py    Lanțul complet
  cli.py         Linia de comandă
```

Ambele straturi înlocuibile (`asr/`, `extract/`) sunt în spatele unui `Protocol`,
deci se pot adăuga backend-uri noi fără să atingi pipeline-ul.

## Teste

```bash
python -m pytest tests/ -q
```

Testele rulează lanțul complet fără audio și fără apel de rețea.

## Limitări curente

- Un singur vorbitor. Nu există diarizare, deci un dialog terapeut–client ajunge
  în transcriere ca text continuu, fără atribuire.
- Nu există istoric între ședințe: fiecare raport se generează independent, fără
  comparație cu evaluările anterioare ale aceluiași client.
- Ieșirea e Markdown. Fără export DOCX/PDF și fără integrare cu un sistem de
  evidență a clienților.
- Raportul necesită verificarea și asumarea specialistului înainte de a fi
  transmis.
