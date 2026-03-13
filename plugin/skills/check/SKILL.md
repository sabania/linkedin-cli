---
name: check
description: "Quick Status-Check ohne API-Calls. Zeigt aktuellen Stand aus Datenspeicher + Session-Info."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /check — Quick Status

Zeigt den aktuellen Stand ohne API-Calls oder Updates. Liest nur den Datenspeicher und config.json.

## Ablauf

1. **Config laden**: `config.json` (inkl. session Block)
2. **Datenspeicher lesen** (kein Agent nötig, direkt lesen):
   - Posts: Anzahl pro Status + Lifecycle
   - Contacts: Anzahl pro Score
   - Fällige Follow-ups
   - Neue Signals (Status=New)
   - Letzter Post: Wann
   - Letzter Report: Wann
   - Aktive Strategie: Version
   - Laufende Experimente

3. **Session-Info anzeigen**:
   - Letzte Session: Wann + wie lange her
   - Letzter Report: Wann
   - Letzter Evolve: Wann
   - Letzter Competitor-Check: Wann

4. **Kompakt anzeigen**:

```
LinkedIn Commander Status (@username)

SESSION:
  Letzte Session: vor 18h (gestern 08:00)
  Letzter Report: KW 10 (vor 4 Tagen)
  Letzter Evolve: vor 11 Tagen
  Letzter Competitor-Check: vor 8 Tagen

CONTENT:
  Posts: 23 total
    Ideas: 3 | Drafts: 1 | Published: 18 | Analyzed: 1
    Active: 2 | Cooling: 1 | Archived: 15
  Letzter Post: vor 1 Tag
  Strategie: v1.2 (seit 03.03.)
  Experiment: hook-type-v1 (7/10 Posts)

CONTACTS:
  Total: 245 | Hot: 5 | Warm: 89 | Cold: 122 | Dormant: 29
  Follow-ups fällig: 2

SIGNALS:
  Neue: 3 (1 High, 2 Medium)

EMPFEHLUNG:
  → /auto für Morning Check (18h seit letzter Session)
```

## Regeln

- **Keine API-Calls** — nur lokale Daten lesen
- **Keine Updates** — nichts schreiben
- **Sofort** — muss in unter 5 Sekunden fertig sein
- **Session-Info immer zeigen** — hilft dem User zu wissen was aktuell ist
