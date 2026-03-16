---
name: contacts
description: "Contacts & Leads management. Warm Scores, ICP Matching, Hot Leads, Follow-ups, Dormant Connections, Network Health. Absorbs /network as sub-command."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
---

# /contacts — Manage Contacts

Manages LinkedIn contacts and leads with Warm Score, ICP Match, and follow-up tracking.

**IMPORTANT: Delegate the work to the `contact-scanner` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the sub-command (scan, hot, follow-up, stats, etc.).**

## Usage

```
/contacts scan          # Scan new engagers (via contact-scanner)
/contacts hot           # Show hot contacts (Warm Score >= 60)
/contacts warm          # Warm contacts (Score 25-59)
/contacts follow-up     # Due follow-ups
/contacts dormant       # Dormant connections (>90 days inactive)
/contacts <name>        # Search/show specific contact
/contacts stats         # Network Health + statistics (absorbs /network)
```

## Workflow

### scan
1. **Start `contact-scanner` agent**
2. Show new and updated contacts
3. Warm Scores and ICP matching

### hot
Contacts with score "Hot" from data/contacts/:
```
Grep("score: Hot", path="data/contacts/") → Read each file
```
```
Hot Contacts (5):

  1. Anna Schmidt | CTO @ TechAG
     Warm Score: 85 | ICP: High | 4 Interactions
     Last: Comment 2 days ago
     Status: Engaged → Ready for outreach

  2. Peter Mueller | VP Sales @ SaaS Inc
     Warm Score: 72 | ICP: High | 3 Interactions
     Last: Reaction 5 days ago
     Status: New → Research + Connect
```

### follow-up
Contacts with follow_up_date <= today:
```
Grep("follow_up_date:", path="data/contacts/") → Read each, check date
```
```
Due Follow-ups (2):

  1. Max Muster | Developer @ StartupCo
     Status: Contacted | Outreach: Connection Request 8 days ago
     Response: No Response → Re-follow-up or close out?

  2. Lisa Weber | Head of Product @ BigCorp
     Status: Dormant → Reactivated
     → Reactivate with personalized message
```

### dormant
Connected contacts with last_interaction > dormant_days (default 90 days):
```
Grep("status: Dormant", path="data/contacts/") → Read each
```

### <name>
Search contact and show all details:
```
Grep("<name>", path="data/contacts/") → Read matching file
```
- Profile data, Warm Score, ICP Match
- Interaction history
- Outreach history
- Optional: Refresh profile via CLI

### stats (absorbs /network)
Network Health + contact statistics:
```
Contact Statistics:

Total: 245 | Hot: 5 | Warm: 89 | Cold: 122 | Dormant: 29
New (this week): 12
ICP Match: 34 High, 67 Medium, 144 Low/None
Follow-ups due: 3
Avg Warm Score: 28

Network Health:
  Roles: 75% Developer, 15% Manager, 5% C-Level, 5% Other
  → Gap in decision-makers (ICP says CTO/VP)
  Industries: 80% Software, 10% Finance, 10% Other
  → Too one-sided for lead-gen goal
  Connection Degree: 60% 1st, 30% 2nd, 10% 3rd
  Audience vs. ICP: 60% Developer instead of CTO → adjust content
```

## Rules

- **Privacy** — only public LinkedIn data
- **No spam** — outreach only with user confirmation
- **Quality > Quantity** — better 10 Hot than 100 Cold
- **Warm Score decay** — scores age, applied automatically during /auto and during standalone /contacts scan (if >24h since last session)
