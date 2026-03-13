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
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show recent notifications."""
    from auth import get_client
    api = get_client()
    result = api.get_notifications(limit=limit, unread_only=unread)

    if json_output:
        from commands import output_json
        output_json(result)
        return

    if not result:
        console.print("[dim]No notifications found.[/dim]")
        return

    table = Table(title=f"Notifications ({len(result)})")
    table.add_column("", width=2)
    table.add_column("Date", style="dim", width=16)
    table.add_column("Actor", style="green", width=20)
    table.add_column("Notification")

    for n in result:
        marker = "" if n["read"] else "[bold red]*[/bold red]"
        actor = n.get("actor_name", "")
        table.add_row(marker, n["date"], actor, n["headline"][:120])

    console.print(table)
