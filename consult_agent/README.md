# consult-agent

Transformă înregistrarea audio a unui consult medical într-un raport structurat,
completând un template predefinit.

```
audio  →  [ASR]  →  transcriere  →  [extragere LLM]  →  JSON  →  [validare]  →  raport Markdown
```

## Ideea centrală: template-ul este singura sursă de adevăr

`templates/consult_medical.yaml` descrie secțiunile și câmpurile raportului. Din
același fișier se generează automat **și** schema JSON trimisă modelului la
extragere, **și** documentul final. Ca să schimbi raportul — alte secțiuni, alte
câmpuri, altă specialitate — editezi YAML-ul; codul rămâne neatins.

Template-ul livrat acum este un **placeholder** pentru un consult de medicină
internă. Îl înlocuiești cu al tău.

## Instalare

```bash
pip install -r requirements.txt        # nucleu
pip install -r requirements-asr.txt    # transcriere locală (opțional, ~1.5 GB model)
export ANTHROPIC_API_KEY=...           # sau: ant auth login
```

## Utilizare

Rularea normală, cu audio real:

```bash
python -m consult_agent.cli consult.m4a \
  --template templates/consult_medical.yaml \
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
python -m consult_agent.cli samples/consult_01.txt \
  --asr text-file \
  --extractor offline --extraction-json samples/consult_01.extraction.json
```

## Ce face agentul ca să nu inventeze

Într-un document medical, un câmp completat din presupuneri e mai periculos
decât unul gol. Trei mecanisme, în ordinea în care intervin:

1. **Prompt.** Modelul primește instrucțiunea explicită să lase câmpul `null`
   când informația nu apare, și să nu deducă diagnostice din simptome.
2. **Citat obligatoriu.** Pentru fiecare câmp completat, modelul întoarce și un
   citat literal din transcriere.
3. **Verificare mecanică.** `validate.py` caută fiecare citat în transcriere.
   Sub 80% potrivire, câmpul e marcat ca posibilă informație inventată — nu
   depindem de auto-raportarea modelului.

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

## Structură

```
src/consult_agent/
  schema.py      Template YAML → obiecte + generare schemă JSON de extragere
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

- Un singur vorbitor. Nu există diarizare, deci un dialog medic–pacient ajunge
  în transcriere ca text continuu, fără atribuire.
- Fără integrare cu vreun sistem de dosar electronic — ieșirea e un fișier
  Markdown.
- Raportul necesită verificare și semnătura medicului; nu este document clinic
  în sine.
