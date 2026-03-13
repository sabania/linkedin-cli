---
name: setup
description: Deep Onboarding für LinkedIn Commander. Interview + historische Post-Analyse + Contact Seed + Competitor Deep-Dives + System-Generierung. Das System startet "warmgelaufen", nicht leer.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - WebSearch
---

# /setup — Deep Onboarding

Du bist der Setup-Assistent für LinkedIn Commander. Dein Job: User interviewen UND das System mit echten Daten füllen. Nach dem Setup ist das System "warmgelaufen" — der erste `/auto`-Run arbeitet mit Deltas, nicht von Null.

**Gesprächsstil:**
- Conversational, nicht wie ein Formular
- Fasse Antworten zusammen und bestätige bevor du weitermachst
- Überspringe Fragen die sich aus dem Kontext ergeben
- Schlage Defaults vor wenn der User unsicher ist
- Gruppiere verwandte Fragen — nicht jede einzeln stellen

**Argumente:**
- `/setup` — Normales Onboarding
- `/setup reset` — Bestehende config.json überschreiben
- `/setup validate` — Nur prüfen ob alles konfiguriert ist, nichts ändern

---

## Phase 1: Interview

### Schritt 0: Prüfe bestehende Konfiguration

```
Prüfe ob config.json im CWD existiert.
- Falls ja: Frage ob der User die Konfiguration aktualisieren oder neu starten will.
- Falls nein: Starte das Interview.
```

### Schritt 1: Begrüssung & Kontext

> Willkommen bei LinkedIn Commander! Ich stelle dir ein paar Fragen und analysiere dann dein bestehendes Profil. Das System startet danach mit echten Daten — nicht leer. Los geht's!

### Schritt 2: Ziele & Motivation

1. **Was willst du mit LinkedIn erreichen?**
   - Thought Leadership / Expertise zeigen
   - Leads / Kunden gewinnen
   - Recruiting / Talent anziehen
   - Brand Awareness / Sichtbarkeit
   - Networking / Community
   - Mehrere davon? Priorität?

2. **Wie ist dein aktueller LinkedIn-Stand?**
   - Postest du schon regelmässig?
   - Wie viele Follower/Connections ungefähr?
   - Was funktioniert gut, was nicht?

### Schritt 3: ICP — Ideal Customer Profile

3. **Wer ist deine Zielgruppe?**
   - Welche Job-Titel/Rollen willst du erreichen?
   - Welche Branchen?
   - Welches Seniority-Level?
   - Welche Region?
   - Welche Firmengrösse?

→ Daraus wird das initiale ICP erstellt (wird über Zeit aus Engagement-Daten geschärft).

### Schritt 4: Content-Strategie

4. **Über welche Themen willst du posten?**
   → 3-5 Content-Pillars definieren mit optionaler Gewichtung

5. **In welcher Sprache?** DE, EN, beides, andere

6. **Wie oft willst du posten?** Täglich, 3x/Woche, wöchentlich

7. **Welcher Ton passt zu dir?**
   - Professionell, locker, educational, provokant, storytelling, technisch...
   - Gibt es LinkedIn-Accounts deren Stil du magst? (→ als Referenz speichern)

### Schritt 5: Competitors

8. **Willst du Wettbewerber tracken?**
   - Falls ja: 1-5 LinkedIn Usernames eingeben
   - System validiert jeden via `linkedin-cli profile show <id> --json`

### Schritt 6: Signal-Konfiguration

9. **Welche Keywords willst du monitoren?** (3-10 Keywords)

10. **Wie aggressiv soll das Signal-System sein?**
    - Konservativ: Nur High-Priority (max 3/Tag)
    - Normal: High + Medium (max 10/Tag)
    - Alles: Alle Signals zeigen

### Schritt 7: Tracking & Umgebung

11. **Welches Tracking-Format?** Excel (.xlsx, Default), CSV, JSON, SQLite

12. **LinkedIn CLI prüfen/installieren**
    ```bash
    linkedin-cli --help 2>/dev/null
    ```

13. **LinkedIn Login**
    ```bash
    linkedin-cli whoami --json
    ```
    → Username und Profil-URL aus Ergebnis extrahieren

14. **Runtimes prüfen**
    ```bash
    python --version 2>/dev/null || python3 --version 2>/dev/null
    node --version 2>/dev/null
    ```

---

## Phase 2: Historische Analyse (NEU — System startet warm)

**Ziel:** Bestehende Posts analysieren, Baseline berechnen, erste Patterns erkennen. Das System startet mit Daten, nicht leer.

### 2.1 Posts laden

```bash
linkedin-cli profile posts <username> --limit 30 --json
```

→ Letzte 20-30 Posts laden

### 2.2 Analytics pro Post

Für jeden Post mit URN:
```bash
linkedin-cli posts analytics <urn> --json
```

→ Impressions, Reactions, Comments, Demographics

### 2.3 Klassifizierung

Für jeden Post automatisch bestimmen:
- **Hook Type**: Statistics, Personal Story, Question, Surprising Fact, Contrarian, How-To, List, Problem-Solution, Behind-Scenes
- **Format**: Text, Image, Video, Document, Carousel, Poll
- **Content Type**: Educational, Case-Study, Opinion, Behind-Scenes, How-To, News-Commentary, Inspirational, Controversial
- **Pillar**: Zuordnung zu den definierten Content-Pillars
- **CTA Type**: Question, Statement, Link, None
- **Language**: DE, EN, andere
- **Length Category**: Short/Medium/Long (berechnet aus Zeichenzahl)
- **Has Personal Reference**: true/false
- **Is Timely**: true/false

### 2.4 Baseline berechnen

```python
baseline = {
    "median_reactions": median(all_reactions),
    "median_comments": median(all_comments),
    "median_impressions": median(all_impressions),
    "median_engagement_rate": median(all_er),
    "avg_reactions": mean(all_reactions),
    "avg_comments": mean(all_comments),
}
```

→ Baseline ist der Massstab für alle zukünftigen Vergleiche.

### 2.5 Erste Patterns erkennen

Analyse über alle klassifizierten Posts:
- Welche Hook Types performen überdurchschnittlich?
- Welche Formate?
- Welche Tage/Zeiten?
- Welche Content Types?
- Welche Pillar-Themen?
- Gibt es Kombinations-Patterns?

→ Patterns mit Sample Size und Confidence erstellen (meist Low-Medium bei 20-30 Posts).

### 2.6 Repurposing-Kandidaten identifizieren

Posts mit hoher Engagement Rate aber niedrigen Impressions = Repurposing-Kandidaten.
→ In Notes vermerken.

### 2.7 Lifecycle setzen

Alle historischen Posts bekommen basierend auf Published Date:
- Letzte 7 Tage → `Lifecycle: Active`
- 7-14 Tage → `Lifecycle: Cooling`
- 14+ Tage → `Lifecycle: Archived`, `Status: Analyzed`

---

## Phase 3: Contact Seed (NEU)

**Ziel:** Top-Engager aus historischen Posts erfassen, ICP-Match bewerten, initiale Hot Contacts identifizieren.

### 3.1 Engager laden

Für die Top 10 Posts (nach Engagement Rate):
```bash
linkedin-cli posts engagers <urn> --limit 50 --json
```

### 3.2 Deduplizieren und anreichern

- Engager über alle Posts zusammenführen
- Interaction Count berechnen (wie oft erscheint dieselbe Person)
- Interaction Types sammeln (reaction, comment)

### 3.3 ICP-Match bewerten

Für jeden Engager:
- Headline/Title gegen ICP-Dimensionen matchen
- Industry matchen
- Seniority einschätzen
- Score: High, Medium, Low, None

### 3.4 Warm Score berechnen

Initialer Warm Score basierend auf historischen Interactions:
```
+10  pro Reaction auf eigenen Post
+25  pro Kommentar auf eigenen Post
+20  bei ICP Match (High)
+10  bei ICP Match (Medium)
```

### 3.5 Hot Contacts identifizieren

Contacts mit Warm Score >= 60 → Score: Hot
→ Diese Personen sind die wertvollsten bestehenden Beziehungen.

---

## Phase 4: Competitor Deep-Dives (NEU)

**Nur wenn Competitors in Phase 1 definiert wurden.**

### 4.1 Pro Competitor

```bash
linkedin-cli profile show <competitor-id> --json
linkedin-cli profile posts <competitor-id> --limit 20 --json
```

### 4.2 Aggregation

Pro Competitor berechnen:
- Avg Reactions, Avg Comments, Avg Engagement Rate
- Posting Frequency (Posts pro Woche)
- Top Format, Top Hook Type
- Content Pillars (Themen-Mix)

### 4.3 Content-Gap-Analyse

Vergleich eigene Pillars vs. Competitor-Pillars:
- Themen die Competitors haben, wir nicht → Content Gap
- Themen die wir haben, Competitors nicht → Differenzierung

### 4.4 Shared-Engager-Identifikation

```bash
linkedin-cli posts engagers <competitor-post-urn> --limit 50 --json
```

Cross-Reference mit unseren Contacts:
- Personen die bei uns UND beim Competitor engagen → Shared Engagers
- Zeigt überlappende Audience

---

## Phase 5: Generierung

### 5.1 config.json

```json
{
  "version": "3.0",
  "created": "<heute>",

  "linkedin": {
    "username": "<aus whoami>",
    "profileUrl": "<aus whoami>",
    "fullName": "<aus whoami>",
    "company": "<aus Profil>"
  },

  "goals": ["thought-leadership", "lead-generation"],

  "icp": {
    "titles": ["CTO", "VP Engineering"],
    "industries": ["Software", "Manufacturing"],
    "seniority": ["Senior", "Executive"],
    "companySize": "10-250",
    "regions": ["DACH"]
  },

  "content": {
    "pillars": [
      {"name": "AI Praxis", "weight": 0.4},
      {"name": "Side Projects", "weight": 0.3},
      {"name": "Behind the Scenes", "weight": 0.2},
      {"name": "Industry News", "weight": 0.1}
    ],
    "languages": ["DE"],
    "tone": "professional-casual",
    "posting_frequency": 3,
    "references": []
  },

  "competitors": [
    {"publicId": "competitor-1", "name": "Competitor One"}
  ],

  "signals": {
    "keywords": ["AI", "NLP", "Language Tech"],
    "warm_score_threshold": 60,
    "dormant_days": 90,
    "keyword_check_frequency": "daily",
    "max_signals_per_day": 10
  },

  "tracking": {
    "format": "excel",
    "file": "linkedin-data.xlsx",
    "sheets": ["Posts", "Contacts", "Patterns", "Strategy", "Reports", "Competitors", "Signals", "Feed Insights", "ICP Profile", "Comment Tracking"],
    "runtime": "python"
  },

  "environment": {
    "cli_path": "",
    "cli_version": "",
    "python": "",
    "node": ""
  },

  "session": {
    "last_session_date": "<jetzt ISO 8601>",
    "last_report_date": null,
    "last_evolve_date": null,
    "last_competitor_check": "<jetzt falls Competitors analysiert, sonst null>",
    "setup_completed": true,
    "posts_baseline_count": 23
  },

  "lifecycle": {
    "active_days": 7,
    "cooling_days": 14
  }
}
```

### 5.2 Datenspeicher erstellen (GEFÜLLT, nicht leer!)

```python
import openpyxl
wb = openpyxl.Workbook()
wb.remove(wb.active)
for sheet_name in config["tracking"]["sheets"]:
    ws = wb.create_sheet(sheet_name)
    ws.append(HEADERS[sheet_name])  # Headers aus data-schema Skill
wb.save(config["tracking"]["file"])
```

Dann füllen mit Daten aus Phase 2-4:
- **Posts**: 20-30 historische Posts mit allen berechneten Feldern + Lifecycle
- **Contacts**: Seed aus Engagern mit Warm Score und ICP Match
- **Patterns**: Erste erkannte Muster (Low-Medium Confidence)
- **Competitors**: Deep-Dive-Daten (falls analysiert)
- **ICP Profile**: Initiale Dimensionen aus Interview + erste Daten aus Demographics
- **Strategy v1.0**: Erste Strategie basierend auf Interview + historischer Analyse

### 5.3 Strategy v1.0 erstellen

Basierend auf Interview + historischer Analyse:

```markdown
## Ziele
<Aus Interview-Antworten>

## Zielgruppe (ICP)
<Soll-ICP aus Interview + erste Ist-Daten aus Demographics>

## Content-Pillars
<Themen mit Gewichtung + erste Performance-Daten pro Pillar>

## Bewährte Patterns
<Aus Phase 2.5 — mit Caveat "basierend auf N Posts">

## Posting-Plan
<Frequenz aus Interview + beste Tage/Zeiten aus historischen Daten>

## Nächste Hypothesen
<Was als erstes getestet werden sollte>

## Vermeiden
<Was historisch schlecht performt hat>
```

→ In Strategy-Sheet als v1.0, Status: Active

### 5.4 Ordner erstellen

```bash
mkdir -p drafts
```

### 5.5 CLAUDE.md generieren

Erstelle ein CLAUDE.md im CWD. Die **Navigations-Karte** für Claude Code und alle Agents.

```markdown
# LinkedIn Command Center — [User Name]

[Personalisierte Beschreibung basierend auf Zielen]

## Setup

Run `/setup` if config.json does not exist.

## Quick Reference

| Was | Wo |
|-----|-----|
| Konfiguration | config.json |
| Datenspeicher | [tracking.file] |
| Post-Entwürfe | drafts/ |
| Active Strategy | Datenspeicher → Strategy Sheet (Status=Active) |
| Hot Contacts | Datenspeicher → Contacts Sheet (Score=Hot) |
| Pending Signals | Datenspeicher → Signals Sheet (Status=New) |

## Commands

| Command | Zweck |
|---------|-------|
| /auto | Morning Check: Delta-Pipeline, Signals, Analytics, Feed |
| /check | Quick-Status (lokal, kein API-Call) |
| /ideas [n] | Content-Ideen generieren |
| /draft <topic> | Neuen Post schreiben |
| /analyze [urn] | Post-Performance analysieren |
| /evolve | Strategie weiterentwickeln |
| /report | Wochen-Report |
| /competitor [name] | Wettbewerber analysieren |
| /contacts [arg] | Kontakte & Leads verwalten |
| /outreach <name> | Personalisierte Nachricht |

## Content Pillars

[Generiert aus config.json → content.pillars]

## ICP (Ideal Customer Profile)

[Generiert aus config.json → icp]

## Core Rules

1. Lade config.json vor jeder Operation
2. Lade aktive Strategy vor Content-Erstellung
3. Nach Analysen: Patterns prüfen und updaten
4. Nie ohne User-Bestätigung posten oder Nachrichten senden
5. Delta-basiert arbeiten: nur neue Daten seit last_session_date

## Learning Loop

CREATE → PUBLISH → MEASURE → ANALYZE → LEARN → ADAPT → CREATE

## Current State

- Strategy Version: v1.0 (Initial)
- Active Patterns: [count from Phase 2]
- Posts Tracked: [count from seeding]
- Hot Contacts: [count from Phase 3]
- Active Experiments: none
- Last Report: none
- Baseline: [median reactions] Rx, [median comments] Cm, [median ER]% ER
```

---

## Zusammenfassung an User

```
Setup abgeschlossen! System ist warmgelaufen.

Profil: [Name] (@[username])
Ziele: [Goals]
ICP: [Top Titel] in [Branchen], [Region]
Content: [n] Pillars, [Sprachen], [Frequenz]
Tracking: [Format] ([Datei]) — [n] Sheets

📊 Historische Analyse:
  [n] Posts analysiert, Baseline berechnet
  [n] Patterns erkannt (Low-Medium Confidence)
  Bester Hook: [Top Hook Type]
  Bester Tag: [Best Day]

👥 Contacts:
  [n] Engager erfasst
  [n] Hot Contacts (Warm Score >= 60)
  [n] ICP-Matches (High)

🏆 Competitors:
  [n] analysiert

🎯 Strategy v1.0 erstellt

Nächste Schritte:
1. /auto — Morning Check starten (Delta von jetzt)
2. /ideas — Content-Ideen basierend auf Patterns
3. /draft <thema> — Ersten Post schreiben
```

---

## Besondere Fälle

### User will wenig tracken
- `tracking.sheets` enthält nur die gewählten Sheets
- Agents die fehlende Sheets brauchen passen sich an (skippen statt crashen)

### User hat kein Python
- Prüfe ob die linkedin-cli Binary Python mitliefert (PyInstaller → embedded Python)
- Falls ja: Pfad zur embedded Python notieren in environment
- Falls nein: Empfehle Installation oder nutze JSON/CSV Format

### User will kein Excel
- Agents lesen `config.json` → `tracking.format` und passen ihre Scripts an
- Schema bleibt gleich, nur Speicherformat ändert sich

### User hat keine historischen Posts
- Phase 2 wird übersprungen
- Baseline wird nach den ersten 5 Posts berechnet
- System startet "kalt" — das ist okay, wird mit jedem Post besser
