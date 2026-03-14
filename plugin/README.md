# LinkedIn Commander v3 — Plugin Architecture

Self-learning LinkedIn management system. 9 AI agents work as a cohesive marketing team in a delta-based pipeline. The system analyzes, learns, and adapts — but the human decides.

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
    REPORT -.->|">2 weeks"| CA
    ADHOC --> CW
    ADHOC --> PA
    ADHOC --> CA

    subgraph "Data Store"
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

## Session Model

```mermaid
graph TD
    START["Session Start<br/>(Cron or ad-hoc)"] --> LOAD["Load config.json<br/>Check last_session_date"]
    LOAD --> LOCAL["Local Calculations<br/>(NO API call)"]
    LOCAL --> |"Lifecycle transitions<br/>Warm Score decay<br/>Signal expiry"| DELTA["Fetch Delta Data<br/>(only NEW data)"]
    DELTA --> |"Notifications 1 call<br/>Active Post Analytics<br/>Feed 1 call"| PROCESS["Process<br/>(Collect → Enrich → Detect)"]
    PROCESS --> SUMMARY["Summary<br/>to Human"]
    SUMMARY --> UPDATE["last_session_date<br/>= now"]
```

## Daily Pipeline (3 Stages)

```mermaid
graph LR
    subgraph "Stage 1: COLLECT"
        DC["data-collector<br/>(haiku)"]
        N["Notifications<br/>1 API call"]
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

    state "Measurement Phase (Lifecycle)" as measurement {
        [*] --> Active: Published
        Active --> Cooling: Day 7
        Cooling --> Archived: Day 14
    }
```

## Human-in-the-Loop Gates

```mermaid
graph TD
    subgraph "Agent does AUTONOMOUSLY"
        D["Collect data"]
        SC["Score contacts"]
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
| contact-scanner | Community Manager | sonnet | Daily (Stage 2) | None (pipeline input) |
| signal-detector | Intelligence Officer | sonnet | Daily (Stage 3a) | Keyword search |
| feed-analyst | Social Media Scout | sonnet | Daily (Stage 3b) | Feed list |
| post-analyzer | Performance Analyst | sonnet | Weekly + on-demand | None (stored data) |
| report-builder | Reporting Analyst | sonnet | Weekly + on-demand | Profile network |
| strategy-evolver | Head of Strategy | opus | Weekly + on-demand | None (synthesizes) |
| content-writer | Content Creator | sonnet | On-demand | Profile show/posts |
| competitor-analyst | Market Researcher | sonnet | On-demand / >2 weeks | Profile show/posts/engagers |

## Skills (12 Commands)

| Command | Purpose | Agents |
|---------|---------|--------|
| `/setup` | Deep onboarding (5 phases) | All |
| `/auto` | Morning Check (3-stage pipeline) | data-collector, contact-scanner, signal-detector, feed-analyst |
| `/check` | Quick status (local, no API) | None |
| `/ideas [n]` | Generate content ideas | content-writer |
| `/draft <topic>` | Write post or comment | content-writer |
| `/analyze [urn]` | Analyze post performance | post-analyzer |
| `/evolve` | Evolve strategy | strategy-evolver |
| `/report` | Weekly report | report-builder |
| `/competitor <name>` | Analyze competitor | competitor-analyst |
| `/contacts [arg]` | Contacts & network health | contact-scanner |
| `/outreach <name>` | Personalized message | content-writer |
| `data-schema` | Schema reference (not user-invocable) | — |

## Data Model

```mermaid
erDiagram
    Posts ||--o{ Contacts : "Engagers"
    Posts ||--o{ Patterns : "generates"
    Posts ||--o{ Signals : "triggers"
    Contacts ||--o{ Signals : "affects"
    Patterns ||--o{ Strategy : "informs"
    Strategy ||--o{ Posts : "guides"
    Competitors ||--o{ Patterns : "Learnings"
    FeedInsights ||--o{ Signals : "Opportunities"
    ICPProfile ||--o{ Strategy : "sharpens"
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
5. Warm Score decay is calculated locally (no API needed)

## Setup = Warm Start

`/setup` does more than an interview — it analyzes existing posts, identifies engagers, detects initial patterns, and fills the data store. The first `/auto` run works with deltas, not from scratch.

```mermaid
graph TD
    P1["Phase 1: Interview<br/>Goals, ICP, Pillars, Tone"] --> P2["Phase 2: Historical Analysis<br/>20-30 Posts + Analytics + Patterns"]
    P2 --> P3["Phase 3: Contact Seed<br/>Top Engagers + ICP Match + Warm Score"]
    P3 --> P4["Phase 4: Competitor Deep-Dives<br/>Profile + Posts + Content Gaps"]
    P4 --> P5["Phase 5: Generation<br/>config.json + FILLED Data Store<br/>+ Strategy v1.0 + CLAUDE.md"]
```

## Dashboard

`plugin/dashboard.html` — Interactive HTML dashboard that reads `linkedin-data.xlsx` live (via SheetJS). No server needed, just open in browser. Ships with the plugin.

**Tabs:** Overview, Posts, Contacts, Signals, Feed, Patterns, Competitors, Strategy

- Agents write to Excel — the dashboard displays it
- Agents know nothing about the dashboard
- Data is always current (Excel is read live on each open)
- Filters, sorting, charts — all client-side

## File Structure

```
linkedin-cli/
├── config.json              # Central configuration + session state
├── linkedin-data.xlsx       # Data store (10 sheets)
├── drafts/                  # Post drafts (.md)
├── CLAUDE.md                # Navigation map (generated by /setup)
└── plugin/
    ├── plugin.json           # Plugin manifest
    ├── README.md             # This file
    ├── dashboard.html        # Interactive dashboard (reads Excel live)
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
        ├── setup/            # Deep onboarding (5 phases)
        ├── auto/             # Morning Check (3-stage pipeline)
        ├── check/            # Quick status (local)
        ├── ideas/            # Generate ideas
        ├── draft/            # Write post/comment
        ├── analyze/          # Analyze performance
        ├── evolve/           # Evolve strategy
        ├── report/           # Weekly report
        ├── competitor/       # Analyze competitors
        ├── contacts/         # Contacts + network health
        ├── outreach/         # Outreach messages
        └── data-schema/      # Schema reference
```

## Core Principles

1. **Delta-based** — Never rescan everything. Only new data since last session.
2. **Notifications first** — 1 API call = 80% of deltas.
3. **Post lifecycle** — Active (7d) → Cooling (14d) → Archived (never touched again).
4. **Pipeline, not silos** — Agents work sequentially: Collect → Enrich → Detect.
5. **Human-in-the-loop** — Agent analyzes and proposes. Human decides and acts.
6. **Learning loop** — strategy-evolver is the brain. Without it, the system doesn't learn.
7. **Warm start** — Setup fills the data store. No cold start.
