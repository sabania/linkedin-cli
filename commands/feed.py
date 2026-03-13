"""Feed commands."""

import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def list(
    limit: int = typer.Option(25, "--limit", "-n", help="Number of posts"),
    no_promoted: bool = typer.Option(True, "--no-promoted/--with-promoted", help="Exclude promoted posts"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show your LinkedIn feed."""
    from auth import get_client
    api = get_client()
    posts = api.get_feed_posts(limit=limit, exclude_promoted_posts=no_promoted)

    if json_output:
        from commands import output_json
        output_json(posts)
        return

    if not posts:
        console.print("[dim]No posts found.[/dim]")
        return

    for i, post in enumerate(posts, 1):
        author = post.get("author", "Unknown")
        author_pid = post.get("author_profile_id", "")
        posted_at = post.get("posted_at", "")
        repost = " [yellow]↻ repost[/yellow]" if post.get("is_repost") else ""
        text = post.get("text", "")

        console.print(f"[bold cyan]#{i}[/bold cyan] [bold]{author}[/bold]  [dim]{author_pid}[/dim]{repost}")
        console.print(f"[dim]{posted_at}[/dim]")
        console.print(text[:300] if text else "[dim]No text[/dim]")
        console.print(
            f"[dim]Reactions: {post.get('reactions', 0)} | "
            f"Comments: {post.get('comments', 0)} | "
            f"Shares: {post.get('shares', 0)}[/dim]"
        )
        if post.get("urn"):
            console.print(f"[dim]URN: {post['urn']}[/dim]")
        console.print("---")
