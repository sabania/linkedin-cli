---
name: auto
description: "Morning Check / Session Entry Point. Delta pipeline: Stage 1 COLLECT → Stage 2 ENRICH → Stage 3 DETECT (+ Feed parallel). Merges previous /daily + /auto."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
---

# /auto — Morning Check (Session Entry Point)

The central entry point for every automated session. Runs the 3-stage pipeline and gives the user a prioritized summary.

**Replaces the previous `/daily` and `/auto`.** Called by cron job (daily ~08:00) or manually.

**IMPORTANT: Delegate the work to the specialized agents. Do NOTHING yourself — you are only the orchestrator.**

Use the `Agent` tool to start the following agents **sequentially** (Stage 1→2→3) or **in parallel** (3a+3b):
- **Stage 1:** Start `data-collector` agent
- **Stage 2:** Start `contact-scanner` agent (with Stage 1 output)
- **Stage 3a:** Start `signal-detector` agent (with Stage 2 output)
- **Stage 3b:** Start `feed-analyst` agent (parallel to 3a)

## Usage

```
/auto              # Full Morning Check (3-stage pipeline)
/auto quick        # Stage 1 only (collect data, no feed)
```

## 3-Stage Pipeline

```
Stage 1: COLLECT          Stage 2: ENRICH         Stage 3: DETECT
data-collector  ────────► contact-scanner  ──────► signal-detector
(Data Analyst)            (Community Manager)      (Intelligence Officer)
                                           parallel:
                                                    feed-analyst
                                                    (Social Media Scout)
```

### Stage 1: COLLECT (data-collector agent)

**What happens:**
1. Local calculations (NO API call):
   - Post lifecycle transitions (Active → Cooling → Archived)
   - Archive posts at day 14 (full → mini-summary in data/posts/archive/)
   - Warm Score decay (-5 per week since last session)
   - Signal expiry (New > 7 days → Expired)
2. Auto-discover new published posts via CLI
3. Fetch notifications (1 API call = 80% of deltas)
4. Analytics for active posts (only lifecycle: Active/Cooling)
5. Snapshot checks (Day 3/7/14)

**Output → Stage 2:** New/updated contacts with interaction type and post URN.

### Stage 2: ENRICH (contact-scanner agent)

**Input:** Output from Stage 1 (no own API calls).

**What happens:**
1. Update contacts (create new or update existing in data/contacts/)
2. Recalculate Warm Scores
3. ICP matching for new contacts
4. Dormant detection + reactivation
5. Identify follow-ups

**Output → Stage 3:** Enriched contacts (score changes, new hot contacts, reactivations).

### Stage 3: DETECT (parallel)

**3a: signal-detector agent**
- Input: Enriched contacts from Stage 2
- Detect signals from pipeline input (no API needed for most)
- Optional: Keyword search (1 API call per keyword)
- Write signal files to data/signals/
- Output: Prioritized signal list

**3b: feed-analyst agent (parallel)**
- Independent from Stage 1-2 (own feed call)
- Fetch feed (1 API call)
- Write insight files to data/feed-insights/
- Detect trends, find comment opportunities
- Output: Trending topics + comment opportunities

## Summary to User

```
Morning Check complete (since last session: 18h)

DATA:
  [n] notifications processed
  [n] post metrics updated
  [n] lifecycle transitions (Active→Cooling: 1, Archived: 0)
  [n] new posts auto-discovered

CONTACTS:
  [n] new contacts | [n] updated
  [n] new hot contacts: [names]
  [n] follow-ups due

SIGNALS ([n] new):
  HIGH: engagement_hot — Anna Schmidt (Score: 72)
  HIGH: job_change — Max Mueller (→ VP Engineering @ NewCo)
  MEDIUM: keyword_mention — "AI Agents" in post by @tech-leader

FEED:
  Trending: "AI Agents" (7x, 2.3x avg), "Remote Work" (4x)
  Comment Opportunities:
    1. [HIGH] @sarah-k: "The future of..." (89 Rx in 3h)
    2. [MEDIUM] @tech-leader: "Why we switched..." (45 Rx in 5h)

NEEDS YOUR DECISION:
  - 2 follow-ups due → /contacts follow-up
  - Last post 5 days ago → /draft for new post?
  - New patterns detected → /evolve for strategy update?
  - 2 comment opportunities → Write draft?

ALL GOOD:
  Content pipeline: 5 Ideas, 2 Drafts
  Competitors: current (8 days ago)
  Strategy: v1.2
```

## Optional Checks (at the end)

After the pipeline — hints only, no actions:
- Content pipeline thin (< 3 Ideas in drafts/)? → "/ideas to refill"
- Published post without analysis? → "/analyze <urn>"
- Competitor data > 2 weeks old? → "Competitor update will happen at next /report"
- Weekly report due? → "Create /report"

## Rules

- **Update session** — after completion set `session.last_session_date`
- **Delta-based** — only data since last session
- **Pipeline order** — Stage 1 → 2 → 3 (Feed parallel to 3)
- **Collect data: yes. External actions: only with confirmation.**
- **Never post, send, or comment autonomously**
- **Short and actionable** — no long explanations
- **Agents in parallel** where possible (Stage 3a + 3b)
- **Priority** — signals and follow-ups before content
