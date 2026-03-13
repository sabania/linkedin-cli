---
name: competitor
description: Wettbewerber analysieren. Posts, Engagement, Content-Strategie auswerten und Learnings extrahieren.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /competitor — Wettbewerber analysieren

Analysiert einen LinkedIn-Wettbewerber.

## Verwendung

```
/competitor <username>    # Spezifischen Account analysieren
/competitor               # Alle gespeicherten Competitors updaten
```

## Ablauf

1. **`competitor-analyst` Agent** starten mit Username
2. **Ergebnis anzeigen** und in Competitors-Sheet speichern
3. **Vergleich mit eigenen Zahlen** zeigen

## Regeln

- **Öffentliche Daten only**
- **Learnings in eigene Strategie** einbauen (via `/evolve`)
- **Max 5-7 Competitors** aktiv tracken
