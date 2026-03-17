---
name: auto
description: "Morning Check / Session Entry Point. Delta pipeline: Stage 1 COLLECT → Stage 2 DETECT (+ Feed parallel). On-the-fly engagement analysis, no stored contacts."
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

The central entry point for every automated session. Runs the 2-stage pipeline and gives the user a prioritized summary.

**Replaces the previous `/daily` and `/auto`.** Called by cron job (daily ~08:00) or manually.

**IMPORTANT: Delegate the work to the specialized agents. Do NOTHING yourself — you are only the orchestrator.**

Use the `Agent` tool to start the following agents **sequentially** (Stage 1→2) or **in parallel** (2a+2b):
- **Stage 1:** Start `data-collector` agent
- **Stage 2a:** Start `signal-detector` agent (with Stage 1 output)
- **Stage 2b:** Start `feed-analyst` agent (parallel to 2a)

## Usage

```
/auto              # Full Morning Check (2-stage pipeline)
/auto quick        # Stage 1 only (collect data, no feed)
```

## 2-Stage Pipeline

```
Stage 1: COLLECT              Stage 2: DETECT
data-collector  ────────────► signal-detector
(Data Analyst)         parallel:
                               feed-analyst
                               (Social Media Scout)
```

### Stage 1: COLLECT (data-collector agent)

**What happens:**
1. Local calculations (NO API call):
   - Post lifecycle transitions (Active → Cooling → Archived)
   - Archive posts at day 14 (full → mini-summary in data/posts/archive/)
   - Signal cleanup (> 7 days → delete)
   - Draft cleanup check (> 30 days → suggestion)
2. Auto-discover new published posts via CLI
3. Fetch notifications (1 API call = 80% of deltas)
4. Analytics for active posts (only lifecycle: Active/Cooling)
5. Snapshot checks (Day 3/7/14)

**Output → Stage 2:** Engagement data (commenters, reactors, profile viewers, new connections — with name, headline, post URN).

### Stage 2: DETECT (parallel)

**2a: signal-detector agent**
- Input: Engagement data from Stage 1
- On-the-fly ICP matching (headline vs. config.icp — no stored contacts)
- Generate signals: outreach_candidate, comment_reply, new_connection_icp, profile_view, keyword_mention
- Write signal files to data/signals/
- Output: Prioritized signal list

**2b: feed-analyst agent (parallel)**
- Independent from Stage 1 (own feed call)
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

SIGNALS ([n] new):
  HIGH: comment_reply — Sarah K commented on "AI in Practice"
  HIGH: outreach_candidate — Anna Schmidt (CTO @ TechAG, ICP: High)
  MEDIUM: keyword_mention — "AI Agents" in post by @tech-leader

FEED:
  Trending: "AI Agents" (7x, 2.3x avg), "Remote Work" (4x)
  Comment Opportunities:
    1. [HIGH] @sarah-k: "The future of..." (89 Rx in 3h)
    2. [MEDIUM] @tech-leader: "Why we switched..." (45 Rx in 5h)

NEEDS YOUR DECISION:
  - 2 comment replies pending → reply on LinkedIn
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
- **Pipeline order** — Stage 1 → 2 (Feed parallel to 2)
- **Collect data: yes. External actions: only with confirmation.**
- **Never post, send, or comment autonomously**
- **Short and actionable** — no long explanations
- **Agents in parallel** where possible (Stage 2a + 2b)
- **Priority** — signals before content
