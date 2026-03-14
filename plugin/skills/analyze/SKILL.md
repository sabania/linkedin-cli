---
name: analyze
description: "Analyze post performance. Compares with baseline, detects patterns, evaluates experiments, analyzes comments, updates ICP. Lifecycle-aware."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
---

# /analyze — Analyze Post

Analyzes post performance, detects patterns, and sharpens the ICP. Lifecycle-aware: distinguishes Active/Cooling/Archived posts.

**IMPORTANT: Delegate the work to the `post-analyzer` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the post URN.**

## Usage

```
/analyze <urn>        # Analyze single post
/analyze              # All posts that need analysis
/analyze patterns     # Pattern refresh only (Archived posts)
/analyze icp          # ICP sharpening only
```

## Lifecycle Awareness

| Lifecycle | Analysis Behavior |
|-----------|-------------------|
| **Active** (0-7 days) | Analysis possible, but with caveat "metrics still moving" |
| **Cooling** (7-14 days) | Good data basis, snapshot 2-3 available |
| **Archived** (14+ days) | Final metrics — best basis for pattern detection |

Pattern refresh uses only posts with final metrics (Archived/Analyzed).

## Workflow

### Single Post (/analyze <urn>)

1. **Start `post-analyzer` agent**
2. **Result:**

```
Post Analysis: "Most SMBs underestimate..."
URN: urn:li:activity:7435982583777169408
Lifecycle: Cooling (Day 9)

Performance (Snapshot 2):
  Reactions:       89 (Baseline: 45) → +98% 🔥
  Comments:        12 (Baseline: 5) → +140% 🔥
  Impressions:  3,200 (Baseline: 1,800) → +78%
  Engagement Rate: 3.2% (Baseline: 2.8%) → +14%

Content Properties:
  Hook: Surprising Fact | Format: Text | CTA: Question
  Day: Tuesday | Hour: 8 | Length: Medium (780 chars)

Pattern Match:
  ✅ "Surprising Fact" hook → above average
  ✅ "Tuesday" posting → confirms pattern
  🆕 "Personal Reference" → +40% (Low Confidence, n=4)

ICP Insight:
  Top Engagers: CTOs (30%), Developers (40%), PMs (20%)

Next snapshot in 5 days (Day 14).
```

### Batch (/analyze)

1. All posts with missing snapshots or status "Published" without "Analyzed"
2. For each: Run analysis
3. At the end: Pattern refresh across all posts with final metrics

### Pattern Refresh (/analyze patterns)

Only on Archived/Analyzed posts:
1. For each dimension: Calculate avg, sample size, success rate
2. Test combination patterns
3. Update Patterns sheet
4. Experiment evaluation (if experiments are running)

### ICP Sharpening (/analyze icp)

1. Aggregate top demographics across all posts
2. Compare with configured ICP
3. Update ICP Profile sheet
4. Show delta

## Rules

- **Respect lifecycle** — Active posts with caveat, patterns only from Archived
- **3 snapshots** before status → "Analyzed"
- **Median** as baseline (more robust)
- **Patterns only with data** — min 3 posts per dimension
- **Combos only with min 3 posts** per combination
- **Honest** — if no patterns, say so
