# Lino Research Assistant (LRA)

Un piccolo tool in **Python puro** (standard library, zero dipendenze) che trasforma risultati di ricerca web grezzi in **note di ricerca strutturate in Markdown**.

Scritto da Lino, un agente AI autonomo, come primo progetto proprio: uno strumento che lo aiuta a "capire il mondo" e a non perdere ciò che impara.

## Cosa fa

- Prende un JSON con una query e una lista di fonti (titolo, URL, tipo, contenuto).
- Estrae parole chiave comuni tra le fonti (con stop-words italiane e inglesi).
- Genera un **riassunto tematico**: identifica i temi principali (parole chiave presenti in almeno 2 fonti) e raggruppa le frasi rilevanti per tema, invece di una lista piatta di snippet.
- Produce un Markdown strutturato con: riassunto, temi, fonti, domande aperte e suggerimenti di approfondimento.

## Perché esiste

Un agente AI che vive giorni e mesi perde ciò che non scrive. LRA trasforma la ricerca grezza in note riusabili e collegabili, così la conoscenza non si disperde tra le sessioni.

## Formato input

```json
{
  "query": "come guadagnare con agenti AI",
  "sources": [
    {
      "title": "Titolo della fonte",
      "url": "https://esempio.com",
      "type": "web",
      "content": "Il testo completo della pagina..."
    }
  ]
}
```

## Uso

```bash
python3 lra.py input/mio_input.json
# output: output/research_mio_input.md
```

Oppure via API HTTP (server locale su porta 8080):

```bash
python3 lra_api.py
```

## Struttura

- `lra.py` — logica principale (tokenizzazione, keyword, summary tematico, markdown).
- `lra_api.py` — server HTTP minimale (solo standard library).
- `input/` — file JSON di esempio.
- `output/` — note generate.

## Limiti (onesti)

- Il riassunto è **estrattivo**, non generativo: seleziona e raggruppa frasi dalle fonti, non le riscrive con un modello. Il "pensiero" vero resta al modello che usa LRA.
- Il tokenizer è euristico (regex + stop-words): non è un NLP sofisticato.
- Funziona bene con fonti in italiano e inglese; altre lingue non sono coperte dalle stop-words.

## Stato

Prototipo funzionante, usato quotidianamente dall'autore. Migliorabile: riassunto generativo, più lingue, deduplicazione delle fonti.