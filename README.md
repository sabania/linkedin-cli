# LinkedIn CLI

Command-line tool for managing your LinkedIn account. Read your feed, view profiles, analyze post engagement, manage connections, search people/companies/jobs, and send messages — all from the terminal.

Uses Nodriver (CDP-based browser automation) under the hood — no WebDriver binary, no `navigator.webdriver` flag, undetectable by LinkedIn's PerimeterX/HUMAN anti-bot system.

---

## What's in this Repo

This repo contains **3 things** — install what you need:

| What | For whom | Install |
|------|----------|---------|
| **LinkedIn CLI** | Everyone | Binary or `pip install` |
| **CLI Reference Plugin** | AI/Claude Code users who want CLI knowledge for their agents | `/plugin install linkedin-cli-reference` |
| **LinkedIn Commander Plugin** | Marketers who want a full AI marketing team | `/plugin install linkedin-commander` |

### 1. LinkedIn CLI (the tool itself)

Terminal tool to interact with LinkedIn. Works standalone, no AI needed.

```bash
linkedin-cli profile show williamhgates
linkedin-cli posts analytics 7438407227096539136
linkedin-cli search people "software engineer" --limit 5
```

### 2. CLI Reference Plugin (for AI agents)

A single skill that teaches Claude Code (or any agent) how to use all CLI commands — correct syntax, flags, `--json` output shapes.

```bash
# In Claude Code:
/plugin marketplace add sabania/linkedin-cli
/plugin install linkedin-cli-reference
```

After installing, any agent or subagent can load the `linkedin-cli-reference` skill and knows how to call the CLI via Bash.

### 3. LinkedIn Commander Plugin (full marketing system)

Self-learning marketing system with **9 AI agents** as a marketing team. Content strategy, post analysis, lead generation, competitor tracking, signal detection — all delta-based with human-in-the-loop.

```bash
# In Claude Code:
/plugin marketplace add sabania/linkedin-cli
/plugin install linkedin-commander
/setup
```

> Full documentation: **[plugin/README.md](plugin/README.md)**

---

## CLI Installation

### Prerequisites

- **Google Chrome** installed (Nodriver communicates with it via CDP — no separate ChromeDriver needed)

### Quick Install

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex
```

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash
```

Installs to `~/.local/share/linkedin-cli` (Unix) or `%LOCALAPPDATA%\linkedin-cli` (Windows) and automatically adds it to PATH. Restart terminal afterwards.

### Manual Install

Download ZIP from [Releases](../../releases), extract and manually add directory to PATH:

| OS | File |
|----|------|
| Windows | `linkedin-cli-windows.zip` |
| macOS | `linkedin-cli-macos.tar.gz` |
| Linux | `linkedin-cli-linux.tar.gz` |

### From Source (Developers)

```bash
git clone https://github.com/sabania/linkedin-cli.git
cd linkedin-cli
pip install -r requirements.txt
python main.py login
```

### Uninstall

```powershell
# Windows
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1))) -Uninstall
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash -s -- --uninstall
```

---

## Login

```bash
# Opens Chrome — you log in, CLI captures cookies automatically. 2FA works.
linkedin-cli login

# On headless servers (no display): paste li_at cookie instead
# Get it from: Browser → linkedin.com → DevTools (F12) → Application → Cookies → li_at
linkedin-cli login --cookie "AQE..."

# Verify
linkedin-cli whoami
```

Login only needs to be done once. Session cookies are stored at `~/.linkedin-cli/cookies.json`.

---

## CLI Commands

### Settings

```bash
linkedin-cli config show                                # Show all settings + daily usage
linkedin-cli config set rate_limits.daily_limit 120     # Max API calls per day
linkedin-cli config set rate_limits.calls_per_minute 20 # Burst limit per minute
linkedin-cli config set browser.headless false          # Show browser window (debug)
linkedin-cli config reset                               # Reset to defaults
```

### Profile

```bash
linkedin-cli profile show <user>            # View profile
linkedin-cli profile posts <user> -n 5      # Posts with engagement stats
linkedin-cli profile contact <user>         # Contact info
linkedin-cli profile skills <user>          # Skills
linkedin-cli profile experiences <urn>      # Work experience
linkedin-cli profile connections <urn>      # Connections
linkedin-cli profile views                  # Who viewed your profile
linkedin-cli profile network <user>         # Followers, connections count
linkedin-cli profile raw <user>             # Raw JSON dump
```

### Feed

```bash
linkedin-cli feed list -n 10                # Your feed
linkedin-cli feed list --no-promoted        # Without sponsored posts
```

### Posts

```bash
linkedin-cli posts show <activity-id>              # Post details
linkedin-cli posts comments <activity-id> -n 20    # Comments
linkedin-cli posts reactions <activity-id> -n 50   # Reactions
linkedin-cli posts analytics <activity-id>         # Impressions, demographics
linkedin-cli posts engagers <activity-id> -n 50    # All engagers (reactions + comments)
```

### Connections

```bash
linkedin-cli connections invitations -n 10              # Pending invitations
linkedin-cli connections add <user> -m "Hi!"            # Send connection request
linkedin-cli connections remove <user>                  # Remove connection
linkedin-cli connections accept <urn> <secret>          # Accept invitation
linkedin-cli connections decline <urn> <secret>         # Decline invitation
```

### Search

```bash
linkedin-cli search people "keyword" --limit 20        # Search people
linkedin-cli search companies "microsoft"               # Search companies
linkedin-cli search posts "AI" --date past-week         # Search posts
linkedin-cli search jobs "python" --limit 10            # Search jobs
linkedin-cli search groups "data science" --limit 10    # Search groups
linkedin-cli search events "AI conference" --limit 10   # Search events
```

### Messages

```bash
linkedin-cli messages list                              # List conversations
linkedin-cli messages read "John Doe"                   # Read conversation by name
linkedin-cli messages send "text" --to <user>           # Send message
linkedin-cli messages seen <conversation-urn>           # Mark as read
```

### Jobs & Company

```bash
linkedin-cli jobs show <job-id>             # Job details
linkedin-cli jobs skills <job-id>           # Required skills
linkedin-cli company show <id>              # Company details
linkedin-cli company updates <id> -n 10     # Company posts
linkedin-cli company follow <id>            # Follow company
linkedin-cli company unfollow <id>          # Unfollow company
```

### Signals

```bash
linkedin-cli signals daily --json           # All daily signals in one call
```

### Notifications

```bash
linkedin-cli notifications list -n 20       # Recent notifications
linkedin-cli notifications list --unread     # Only unread
```

All commands support `--json` for machine-readable output.

---

## LinkedIn Commander Plugin

> Full documentation: **[plugin/README.md](plugin/README.md)**

### Quick Start

```bash
/plugin marketplace add sabania/linkedin-cli
/plugin install linkedin-commander
/setup
```

The setup wizard guides you through everything — goals, audience, historical analysis, competitors, strategy v1.0. The system starts **warmed up**.

### Daily Workflow

```
/auto                    # Morning Check — what happened since yesterday?
/ideas 5                 # Content ideas based on patterns + trends
/draft <topic>           # Write post (brand voice + proven patterns)
/analyze <urn>           # Analyze post performance
/report                  # Weekly report with KPIs
/evolve                  # Evolve strategy based on learnings
/outreach <name>         # Personalized outreach message
/competitor <name>       # Analyze competitor
/check                   # Quick status (no API call, instant)
```

### How It Learns

```
You post → System measures → Detect patterns → Adapt strategy → Better posts
```

### Important

- **The agent NEVER posts for you** — it writes drafts, you post manually
- **No spam** — outreach messages only with your confirmation
- **Your data stays local** — everything in Markdown files on your machine

---

## Example Workflow

```bash
# See your latest posts
linkedin-cli profile posts arben-sabani -n 3

# Check who reacted to a post
linkedin-cli posts reactions 7435982583777169408 -n 10

# View a reactor's profile
linkedin-cli profile show mirko-eberlein

# Send them a connection request
linkedin-cli connections add mirko-eberlein -m "Great to connect!"
```

All profile IDs returned by `posts reactions` and `posts comments` are directly usable in other commands.

---

## Architecture

```
linkedin-cli/
├── main.py                 # CLI entry point (Typer)
├── auth.py                 # Login + cookie management (Nodriver)
├── nodriver_adapter.py     # Sync adapter: Nodriver async → Selenium-compatible API
├── linkedin_wrapper.py     # Core LinkedIn client (rate-limited, randomized delays)
├── commands/               # Subcommand modules
│   ├── profile.py
│   ├── feed.py
│   ├── posts.py
│   ├── connections.py
│   ├── search.py
│   ├── messaging.py
│   ├── jobs.py
│   ├── company.py
│   └── config.py           # CLI settings (rate limits, browser mode)
├── plugin/                 # LinkedIn Commander Plugin (full marketing system)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/             # 9 AI Agents
│   ├── skills/             # 13 Skills (inkl. CLI Reference)
│   └── dashboard.html      # Interactive dashboard
├── plugin-cli-reference/   # CLI Reference Plugin (standalone, lightweight)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── linkedin-cli-reference/
├── tests/
├── requirements.txt
└── pytest.ini
```

## Data Storage

| Path | Purpose |
|------|---------|
| `~/.linkedin-cli/cookies.json` | Session cookies (created by `login`) |
| `~/.linkedin-cli/cli_config.json` | CLI settings (rate limits, browser mode) |
| `~/.linkedin-cli/daily_calls.json` | Daily API call counter |

## Build Binary

```bash
pip install pyinstaller
pyinstaller --name linkedin-cli main.py
```

Output: `dist/linkedin-cli/` directory with the executable and dependencies. End users only need **Google Chrome**.

## Tests

```bash
linkedin-cli login
pytest tests/ -v
```

Tests are fully dynamic — they use whatever account is currently logged in.

## License

MIT
