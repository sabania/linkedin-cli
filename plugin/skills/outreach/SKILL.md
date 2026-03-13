---
name: outreach
description: Personalisierte Outreach-Nachricht für einen LinkedIn-Kontakt generieren.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /outreach — Outreach-Nachricht

Generiert eine personalisierte Nachricht für einen LinkedIn-Kontakt.

## Verwendung

```
/outreach <name-oder-public-id>
```

## Ablauf

1. **Contact laden** aus Datenspeicher (Name oder Public ID)
2. **`content-writer` Agent** starten im Outreach-Modus:
   - Profil-Daten holen
   - Gemeinsame Interaktion als Aufhänger
   - Personalisierte Nachricht schreiben
3. **Nachricht zeigen** — User entscheidet ob/wie senden

## Nachricht-Typen

- **Connection Request** (max 300 Zeichen): Kurz, Bezug auf gemeinsame Interaktion
- **Follow-up Message**: Längere Nachricht an bestehende Connection
- **InMail**: Für Nicht-Connections (falls Premium)

## Regeln

- **Nie automatisch senden** — immer User-Bestätigung
- **Kein Sales-Pitch** im ersten Kontakt
- **Authentisch** — wie Brand Voice, persönlich
- **Bezug herstellen** — warum schreibst du genau dieser Person?
