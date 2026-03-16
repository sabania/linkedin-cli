---
name: draft
description: "Create a new LinkedIn post or strategic comment. Uses brand voice, strategy, and patterns. +Comment draft mode."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
---

# /draft — Create Post or Comment

Creates LinkedIn post drafts or strategic comments.

**IMPORTANT: Delegate the work to the `content-writer` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the topic + mode (Post or Comment).**

## Usage

```
/draft <topic>              # Post about a topic
/draft                      # Take next approved idea from pipeline
/draft comment <urn>        # Comment draft for a post (absorbs /comment)
```

## Workflow

### Post Draft

1. **Determine topic:**
   - Argument provided? → Use that topic
   - No argument? → Oldest idea with status "Approved" from drafts/
   - No approved idea? → Ask user or suggest `/ideas`

2. **Start `content-writer` agent** with the topic

3. **Present draft** — show the written post to the user

4. **Feedback loop:**
   - User can suggest changes
   - Iteratively improve post
   - When satisfied: Save to drafts/draft-{date}-{slug}.md

### Comment Draft (/draft comment <urn>)

1. **Load target post** (from data/feed-insights/ or via URN)
2. **Start `content-writer` agent** in comment mode:
   - Reference the post content (not generic)
   - Bring in own expertise
   - Max 300-500 characters
   - Question at the end (encourages thread)
3. **Show to user** — never post automatically

## Rules

- **Always show the draft** before saving
- **User has the final word** — never finalize autonomously
- **One draft per call** — not multiple at once
- **NEVER post automatically** — user copies and posts manually
