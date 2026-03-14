# LinkedIn Command Center v3

Self-learning LinkedIn management system. 9 AI agents as a cohesive marketing team. Delta-based pipeline. The human decides — the agent analyzes and supports.

## Setup

**First-time setup:** Run `/setup` — deep onboarding with 5 phases (interview + historical analysis + contact seed + competitor deep-dives + populated data store).

Check if `config.json` exists. If not, run `/setup`.

**Setup options:**
- `/setup` — Deep onboarding (system starts warmed up)
- `/setup reset` — Overwrite existing config
- `/setup validate` — Only check config, change nothing

## Loading Configuration

**IMPORTANT:** Load `config.json` before all operations:

```
config.json contains:
- linkedin.username → LinkedIn API calls
- session.last_session_date → Delta calculation
- lifecycle.active_days / cooling_days → Post lifecycle
- content.pillars → Content strategy
- icp → Ideal Customer Profile
- tracking.format / file → Data store access
```

## Data Structure

### Data Store (10 Sheets)

| Sheet | Purpose |
|-------|---------|
| Posts (33 columns) | Content lifecycle + metrics + lifecycle (Active/Cooling/Archived) |
| Contacts (23) | LinkedIn contacts with Warm Score + ICP Match |
| Patterns (14) | Detected success patterns with confidence |
| Strategy (5) | Versioned content strategy (Active/Archived) |
| Reports (16) | Weekly performance reports |
| Competitors (18) | Competitor tracking |
| Signals (11) | Trigger events and opportunities |
| Feed Insights (14) | Feed analysis, trends, comment opportunities |
| ICP Profile (7) | Ideal Customer Profile (sharpened over time) |
| Comment Tracking (9) | Strategic comments |

### Post Lifecycle (orthogonal to Status)

| Phase | Days | API Load |
|-------|------|----------|
| Active | 0-7 | Analytics on every /auto |
| Cooling | 7-14 | Final snapshot |
| Archived | 14+ | None (never touched again) |

### Local Files

| Path | Purpose |
|------|---------|
| `config.json` | Central configuration + session state |
| `linkedin-data.xlsx` | Data store (or CSV/JSON/SQLite) |
| `drafts/` | Post drafts (.md) |
| `plugin/dashboard.html` | Interactive dashboard (reads Excel live via SheetJS) |

## Commands

| Command | Purpose |
|---------|---------|
| `/setup` | Deep onboarding: 5-phase setup with historical analysis |
| `/auto` | Morning Check: 3-stage delta pipeline (Collect → Enrich → Detect) |
| `/check` | Quick status: local data only, no API |
| `/ideas [n]` | Generate content ideas (8 sources) |
| `/draft <topic>` | Write post or comment |
| `/analyze [urn]` | Analyze post performance (lifecycle-aware) |
| `/evolve` | Evolve strategy (human gate) |
| `/report` | Create weekly report |
| `/competitor <name>` | Analyze competitor (delta-based) |
| `/contacts [arg]` | Manage contacts + network health |
| `/outreach <name>` | Generate personalized message |

## Agents (Marketing Team)

| Agent | Role | Model | Pipeline |
|-------|------|-------|----------|
| data-collector | Data Analyst | haiku | Daily Stage 1: COLLECT |
| contact-scanner | Community Manager | sonnet | Daily Stage 2: ENRICH |
| signal-detector | Intelligence Officer | sonnet | Daily Stage 3a: DETECT |
| feed-analyst | Social Media Scout | sonnet | Daily Stage 3b: DETECT (parallel) |
| post-analyzer | Performance Analyst | sonnet | Weekly + on-demand |
| report-builder | Reporting Analyst | sonnet | Weekly + on-demand |
| strategy-evolver | Head of Strategy | opus | Weekly + on-demand (Learning Loop) |
| content-writer | Content Creator | sonnet | On-demand |
| competitor-analyst | Market Researcher | sonnet | On-demand |

## Core Rules

1. **Delta-based** — only new data since `session.last_session_date`
2. **Notifications first** — 1 API call = 80% of deltas
3. **Respect lifecycle** — never touch archived posts
4. **Load config** before every operation
5. **Load active strategy** before content creation
6. **Update patterns** after analyses
7. **NEVER post, send, or comment** — human acts, agent supports
8. **Human gate** for strategy changes

## Learning Loop

```
CREATE → PUBLISH → MEASURE → ANALYZE → LEARN → ADAPT → CREATE
```

strategy-evolver is the brain. Without it, the system doesn't learn.

## Cron Jobs (external)

| Job | Frequency | What |
|-----|-----------|------|
| Morning Check | Daily ~08:00 | `/auto` |
| Weekly Review | Sunday ~20:00 | `/report` + `/evolve` |
