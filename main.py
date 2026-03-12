"""LinkedIn CLI - Command line interface for LinkedIn management."""

import os
import sys

# Fix Unicode output on Windows (PyInstaller binary + cmd.exe)
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import typer

from commands.profile import app as profile_app
from commands.feed import app as feed_app
from commands.posts import app as posts_app
from commands.connections import app as connections_app
from commands.search import app as search_app
from commands.messaging import app as messaging_app
from commands.jobs import app as jobs_app
from commands.company import app as company_app

app = typer.Typer(
    name="linkedin-cli",
    help="LinkedIn Management CLI - Profile, Feed, Posts, Connections & more.",
    no_args_is_help=True,
)

app.add_typer(profile_app, name="profile", help="Profile operations")
app.add_typer(feed_app, name="feed", help="Feed & timeline")
app.add_typer(posts_app, name="posts", help="Post interactions")
app.add_typer(connections_app, name="connections", help="Connection management")
app.add_typer(search_app, name="search", help="Search people, companies, jobs")
app.add_typer(messaging_app, name="messages", help="Messaging")
app.add_typer(jobs_app, name="jobs", help="Job search & details")
app.add_typer(company_app, name="company", help="Company info & updates")


@app.command()
def login(
    cookie: str = typer.Option("", "--cookie", "-c", help="Paste li_at cookie manually instead of browser login"),
):
    """Login to LinkedIn. Opens Chrome for you to log in.

    The browser will open linkedin.com/login. After you log in,
    the CLI captures the session cookie automatically. 2FA works fine.

    Alternatively, pass --cookie to skip the browser.
    """
    from auth import browser_login

    if cookie:
        typer.echo("Manual cookie mode not supported. Use browser login.")
        raise typer.Exit(1)

    browser_login()
    typer.echo("Login successful!")


@app.command()
def whoami():
    """Show current logged-in profile."""
    from auth import get_client
    from rich.console import Console
    from rich.table import Table

    console = Console()
    api = get_client()
    profile = api.get_user_profile()
    mini = profile.get("miniProfile", {})

    table = Table(title="Current Profile")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", f"{mini.get('firstName', '')} {mini.get('lastName', '')}")
    table.add_row("Occupation", mini.get("occupation", ""))
    table.add_row("Public ID", mini.get("publicIdentifier", ""))
    table.add_row("URN", mini.get("entityUrn", ""))
    table.add_row("Premium", str(profile.get("premiumSubscriber", False)))

    console.print(table)


if __name__ == "__main__":
    app()
