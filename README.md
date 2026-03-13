# LinkedIn CLI

Command-line tool for managing your LinkedIn account. Read your feed, view profiles, analyze post engagement, manage connections, search people/companies/jobs, and send messages — all from the terminal.

Uses Selenium with a real Chrome browser under the hood, so LinkedIn's bot detection doesn't trigger.

---

## LinkedIn Commander Plugin

Dieses Repo enthält auch das **LinkedIn Commander Plugin** — ein selbstlernendes Marketing-System mit 9 AI Agents als Marketing-Team. Es läuft auf Claude Code und nutzt die LinkedIn CLI als Datenquelle.

**Was es kann:** Content-Strategie, Post-Analyse, Lead-Generierung, Competitor-Tracking, Signal-Erkennung — alles delta-basiert mit Human-in-the-Loop. Du entscheidest, der Agent unterstützt.

> Komplette Plugin-Dokumentation: **[plugin/README.md](plugin/README.md)**

### Schnellstart (3 Schritte)

**1. LinkedIn CLI installieren + einloggen**
```bash
# Windows
irm https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.ps1 | iex

# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh | bash

# Einloggen (einmalig)
linkedin-cli login
```

**2. Plugin in Claude Code aktivieren**
```bash
# In Claude Code:
claude --plugin-dir ./plugin

# Oder über Marketplace:
/plugin marketplace add sabania/linkedin-cli
/plugin install linkedin-commander
```

**3. Setup starten**
```
/setup
```
Das wars. Der Setup-Wizard führt dich durch alles:
- Deine Ziele und Zielgruppe definieren
- Bestehende Posts automatisch analysieren (Baseline + erste Patterns)
- Top-Engager als Contacts erfassen
- Competitors analysieren
- Strategie v1.0 erstellen

Das System startet **warmgelaufen** — nicht leer.

### Danach: Täglicher Workflow

```
/auto                    # Morning Check — was ist seit gestern passiert?
```

Du bekommst:
- Wer hat mit deinen Posts interagiert (Namen, nicht nur Zahlen)
- Wie performen deine aktiven Posts
- Neue Signals (Job-Wechsel, Hot Contacts, Keyword-Mentions)
- Feed-Trends und Comment-Opportunities
- Fällige Follow-ups
- Was du heute tun solltest

### Content erstellen

```
/ideas 5                 # 5 Content-Ideen basierend auf Patterns + Trends
/draft <thema>           # Post schreiben (Brand Voice + bewährte Patterns)
/draft comment <urn>     # Strategischen Kommentar auf fremden Post schreiben
```

### Performance tracken

```
/analyze <urn>           # Einzelnen Post analysieren
/report                  # Wochen-Report mit KPIs und Trends
/evolve                  # Strategie basierend auf Learnings weiterentwickeln
```

### Contacts & Competitors

```
/contacts hot            # Deine wertvollsten Kontakte
/contacts follow-up      # Fällige Follow-ups
/outreach <name>         # Personalisierte Nachricht generieren
/competitor <name>       # Wettbewerber analysieren
/check                   # Quick Status (kein API-Call, sofort)
```

### Dashboard

Öffne `plugin/dashboard.html` im Browser — interaktives Dashboard das dein Excel live liest. Posts, Contacts, Signals, Patterns, Competitors — alles auf einen Blick.

### Wie es lernt

```
Du postest → System misst → Patterns erkennen → Strategie anpassen → bessere Posts
```

Mit jedem Post wird das System schlauer. Der `strategy-evolver` Agent (das "Gehirn") analysiert wöchentlich was funktioniert und schlägt Strategie-Updates vor — du bestätigst oder lehnst ab.

### Wichtig

- **Der Agent postet NIE für dich** — er schreibt Drafts, du postest manuell
- **Kein Spam** — Outreach-Nachrichten nur mit deiner Bestätigung
- **Deine Daten bleiben lokal** — alles in einem Excel-File auf deinem Rechner

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

Installiert nach `~/.local/share/linkedin-cli` (Unix) bzw. `%LOCALAPPDATA%\linkedin-cli` (Windows) und fügt es automatisch zum PATH hinzu. Danach Terminal neu starten.

### Manual Install

Download ZIP von [Releases](../../releases), entpacken und Verzeichnis manuell zum PATH hinzufügen:

| OS | Datei |
|----|-------|
| Windows | `linkedin-cli-windows.zip` |
| macOS | `linkedin-cli-macos.tar.gz` |
| Linux | `linkedin-cli-linux.tar.gz` |

### From Source (Entwickler)

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
# 1. Login — öffnet Chrome, du loggst dich ein, CLI speichert Session automatisch
linkedin-cli login

# 2. Prüfen ob es geklappt hat
linkedin-cli whoami

# 3. Loslegen
linkedin-cli feed list -n 5
linkedin-cli profile posts <dein-public-id> -n 3
linkedin-cli search people "software engineer" --limit 5
```

Login muss nur einmal gemacht werden. Session-Cookies werden unter `~/.linkedin-cli/cookies.json` gespeichert.

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
├── plugin/                 # LinkedIn Commander Plugin (Claude Code)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── agents/             # 9 AI Agents
│   ├── skills/             # 12 Skills/Commands
│   ├── dashboard.html      # Interaktives Dashboard
│   ├── README.md           # Plugin-Dokumentation
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
