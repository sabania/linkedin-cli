---
name: linkedin-cli-reference
description: "Complete reference for the linkedin-cli tool. Load this skill when you need to call the CLI via Bash to fetch LinkedIn data, manage connections, or send messages."
user-invocable: false
allowed-tools:
  - Bash
---

# LinkedIn CLI Reference

Complete command reference for `linkedin-cli`. Use `--json` on every read command to get machine-readable output.

**Rate limits apply:** Max 15 calls/minute, 80/day (configurable via `config set`).

---

## Prerequisites & Installation

Before using any command, ensure the CLI is installed and logged in:

```bash
# Check if installed
linkedin-cli --help 2>/dev/null
```

**If not found — install:**

```bash
# Windows (PowerShell)
powershell -Command "irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex"

# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash

# From source (if pip available)
git clone https://github.com/sabania/linkedin-cli.git ~/.linkedin-cli-src
cd ~/.linkedin-cli-src && pip install -r requirements.txt
```

After install, restart terminal if `linkedin-cli` is not found in PATH.

**Check login:**

```bash
linkedin-cli whoami --json
```

If not logged in, the CLI will exit with "Not logged in. Run 'linkedin-cli login' first." — inform the user they need to run `linkedin-cli login` (or `login --cookie` on headless servers).

---

## Authentication

```bash
# Browser login (needs display)
linkedin-cli login

# Cookie login (headless servers — no display needed)
linkedin-cli login --cookie "<li_at value>"

# Verify session
linkedin-cli whoami --json
```

**Cookie finden:** Browser → linkedin.com → DevTools (F12) → Application → Cookies → `li_at` → Value kopieren.

---

## Profile

```bash
# Own profile
linkedin-cli whoami --json
# → {plainId, miniProfile: {firstName, lastName, publicIdentifier, occupation, entityUrn}, premiumSubscriber}

# Any profile (by public ID or URN)
linkedin-cli profile show <public-id> --json
# → {firstName, lastName, headline, locationName, summary, followerCount, connectionCount, publicIdentifier, entityUrn}

# Contact info
linkedin-cli profile contact <public-id> --json
# → {email_address, phone_numbers, twitter, websites}

# Skills (DOM scraping — slower)
linkedin-cli profile skills <public-id> --json
# → ["Skill1", "Skill2", ...]

# Work experience (DOM scraping — slower)
linkedin-cli profile experiences <public-id> --json
# → [{company, title, duration, description}, ...]

# Connections of a profile
linkedin-cli profile connections <urn-id> --json
# → [{firstName, lastName, headline, public_id}, ...]

# Posts from a profile
linkedin-cli profile posts <public-id> --limit 5 --json
# → [{urn, text, reactions, comments, shares, posted_at, post_url}, ...]

# Who viewed your profile
linkedin-cli profile views --json
# → [profile view elements]

# Network info (follower/connection count)
linkedin-cli profile network <public-id> --json
```

---

## Posts

All post commands accept either full URN (`urn:li:activity:1234`) or just the activity ID (`1234`).

```bash
# Show a single post
linkedin-cli posts show <urn> --json
# → {urn, text, author, author_profile_id, reactions, comments, shares, date, url}

# Post analytics (Impressions, Demographics — requires Premium)
linkedin-cli posts analytics <urn> --json
# → {activity_id, Impressions, Reactions, Comments, Reposts, "Members reached",
#    date, url, demographics: {
#      "Job title": [{value, pct}], "Industry": [{value, pct}],
#      "Company size": [{value, pct}], "Seniority": [{value, pct}]
#    }}

# Comments on a post
linkedin-cli posts comments <urn> --limit 10 --json
# → [{author, text, profileId, profileUrl}, ...]

# Reactions on a post
linkedin-cli posts reactions <urn> --limit 10 --json
# → [{name, headline, profileId, profileUrl}, ...]

# Engagers (reactions + comments combined, deduplicated)
linkedin-cli posts engagers <urn> --limit 10 --json
# → [{name, headline, profileId, profileUrl, interaction_type: "reaction"|"comment"|"both"}, ...]
```

---

## Feed

```bash
# Your LinkedIn feed
linkedin-cli feed list --limit 10 --json
# → [{urn, text, author, author_profile_id, reactions, comments, shares, posted_at, post_url, is_repost}, ...]
```

---

## Notifications

```bash
linkedin-cli notifications list --limit 10 --json
# → [{headline, date, read, notification_urn, action_url, actor_name, actor_profile_id}, ...]

# Only unread
linkedin-cli notifications list --unread --json
```

---

## Signals (Combined Endpoint)

Aggregates profile views, post engagers, invitations, and notifications in one call.

```bash
linkedin-cli signals daily --limit 5 --posts 3 --json
# → {
#     profile_views: [...],
#     post_engagers: [{name, headline, profileId, interaction_type, post_urn}, ...],
#     invitations: [{name, headline, profile_id, message, sent_time}, ...],
#     notifications: [{headline, date, read, actor_name, actor_profile_id}, ...]
#   }
```

---

## Connections

```bash
# Pending invitations
linkedin-cli connections invitations --limit 10 --json
# → [{name, headline, profile_id, message, entity_urn, shared_secret, sent_time}, ...]

# Send connection request
linkedin-cli connections add <public-id>
linkedin-cli connections add <public-id> --message "Hi, let's connect!"

# Accept/decline invitation
linkedin-cli connections accept <entity-urn> --secret <shared-secret>
linkedin-cli connections decline <entity-urn> --secret <shared-secret>

# Remove connection
linkedin-cli connections remove <public-id>
```

---

## Search

```bash
# People
linkedin-cli search people "software engineer" --limit 10 --json
# → [{name, headline, location, public_id, urn_id, url, connection_degree}, ...]

# Companies
linkedin-cli search companies "microsoft" --limit 10 --json

# Posts/Content
linkedin-cli search posts "AI" --limit 10 --json
linkedin-cli search posts "AI" --sort-by "date_posted" --json

# Jobs
linkedin-cli search jobs "python developer" --limit 10 --json

# Groups
linkedin-cli search groups "data science" --limit 10 --json

# Events
linkedin-cli search events "AI conference" --limit 10 --json
```

---

## Messaging

```bash
# List conversations
linkedin-cli messages list --json
# → [{conversation_id, participants, last_message, unread}, ...]

# Read messages by participant name
linkedin-cli messages read "John Doe" --json

# Send message (to existing conversation)
linkedin-cli messages send --conversation <conv-id> --message "Hello!"

# Send message (to person by profile ID — creates new conversation)
linkedin-cli messages send --to <public-id> --message "Hello!"

# Mark conversation as read
linkedin-cli messages seen <conv-id>
```

---

## Company

```bash
# Company details
linkedin-cli company show <company-slug> --json

# Recent posts from company
linkedin-cli company updates <company-slug> --limit 5 --json

# Follow/unfollow
linkedin-cli company follow <company-slug>
linkedin-cli company unfollow <company-slug>
```

---

## Jobs

```bash
# Job details
linkedin-cli jobs show <job-id> --json

# Required skills
linkedin-cli jobs skills <job-id> --json
```

---

## Config & Rate Limits

```bash
# Show all settings + daily usage counter
linkedin-cli config show

# Change settings
linkedin-cli config set rate_limits.daily_limit 120
linkedin-cli config set rate_limits.calls_per_minute 20
linkedin-cli config set browser.headless false     # show browser window (debug)

# Reset to defaults
linkedin-cli config reset
```

| Setting | Default | Description |
|---------|---------|-------------|
| `rate_limits.daily_limit` | 80 | Max API calls per day |
| `rate_limits.calls_per_minute` | 15 | Max burst calls per minute |
| `browser.headless` | true | Run Chrome headless (no window) |

---

## Best Practices for Agents

1. **Always use `--json`** — structured output is parseable, table output is not
2. **Use `--limit`** — fetch only what you need, each call costs rate limit budget
3. **Prefer `signals daily`** — one call aggregates views + engagers + invitations + notifications
4. **Activity ID shorthand** — `linkedin-cli posts show 7438407227096539136` works (no full URN needed)
5. **Check rate limits** — if you get `RuntimeError: Daily LinkedIn API limit reached`, stop and inform the user
6. **Never post or send automatically** — always show output to user first, let them decide
7. **Cache results** — don't call the same endpoint twice for the same data in one session
