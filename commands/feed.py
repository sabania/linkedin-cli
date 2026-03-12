"""Feed commands."""

import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def list(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of posts"),
    offset: int = typer.Option(0, "--offset", help="Offset"),
    no_promoted: bool = typer.Option(True, "--no-promoted/--with-promoted", help="Exclude promoted posts"),
):
    """Show your LinkedIn feed."""
    from auth import get_client
    api = get_client()
    posts = api.get_feed_posts(limit=limit, offset=offset, exclude_promoted_posts=no_promoted)

    if not posts:
        console.print("[dim]No posts found.[/dim]")
        return

    for i, post in enumerate(posts, 1):
        author = post.get("author", "Unknown")
        text = post.get("text", "")

        console.print(f"[bold cyan]#{i}[/bold cyan] [bold]{author}[/bold]")
        console.print(text[:300] if text else "[dim]No text[/dim]")
        console.print(
            f"[dim]Reactions: {post.get('reactions', 0)} | "
            f"Comments: {post.get('comments', 0)}[/dim]"
        )
        if post.get("urn"):
            console.print(f"[dim]URN: {post['urn']}[/dim]")
        console.print("---")
