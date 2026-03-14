---
name: report
description: Wöchentlichen Performance-Report erstellen mit KPIs, Trends und Insights.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /report — Wochen-Report

Erstellt einen wöchentlichen Performance-Report.

**WICHTIG: Delegiere die Arbeit an den `report-builder` Agent. Mach NICHTS selbst — starte den Agent mit dem `Agent`-Tool.**

## Verwendung

```
/report               # Report für aktuelle Woche
/report last          # Report für letzte Woche
```

## Ablauf

1. **Daten aktualisieren** via `data-collector` Agent (aktuelle Zahlen holen)
2. **Report erstellen** via `report-builder` Agent
3. **Report anzeigen** und im Datenspeicher speichern

## Regeln

- **Immer aktuelle Daten** — vor dem Report frische Zahlen holen
- **Vergleichbar** — gleiches Format jede Woche
- **Actionable Insights** — nicht nur Zahlen, auch Empfehlungen
