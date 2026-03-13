# LinkedIn Command Center v3

Selbstlernendes LinkedIn-Management-System. 9 AI Agents als kohärentes Marketing-Team. Delta-basierte Pipeline. Der Mensch entscheidet — der Agent analysiert und unterstützt.

## Setup

**Erstmalige Einrichtung:** `/setup` ausführen — Deep Onboarding mit 5 Phasen (Interview + historische Analyse + Contact Seed + Competitor Deep-Dives + gefüllter Datenspeicher).

Prüfe ob `config.json` existiert. Falls nicht, führe `/setup` aus.

**Setup-Optionen:**
- `/setup` — Deep Onboarding (System startet warmgelaufen)
- `/setup reset` — Bestehende Config überschreiben
- `/setup validate` — Nur Config prüfen, nichts ändern

## Konfiguration laden

**WICHTIG:** Vor allen Operationen `config.json` laden:

```
config.json enthält:
- linkedin.username → LinkedIn API Aufrufe
- session.last_session_date → Delta-Berechnung
- lifecycle.active_days / cooling_days → Post-Lifecycle
- content.pillars → Content-Strategie
- icp → Ideal Customer Profile
- tracking.format / file → Datenspeicher-Zugriff
```

## Datenstruktur

### Datenspeicher (10 Sheets)

| Sheet | Zweck |
|-------|-------|
| Posts (33 Spalten) | Content-Lifecycle + Metriken + Lifecycle (Active/Cooling/Archived) |
| Contacts (23) | LinkedIn-Kontakte mit Warm Score + ICP Match |
| Patterns (14) | Erkannte Erfolgsmuster mit Confidence |
| Strategy (5) | Versionierte Content-Strategie (Active/Archived) |
| Reports (16) | Wöchentliche Performance-Reports |
| Competitors (18) | Wettbewerber-Tracking |
| Signals (11) | Trigger-Events und Opportunities |
| Feed Insights (14) | Feed-Analyse, Trends, Comment-Opportunities |
| ICP Profile (7) | Ideal Customer Profile (wird geschärft) |
| Comment Tracking (9) | Strategische Kommentare |

### Post-Lifecycle (orthogonal zu Status)

| Phase | Tage | API-Last |
|-------|------|----------|
| Active | 0-7 | Analytics bei jedem /auto |
| Cooling | 7-14 | Letzter Snapshot |
| Archived | 14+ | Null (nie wieder angefasst) |

### Lokale Dateien

| Pfad | Zweck |
|------|-------|
| `config.json` | Zentrale Konfiguration + Session-State |
| `linkedin-data.xlsx` | Datenspeicher (oder CSV/JSON/SQLite) |
| `drafts/` | Post-Entwürfe (.md) |
| `plugin/dashboard.html` | Interaktives Dashboard (liest Excel live via SheetJS) |

## Commands

| Command | Zweck |
|---------|-------|
| `/setup` | Deep Onboarding: 5-Phasen Setup mit historischer Analyse |
| `/auto` | Morning Check: 3-Stage Delta-Pipeline (Collect → Enrich → Detect) |
| `/check` | Quick Status: nur lokale Daten, kein API |
| `/ideas [n]` | Content-Ideen generieren (8 Quellen) |
| `/draft <thema>` | Post oder Kommentar schreiben |
| `/analyze [urn]` | Post-Performance analysieren (Lifecycle-aware) |
| `/evolve` | Strategie weiterentwickeln (Human-Gate) |
| `/report` | Wochen-Report erstellen |
| `/competitor <name>` | Wettbewerber analysieren (Delta-basiert) |
| `/contacts [arg]` | Kontakte verwalten + Network Health |
| `/outreach <name>` | Personalisierte Nachricht generieren |

## Agents (Marketing-Team)

| Agent | Rolle | Model | Pipeline |
|-------|-------|-------|----------|
| data-collector | Data Analyst | haiku | Daily Stage 1: COLLECT |
| contact-scanner | Community Manager | sonnet | Daily Stage 2: ENRICH |
| signal-detector | Intelligence Officer | sonnet | Daily Stage 3a: DETECT |
| feed-analyst | Social Media Scout | sonnet | Daily Stage 3b: DETECT (parallel) |
| post-analyzer | Performance Analyst | sonnet | Weekly + on-demand |
| report-builder | Reporting Analyst | sonnet | Weekly + on-demand |
| strategy-evolver | Head of Strategy | opus | Weekly + on-demand (Learning Loop) |
| content-writer | Content Creator | sonnet | On-demand |
| competitor-analyst | Market Researcher | sonnet | On-demand |

## Kernregeln

1. **Delta-basiert** — nur neue Daten seit `session.last_session_date`
2. **Notifications first** — 1 API-Call = 80% der Deltas
3. **Lifecycle respektieren** — Archived Posts nie anfassen
4. **Config laden** vor jeder Operation
5. **Aktive Strategy laden** vor Content-Erstellung
6. **Patterns updaten** nach Analysen
7. **NIE posten, senden, kommentieren** — Mensch handelt, Agent unterstützt
8. **Human-Gate** bei Strategie-Änderungen

## Learning Loop

```
CREATE → PUBLISH → MEASURE → ANALYZE → LEARN → ADAPT → CREATE
```

strategy-evolver ist das Gehirn. Ohne ihn lernt das System nicht.

## Cron-Jobs (extern)

| Job | Frequenz | Was |
|-----|----------|-----|
| Morning Check | Täglich ~08:00 | `/auto` |
| Weekly Review | Sonntag ~20:00 | `/report` + `/evolve` |
