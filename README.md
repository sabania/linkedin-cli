# LinkedIn CLI

Command-line tool for managing your LinkedIn account. Read your feed, view profiles, analyze post engagement, manage connections, search people/companies/jobs, and send messages — all from the terminal.

Uses Selenium with a real Chrome browser under the hood, so LinkedIn's bot detection doesn't trigger.

---

## LinkedIn Commander Plugin

This repo also contains the **LinkedIn Commander Plugin** — a self-learning marketing system with 9 AI agents as a marketing team. It runs on Claude Code and uses the LinkedIn CLI as data source.

**What it does:** Content strategy, post analysis, lead generation, competitor tracking, signal detection — all delta-based with human-in-the-loop. You decide, the agent supports.

> Full plugin documentation: **[plugin/README.md](plugin/README.md)**

### Quick Start (3 Steps)

**1. Install LinkedIn CLI + Log in**
```bash
# Windows
irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex

# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash

# Log in (one-time)
linkedin-cli login
```

**2. Activate Plugin in Claude Code**
```bash
# In Claude Code:
claude --plugin-dir ./plugin

# Or via Marketplace:
/plugin marketplace add sabania/linkedin-cli
/plugin install linkedin-commander
```

**3. Start Setup**
```
/setup
```
That's it. The setup wizard guides you through everything:
- Define your goals and target audience
- Automatically analyze existing posts (baseline + initial patterns)
- Analyze competitors
- Create strategy v1.0

The system starts **warmed up** — not empty.

### After That: Daily Workflow

```
/auto                    # Morning Check — what happened since yesterday?
```

You get:
- Who interacted with your posts (names, not just numbers)
- How your active posts are performing
- New signals (outreach candidates, comment replies, keyword mentions)
- Feed trends and comment opportunities
- What you should do today

### Create Content

```
/ideas 5                 # 5 content ideas based on patterns + trends
/draft <topic>           # Write post (brand voice + proven patterns)
/draft comment <urn>     # Write strategic comment on someone else's post
```

### Track Performance

```
/analyze <urn>           # Analyze single post
/report                  # Weekly report with KPIs and trends
/evolve                  # Evolve strategy based on learnings
```

### Outreach & Competitors

```
/outreach <name>         # Generate personalized message
/competitor <name>       # Analyze competitor
/check                   # Quick status (no API call, instant)
```

### Dashboard

Open `plugin/dashboard.html` in your browser — interactive dashboard. Posts, Signals, Patterns, Competitors — all at a glance.

### How It Learns

```
You post → System measures → Detect patterns → Adapt strategy → Better posts
```

With every post, the system gets smarter. The `strategy-evolver` agent (the "brain") weekly analyzes what works and proposes strategy updates — you confirm or reject.

### Important

- **The agent NEVER posts for you** — it writes drafts, you post manually
- **No spam** — outreach messages only with your confirmation
- **Your data stays local** — everything in Markdown files on your machine

---

## CLI Installation

### Prerequisites

- **Google Chrome** installed (required — Selenium controls it directly)
- ChromeDriver is auto-downloaded by Selenium, no manual install needed

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
irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex -Uninstall
```

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash -s -- --uninstall
```

## Quick Start

```bash
# 1. Login — opens Chrome, you log in, CLI saves session automatically
linkedin-cli login

# 2. Verify it worked
linkedin-cli whoami

# 3. Get started
linkedin-cli feed list -n 5
linkedin-cli profile posts <your-public-id> -n 3
linkedin-cli search people "software engineer" --limit 5
```

Login only needs to be done once. Session cookies are stored at `~/.linkedin-cli/cookies.json`.

## CLI Commands

### Authentication

```bash
linkedin-cli login                  # Open Chrome to log in
linkedin-cli whoami                 # Show current profile
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
```

### Messages

```bash
linkedin-cli messages list                              # List conversations
linkedin-cli messages read <conversation-urn>           # Read conversation
linkedin-cli messages send "text" --to <user>           # Send message
linkedin-cli messages seen <conversation-urn>           # Mark as read
```

### Jobs & Company

```bash
linkedin-cli jobs show <job-id>             # Job details
linkedin-cli jobs skills <job-id>           # Required skills
linkedin-cli company show <id>              # Company details
linkedin-cli company updates <id> -n 10     # Company posts
```

### Signals

```bash
linkedin-cli signals daily --json           # All daily signals in one call
```

### Notifications

```bash
linkedin-cli notifications list -n 20       # Recent notifications
```

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

## Architecture

```
linkedin-cli/
├── main.py                 # CLI entry point (Typer)
├── auth.py                 # Login + cookie management (Selenium)
├── linkedin_wrapper.py     # Core LinkedIn client
├── commands/               # Subcommand modules
│   ├── profile.py
│   ├── feed.py
│   ├── posts.py
│   ├── connections.py
│   ├── search.py
│   ├── messaging.py
│   ├── jobs.py
│   └── company.py
├── data/                   # Tracking data (Markdown file-per-record)
├── drafts/                 # Post drafts (.md)
├── plugin/                 # LinkedIn Commander Plugin (Claude Code)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/             # 9 AI Agents
│   ├── skills/             # 12 Skills/Commands
│   ├── dashboard.html      # Interactive dashboard
│   ├── README.md           # Plugin documentation
│   └── LICENSE
├── tests/
├── requirements.txt
└── pytest.ini
```

## Data Storage

| Path | Purpose |
|------|---------|
| `~/.linkedin-cli/cookies.json` | Session cookies (created by `login`) |
| `~/.linkedin-cli/chrome_profile/` | Chrome profile for visible login sessions |

## License

MIT
