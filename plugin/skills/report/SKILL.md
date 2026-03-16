---
name: report
description: Create weekly performance report with KPIs, trends, and insights.
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

# /report — Weekly Report

Creates a weekly performance report.

**IMPORTANT: Delegate the work to the `report-builder` agent. Do NOTHING yourself — start the agent with the `Agent` tool.**

## Usage

```
/report               # Report for current week
/report last          # Report for last week
```

## Workflow

1. **Update data** via `data-collector` agent (fetch current numbers)
2. **Create report** via `report-builder` agent
3. **Display report** and save as data/reports/{year}-cw{week}.md

## Rules

- **Always fresh data** — fetch current numbers before the report
- **Comparable** — same format every week
- **Actionable insights** — not just numbers, also recommendations
