---
name: competitor
description: Analyze competitors. Evaluate posts, engagement, content strategy and extract learnings.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /competitor — Analyze Competitor

Analyzes a LinkedIn competitor.

**IMPORTANT: Delegate the work to the `competitor-analyst` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the username.**

## Usage

```
/competitor <username>    # Analyze specific account
/competitor               # Update all saved competitors
```

## Workflow

1. **Start `competitor-analyst` agent** with username
2. **Display result** and save in Competitors sheet
3. **Show comparison** with own numbers

## Rules

- **Public data only**
- **Feed learnings into strategy** (via `/evolve`)
- **Max 5-7 competitors** actively tracked
