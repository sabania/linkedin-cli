---
name: outreach
description: Generate personalized outreach message for a LinkedIn contact.
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

# /outreach — Outreach Message

Generates a personalized message for a LinkedIn contact.

**IMPORTANT: Delegate the work to the `content-writer` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the contact name/ID.**

## Usage

```
/outreach <name-or-public-id>
```

## Workflow

1. **Fetch profile live**: `linkedin-cli profile show <name-or-id> --json` → get current headline, company, etc.
2. **Check signals**: `Grep("<name-or-id>", path="data/signals/")` → find recent interactions (outreach_candidate, comment_reply, etc.)
3. **Start `content-writer` agent** in outreach mode:
   - Use live profile data + signal context
   - Use shared interaction as conversation hook
   - Write personalized message
4. **Show message** — user decides whether/how to send

## Message Types

- **Connection Request** (max 300 characters): Short, reference shared interaction
- **Follow-up Message**: Longer message to existing connection
- **InMail**: For non-connections (if Premium)

## Rules

- **Never send automatically** — always get user confirmation
- **No sales pitch** in first contact
- **Authentic** — matches brand voice, personal
- **Establish connection** — why are you writing to this specific person?
