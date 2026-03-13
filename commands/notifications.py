"""Notification commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("list")
def list_notifications(
    limit: int = typer.Option(25, "--limit", "-n", help="Max notifications"),
    unread: bool = typer.Option(False, "--unread", "-u", help="Show only unread"),
):
    """Show recent notifications."""
    from auth import get_client
    api = get_client()
    result = api.get_notifications(limit=limit, unread_only=unread)

    if not result:
        console.print("[dim]No notifications found.[/dim]")
        return

    table = Table(title=f"Notifications ({len(result)})")
    table.add_column("", width=2)
    table.add_column("Date", style="dim", width=16)
    table.add_column("Notification")

    for n in result:
        marker = "" if n["read"] else "[bold red]*[/bold red]"
        table.add_row(marker, n["date"], n["headline"][:120])

    console.print(table)
