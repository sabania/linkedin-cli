---
name: data-schema
description: Complete data schema for LinkedIn tracking. 10 sheets with all columns, types, allowed values. Agents read this skill before reading/writing data.
user-invocable: false
---

# Data Schema Reference

The data store (format set during `/setup` — default: Excel `.xlsx`) tracks all LinkedIn marketing data. The schema below is the **default template** — users can customize it during onboarding.

**Before every data operation:**
1. Read `config.json` → `tracking` for format, file, active sheets, runtime
2. Read this skill for column structure
3. Adapt your script to `tracking.runtime` (python/node/etc.)

---

## Sheet: Posts (33 Columns)

Tracks the entire content lifecycle from idea to analyzed. Every property that can influence performance is a column.

| Column | Type | Source | Description | Allowed Values |
|--------|------|--------|-------------|----------------|
| Title | text | Agent/User | Hook/first line (~80 chars) | |
| Status | select | System/User | Content pipeline status | Idea, Approved, Draft, In Review, Ready, Scheduled, Published, Analyzed, Evolved, Rejected |
| Lifecycle | select | Calculated | Measurement phase (orthogonal to Status) | Active, Cooling, Archived |
| Pillar | select | Agent/User | Content pillar | *From config.json → content.pillars* |
| Hook Type | select | Agent | Style of the first line | Statistics, Personal Story, Question, Surprising Fact, Contrarian, How-To, List, Problem-Solution, Behind-Scenes |
| Format | select | Agent/CLI | Content format | Text, Image, Video, Document, Carousel, Poll |
| Content Type | select | Agent | Content category | Educational, Case-Study, Opinion, Behind-Scenes, How-To, News-Commentary, Inspirational, Controversial |
| Language | select | Agent | Language | DE, EN, *other* |
| Length Category | select | Calculated | Length category | Short (<500 chars), Medium (500-1500), Long (>1500) |
| Char Count | number | Calculated | Exact character count | |
| CTA Type | select | Agent | Call-to-action at the end | Question, Statement, Link, None |
| Hashtag Count | number | Calculated | Number of hashtags | |
| Hashtags | text | Calculated | Comma-separated | |
| Emoji Count | number | Calculated | Number of emojis | |
| Has Personal Reference | boolean | Agent | References own project/experience | true, false |
| Is Timely | boolean | Agent | Current event vs. evergreen | true, false |
| LinkedIn URL | text | User | Post URL after publishing | |
| URN | text | CLI | LinkedIn Activity URN | `urn:li:activity:...` |
| Published Date | date | User/CLI | Publication date | ISO 8601 |
| Published Day | select | Calculated | Day of the week | Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday |
| Published Hour | number | Calculated | Time of day (0-23) | |
| Reactions | number | CLI | Current reactions | |
| Comments | number | CLI | Current comments | |
| Shares | number | CLI | Current shares | |
| Impressions | number | CLI | From Analytics | |
| Members Reached | number | CLI | Unique viewers (Analytics) | |
| Engagement Rate | number | Calculated | (Reactions+Comments+Shares)/Impressions*100 | |
| Followers Gained | number | CLI | New followers from this post | |
| Profile Views From Post | number | CLI | Profile visits from this post | |
| Top Demographics | text | CLI | JSON: Top job titles, industries, seniority from Analytics | |
| Last Snapshot | number | System | Which measurement (1-3) | 1, 2, 3 |
| Snapshot Date | date | System | Last measurement | ISO 8601 |
| Experiment | text | Agent | Experiment assignment | |
| Idea Source | text | Agent | Where the idea came from | Feed Trend, Competitor Gap, Repurpose, Pattern, News, Experiment, Audience Request, Manual |
| Draft Path | text | System | Path to .md draft file | Relative to CWD |

### Status Flow
```
Idea → Approved → Draft → [In Review →] Ready → [Scheduled →] Published → Analyzed → Evolved
                                                                                ↓
Any status can → Rejected
```

### Snapshot Timing
- Snapshot 1: Day 3 after publication
- Snapshot 2: Day 7
- Snapshot 3: Day 14 → Status changes to "Analyzed"

### Post Lifecycle (Measurement Phase)

Orthogonal to Status (content pipeline). A post can be `Published + Active`, then `Published + Cooling`, then `Analyzed + Archived`.

| Phase | Days Since Published | What Happens | API Load |
|-------|---------------------|-------------|----------|
| **Active** | 0-7 | Every session: Update metrics from notifications | Analytics during Morning Check |
| **Cooling** | 7-14 | Final snapshot at day 14 | 1x Analytics call |
| **Archived** | 14+ | Final metrics. Never touched again. | None |

**Automatic transitions (at session start, local):**
```python
for post in posts.where(status="Published"):
    days = (today - post.published_date).days
    if days >= 14 and post.lifecycle != "Archived":
        post.lifecycle = "Archived"
        post.status = "Analyzed"  # if Snapshot 3 exists
    elif days >= 7 and post.lifecycle == "Active":
        post.lifecycle = "Cooling"
    elif post.lifecycle is None:
        post.lifecycle = "Active"
```

---

## Sheet: Contacts (23 Columns)

Tracks LinkedIn contacts, leads, and engagement relationships. Central sheet for audience intelligence.

| Column | Type | Source | Description | Allowed Values |
|--------|------|--------|-------------|----------------|
| Name | text | CLI | Full name | |
| LinkedIn URL | text | Calculated | Profile URL | |
| Public ID | text | CLI | LinkedIn username/slug | |
| Headline | text | CLI | Job title/headline | |
| Company | text | CLI | Current company | |
| Industry | text | CLI | Industry (from profile) | |
| Location | text | CLI | Location | |
| Connection Degree | select | CLI | Connection degree | 1st, 2nd, 3rd |
| Source | select | System | How discovered | Post Reaction, Comment, Profile View, Invitation, Search, Competitor Engager, Feed, Manual |
| Source Detail | text | System | Details (e.g., post URN, search term) | |
| Interaction Types | text | System | Comma-separated | like, comment, share, view, reply, praise, interest, empathy, entertainment |
| Score | select | Calculated | Lead temperature (from Warm Score) | Hot, Warm, Cold |
| Warm Score | number | Calculated | Numeric score 0-100 | |
| ICP Match | select | System | Matches Ideal Customer Profile | High, Medium, Low, None |
| Status | select | User/System | Relationship status | New, Researched, Engaged, Contacted, Replied, Connected, Dormant |
| First Seen | date | System | First contact | ISO 8601 |
| Last Interaction | date | System | Last interaction | ISO 8601 |
| Interaction Count | number | System | Total number of interactions | |
| Follow-up Date | date | System | Next follow-up | ISO 8601 |
| Last Outreach | date | User | When last message was sent | ISO 8601 |
| Outreach Type | select | User | Type of last outreach | Connection Request, Message, InMail, Comment Reply |
| Response Status | select | User | Response to last outreach | Pending, Accepted, Replied, No Response |
| Notes | text | User/Agent | Free text | |

### Warm Score Calculation
```
+10  per reaction on own post
+25  per comment on own post
+15  for profile view
+5   per message (sent or received)
+20  for ICP Match (High)
+10  for ICP Match (Medium)
-5   per week without interaction (decay)
Cap: 100
```

### Score Derivation from Warm Score
- **Hot**: Warm Score >= 60
- **Warm**: Warm Score 25-59
- **Cold**: Warm Score < 25

### Dormant Detection
Contact with Status "Connected" and Last Interaction > 90 days → Status becomes "Dormant"

---

## Sheet: Patterns (14 Columns)

Detected content patterns with confidence level. Basis for data-driven strategy.

| Column | Type | Source | Description | Allowed Values |
|--------|------|--------|-------------|----------------|
| Name | text | Agent | Pattern name | e.g. "Question hooks boost comments" |
| Type | select | Agent | Pattern category | Hook, Format, Topic, Timing, Length, CTA, Content-Type, Combination |
| Dimension | text | Agent | Tested value | e.g. "Question", "Video", "Tuesday" |
| Dimension 2 | text | Agent | For combination patterns | e.g. "Carousel" in "Question + Carousel" |
| Avg Reactions | number | Calculated | Average reactions | |
| Avg Comments | number | Calculated | Average comments | |
| Avg Engagement Rate | number | Calculated | Average engagement rate | |
| Avg Impressions | number | Calculated | Average impressions | |
| Sample Size | number | Calculated | Number of posts | |
| Success Rate | number | Calculated | % above baseline | |
| Confidence | select | Calculated | Statistical confidence | Low (<5 Posts), Medium (5-15), High (>15) |
| Status | select | Agent | Pattern status | Active, Testing, Deprecated, Disproven |
| Discovery Date | date | System | When first detected | ISO 8601 |
| Notes | text | Agent | Hypothesis, confounds | |

### Pattern Dimensions for Analysis

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

## Sheet: Strategy (5 Columns — unchanged)

Versioned content strategy. Only one row with Status=Active.

| Column | Type | Description | Allowed Values |
|--------|------|-------------|----------------|
| Version | text | Version identifier | e.g. "v1.0", "v2.1" |
| Status | select | Whether active | Active, Archived |
| Valid From | date | Valid from | ISO 8601 |
| Changes | text | What changed | |
| Content | text | Full strategy text | Markdown |

---

## Sheet: Reports (16 Columns)

Weekly performance reports with KPIs and trends.

| Column | Type | Description |
|--------|------|-------------|
| Week | text | e.g. "CW 11 2026" |
| Period Start | date | Period start |
| Period End | date | Period end |
| Posts Count | number | Published posts |
| Total Reactions | number | Sum of reactions |
| Total Comments | number | Sum of comments |
| Total Impressions | number | Sum of impressions |
| Avg Reactions | number | Average per post |
| Avg Comments | number | Average per post |
| Avg Engagement Rate | number | Average engagement rate |
| Followers | number | Current count |
| Follower Change | number | +/- since last report |
| Top Post URN | text | Best post of the week |
| Pillar Distribution | text | JSON: Pillar distribution |
| Competitor Comparison | text | Short comparison text |
| Insights | text | Key learnings |

---

## Sheet: Competitors (18 Columns)

Competitor tracking and benchmarking.

| Column | Type | Source | Description |
|--------|------|--------|-------------|
| Name | text | User | Name |
| Public ID | text | User/CLI | LinkedIn username |
| LinkedIn URL | text | Calculated | Profile URL |
| Headline | text | CLI | Their headline |
| Followers | number | CLI | Follower count |
| Follower Change | number | Calculated | Delta since last analysis |
| Posting Frequency | text | Agent | Posts per week |
| Avg Reactions | number | Calculated | Average per post |
| Avg Comments | number | Calculated | Average per post |
| Avg Engagement Rate | number | Calculated | Engagement rate |
| Top Format | select | Agent | Best content format |
| Top Hook Type | select | Agent | Most common hook style |
| Content Pillars | text | Agent | Their topic mix |
| Shared Engagers | number | Agent | People who engage with both |
| Content Gaps | text | Agent | Topics they have that we don't |
| Last Analyzed | date | System | Last analysis |
| Analysis Count | number | System | How often analyzed |
| Notes | text | Agent | Key learnings |

---

## Sheet: Signals (11 Columns)

Trigger events that prompt actions. Signal inbox for daily work.

| Column | Type | Source | Description | Allowed Values |
|--------|------|--------|-------------|----------------|
| Date | date | System | When detected | ISO 8601 |
| Type | select | System | Signal type | profile_view, engagement_hot, repeat_engagement, job_change, keyword_mention, competitor_post, new_follower_icp, dormant_reactivation, comment_opportunity, funding_signal |
| Contact Name | text | System | Affected person | |
| Contact Public ID | text | System | For linking | |
| Headline | text | System | Context | |
| Priority | select | Calculated | Urgency | High, Medium, Low |
| Action | select | System | Recommended action | follow_up, connect, comment, outreach, research, monitor |
| Action Detail | text | Agent | Concrete recommendation | |
| Status | select | User/System | Processing status | New, Acknowledged, Acted, Dismissed, Expired |
| Source | text | System | What triggered it (URN, search, etc.) | |
| Notes | text | Agent | Additional context | |

### Signal Types and Default Priority

| Type | Priority | Trigger | Recommended Action |
|------|----------|---------|-------------------|
| engagement_hot | High | Warm Score exceeds threshold | outreach |
| repeat_engagement | High | 3+ interactions in 30 days | follow_up |
| job_change | High | Headline has changed | outreach |
| new_follower_icp | High | New follower matches ICP | connect |
| profile_view | Medium | Someone viewed profile | research |
| keyword_mention | Medium | Keyword in new post | comment |
| dormant_reactivation | Medium | Silent contact engages again | follow_up |
| comment_opportunity | Medium | High-momentum post in feed | comment |
| competitor_post | Low | New post from competitor | monitor |
| funding_signal | Medium | Company posting many jobs / growing | research |

### Signal Lifecycle
```
Detected → New → Acknowledged → Acted / Dismissed
                                    ↓
New → Expired (after 7 days without action)
```

---

## Sheet: Feed Insights (14 Columns)

Analyzed feed posts for trend detection and comment intelligence.

| Column | Type | Source | Description |
|--------|------|--------|-------------|
| URN | text | CLI | Post URN |
| Author | text | CLI | Who posted |
| Author Public ID | text | CLI | For linking |
| Text Preview | text | CLI | First 200 characters |
| Topic | text | Agent | Detected topic (AI-classified, maps to own pillars + "Other") |
| Reactions | number | CLI | Reaction count |
| Comments | number | CLI | Comment count |
| Posted At | date | CLI | Publication time |
| Momentum Score | number | Calculated | `(reactions + comments*2) / max(hours_since_post, 1)` |
| Is Competitor | boolean | System | Is a tracked competitor |
| Comment Opportunity | boolean | Agent | Worth commenting on |
| Comment Priority | select | Agent | Prioritization | High, Medium, Low |
| Trend Tag | text | Agent | Trending topic tag |
| Scanned Date | date | System | When scanned |

### Momentum Score
Measures how fast a post collects engagement:
```
momentum = (reactions + comments * 2) / max(hours_since_posted, 1)
```
High score + relevant topic + young post = comment opportunity.

### Trend Detection
Topic tags are aggregated over 7 days. Topics with 3+ appearances and above-average engagement = trend → feeds into `/ideas`.

---

## Sheet: ICP Profile (7 Columns)

Ideal Customer Profile — sharpened over time from engagement data.

| Column | Type | Source | Description | Allowed Values |
|--------|------|--------|-------------|----------------|
| Dimension | select | System | Profile dimension | Job Title, Industry, Seniority, Company Size, Location, Function |
| Value | text | Agent | Concrete value | e.g. "CTO", "Software", "DACH" |
| Engagement Count | number | Calculated | How many engagers match | |
| Conversion Rate | number | Calculated | % that became hot contacts | |
| Source | text | System | Where the data comes from | Post Demographics, Engager Profiles, Manual |
| Confidence | select | Calculated | Data confidence | Low, Medium, High |
| Last Updated | date | System | Last update | ISO 8601 |

### ICP Sharpening
1. Initial: User defines target ICP during setup
2. Post demographics (from `posts analytics --json`) show who actually engages
3. Engager profiles show which titles/industries interact
4. Delta between target ICP and actual ICP → strategy adjustment
5. Conversion rate shows which dimensions actually lead to hot contacts

---

## Sheet: Comment Tracking (9 Columns)

Tracks strategic comments on other people's posts.

| Column | Type | Source | Description |
|--------|------|--------|-------------|
| Target Post URN | text | User/Agent | Where commented |
| Target Author | text | Agent | Whose post |
| Target Author Public ID | text | Agent | For linking |
| Comment Text | text | User | What was commented |
| Comment Date | date | User | When |
| Target Post Reactions | number | CLI | How big the target post was |
| Visibility Gained | select | Agent | Estimated visibility (High/Medium/Low) |
| New Connections From | number | User | Resulting new connections |
| Notes | text | User | Free text |

---

## config.json Session & Lifecycle Block

In addition to the existing config fields (`linkedin`, `goals`, `icp`, `content`, `competitors`, `signals`, `tracking`, `environment`), the config contains:

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

**Delta calculation at session start:**
```python
from datetime import datetime
last = datetime.fromisoformat(config["session"]["last_session_date"])
delta = datetime.now() - last
# → Only fetch data since last_session_date
# → Warm Score decay: -5 * (delta.days / 7)
# → Calculate lifecycle transitions for all Published posts
```

---

## Data Access Patterns

### Reading Excel (Python)
```python
import openpyxl

wb = openpyxl.load_workbook("linkedin-data.xlsx")
ws = wb["Posts"]
headers = [cell.value for cell in ws[1]]
records = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if all(v is None for v in row):
        continue
    records.append(dict(zip(headers, row)))
```

### Writing/Updating Excel (Python)
```python
import openpyxl

wb = openpyxl.load_workbook("linkedin-data.xlsx")
ws = wb["Posts"]
headers = [cell.value for cell in ws[1]]

# Append new row
ws.append(["My Post Title", "Idea", "AI Praxis", ...])

# Update existing row (find by URN)
urn_col = headers.index("URN") + 1
for row in ws.iter_rows(min_row=2):
    if row[urn_col - 1].value == target_urn:
        row[headers.index("Reactions")].value = new_reactions
        break

wb.save("linkedin-data.xlsx")
```

### Creating Excel with all Sheets (Python)
```python
import openpyxl

SCHEMA = {
    "Posts": ["Title", "Status", "Lifecycle", "Pillar", ...],  # 33 columns
    "Contacts": ["Name", "LinkedIn URL", ...],     # 23 columns
    "Patterns": ["Name", "Type", ...],             # 14 columns
    "Strategy": ["Version", "Status", ...],        # 5 columns
    "Reports": ["Week", "Period Start", ...],      # 16 columns
    "Competitors": ["Name", "Public ID", ...],     # 18 columns
    "Signals": ["Date", "Type", ...],              # 11 columns
    "Feed Insights": ["URN", "Author", ...],       # 14 columns
    "ICP Profile": ["Dimension", "Value", ...],    # 7 columns
    "Comment Tracking": ["Target Post URN", ...],  # 9 columns
}

wb = openpyxl.Workbook()
wb.remove(wb.active)
for sheet_name, headers in SCHEMA.items():
    ws = wb.create_sheet(sheet_name)
    ws.append(headers)
wb.save("linkedin-data.xlsx")
```

### Querying (Python)
```python
# Published posts sorted by engagement rate
published = sorted(
    [r for r in posts if r["Status"] == "Published"],
    key=lambda r: r.get("Engagement Rate") or 0,
    reverse=True
)

# Hot contacts with pending follow-up
from datetime import date
hot_followups = [
    r for r in contacts
    if r.get("Score") == "Hot"
    and r.get("Follow-up Date")
    and r["Follow-up Date"] <= date.today()
]

# New signals
new_signals = [s for s in signals if s.get("Status") == "New"]
high_priority = [s for s in new_signals if s.get("Priority") == "High"]

# Trending topics from feed
from collections import Counter
topics = Counter(f.get("Topic") for f in feed_insights if f.get("Topic"))
trending = [t for t, count in topics.most_common(5) if count >= 3]

# Active patterns with high confidence
proven = [p for p in patterns if p["Status"] == "Active" and p["Confidence"] == "High"]
```
