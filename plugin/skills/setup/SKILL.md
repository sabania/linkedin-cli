---
name: setup
description: Deep onboarding for LinkedIn Commander. Interview + historical post analysis + contact seed + competitor deep dives + system generation. The system starts "warmed up", not empty.
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

You are the setup assistant for LinkedIn Commander. Your job: interview the user AND fill the system with real data. After setup, the system is "warmed up" — the first `/auto` run works with deltas, not from scratch.

**Conversation style:**
- Conversational, not like a form
- Summarize answers and confirm before moving on
- Skip questions that can be inferred from context
- Suggest defaults when the user is unsure
- Group related questions — don't ask each one individually

**Arguments:**
- `/setup` — Normal onboarding
- `/setup reset` — Overwrite existing config.json
- `/setup validate` — Only check if everything is configured, change nothing

---

## Phase 1: Interview

### Step 0: Check existing configuration

```
Check if config.json exists in CWD.
- If yes: Ask if the user wants to update the configuration or start fresh.
- If no: Start the interview.
```

### Step 1: Welcome & Context

> Welcome to LinkedIn Commander! I'll ask you a few questions and then analyze your existing profile. The system will start with real data — not empty. Let's go!

### Step 2: Goals & Motivation

1. **What do you want to achieve with LinkedIn?**
   - Thought Leadership / Show expertise
   - Leads / Win customers
   - Recruiting / Attract talent
   - Brand Awareness / Visibility
   - Networking / Community
   - Multiple? Priority?

2. **What's your current LinkedIn status?**
   - Do you post regularly?
   - How many followers/connections approximately?
   - What works well, what doesn't?

### Step 3: ICP — Ideal Customer Profile

3. **Who is your target audience?**
   - Which job titles/roles do you want to reach?
   - Which industries?
   - Which seniority level?
   - Which region?
   - Which company size?

→ This creates the initial ICP (refined over time from engagement data).

### Step 4: Content Strategy

4. **What topics do you want to post about?**
   → Define 3-5 content pillars with optional weighting

5. **In which language?** DE, EN, both, other

6. **How often do you want to post?** Daily, 3x/week, weekly

7. **What tone fits you?**
   - Professional, casual, educational, provocative, storytelling, technical...
   - Are there LinkedIn accounts whose style you like? (→ save as reference)

### Step 5: Competitors

8. **Do you want to track competitors?**
   - If yes: Enter 1-5 LinkedIn usernames
   - System validates each via `linkedin-cli profile show <id> --json`

### Step 6: Signal Configuration

9. **Which keywords do you want to monitor?** (3-10 keywords)

10. **How aggressive should the signal system be?**
    - Conservative: Only high priority (max 3/day)
    - Normal: High + Medium (max 10/day)
    - Everything: Show all signals

### Step 7: Environment

11. **Check/install LinkedIn CLI**
    ```bash
    linkedin-cli --help 2>/dev/null
    ```
    If not found — install automatically based on environment:

    **Windows (PowerShell):**
    ```bash
    powershell -Command "irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex"
    ```

    **macOS / Linux:**
    ```bash
    curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash
    ```

    **From source (if pip is available):**
    ```bash
    git clone https://github.com/sabania/linkedin-cli.git ~/.linkedin-cli-src
    cd ~/.linkedin-cli-src && pip install -r requirements.txt
    ```

    → After installation, check `linkedin-cli --help` again. If PATH isn't updated, remind user to restart terminal.

12. **LinkedIn Login**
    ```bash
    linkedin-cli whoami --json
    ```
    → Extract username and profile URL from result

---

## Phase 2: Historical Analysis (system starts warm)

**Goal:** Analyze existing posts, calculate baseline, detect initial patterns. The system starts with data, not empty.

### 2.1 Load Posts

```bash
linkedin-cli profile posts <username> --limit 30 --json
```

→ Load last 20-30 posts

### 2.2 Analytics per Post

For each post with URN:
```bash
linkedin-cli posts analytics <urn> --json
```

→ Impressions, Reactions, Comments, Demographics

### 2.3 Classification

For each post, automatically determine:
- **Hook Type**: Statistics, Personal Story, Question, Surprising Fact, Contrarian, How-To, List, Problem-Solution, Behind-Scenes
- **Format**: Text, Image, Video, Document, Carousel, Poll
- **Content Type**: Educational, Case-Study, Opinion, Behind-Scenes, How-To, News-Commentary, Inspirational, Controversial
- **Pillar**: Assignment to defined content pillars
- **CTA Type**: Question, Statement, Link, None
- **Language**: DE, EN, other
- **Length Category**: Short/Medium/Long (calculated from character count)
- **Has Personal Reference**: true/false
- **Is Timely**: true/false

### 2.4 Calculate Baseline

```
baseline = {
    median_reactions: median(all_reactions),
    median_comments: median(all_comments),
    median_impressions: median(all_impressions),
    median_engagement_rate: median(all_er),
    avg_reactions: mean(all_reactions),
    avg_comments: mean(all_comments),
}
```

→ Baseline is the benchmark for all future comparisons.

### 2.5 Detect Initial Patterns

Analysis across all classified posts:
- Which hook types perform above average?
- Which formats?
- Which days/times?
- Which content types?
- Which pillar topics?
- Are there combination patterns?

→ Create patterns with sample size and confidence (usually Low-Medium with 20-30 posts).

### 2.6 Identify Repurposing Candidates

Posts with high engagement rate but low impressions = repurposing candidates.
→ Note in the post body.

### 2.7 Set Lifecycle

All historical posts get lifecycle based on published date:
- Last 7 days → `lifecycle: Active`
- 7-14 days → `lifecycle: Cooling`
- 14+ days → Write to `data/posts/archive/` with mini-summary schema

---

## Phase 3: Contact Seed

**Goal:** Capture top engagers from historical posts, evaluate ICP match, identify initial hot contacts.

### 3.1 Load Engagers

For the top 10 posts (by engagement rate):
```bash
linkedin-cli posts engagers <urn> --limit 50 --json
```

### 3.2 Deduplicate and Enrich

- Merge engagers across all posts
- Calculate interaction count (how often the same person appears)
- Collect interaction types (reaction, comment)

### 3.3 Evaluate ICP Match

For each engager:
- Match headline/title against ICP dimensions
- Match industry
- Estimate seniority
- Score: High, Medium, Low, None

### 3.4 Calculate Warm Score

Initial Warm Score based on historical interactions:
```
+10  per reaction on own post
+25  per comment on own post
+20  for ICP Match (High)
+10  for ICP Match (Medium)
```

### 3.5 Identify Hot Contacts

Contacts with Warm Score >= 60 → Score: Hot
→ These are the most valuable existing relationships.

---

## Phase 4: Competitor Deep Dives

**Only if competitors were defined in Phase 1.**

### 4.1 Per Competitor

```bash
linkedin-cli profile show <competitor-id> --json
linkedin-cli profile posts <competitor-id> --limit 20 --json
```

### 4.2 Aggregation

Per competitor, calculate:
- Avg Reactions, Avg Comments, Avg Engagement Rate
- Posting frequency (posts per week)
- Top Format, Top Hook Type
- Content Pillars (topic mix)

### 4.3 Content Gap Analysis

Compare own pillars vs. competitor pillars:
- Topics competitors cover that we don't → Content Gap
- Topics we cover that competitors don't → Differentiation

### 4.4 Shared Engager Identification

```bash
linkedin-cli posts engagers <competitor-post-urn> --limit 50 --json
```

Cross-reference with our contacts:
- People who engage with both us AND the competitor → Shared Engagers
- Shows overlapping audience

---

## Phase 5: Generation

### 5.1 config.json

```json
{
  "version": "3.0",
  "created": "<today>",

  "linkedin": {
    "username": "<from whoami>",
    "profileUrl": "<from whoami>",
    "fullName": "<from whoami>",
    "company": "<from profile>"
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
    "format": "markdown",
    "data_dir": "data",
    "drafts_dir": "drafts"
  },

  "environment": {
    "cli_path": "",
    "cli_version": ""
  },

  "session": {
    "last_session_date": "<now ISO 8601>",
    "last_report_date": null,
    "last_evolve_date": null,
    "last_competitor_check": "<now if competitors analyzed, else null>",
    "setup_completed": true,
    "posts_baseline_count": 23
  },

  "lifecycle": {
    "active_days": 7,
    "cooling_days": 14
  }
}
```

### 5.2 Create Directory Structure

```bash
mkdir -p data/{posts/archive,contacts,patterns,strategy,reports,competitors,signals,feed-insights,icp,comments}
mkdir -p drafts
```

### 5.3 Write Data Files (FILLED, not empty!)

Fill with data from Phase 2-4, writing one Markdown file per record:

**Posts** (Active/Cooling → `data/posts/`, Archived → `data/posts/archive/`):
```
For each historical post:
  if days_since_published < 14:
    Write("data/posts/{date}-{slug}.md", frontmatter + body)
  else:
    Write("data/posts/archive/{date}-{slug}.md", mini-summary frontmatter)
```

**Contacts** (file per engager):
```
For each engager:
  Write("data/contacts/{public-id}.md", frontmatter with Warm Score + ICP Match)
```

**Patterns** (file per detected pattern):
```
For each pattern:
  Write("data/patterns/{type}-{slug}.md", frontmatter with confidence + metrics)
```

**Competitors** (file per competitor):
```
For each competitor:
  Write("data/competitors/{public-id}.md", frontmatter with all analysis data)
```

**ICP Profile** (file per dimension-value):
```
For each ICP dimension:
  Write("data/icp/{dimension}-{value}.md", frontmatter with engagement data)
```

**Strategy v1.0**:
```
Write("data/strategy/v1.0.md", frontmatter + full strategy text)
```

### 5.4 Create Strategy v1.0

Based on interview + historical analysis:

```markdown
---
version: v1.0
status: Active
valid_from: <today>
changes: "Initial strategy based on setup analysis"
---
## Goals
<From interview answers>

## Target Audience (ICP)
<Target ICP from interview + first actual data from demographics>

## Content Pillars
<Topics with weights + initial performance data per pillar>

## Proven Patterns
<From Phase 2.5 — with caveat "based on N posts">

## Posting Plan
<Frequency from interview + best days/times from historical data>

## Next Hypotheses
<What should be tested first>

## Avoid
<What historically performed poorly>
```

### 5.5 Generate CLAUDE.md

Create a CLAUDE.md in CWD. The **navigation map** for Claude Code and all agents.

```markdown
# LinkedIn Command Center — [User Name]

[Personalized description based on goals]

## Setup

Run `/setup` if config.json does not exist.

## Quick Reference

| What | Where |
|------|-------|
| Configuration | config.json |
| Data Directory | data/ |
| Post Drafts | drafts/ |
| Active Strategy | data/strategy/ (status: Active) |
| Hot Contacts | data/contacts/ (score: Hot) |
| Pending Signals | data/signals/ (status: New) |
| Dashboard | plugin/dashboard.html |

## Commands

| Command | Purpose |
|---------|---------|
| /auto | Morning Check: Delta pipeline, signals, analytics, feed |
| /check | Quick status (local, no API call) |
| /ideas [n] | Generate content ideas |
| /draft <topic> | Write new post |
| /analyze [urn] | Analyze post performance |
| /evolve | Evolve strategy |
| /report | Weekly report |
| /competitor [name] | Analyze competitor |
| /contacts [arg] | Manage contacts & leads |
| /outreach <name> | Personalized message |

## Content Pillars

[Generated from config.json → content.pillars]

## ICP (Ideal Customer Profile)

[Generated from config.json → icp]

## Core Rules

1. Load config.json before every operation
2. Load active strategy before content creation
3. After analyses: check and update patterns
4. Never post or send messages without user confirmation
5. Work delta-based: only new data since last_session_date

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

## Summary to User

```
Setup complete! System is warmed up.

Profile: [Name] (@[username])
Goals: [Goals]
ICP: [Top titles] in [industries], [region]
Content: [n] pillars, [languages], [frequency]
Tracking: Markdown (data/) — file-per-record

Historical Analysis:
  [n] posts analyzed, baseline calculated
  [n] patterns detected (Low-Medium Confidence)
  Best hook: [Top Hook Type]
  Best day: [Best Day]

Contacts:
  [n] engagers captured
  [n] hot contacts (Warm Score >= 60)
  [n] ICP matches (High)

Competitors:
  [n] analyzed

Strategy v1.0 created

Next steps:
1. /auto — Start morning check (delta from now)
2. /ideas — Content ideas based on patterns
3. /draft <topic> — Write your first post
```

---

## Special Cases

### User has no historical posts
- Phase 2 is skipped
- Baseline is calculated after the first 5 posts
- System starts "cold" — that's okay, it improves with every post
