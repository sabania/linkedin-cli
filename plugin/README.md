# LinkedIn Commander v3 — Plugin Architecture

Selbstlernendes LinkedIn-Management-System. 9 AI Agents arbeiten als kohärentes Marketing-Team in einer Delta-basierten Pipeline. Das System analysiert, lernt und adaptiert — aber der Mensch entscheidet.

## Architektur

```mermaid
graph TB
    subgraph "Cron (extern)"
        CRON_M["☀️ Morning Check<br/>täglich ~08:00"]
        CRON_W["📊 Weekly Review<br/>Sonntag ~20:00"]
    end

    subgraph "Entry Points"
        AUTO["/auto"]
        REPORT["/report + /evolve"]
        ADHOC["Ad-hoc Commands<br/>/ideas /draft /analyze ..."]
    end

    subgraph "3-Stage Pipeline (Daily)"
        S1["Stage 1: COLLECT<br/>data-collector<br/>(Data Analyst)"]
        S2["Stage 2: ENRICH<br/>contact-scanner<br/>(Community Manager)"]
        S3A["Stage 3a: DETECT<br/>signal-detector<br/>(Intelligence Officer)"]
        S3B["Stage 3b: DETECT<br/>feed-analyst<br/>(Social Media Scout)"]
    end

    subgraph "Weekly"
        PA["post-analyzer<br/>(Performance Analyst)"]
        RB["report-builder<br/>(Reporting Analyst)"]
        SE["strategy-evolver<br/>(Head of Strategy)"]
        CA["competitor-analyst<br/>(Market Researcher)"]
    end

    subgraph "On-Demand"
        CW["content-writer<br/>(Content Creator)"]
    end

    CRON_M --> AUTO
    CRON_W --> REPORT
    AUTO --> S1 --> S2 --> S3A
    S2 --> S3B
    REPORT --> PA --> RB --> SE
    REPORT -.->|">2 Wochen"| CA
    ADHOC --> CW
    ADHOC --> PA
    ADHOC --> CA

    subgraph "Datenspeicher"
        DS[(Excel/CSV/JSON<br/>10 Sheets)]
    end

    S1 --> DS
    S2 --> DS
    S3A --> DS
    S3B --> DS
    PA --> DS
    RB --> DS
    SE --> DS
    CA --> DS
    CW --> DS
```

## Session-Modell

```mermaid
graph TD
    START["Session-Start<br/>(Cron oder ad-hoc)"] --> LOAD["config.json laden<br/>last_session_date prüfen"]
    LOAD --> LOCAL["Lokale Berechnungen<br/>(KEIN API-Call)"]
    LOCAL --> |"Lifecycle-Übergänge<br/>Warm Score Decay<br/>Signal-Expiry"| DELTA["Delta-Daten holen<br/>(nur NEUE Daten)"]
    DELTA --> |"Notifications 1 Call<br/>Active Post Analytics<br/>Feed 1 Call"| PROCESS["Verarbeiten<br/>(Collect → Enrich → Detect)"]
    PROCESS --> SUMMARY["Zusammenfassung<br/>an Mensch"]
    SUMMARY --> UPDATE["last_session_date<br/>= now"]
```

## Daily Pipeline (3 Stages)

```mermaid
graph LR
    subgraph "Stage 1: COLLECT"
        DC["data-collector<br/>(haiku)"]
        N["Notifications<br/>1 API-Call"]
        A["Active Post<br/>Analytics"]
        DC --> N
        DC --> A
    end

    subgraph "Stage 2: ENRICH"
        CS["contact-scanner<br/>(sonnet)"]
        WS["Warm Scores"]
        ICP["ICP Match"]
        CS --> WS
        CS --> ICP
    end

    subgraph "Stage 3: DETECT"
        SD["signal-detector<br/>(sonnet)"]
        FA["feed-analyst<br/>(sonnet)"]
        SIG["Signals"]
        OPP["Comment<br/>Opportunities"]
        SD --> SIG
        FA --> OPP
    end

    DC -->|"Contacts +<br/>Interactions"| CS
    CS -->|"Scored<br/>Contacts"| SD
```

## Post Lifecycle

```mermaid
stateDiagram-v2
    direction LR

    state "Content Pipeline (Status)" as pipeline {
        [*] --> Idea: /ideas
        Idea --> Approved: User approves
        Idea --> Rejected: User rejects
        Approved --> Draft: /draft
        Draft --> Ready: User approves
        Ready --> Published: User posts on LinkedIn
        Published --> Analyzed: 3 Snapshots done
        Analyzed --> Evolved: /evolve
    }

    state "Mess-Phase (Lifecycle)" as measurement {
        [*] --> Active: Published
        Active --> Cooling: Day 7
        Cooling --> Archived: Day 14
    }
```

## Human-in-the-Loop Gates

```mermaid
graph TD
    subgraph "Agent macht AUTONOM"
        D["Daten sammeln"]
        SC["Contacts scoren"]
        SI["Signals erkennen"]
        P["Patterns erkennen"]
        I["Ideen generieren"]
        DR["Drafts schreiben"]
        R["Reports erstellen"]
        SV["Strategie VORSCHLAGEN"]
    end

    subgraph "Mensch entscheidet IMMER"
        IA["Idee annehmen/ablehnen"]
        DA["Draft freigeben"]
        PO["Auf LinkedIn posten"]
        OU["Outreach senden"]
        CO["Kommentar posten"]
        SA["Strategie aktivieren"]
        CN["Connection annehmen"]
    end

    I -->|"vorschlagen"| IA
    DR -->|"vorlegen"| DA
    DA -->|"Ready"| PO
    SV -->|"Human Gate"| SA

    style PO fill:#ff6b6b
    style OU fill:#ff6b6b
    style CO fill:#ff6b6b
    style CN fill:#ff6b6b
    style SA fill:#ffd93d
```

## Learning Loop

```mermaid
graph LR
    CREATE["CREATE<br/>content-writer"] --> PUBLISH["PUBLISH<br/>User postet"]
    PUBLISH --> MEASURE["MEASURE<br/>data-collector"]
    MEASURE --> ANALYZE["ANALYZE<br/>post-analyzer"]
    ANALYZE --> LEARN["LEARN<br/>Patterns + ICP"]
    LEARN --> ADAPT["ADAPT<br/>strategy-evolver"]
    ADAPT --> CREATE

    style ADAPT fill:#4ecdc4
```

## Agents (Marketing-Team)

| Agent | Team-Rolle | Model | Wann | API-Calls |
|-------|-----------|-------|------|-----------|
| data-collector | Data Analyst | haiku | Daily (Stage 1) | Notifications, Analytics |
| contact-scanner | Community Manager | sonnet | Daily (Stage 2) | Keine (Pipeline-Input) |
| signal-detector | Intelligence Officer | sonnet | Daily (Stage 3a) | Keywords-Search |
| feed-analyst | Social Media Scout | sonnet | Daily (Stage 3b) | Feed list |
| post-analyzer | Performance Analyst | sonnet | Weekly + on-demand | Keine (gespeicherte Daten) |
| report-builder | Reporting Analyst | sonnet | Weekly + on-demand | Profile network |
| strategy-evolver | Head of Strategy | opus | Weekly + on-demand | Keine (synthesisiert) |
| content-writer | Content Creator | sonnet | On-demand | Profile show/posts |
| competitor-analyst | Market Researcher | sonnet | On-demand / >2 Wochen | Profile show/posts/engagers |

## Skills (12 Commands)

| Command | Zweck | Agents |
|---------|-------|--------|
| `/setup` | Deep Onboarding (5 Phasen) | Alle |
| `/auto` | Morning Check (3-Stage Pipeline) | data-collector, contact-scanner, signal-detector, feed-analyst |
| `/check` | Quick Status (lokal, kein API) | Keine |
| `/ideas [n]` | Content-Ideen generieren | content-writer |
| `/draft <thema>` | Post oder Kommentar schreiben | content-writer |
| `/analyze [urn]` | Post-Performance analysieren | post-analyzer |
| `/evolve` | Strategie weiterentwickeln | strategy-evolver |
| `/report` | Wochen-Report | report-builder |
| `/competitor <name>` | Wettbewerber analysieren | competitor-analyst |
| `/contacts [arg]` | Kontakte & Network Health | contact-scanner |
| `/outreach <name>` | Personalisierte Nachricht | content-writer |
| `data-schema` | Schema-Referenz (nicht user-invocable) | — |

## Datenmodell

```mermaid
erDiagram
    Posts ||--o{ Contacts : "Engagers"
    Posts ||--o{ Patterns : "erzeugt"
    Posts ||--o{ Signals : "triggert"
    Contacts ||--o{ Signals : "betrifft"
    Patterns ||--o{ Strategy : "informiert"
    Strategy ||--o{ Posts : "leitet"
    Competitors ||--o{ Patterns : "Learnings"
    FeedInsights ||--o{ Signals : "Opportunities"
    ICPProfile ||--o{ Strategy : "schaerft"
    Reports ||--o{ Strategy : "Trends"

    Posts {
        string Title
        select Status
        select Lifecycle
        number Reactions
        number Engagement_Rate
        string URN
    }

    Contacts {
        string Name
        number Warm_Score
        select ICP_Match
        select Score
        date Follow_up_Date
    }

    Patterns {
        string Name
        select Confidence
        select Status
        number Success_Rate
    }

    Strategy {
        string Version
        select Status
        text Content
    }

    Competitors {
        string Name
        number Avg_ER
        text Content_Gaps
    }

    Signals {
        select Type
        select Priority
        select Status
        string Action
    }

    FeedInsights {
        string Topic
        number Momentum_Score
        boolean Comment_Opportunity
    }

    ICPProfile {
        select Dimension
        string Value
        number Engagement_Count
    }

    Reports {
        string Week
        number Total_Reactions
        number Follower_Change
    }
```

## Cron-Jobs (extern)

| Job | Frequenz | Command | Dauer |
|-----|----------|---------|-------|
| Morning Check | Täglich ~08:00 | `/auto` | ~2 min |
| Weekly Review | Sonntag ~20:00 | `/report` + `/evolve` | ~5 min |

Cron ist **nicht Teil des Plugins** — wird extern konfiguriert und ruft Claude Code mit Session-ID + CWD auf.

## Delta-Prinzip

Das System arbeitet **nie** alles von vorne auf. Stattdessen:

1. `config.json → session.last_session_date` speichert wann zuletzt gelaufen
2. Bei jedem Start: nur Daten seit letzter Session holen
3. Notifications = effizienteste Quelle (1 API-Call = 80% der Deltas)
4. Post-Lifecycle begrenzt API-Calls: Archived Posts werden nie wieder angefasst
5. Warm Score Decay wird lokal berechnet (kein API nötig)

## Setup = Warmstart

`/setup` macht mehr als ein Interview — es analysiert bestehende Posts, identifiziert Engager, erkennt erste Patterns und füllt den Datenspeicher. Der erste `/auto`-Run arbeitet mit Deltas, nicht von Null.

```mermaid
graph TD
    P1["Phase 1: Interview<br/>Ziele, ICP, Pillars, Tone"] --> P2["Phase 2: Historische Analyse<br/>20-30 Posts + Analytics + Patterns"]
    P2 --> P3["Phase 3: Contact Seed<br/>Top-Engager + ICP Match + Warm Score"]
    P3 --> P4["Phase 4: Competitor Deep-Dives<br/>Profile + Posts + Content Gaps"]
    P4 --> P5["Phase 5: Generierung<br/>config.json + GEFÜLLTER Datenspeicher<br/>+ Strategy v1.0 + CLAUDE.md"]
```

## Dashboard

`plugin/dashboard.html` — Interaktives HTML-Dashboard das `linkedin-data.xlsx` live liest (via SheetJS). Kein Server nötig, einfach im Browser öffnen. Wird mit dem Plugin ausgeliefert.

**Tabs:** Overview, Posts, Contacts, Signals, Feed, Patterns, Competitors, Strategy

- Agents schreiben in Excel — das Dashboard zeigt es an
- Agents wissen nichts vom Dashboard
- Daten sind immer aktuell (Excel wird bei jedem Öffnen live gelesen)
- Filter, Sortierung, Charts — alles client-side

## Dateistruktur

```
linkedin-cli/
├── config.json              # Zentrale Konfiguration + Session-State
├── linkedin-data.xlsx       # Datenspeicher (10 Sheets)
├── drafts/                  # Post-Entwürfe (.md)
├── CLAUDE.md                # Navigations-Karte (generiert bei /setup)
└── plugin/
    ├── plugin.json           # Plugin-Manifest
    ├── README.md             # Diese Datei
    ├── dashboard.html        # Interaktives Dashboard (liest Excel live)
    ├── agents/
    │   ├── data-collector/   # Stage 1: COLLECT
    │   ├── contact-scanner/  # Stage 2: ENRICH
    │   ├── signal-detector/  # Stage 3a: DETECT
    │   ├── feed-analyst/     # Stage 3b: DETECT (parallel)
    │   ├── post-analyzer/    # Weekly: Performance
    │   ├── report-builder/   # Weekly: Reports
    │   ├── strategy-evolver/ # Weekly: Learning Loop
    │   ├── content-writer/   # On-demand: Content
    │   └── competitor-analyst/ # On-demand: Market Research
    └── skills/
        ├── setup/            # Deep Onboarding (5 Phasen)
        ├── auto/             # Morning Check (3-Stage Pipeline)
        ├── check/            # Quick Status (lokal)
        ├── ideas/            # Ideen generieren
        ├── draft/            # Post/Kommentar schreiben
        ├── analyze/          # Performance analysieren
        ├── evolve/           # Strategie weiterentwickeln
        ├── report/           # Wochen-Report
        ├── competitor/       # Wettbewerber analysieren
        ├── contacts/         # Kontakte + Network Health
        ├── outreach/         # Outreach-Nachrichten
        └── data-schema/      # Schema-Referenz
```

## Kernprinzipien

1. **Delta-basiert** — Nie alles neu scannen. Nur neue Daten seit letzter Session.
2. **Notifications first** — 1 API-Call = 80% der Deltas.
3. **Post-Lifecycle** — Active (7d) → Cooling (14d) → Archived (nie wieder angefasst).
4. **Pipeline, nicht Silos** — Agents arbeiten sequentiell: Collect → Enrich → Detect.
5. **Human-in-the-Loop** — Agent analysiert und schlägt vor. Mensch entscheidet und handelt.
6. **Learning Loop** — strategy-evolver ist das Gehirn. Ohne ihn lernt das System nicht.
7. **Warmstart** — Setup füllt den Datenspeicher. Kein Kaltstart.
