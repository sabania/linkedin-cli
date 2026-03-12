"""Connection management commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def invitations(
    limit: int = typer.Option(10, "--limit", "-n"),
):
    """Show pending invitations."""
    from auth import get_client
    api = get_client()
    result = api.get_invitations(limit=limit)

    table = Table(title="Pending Invitations")
    table.add_column("From", style="green")
    table.add_column("Message")
    table.add_column("URN", style="dim")

    for inv in result:
        from_member = inv.get("fromMember", {})
        name = f"{from_member.get('firstName', '')} {from_member.get('lastName', '')}"
        table.add_row(
            name,
            inv.get("message", "")[:60],
            inv.get("entityUrn", ""),
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
