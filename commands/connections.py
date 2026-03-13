"""Connection management commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def invitations(
    limit: int = typer.Option(25, "--limit", "-n"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show pending invitations."""
    from auth import get_client
    api = get_client()
    result = api.get_invitations(limit=limit)

    if json_output:
        from commands import output_json
        output_json(result)
        return

    table = Table(title="Pending Invitations")
    table.add_column("From", style="green")
    table.add_column("Headline", width=40)
    table.add_column("Message")
    table.add_column("Entity URN", style="dim")
    table.add_column("Secret", style="cyan", width=12)

    for inv in result:
        table.add_row(
            inv.get("name", ""),
            (inv.get("headline", "") or "")[:40],
            (inv.get("message", "") or "")[:60],
            inv.get("entity_urn", ""),
            inv.get("shared_secret", "")[:12],
        )

    console.print(table)


@app.command()
def add(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
    message: str = typer.Option("", "--message", "-m", help="Connection request message"),
):
    """Send a connection request."""
    from auth import get_client
    api = get_client()
    api.add_connection(profile_public_id=username, message=message)
    console.print(f"[green]Connection request sent to {username}[/green]")


@app.command()
def remove(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """Remove a connection."""
    from auth import get_client
    api = get_client()
    api.remove_connection(public_profile_id=username)
    console.print(f"[yellow]Removed connection: {username}[/yellow]")


@app.command()
def accept(
    entity_urn: str = typer.Argument(..., help="Invitation entity URN"),
    shared_secret: str = typer.Argument(..., help="Invitation shared secret"),
):
    """Accept a connection invitation."""
    from auth import get_client
    api = get_client()
    api.reply_invitation(
        invitation_entity_urn=entity_urn,
        invitation_shared_secret=shared_secret,
        action="accept",
    )
    console.print("[green]Invitation accepted[/green]")


@app.command()
def decline(
    entity_urn: str = typer.Argument(..., help="Invitation entity URN"),
    shared_secret: str = typer.Argument(..., help="Invitation shared secret"),
):
    """Decline a connection invitation."""
    from auth import get_client
    api = get_client()
    api.reply_invitation(
        invitation_entity_urn=entity_urn,
        invitation_shared_secret=shared_secret,
        action="reject",
    )
    console.print("[yellow]Invitation declined[/yellow]")
