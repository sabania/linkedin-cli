---
name: check
description: "Quick status check without API calls. Shows current state from data store + session info."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
---

# /check — Quick Status

Shows the current state without API calls or updates. Only reads the data store and config.json.

## Workflow

1. **Load config**: `config.json` (incl. session block)
2. **Read data store** (no agent needed, read directly):
   - Posts: Count per status + lifecycle
   - Contacts: Count per score
   - Due follow-ups
   - New signals (Status=New)
   - Last post: When
   - Last report: When
   - Active strategy: Version
   - Running experiments

3. **Show session info**:
   - Last session: When + how long ago
   - Last report: When
   - Last evolve: When
   - Last competitor check: When

4. **Display compact**:

```
LinkedIn Commander Status (@username)

SESSION:
  Last session: 18h ago (yesterday 08:00)
  Last report: CW 10 (4 days ago)
  Last evolve: 11 days ago
  Last competitor check: 8 days ago

CONTENT:
  Posts: 23 total
    Ideas: 3 | Drafts: 1 | Published: 18 | Analyzed: 1
    Active: 2 | Cooling: 1 | Archived: 15
  Last post: 1 day ago
  Strategy: v1.2 (since Mar 03)
  Experiment: hook-type-v1 (7/10 posts)

CONTACTS:
  Total: 245 | Hot: 5 | Warm: 89 | Cold: 122 | Dormant: 29
  Follow-ups due: 2

SIGNALS:
  New: 3 (1 High, 2 Medium)

RECOMMENDATION:
  → /auto for Morning Check (18h since last session)
```

## Rules

- **No API calls** — only read local data
- **No updates** — write nothing
- **Instant** — must finish in under 5 seconds
- **Always show session info** — helps the user know what's current
