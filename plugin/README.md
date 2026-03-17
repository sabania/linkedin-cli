# LinkedIn Commander v3 — Plugin Architecture

Self-learning LinkedIn management system. 8 AI agents work as a cohesive marketing team in a delta-based pipeline. The system analyzes, learns, and adapts — but the human decides.

## Architecture

```mermaid
graph TB
    subgraph "Cron (external)"
        CRON_M["☀️ Morning Check<br/>daily ~08:00"]
        CRON_W["📊 Weekly Review<br/>Sunday ~20:00"]
    end

    subgraph "Entry Points"
        AUTO["/auto"]
        REPORT["/report + /evolve"]
        ADHOC["Ad-hoc Commands<br/>/ideas /draft /analyze ..."]
    end

    subgraph "2-Stage Pipeline (Daily)"
        S1["Stage 1: COLLECT<br/>data-collector<br/>(Data Analyst)"]
        S2A["Stage 2a: DETECT<br/>signal-detector<br/>(Intelligence Officer)"]
        S2B["Stage 2b: DETECT<br/>feed-analyst<br/>(Social Media Scout)"]
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
    AUTO --> S1 --> S2A
    S1 --> S2B
    REPORT --> PA --> RB --> SE
    REPORT -.->|">2 weeks"| CA
    ADHOC --> CW
    ADHOC --> PA
    ADHOC --> CA

    subgraph "Data Store"
        DS[(Markdown Files<br/>data/ directory)]
    end

    S1 --> DS
    S2A --> DS
    S2B --> DS
    PA --> DS
    RB --> DS
    SE --> DS
    CA --> DS
    CW --> DS
```

## Session Model

```mermaid
graph TD
    START["Session Start<br/>(Cron or ad-hoc)"] --> LOAD["Load config.json<br/>Check last_session_date"]
    LOAD --> LOCAL["Local Calculations<br/>(NO API call)"]
    LOCAL --> |"Lifecycle transitions<br/>Signal cleanup (7d)<br/>Draft cleanup check"| DELTA["Fetch Delta Data<br/>(only NEW data)"]
    DELTA --> |"Notifications 1 call<br/>Active Post Analytics + Comments<br/>Auto-Discovery + Draft Linking<br/>Feed 1 call"| PROCESS["Process<br/>(Collect → Detect)"]
    PROCESS --> SUMMARY["Summary<br/>to Human"]
    SUMMARY --> UPDATE["last_session_date<br/>= now"]
```

## Daily Pipeline (2 Stages)

```mermaid
graph LR
    subgraph "Stage 1: COLLECT"
        DC["data-collector<br/>(haiku)"]
        N["Notifications<br/>1 API call"]
        A["Active Post<br/>Analytics + Comments"]
        AD["Auto-Discovery<br/>+ Draft Linking"]
        DC --> N
        DC --> A
        DC --> AD
    end

    subgraph "Stage 2: DETECT (parallel)"
        SD["signal-detector<br/>(sonnet)"]
        FA["feed-analyst<br/>(sonnet)"]
        SIG["Signals +<br/>ICP Matching"]
        OPP["Comment<br/>Opportunities"]
        SD --> SIG
        FA --> OPP
    end

    DC -->|"Notifications +<br/>Interactions"| SD
    DC -->|"Feed Data"| FA
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

    state "Measurement Phase (Lifecycle)" as measurement {
        [*] --> Active: Published + Auto-Discovery
        Active --> Cooling: Day 7 + Snapshot 2
        Cooling --> Archived: Day 14 + Snapshot 3
    }

    note right of measurement
        Auto-Discovery links drafts/ to data/posts/
        Snapshots record metrics in post body
    end note
```

## Human-in-the-Loop Gates

```mermaid
graph TD
    subgraph "Agent does AUTONOMOUSLY"
        D["Collect data"]
        SI["Detect signals"]
        P["Detect patterns"]
        I["Generate ideas"]
        DR["Write drafts"]
        R["Create reports"]
        SV["PROPOSE strategy"]
    end

    subgraph "Human decides ALWAYS"
        IA["Accept/reject idea"]
        DA["Approve draft"]
        PO["Post on LinkedIn"]
        OU["Send outreach"]
        CO["Post comment"]
        SA["Activate strategy"]
        CN["Accept connection"]
    end

    I -->|"propose"| IA
    DR -->|"present"| DA
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
    CREATE["CREATE<br/>content-writer"] --> PUBLISH["PUBLISH<br/>User posts"]
    PUBLISH --> MEASURE["MEASURE<br/>data-collector"]
    MEASURE --> ANALYZE["ANALYZE<br/>post-analyzer"]
    ANALYZE --> LEARN["LEARN<br/>Patterns + ICP"]
    LEARN --> ADAPT["ADAPT<br/>strategy-evolver"]
    ADAPT --> CREATE

    style ADAPT fill:#4ecdc4
```

## Agents (Marketing Team)

| Agent | Team Role | Model | When | API Calls |
|-------|-----------|-------|------|-----------|
| data-collector | Data Analyst | haiku | Daily (Stage 1) | Notifications, Analytics |
| signal-detector | Intelligence Officer | sonnet | Daily (Stage 2a) | Keyword search |
| feed-analyst | Social Media Scout | sonnet | Daily (Stage 2b) | Feed list |
| post-analyzer | Performance Analyst | sonnet | Weekly + on-demand | None (stored data) |
| report-builder | Reporting Analyst | sonnet | Weekly + on-demand | Profile network |
| strategy-evolver | Head of Strategy | opus | Weekly + on-demand | None (synthesizes) |
| content-writer | Content Creator | sonnet | On-demand | Profile show/posts |
| competitor-analyst | Market Researcher | sonnet | On-demand / >2 weeks | Profile show/posts/engagers |

## Skills (11 Commands)

| Command | Purpose | Agents |
|---------|---------|--------|
| `/setup` | Deep onboarding (4 phases) | All |
| `/auto` | Morning Check (2-stage pipeline) | data-collector, signal-detector, feed-analyst |
| `/check` | Quick status (local, no API) | None |
| `/ideas [n]` | Generate content ideas | content-writer |
| `/draft <topic>` | Write post or comment | content-writer |
| `/analyze [urn]` | Analyze post performance | post-analyzer |
| `/evolve` | Evolve strategy | strategy-evolver |
| `/report` | Weekly report | report-builder |
| `/competitor <name>` | Analyze competitor | competitor-analyst |
| `/outreach <name>` | Personalized message | content-writer |
| `data-schema` | Schema reference (not user-invocable) | — |

## Data Model

```mermaid
erDiagram
    Posts ||--o{ Patterns : "generates"
    Posts ||--o{ Signals : "triggers"
    Patterns ||--o{ Strategy : "informs"
    Strategy ||--o{ Posts : "guides"
    Competitors ||--o{ Patterns : "Learnings"
    FeedInsights ||--o{ Signals : "Opportunities"
    ICPProfile ||--o{ Strategy : "sharpens"
    Reports ||--o{ Strategy : "Trends"

    Posts {
        string title
        select status
        select lifecycle
        number reactions
        number engagement_rate
        string urn
    }

    Patterns {
        string name
        select confidence
        select status
        number success_rate
    }

    Strategy {
        string version
        select status
        text body
    }

    Competitors {
        string name
        number avg_engagement_rate
        text content_gaps
    }

    Signals {
        select type
        select priority
        select status
        string action
    }

    FeedInsights {
        string topic
        number momentum_score
        boolean comment_opportunity
    }

    ICPProfile {
        select dimension
        string value
        number engagement_count
    }

    Reports {
        string week
        number total_reactions
        number follower_change
    }
```

## Cron Jobs (external)

| Job | Frequency | Command | Duration |
|-----|-----------|---------|----------|
| Morning Check | Daily ~08:00 | `/auto` | ~2 min |
| Weekly Review | Sunday ~20:00 | `/report` + `/evolve` | ~5 min |

Cron is **not part of the plugin** — configured externally and calls Claude Code with session ID + CWD.

## Delta Principle

The system **never** reprocesses everything from scratch. Instead:

1. `config.json → session.last_session_date` stores when last run
2. On each start: only fetch data since last session
3. Notifications = most efficient source (1 API call = 80% of deltas)
4. Post lifecycle limits API calls: Archived posts are never touched again
5. Auto-discovery links new published posts to existing drafts
6. Snapshot metrics are recorded in post body at Day 3, 7, 14

## Setup = Warm Start

`/setup` does more than an interview — it analyzes existing posts, identifies engagers, detects initial patterns, and fills the data store. The first `/auto` run works with deltas, not from scratch.

```mermaid
graph TD
    P1["Phase 1: Interview<br/>Goals, ICP, Pillars, Tone"] --> P2["Phase 2: Historical Analysis<br/>20-30 Posts + Analytics + Patterns"]
    P2 --> P3["Phase 3: Competitor Deep-Dives<br/>Profile + Posts + Content Gaps"]
    P3 --> P4["Phase 4: Generation<br/>config.json + FILLED Data Store<br/>+ Strategy v1.0 + CLAUDE.md"]
```

## Dashboard

`plugin/dashboard.html` — Interactive HTML dashboard. No server needed, just open in browser. Ships with the plugin.

**Tabs:** Overview, Posts, Signals, Feed, Patterns, Competitors, Strategy

- Agents write Markdown files to `data/`
- Agents know nothing about the dashboard
- Filters, sorting, charts — all client-side

## File Structure

```
linkedin-cli/
├── config.json              # Central configuration + session state
├── data/                    # All tracking data (Markdown file-per-record)
│   ├── posts/               # Active + Cooling posts (0-14 days)
│   │   └── archive/         # Mini-summaries of archived posts
│   ├── patterns/            # Detected patterns
│   ├── strategy/            # Versioned strategies
│   ├── reports/             # Weekly reports
│   ├── competitors/         # Competitor profiles
│   ├── signals/             # Trigger events
│   ├── feed-insights/       # Feed analysis (7-day retention)
│   └── icp/                 # ICP dimensions
├── drafts/                  # Post drafts (.md)
├── CLAUDE.md                # Navigation map (generated by /setup)
└── plugin/
    ├── plugin.json           # Plugin manifest
    ├── README.md             # This file
    ├── dashboard.html        # Interactive dashboard
    ├── agents/
    │   ├── data-collector.md # Stage 1: COLLECT
    │   ├── signal-detector.md # Stage 2a: DETECT
    │   ├── feed-analyst.md   # Stage 2b: DETECT (parallel)
    │   ├── post-analyzer.md  # Weekly: Performance
    │   ├── report-builder.md # Weekly: Reports
    │   ├── strategy-evolver.md # Weekly: Learning Loop
    │   ├── content-writer.md # On-demand: Content
    │   └── competitor-analyst.md # On-demand: Market Research
    └── skills/
        ├── setup/            # Deep onboarding (4 phases)
        ├── auto/             # Morning Check (2-stage pipeline)
        ├── check/            # Quick status (local)
        ├── ideas/            # Generate ideas
        ├── draft/            # Write post/comment
        ├── analyze/          # Analyze performance
        ├── evolve/           # Evolve strategy
        ├── report/           # Weekly report
        ├── competitor/       # Analyze competitors
        ├── outreach/         # Outreach messages
        └── data-schema/      # Schema reference
```

## Core Principles

1. **Delta-based** — Never rescan everything. Only new data since last session.
2. **Notifications first** — 1 API call = 80% of deltas.
3. **Post lifecycle** — Active (7d) → Cooling (14d) → Archived (never touched again).
4. **Pipeline, not silos** — Agents work sequentially: Collect → Detect.
5. **Human-in-the-loop** — Agent analyzes and proposes. Human decides and acts.
6. **Learning loop** — strategy-evolver is the brain. Without it, the system doesn't learn.
7. **Warm start** — Setup fills the data store. No cold start.
