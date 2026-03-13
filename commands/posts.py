"""Post interaction commands."""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    post_urn: str = typer.Argument(..., help="Post URN or activity ID"),
):
    """Show a single post with full details."""
    from auth import get_client
    api = get_client()
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    post = api.get_post(post_urn=post_urn)

    if not post:
        console.print("[red]Post not found.[/red]")
        return

    # Header
    console.print(Panel(
        f"[bold]{post['author']}[/bold]  [dim]{post['headline']}[/dim]\n"
        f"[dim]{post['date']}[/dim]"
        f"{'  [cyan]' + post['content_type'] + '[/cyan]' if post['content_type'] else ''}",
        title=post["urn"],
    ))

    # Text
    if post["text"]:
        console.print()
        console.print(post["text"])

    # Metrics
    console.print()
    table = Table(title="Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green", justify="right")
    table.add_row("Impressions", f"{post['impressions']:,}")
    table.add_row("Views", f"{post['views']:,}")
    table.add_row("Reactions", f"{post['reactions']:,}")
    table.add_row("Comments", f"{post['comments']:,}")
    table.add_row("Shares", f"{post['shares']:,}")
    console.print(table)

    console.print(f"\n[dim]{post['url']}[/dim]")


@app.command()
def comments(
    post_urn: str = typer.Argument(..., help="Post URN or activity ID (e.g. 7435982583777169408)"),
    limit: int = typer.Option(50, "--limit", "-n", help="Number of comments"),
):
    """Show comments on a post with author profiles."""
    from auth import get_client
    api = get_client()
    # Allow passing just the activity ID
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    result = api.get_post_comments(post_urn=post_urn, limit=limit)

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
    limit: int = typer.Option(50, "--limit", "-n", help="Number of reactions"),
):
    """Show who reacted to a post with their profiles."""
    from auth import get_client
    api = get_client()
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    result = api.get_post_reactions(post_urn=post_urn, limit=limit)

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


@app.command()
def analytics(
    post_urn: str = typer.Argument(..., help="Post URN or activity ID"),
):
    """Show post analytics (impressions, reach, demographics)."""
    from auth import get_client
    api = get_client()
    if not post_urn.startswith("urn:"):
        post_urn = f"urn:li:activity:{post_urn}"

    result = api.get_post_analytics(post_urn=post_urn)

    if not result or "error" in result:
        console.print(f"[red]{result.get('error', 'No analytics data found.')}[/red]")
        return

    # Performance metrics
    perf = Table(title=f"Post Analytics — {result.get('date', '')}")
    perf.add_column("Metric", style="cyan")
    perf.add_column("Value", style="green", justify="right")

    metrics = [
        "Impressions", "Members reached", "Reactions", "Comments",
        "Reposts", "Saves", "Sends on LinkedIn",
        "Profile viewers from this post", "Followers gained from this post",
    ]
    for m in metrics:
        if m in result:
            perf.add_row(m, result[m])

    console.print(perf)

    # Demographics
    demographics = result.get("demographics", {})
    if demographics:
        console.print()
        demo = Table(title="Top Demographics")
        demo.add_column("Category", style="cyan")
        demo.add_column("Value", style="green")
        demo.add_column("%", justify="right")

        for category, items in demographics.items():
            for i, item in enumerate(items[:5]):
                demo.add_row(
                    category if i == 0 else "",
                    item["value"],
                    item["pct"],
                )
            demo.add_section()

        console.print(demo)
