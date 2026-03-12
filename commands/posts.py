"""Post interaction commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def comments(
    post_urn: str = typer.Argument(..., help="Post URN or activity ID (e.g. 7435982583777169408)"),
    count: int = typer.Option(20, "--count", "-n", help="Number of comments"),
):
    """Show comments on a post with author profiles."""
    from auth import get_client
    api = get_client()
    # Allow passing just the activity ID
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    result = api.get_post_comments(post_urn=post_urn, comment_count=count)

    if not result:
        console.print("[dim]No comments found.[/dim]")
        return

    table = Table(title=f"Comments ({len(result)})")
    table.add_column("#", style="dim", width=3)
    table.add_column("Author", style="green", width=25)
    table.add_column("Comment", width=60)
    table.add_column("Profile ID", style="cyan", width=25)

    for i, c in enumerate(result, 1):
        table.add_row(
            str(i),
            c.get("author", ""),
            c.get("text", "")[:100],
            c.get("profileId", ""),
        )

    console.print(table)


@app.command()
def reactions(
    post_urn: str = typer.Argument(..., help="Post URN or activity ID"),
    limit: int = typer.Option(50, "--limit", "-n"),
):
    """Show who reacted to a post with their profiles."""
    from auth import get_client
    api = get_client()
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    result = api.get_post_reactions(post_urn=post_urn, max_results=limit)

    if not result:
        console.print("[dim]No reactions found.[/dim]")
        return

    table = Table(title=f"Reactions ({len(result)})")
    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="green", width=25)
    table.add_column("Headline", width=50)
    table.add_column("Profile ID", style="cyan", width=25)

    for i, r in enumerate(result, 1):
        table.add_row(
            str(i),
            r.get("name", ""),
            r.get("headline", ""),
            r.get("profileId", ""),
        )

    console.print(table)
