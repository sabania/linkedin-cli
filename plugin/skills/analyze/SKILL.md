---
name: analyze
description: "Post-Performance analysieren. Vergleicht mit Baseline, erkennt Patterns, bewertet Experimente, analysiert Comments, updatet ICP. Lifecycle-aware."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /analyze — Post analysieren

Analysiert Post-Performance, erkennt Patterns und schärft das ICP. Lifecycle-aware: unterscheidet Active/Cooling/Archived Posts.

## Verwendung

```
/analyze <urn>        # Einzelnen Post analysieren
/analyze              # Alle Posts die Analyse brauchen
/analyze patterns     # Nur Pattern-Refresh (Archived Posts)
/analyze icp          # Nur ICP-Schärfung
```

## Lifecycle-Awareness

| Lifecycle | Analyse-Verhalten |
|-----------|-------------------|
| **Active** (0-7 Tage) | Analyse möglich, aber mit Caveat "Metriken noch in Bewegung" |
| **Cooling** (7-14 Tage) | Gute Datenbasis, Snapshot 2-3 verfügbar |
| **Archived** (14+ Tage) | Finale Metriken — beste Basis für Pattern-Erkennung |

Pattern-Refresh verwendet nur Posts mit finalen Metriken (Archived/Analyzed).

## Ablauf

### Einzelpost (/analyze <urn>)

1. **`post-analyzer` Agent** starten
2. **Ergebnis:**

```
Post-Analyse: "Die meisten KMUs unterschätzen..."
URN: urn:li:activity:7435982583777169408
Lifecycle: Cooling (Tag 9)

Performance (Snapshot 2):
  Reactions:       89 (Baseline: 45) → +98% 🔥
  Comments:        12 (Baseline: 5) → +140% 🔥
  Impressions:  3,200 (Baseline: 1,800) → +78%
  Engagement Rate: 3.2% (Baseline: 2.8%) → +14%

Content Properties:
  Hook: Surprising Fact | Format: Text | CTA: Question
  Day: Tuesday | Hour: 8 | Length: Medium (780 chars)

Pattern-Match:
  ✅ "Surprising Fact" Hook → überdurchschnittlich
  ✅ "Tuesday" Posting → bestätigt Pattern
  🆕 "Personal Reference" → +40% (Low Confidence, n=4)

ICP Insight:
  Top Engager: CTOs (30%), Developers (40%), PMs (20%)

Nächster Snapshot in 5 Tagen (Tag 14).
```

### Batch (/analyze)

1. Alle Posts mit fehlenden Snapshots oder Status "Published" ohne "Analyzed"
2. Für jeden: Analyse durchführen
3. Am Ende: Pattern-Refresh über alle Posts mit finalen Metriken

### Pattern-Refresh (/analyze patterns)

Nur auf Archived/Analyzed Posts:
1. Für jede Dimension: Avg berechnen, Sample Size, Success Rate
2. Kombinations-Patterns testen
3. Patterns-Sheet updaten
4. Experiment-Evaluation (falls Experimente laufen)

### ICP-Schärfung (/analyze icp)

1. Top Demographics aller Posts aggregieren
2. Mit konfiguriertem ICP vergleichen
3. ICP Profile Sheet updaten
4. Delta zeigen

## Regeln

- **Lifecycle beachten** — Active Posts mit Caveat, Patterns nur aus Archived
- **3 Snapshots** bevor Status → "Analyzed"
- **Median** als Baseline (robuster)
- **Patterns nur mit Daten** — min 3 Posts pro Dimension
- **Kombis nur mit min 3 Posts** pro Kombination
- **Honest** — wenn keine Patterns, das sagen
