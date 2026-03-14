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
---

# /outreach — Outreach Message

Generates a personalized message for a LinkedIn contact.

**IMPORTANT: Delegate the work to the `content-writer` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the contact name/ID.**

## Usage

```
/outreach <name-or-public-id>
```

## Workflow

1. **Load contact** from data store (name or public ID)
2. **Start `content-writer` agent** in outreach mode:
   - Fetch profile data
   - Use shared interaction as conversation hook
   - Write personalized message
3. **Show message** — user decides whether/how to send

## Message Types

- **Connection Request** (max 300 characters): Short, reference shared interaction
- **Follow-up Message**: Longer message to existing connection
- **InMail**: For non-connections (if Premium)

## Rules

- **Never send automatically** — always get user confirmation
- **No sales pitch** in first contact
- **Authentic** — matches brand voice, personal
- **Establish connection** — why are you writing to this specific person?
