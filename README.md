# LinkedIn CLI

Command-line tool for managing your LinkedIn account. Read your feed, view profiles, analyze post engagement, manage connections, search people/companies/jobs, and send messages — all from the terminal.

Uses Selenium with a real Chrome browser under the hood, so LinkedIn's bot detection doesn't trigger.

## Prerequisites

- **Google Chrome** installed (required for all methods — Selenium controls it directly)
- ChromeDriver is auto-downloaded by Selenium, no manual install needed

## Installation

### Binary (kein Python nötig)

Download ZIP für dein OS von [Releases](../../releases):

| OS | Datei |
|----|-------|
| Windows | `linkedin-cli-windows.zip` |
| macOS | `linkedin-cli-macos.zip` |
| Linux | `linkedin-cli-linux.zip` |

ZIP entpacken und aus dem Ordner ausführen — keine Installation, keine Dependencies, nur Chrome:

```bash
# Windows
linkedin-cli.exe login
linkedin-cli.exe feed list -n 5

# macOS / Linux
chmod +x linkedin-cli
./linkedin-cli login
./linkedin-cli feed list -n 5
```

### Python (pip)

Erfordert Python 3.12+:

```bash
pip install linkedin-cli
linkedin-cli login
```

### From Source (Entwickler)

```bash
git clone <repo-url>
cd linkedin-cli
pip install -r requirements.txt
python main.py login
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

## Commands

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
linkedin-cli posts comments <activity-id> -n 20    # Comments (author, text, profile ID)
linkedin-cli posts reactions <activity-id> -n 50    # Reactions (name, headline, profile ID)
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
linkedin-cli search jobs "python" --limit 10            # Search jobs
```

### Messages

```bash
linkedin-cli messages list                              # List conversations
linkedin-cli messages read <conversation-urn>           # Read conversation
linkedin-cli messages send "text" --to <user>           # Send message
linkedin-cli messages seen <conversation-urn>           # Mark as read
```

### Jobs

```bash
linkedin-cli jobs show <job-id>             # Job details
linkedin-cli jobs skills <job-id>           # Required skills
```

### Company

```bash
linkedin-cli company show <id>              # Company details
linkedin-cli company updates <id> -n 10     # Company posts
linkedin-cli company follow <urn>           # Follow
linkedin-cli company unfollow <urn>         # Unfollow
```

## Example Workflow

```bash
# See your latest posts
linkedin-cli profile posts arben-sabani-339074128 -n 3

# Check who reacted to a post (returns usable profile IDs)
linkedin-cli posts reactions 7435982583777169408 -n 10
# → mirko-eberlein, deyaa1, jakobreiter, ...

# View a reactor's full profile
linkedin-cli profile show mirko-eberlein

# Send them a connection request
linkedin-cli connections add mirko-eberlein -m "Great to connect!"
```

All profile IDs returned by `posts reactions` and `posts comments` are directly usable in `profile show`, `profile posts`, `connections add`, and any other command that takes a user ID.

## Build Binary

```bash
pip install pyinstaller
pyinstaller --name linkedin-cli main.py
```

Output: `dist/linkedin-cli/` directory with the executable and dependencies.

The binary is self-contained. End users only need **Google Chrome** — nothing else.

### Cross-Platform Builds (GitHub Actions)

Binaries for all platforms can be built via CI/CD. Each OS runner builds its own binary:

```yaml
# .github/workflows/build.yml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
```

## Tests

```bash
# Login first
linkedin-cli login

# Run all tests (62 tests)
pytest tests/ -v
```

Tests are fully dynamic — they use whatever account is currently logged in. No hardcoded IDs.

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
├── tests/
│   ├── conftest.py         # Dynamic test fixtures
│   ├── test_api.py         # API integration tests
│   └── test_cli.py         # CLI integration tests
├── requirements.txt
└── pytest.ini
```

All API calls run as `fetch()` inside a real Chrome browser, bypassing LinkedIn's bot detection. DOM scraping is used where Voyager API endpoints are deprecated. All selectors are language-independent (CSS classes + data attributes, no locale strings).

## Data Storage

| Path | Purpose |
|------|---------|
| `~/.linkedin-cli/cookies.json` | Session cookies (created by `login`) |
| `~/.linkedin-cli/chrome_profile/` | Chrome profile for visible login sessions |

## License

MIT
