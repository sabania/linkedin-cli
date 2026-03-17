---
name: check
description: "Quick status check without API calls. Shows current state from data files + session info."
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
---

# /check — Quick Status

Shows the current state without API calls or updates. Only reads data files and config.json.

## Workflow

1. **Load config**: `config.json` (incl. session block)
2. **Read data files** (no agent needed, read directly):
   - Posts: `Glob("data/posts/*.md")` → count per lifecycle
   - Post archive: `Glob("data/posts/archive/*.md")` → count
   - Ideas/Drafts: `Glob("drafts/*.md")` → count per status
   - New signals: `Grep("status: New", path="data/signals/")`
   - Active strategy: `Grep("status: Active", path="data/strategy/")`
   - Running experiments: `Grep("experiment:", path="data/posts/")`

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
  Posts tracked: 5 active + 3 cooling + 42 archived
  Ideas: 3 | Drafts: 1
  Last post: 1 day ago
  Strategy: v1.2 (since Mar 03)
  Experiment: hook-type-v1 (7/10 posts)

SIGNALS:
  New: 3 (1 High, 2 Medium)

RECOMMENDATION:
  → /auto for Morning Check (18h since last session)
```

## Signal Management (on user request)

If user asks to update a signal (e.g., "mark signal as acted", "dismiss signal X"):
1. `Grep("<search term>", path="data/signals/")` → find matching signal file
2. Read the file to confirm it's the right signal
3. `Edit(file, "status: New", "status: Acted")` (or Acknowledged/Dismissed as requested)
4. Show confirmation to user

This is the **ONLY write operation** /check performs — all other data is read-only.

## Rules

- **No API calls** — only read local data
- **No updates** — write nothing (except signal status changes on explicit user request)
- **Instant** — must finish in under 5 seconds
- **Always show session info** — helps the user know what's current
