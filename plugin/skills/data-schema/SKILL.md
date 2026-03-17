---
name: data-schema
description: Complete data schema for LinkedIn tracking. Markdown file-per-record with YAML frontmatter. Naming conventions, schemas for all 11 record types, Glob/Read/Write/Edit access patterns.
user-invocable: false
---

# Data Schema Reference

The data store uses **Markdown files with YAML frontmatter** — one file per record, organized in subdirectories under `data/`. This allows agents to use Read/Write/Edit/Glob/Grep directly with zero dependencies.

**Before every data operation:**
1. Read `config.json` → `tracking` for `data_dir` (default: `data`) and `drafts_dir` (default: `drafts`)
2. Read this skill for frontmatter schemas and naming conventions
3. Use Glob/Grep/Read/Write/Edit — no scripts needed

---

## Directory Structure

```
linkedin-cli/
├── config.json
├── drafts/                    # Pre-publish: ideas + drafts
│   ├── idea-ai-agents-future.md
│   └── draft-2026-03-14-ai-agents.md
├── data/
│   ├── posts/                 # Published, actively tracked (0-14 days)
│   │   └── archive/           # Mini-summary of old posts (14+ days)
│   ├── patterns/
│   ├── strategy/
│   ├── reports/
│   ├── competitors/
│   ├── signals/
│   ├── feed-insights/
│   └── icp/
└── plugin/
```

## File Naming Conventions

| Collection | Pattern | Example |
|---|---|---|
| Posts | `{date}-{slug}.md` | `2026-03-14-most-smbs-underestimate.md` |
| Post Archive | same, in `archive/` | `archive/2026-02-28-ai-agents.md` |
| Contacts | `{public-id}.md` | `anna-schmidt.md` |
| Patterns | `{type}-{slug}.md` | `hook-question-boost-comments.md` |
| Strategy | `{version}.md` | `v1.2.md` |
| Reports | `{year}-cw{week}.md` | `2026-cw11.md` |
| Competitors | `{public-id}.md` | `max-anderson.md` |
| Signals | `{date}-{type}-{slug}.md` | `2026-03-14-engagement-hot-anna-schmidt.md` |
| Feed Insights | `{date}-{author-slug}-{urn-suffix}.md` | `2026-03-14-sarah-k-169408.md` |
| ICP | `{dimension}-{value}.md` | `job-title-cto.md` |
| Comments | `{date}-on-{target-author-slug}-{n}.md` | `2026-03-14-on-sarah-k-1.md` |

**Slug algorithm:**
1. Take the input string (title, name, topic)
2. Convert to lowercase
3. Replace spaces and underscores with hyphens
4. Remove all characters except a-z, 0-9, hyphens
5. Collapse multiple hyphens into one
6. Remove leading/trailing hyphens
7. Truncate to 50 characters
8. Remove trailing hyphen if truncation created one

Example: `"Most SMBs underestimate AI!"` → `most-smbs-underestimate-ai`

**URN suffix:** Last 6 digits of the activity URN (e.g., `urn:li:activity:7435982583777169408` → `169408`). Guarantees unique filenames for feed insights from the same author on the same day.

---

## Frontmatter Schemas

### Post (full, in `data/posts/`)

```yaml
---
title: "Most SMBs underestimate..."
status: Published
lifecycle: Active
pillar: AI Praxis
hook_type: Surprising Fact
format: Text
content_type: Educational
language: EN
length_category: Medium
char_count: 780
cta_type: Question
hashtag_count: 3
hashtags: "AI, SMB, Automation"
emoji_count: 2
has_personal_reference: true
is_timely: false
url: "https://linkedin.com/feed/update/..."
urn: "urn:li:activity:7435982583777169408"
published_date: 2026-03-14
published_day: Tuesday
published_hour: 8
reactions: 89
comments: 12
shares: 3
impressions: 3200
members_reached: 2800
engagement_rate: 3.2
followers_gained: 5
profile_views_from_post: 12
top_demographics: '{"Job title": [{"value": "CTO", "pct": "30%"}], "Industry": [{"value": "Software", "pct": "45%"}]}'
last_snapshot: 2
snapshot_date: 2026-03-21
experiment: null
idea_source: Feed Trend
draft_path: "drafts/draft-2026-03-14-most-smbs.md"
---
Notes, analysis results, or any free-text content about this post.
```

#### Allowed Values

| Field | Values |
|-------|--------|
| status | Idea, Approved, Draft, In Review, Ready, Scheduled, Published, Analyzed, Evolved, Rejected |
| lifecycle | Active, Cooling, Archived |
| hook_type | Statistics, Personal Story, Question, Surprising Fact, Contrarian, How-To, List, Problem-Solution, Behind-Scenes |
| format | Text, Image, Video, Document, Carousel, Poll |
| content_type | Educational, Case-Study, Opinion, Behind-Scenes, How-To, News-Commentary, Inspirational, Controversial |
| language | DE, EN, *other* |
| length_category | Short, Medium, Long |
| cta_type | Question, Statement, Link, None |
| idea_source | Feed Trend, Competitor Gap, Repurpose, Pattern, News, Experiment, Audience Request, Manual |

#### Status Flow
```
Idea → Approved → Draft → [In Review →] Ready → [Scheduled →] Published → Analyzed → Evolved
                                                                                ↓
Any status can → Rejected
```

#### Snapshot Timing
- Snapshot 1: Day 3 after publication
- Snapshot 2: Day 7
- Snapshot 3: Day 14 → Status changes to "Analyzed"

### Post Lifecycle (Measurement Phase)

Orthogonal to Status (content pipeline). A post can be `Published + Active`, then `Published + Cooling`, then `Analyzed + Archived`.

| Phase | Days Since Published | What Happens | API Load |
|-------|---------------------|-------------|----------|
| **Active** | 0-7 | Every session: Update metrics from notifications | Analytics during Morning Check |
| **Cooling** | 7-14 | Final snapshot at day 14 | 1x Analytics call |
| **Archived** | 14+ | Extract to archive, delete original | None |

**Automatic transitions (at session start):**
```
For each file in data/posts/*.md:
  Read frontmatter → published_date, lifecycle
  days = (today - published_date)
  if days >= 14 and lifecycle != "Archived":
    → Extract mini-summary to data/posts/archive/{date}-{slug}.md
    → Delete original from data/posts/
  elif days >= 7 and lifecycle == "Active":
    → Edit lifecycle: "Active" → "Cooling"
  elif lifecycle is empty:
    → Edit lifecycle: → "Active"
```

### Post Archive (minimal, in `data/posts/archive/`)

When a post reaches 14+ days, extract a mini-summary and delete the full record. This keeps the active directory small.

```yaml
---
title: "How I built a CLI..."
urn: "urn:li:activity:123"
published_date: 2026-02-28
pillar: Side Projects
hook_type: Personal Story
format: Text
content_type: Educational
reactions: 156
comments: 23
impressions: 4200
engagement_rate: 4.3
---
```

---

### Pattern (`data/patterns/{type}-{slug}.md`)

```yaml
---
name: "Question hooks boost comments"
type: Hook
dimension: Question
dimension_2: null
avg_reactions: 67
avg_comments: 14
avg_engagement_rate: 3.8
avg_impressions: 2900
sample_size: 8
success_rate: 45
confidence: Medium
status: Active
discovery_date: 2026-03-01
---
Notes: Hypothesis confirmed across 8 posts. Question hooks produce 2x comments vs. baseline.
Confounds: Most question posts were published on Tuesday.
```

#### Allowed Values

| Field | Values |
|-------|--------|
| type | Hook, Format, Topic, Timing, Length, CTA, Content-Type, Combination |
| confidence | Low, Medium, High |
| status | Active, Testing, Deprecated, Disproven |

#### Pattern Dimensions for Analysis

| Dimension | Values | Example |
|-----------|--------|---------|
| Hook Type | 9 types | "Question hooks: 2x comments" |
| Format | 6 types | "Carousels: 3x impressions" |
| Content Type | 8 types | "Case Studies > Opinions" |
| Published Day | Mon-Sun | "Tuesday = best day" |
| Published Hour | 0-23 | "8:00 beats 17:00" |
| Length Category | 3 categories | "Medium = sweet spot" |
| CTA Type | 4 types | "Question CTAs: 2x comments" |
| Pillar | User-defined | "AI Praxis = strongest pillar" |
| Has Personal Ref | boolean | "Personal: +40% engagement" |
| Is Timely | boolean | "Timely = reach, Evergreen = engagement" |
| **Combinations** | Pairs | "Question + Carousel + Tuesday" |

---

### Strategy (`data/strategy/{version}.md`)

The body IS the strategy text.

```yaml
---
version: v1.2
status: Active
valid_from: 2026-03-03
changes: "Added question hooks as proven pattern"
---
## Goals
Thought leadership + lead generation...

## Target Audience (ICP)
CTOs and VP Engineering in Software/Manufacturing, DACH region...

## Content Pillars
- AI Praxis (40%): Practical AI applications
- Side Projects (30%): Building in public
...

## Proven Patterns
- Question hooks: 2x comments (n=15)
...

## Avoid
- Video format (disproven, n=8)
```

Only one file should have `status: Active` at a time.

---

### Report (`data/reports/{year}-cw{week}.md`)

```yaml
---
week: "CW 11 2026"
period_start: 2026-03-10
period_end: 2026-03-16
posts_count: 3
total_reactions: 156
total_comments: 23
total_impressions: 4200
avg_reactions: 52
avg_comments: 7.7
avg_engagement_rate: 3.8
followers: 1234
follower_change: 12
top_post_urn: "urn:li:activity:7435982583777169408"
pillar_distribution: '{"AI Praxis": 2, "Side Projects": 1}'
competitor_comparison: "Your Avg ER: 3.8% | @competitor-1: 2.1%"
---
## Insights
- Question hooks still on top (pattern confirmed)
- "Behind the Scenes" pillar missing — plan for next week
- Tuesday posts perform 30% above average

## Next Week
- Plan 1x Behind the Scenes post
- Continue experiment hook-type-v1
```

---

### Competitor (`data/competitors/{public-id}.md`)

```yaml
---
name: Max Anderson
public_id: max-anderson
linkedin_url: "https://linkedin.com/in/max-anderson"
headline: "Head of AI @ TechCorp"
followers: 5200
follower_change: 120
posting_frequency: "4x/week"
avg_reactions: 55
avg_comments: 12
avg_engagement_rate: 2.8
top_format: Carousel
top_hook_type: Question
content_pillars: "AI, Leadership, Product"
shared_engagers: 23
content_gaps: "Team Leadership — they post about it, we don't"
last_analyzed: 2026-03-14
analysis_count: 3
---
Notes: Strong on carousels. Question hooks are their top format.
Inverse gap: We cover Open Source, they don't.
```

---

### Signal (`data/signals/{date}-{type}-{slug}.md`)

```yaml
---
date: 2026-03-14
type: outreach_candidate
contact_name: Anna Schmidt
contact_public_id: anna-schmidt
headline: "CTO @ TechAG"
priority: High
action: outreach
action_detail: "ICP Match High — commented on your post about AI Agents"
status: New
source: "urn:li:activity:7435982583777169408"
---
Additional context or notes.
```

#### Signal Types and Default Priority

| Type | Priority | Trigger | Recommended Action |
|------|----------|---------|-------------------|
| outreach_candidate | High | ICP Match High + interaction | outreach |
| comment_reply | High | Someone commented on your post | reply |
| engagement_cluster | High | Same person 2+ interactions in batch | outreach |
| new_connection_icp | High | New connection/follower matches ICP | welcome_message |
| profile_view | Medium | Someone viewed profile | research |
| keyword_mention | Medium | Keyword in new post | comment |
| comment_opportunity | Medium | High-momentum post in feed | comment |
| competitor_post | Low | New post from competitor | monitor |
| funding_signal | Medium | Company posting many jobs / growing | research |

#### Signal Lifecycle
```
Detected → New → Acknowledged → Acted / Dismissed
                    ↓
        Deleted after 7 days (automatic cleanup)
```

---

### Feed Insight (`data/feed-insights/{date}-{author-slug}-{urn-suffix}.md`)

```yaml
---
urn: "urn:li:activity:..."
author: Sarah K.
author_public_id: sarah-k
text_preview: "The future of AI agents is..."
topic: AI Agents
reactions: 89
comments: 15
posted_at: 2026-03-14T09:30:00
momentum_score: 45.3
is_competitor: false
comment_opportunity: true
comment_priority: High
trend_tag: "AI Agents"
scanned_date: 2026-03-14
---
```

#### Momentum Score
```
momentum = (reactions + comments * 2) / max(hours_since_posted, 1)
```
High score + relevant topic + young post = comment opportunity.

#### Trend Detection
Topic tags aggregated over 7 days. Topics with 3+ appearances and above-average engagement = trend → feeds into `/ideas`.

#### 7-Day Retention
Feed Insights older than 7 days are deleted on each scan.

---

### ICP Profile (`data/icp/{dimension}-{value}.md`)

```yaml
---
dimension: Job Title
value: CTO
engagement_count: 45
conversion_rate: 12.5
source: Post Demographics
confidence: High
last_updated: 2026-03-14
---
```

#### Allowed Values

| Field | Values |
|-------|--------|
| dimension | Job Title, Industry, Seniority, Company Size, Location, Function |
| source | Post Demographics, Engager Profiles, Manual |
| confidence | Low, Medium, High |

#### ICP Sharpening
1. Initial: User defines target ICP during setup
2. Post demographics (from `posts analytics --json`) show who actually engages
3. Engager profiles show which titles/industries interact
4. Delta between target ICP and actual ICP → strategy adjustment
5. Conversion rate shows which dimensions actually lead to hot contacts

---

## Post Retention (Sliding Window)

| Where | What | Max Files |
|-------|------|-----------|
| `drafts/` | Ideas + Drafts (pre-publish) | ~15 active |
| `data/posts/` | Active + Cooling (0-14 days) | ~15-20 |
| `data/posts/archive/` | Analyzed posts (mini-summary) | Grows, but small files |

**Lifecycle:**
1. `/auto` discovers new published post via CLI API
2. Creates `data/posts/{date}-{slug}.md` (lifecycle: Active)
3. Day 7 → Edit lifecycle to Cooling
4. Day 14 → Extract patterns/baseline → Write mini-summary to `archive/` → Delete original
5. Ideas in drafts/ older than 30 days → suggest cleanup

**Auto-discovery:** `linkedin-cli profile posts <username> --limit 5 --json`, check URN against existing files via Grep, create new record if not found.

---

## config.json Session & Lifecycle Block

```json
{
  "session": {
    "last_session_date": "2026-03-13T08:00:00Z",
    "last_report_date": "2026-03-09",
    "last_evolve_date": "2026-03-09",
    "last_competitor_check": "2026-03-01",
    "setup_completed": true,
    "posts_baseline_count": 23
  },
  "lifecycle": {
    "active_days": 7,
    "cooling_days": 14
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `session.last_session_date` | ISO 8601 | When the agent last ran (for delta calculation) |
| `session.last_report_date` | ISO 8601 | Last weekly report |
| `session.last_evolve_date` | ISO 8601 | Last strategy evolution |
| `session.last_competitor_check` | ISO 8601 | Last competitor check |
| `session.setup_completed` | boolean | Setup completed? |
| `session.posts_baseline_count` | number | Number of posts at initial analysis |
| `lifecycle.active_days` | number | Days until Active → Cooling (default: 7) |
| `lifecycle.cooling_days` | number | Days until Cooling → Archived (default: 14) |

---

## Data Access Patterns

### Read all records
```
Glob("data/posts/*.md") → list of files
For each file: Read(file) → parse YAML frontmatter
```

### Find by field
```
Grep("urn: \"urn:li:activity:123\"", path="data/posts/") → matching file
```

### Create record
```
Write("data/signals/{date}-outreach-anna-schmidt.md", "---\ndate: 2026-03-14\ntype: outreach_candidate\n...\n---")
```

### Delete record
```
Bash("rm data/signals/2026-03-01-keyword-old-signal.md")
```

### Find Active Posts
```
Grep("lifecycle: Active", path="data/posts/") → list of files
```

### Find New Signals
```
Grep("status: New", path="data/signals/") → list of files
```

### Find Active Strategy
```
Grep("status: Active", path="data/strategy/") → matching file
```

### Check for duplicate URN
```
Grep("urn: \"urn:li:activity:123\"", path="data/posts/") → if found, skip
```

### Aggregate (e.g., count signals per priority)
```
Grep("priority: High", path="data/signals/", output_mode="count") → count
Grep("priority: Medium", path="data/signals/", output_mode="count") → count
```

