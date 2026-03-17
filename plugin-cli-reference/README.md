# LinkedIn CLI Reference Plugin

Teaches Claude Code (or any AI agent) how to use all `linkedin-cli` commands — correct syntax, flags, and `--json` output shapes.

## Install

```bash
# Add marketplace (once)
/plugin marketplace add sabania/linkedin-cli

# Install plugin
/plugin install linkedin-cli-reference
```

## What's included

One skill: `linkedin-cli-reference` — a complete command reference covering:

- Authentication (login, cookie login for headless servers)
- Profile, Posts, Feed, Notifications, Signals
- Search (people, companies, posts, jobs, groups, events)
- Connections, Messaging, Company, Jobs
- Config & Rate Limits
- JSON output shapes for every command
- Best practices for AI agents

## Usage

Any agent or subagent with `skills: [linkedin-cli-reference]` and `tools: [Bash]` can call the CLI.

Example agent definition:
```yaml
---
description: "My custom LinkedIn agent"
tools:
  - Bash
  - Read
  - Write
skills:
  - linkedin-cli-reference
---
```

The agent then knows all commands, flags, and output formats.

## Prerequisite

The `linkedin-cli` binary must be installed and logged in. See [main README](../README.md#cli-installation).

## Full Marketing System

Want more than just the CLI reference? The **LinkedIn Commander** plugin includes 9 AI agents as a marketing team:

```bash
/plugin install linkedin-commander
```

See [plugin/README.md](../plugin/README.md) for details.
