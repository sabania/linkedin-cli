"""Signal aggregation commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def daily(
    limit: int = typer.Option(5, "--limit", "-n", help="Max items per section"),
    posts: int = typer.Option(3, "--posts", "-p", help="Number of recent posts to check for engagers"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Daily signal aggregation: views, engagers, invitations, notifications."""
    from auth import get_client
    api = get_client()

    # Get own public_id
    me = api.get_user_profile()
    pub_id = me.get("miniProfile", {}).get("publicIdentifier", "")

    # Get recent post URNs
    my_posts = api.get_profile_posts(public_id=pub_id, limit=posts) if pub_id else []
    post_urns = [p["urn"] for p in my_posts if p.get("urn")]

    # Aggregate signals
    signals = api.get_signals(recent_post_urns=post_urns, limit=limit)

    if json_output:
        from commands import output_json
        output_json(signals)
        return

    # Profile Views
    views = signals.get("profile_views", [])
    console.print(f"\n[bold cyan]Profile Views[/bold cyan] ({len(views)})")
    if views:
        for v in views[:limit]:
            if isinstance(v, dict):
                name = v.get("name", "Unknown")
                console.print(f"  - {name}")
    else:
        console.print("  [dim]No recent views[/dim]")

    # Post Engagers
    engagers = signals.get("post_engagers", [])
    console.print(f"\n[bold cyan]Post Engagers[/bold cyan] ({len(engagers)})")
    if engagers:
        table = Table()
        table.add_column("Name", style="green")
        table.add_column("Interaction", style="yellow")
        table.add_column("Post URN", style="dim")
        table.add_column("Profile ID", style="cyan")
        for e in engagers[:limit * 3]:
            table.add_row(
                e.get("name", ""),
                e.get("interaction_type", ""),
                e.get("post_urn", "").split(":")[-1],
                e.get("profileId", ""),
            )
        console.print(table)
    else:
        console.print("  [dim]No engagers on recent posts[/dim]")

    # Invitations
    invitations = signals.get("invitations", [])
    console.print(f"\n[bold cyan]Pending Invitations[/bold cyan] ({len(invitations)})")
    if invitations:
        for inv in invitations[:limit]:
            name = inv.get("name", "Unknown")
            headline = inv.get("headline", "")
            console.print(f"  - [green]{name}[/green]  {headline[:50]}")
    else:
        console.print("  [dim]No pending invitations[/dim]")

    # Notifications
    notifs = signals.get("notifications", [])
    console.print(f"\n[bold cyan]Unread Notifications[/bold cyan] ({len(notifs)})")
    if notifs:
        for n in notifs[:limit]:
            marker = "[bold red]*[/bold red] " if not n.get("read", True) else "  "
            console.print(f"  {marker}{n.get('headline', '')[:100]}")
    else:
        console.print("  [dim]No unread notifications[/dim]")

    console.print()
