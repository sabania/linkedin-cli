---
name: evolve
description: "Content-Strategie weiterentwickeln. Orchestriert strategy-evolver Agent. Human-Gate für neue Versionen. Wöchentlich bei Weekly Review oder on-demand."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /evolve — Strategie weiterentwickeln

Entwickelt die Content-Strategie basierend auf Patterns, ICP-Daten, Competitor-Insights und Performance-Trends.

## Verwendung

```
/evolve              # Vollständige Strategy-Evolution
/evolve check        # Nur prüfen ob Update nötig (kein Vorschlag)
```

## Ablauf

1. **`strategy-evolver` Agent** starten (opus-Modell — der Head of Strategy)

2. **Agent analysiert:**
   - Neue Patterns seit letztem Evolve
   - ICP-Delta (Soll vs. Ist Audience)
   - Competitor-Learnings
   - Pillar-Balance (Ist vs. Soll)
   - KPI-Trends aus Reports

3. **Ergebnis präsentieren:**
   - Was hat sich geändert seit letztem Evolve
   - Welche Patterns sind neu/bestätigt/deprecated
   - Empfehlung: Strategy-Update nötig? (ja/nein mit Begründung)

4. **Falls Update empfohlen — Diff zeigen:**
   ```
   Strategy v1.2 → v1.3 (Vorschlag)

   ÄNDERUNGEN:
   + "Question hooks boost comments 2x" → Bewährte Patterns
   + Dienstag + Donnerstag als beste Tage → Posting-Plan
   - "Video-Format" → Vermeiden (Disproven, Sample: 8)
   ~ AI Praxis: 40% → 50% (stärkstes Pillar)
   ~ Behind the Scenes: 20% → 15% (unterperformt)

   BEGRÜNDUNG:
   - 3 neue High-Confidence Patterns
   - ICP-Delta: 60% Developers statt CTOs → mehr Educational Content
   - Competitor-Gap: "Team Leadership" Thema unbesetzt

   Soll ich diese Strategie aktivieren? [Ja/Nein]
   ```

5. **Human-Gate:**
   - **User bestätigt** → Alte Strategy archivieren, neue aktivieren, CLAUDE.md updaten
   - **User lehnt ab** → Aktuelle Strategy bleibt, Feedback dokumentieren
   - **User modifiziert** → Anpassungen einarbeiten, nochmal vorlegen

## Session

- Nach Evolve: `session.last_evolve_date` auf heute setzen
- Bei Weekly Review: Wird automatisch nach `/report` aufgerufen

## Regeln

- **HUMAN-GATE** — nie ohne User-Bestätigung die aktive Strategie ändern
- **Zeige die Diff** — was ändert sich von alt zu neu
- **Empfehle Experimente** für Bereiche mit Low Confidence
- **Konservativ** — v1.1 statt v2.0 (kleine Schritte)
- **Evidenz-basiert** — keine Änderungen ohne Daten
