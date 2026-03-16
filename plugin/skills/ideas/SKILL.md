---
name: ideas
description: Generate content ideas from 8 sources. Feed Trends, Competitor Gaps, Repurposing, Patterns, News, Experiments, Audience Requests, User Input.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Agent
  - Glob
  - Grep
  - WebSearch
---

# /ideas — Generate Ideas

Generates content ideas from 8 different sources for maximum variety and relevance.

**IMPORTANT: Delegate the work to the `content-writer` agent. Do NOTHING yourself — start the agent with the `Agent` tool and pass the count + optional pillar.**

## Usage

```
/ideas              # 5 ideas from all sources (default)
/ideas 10           # 10 ideas
/ideas AI Praxis    # Ideas for a specific pillar
```

## 8 Sources

1. **Feed Trends** — What's hot in data/feed-insights/ right now?
2. **Competitor Gaps** — Topics competitors cover that you don't (from data/competitors/)
3. **Repurposing** — Good old content repackaged (from data/posts/archive/)
4. **Pattern-Driven** — Ideas that deliberately use proven patterns (from data/patterns/)
5. **News/WebSearch** — Current events in your niche
6. **Experiment-Driven** — Posts for running experiments
7. **Audience Requests** — Questions/requests from comments on your posts (from `## Top Comments` sections in `data/posts/*.md`)
8. **User Input** — Your topic broken into different angles

## Workflow

1. **Start `content-writer` agent** with count and optional pillar
2. **Present ideas:**

```
Content Ideas (5):

1. "Most AI projects don't fail because of the technology..."
   Pillar: AI Praxis | Hook: Surprising Fact | Format: Text
   Source: Feed Trend ("AI Agents" trending this week)
   Why: Trending topic + your strongest pillar

2. "How I built a CLI in one weekend..."
   Pillar: Side Projects | Hook: Personal Story | Format: Carousel
   Source: Repurpose (Original: URN:123, 89 Reactions but only 1.2k Impressions)
   Why: Good content deserves more reach, Carousel = 3x Impressions (Pattern)

3. "Does a 10-person team really need an AI tool?"
   Pillar: AI Praxis | Hook: Question | Format: Text
   Source: Experiment (hook-type-v1: Question variant, needs 2 more posts)
   Why: Experiment running, question hooks need more data points

4. "What Apostroph learned about AI translation..."
   Pillar: Behind the Scenes | Hook: Behind-Scenes | Format: Document
   Source: Competitor Gap (@competitor-1 posts about it, you don't)
   Why: Close content gap, Behind the Scenes is underrepresented

5. "OpenAI just launched... here's what it means for SMBs"
   Pillar: Industry News | Hook: News-Commentary | Format: Text
   Source: News (WebSearch: current AI announcements)
   Why: Timely content = high reach
```

3. **User chooses:**
   - Good → Save as idea-{slug}.md in drafts/ with status "Approved"
   - Not good → Status "Rejected"
   - Modify → Adjust idea

## Rules

- **Variety** — min. 2 pillars, 2 hook types, 2 formats
- **No duplicates** — check against existing posts and ideas in drafts/
- **Data-based** — every idea has a reasoning
- **Respect pillar weights** (from config)
- **Experiment-aware** — if an experiment is running, at least 1 matching idea
