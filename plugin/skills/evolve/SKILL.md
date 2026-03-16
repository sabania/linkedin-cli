---
name: evolve
description: "Evolve content strategy. Orchestrates strategy-evolver agent. Human gate for new versions. Weekly during Weekly Review or on-demand."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
---

# /evolve — Evolve Strategy

Evolves the content strategy based on patterns, ICP data, competitor insights, and performance trends.

**IMPORTANT: Delegate the work to the `strategy-evolver` agent. Do NOTHING yourself — start the agent with the `Agent` tool. The agent proposes, the human decides.**

## Usage

```
/evolve              # Full strategy evolution
/evolve check        # Only check if update is needed (no proposal)
```

## Workflow

1. **Start `strategy-evolver` agent** (opus model — the Head of Strategy)

2. **Agent analyzes** (reads data/patterns/, data/reports/, data/icp/, data/competitors/):
   - New patterns since last evolve
   - ICP delta (target vs. actual audience)
   - Competitor learnings
   - Pillar balance (actual vs. target)
   - KPI trends from reports

3. **Present result:**
   - What has changed since last evolve
   - Which patterns are new/confirmed/deprecated
   - Recommendation: Strategy update needed? (yes/no with reasoning)

4. **If update recommended — show diff:**
   ```
   Strategy v1.2 → v1.3 (Proposal)

   CHANGES:
   + "Question hooks boost comments 2x" → Proven Patterns
   + Tuesday + Thursday as best days → Posting Plan
   - "Video format" → Avoid (Disproven, Sample: 8)
   ~ AI Praxis: 40% → 50% (strongest pillar)
   ~ Behind the Scenes: 20% → 15% (underperforming)

   REASONING:
   - 3 new High-Confidence patterns
   - ICP delta: 60% Developers instead of CTOs → more Educational content
   - Competitor gap: "Team Leadership" topic uncovered

   Should I activate this strategy? [Yes/No]
   ```

5. **Human Gate:**
   - **User confirms** → Archive old strategy, write new version to data/strategy/, update CLAUDE.md
   - **User rejects** → Current strategy stays, document feedback
   - **User modifies** → Incorporate adjustments, present again

## Session

- After evolve: Set `session.last_evolve_date` to today
- During Weekly Review: Automatically called after `/report`

## Rules

- **HUMAN GATE** — never change the active strategy without user confirmation
- **Show the diff** — what changes from old to new
- **Recommend experiments** for areas with Low Confidence
- **Conservative** — v1.1 instead of v2.0 (small steps)
- **Evidence-based** — no changes without data
