"""Profile commands."""

import json

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """Show a LinkedIn profile."""
    from auth import get_client
    api = get_client()
    profile = api.get_profile(public_id=username)

    table = Table(title=f"Profile: {username}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", f"{profile.get('firstName', '')} {profile.get('lastName', '')}")
    table.add_row("Headline", profile.get("headline", ""))
    table.add_row("Location", profile.get("locationName", ""))
    table.add_row("Industry", profile.get("industryName", ""))
    table.add_row("Summary", (profile.get("summary", "") or "")[:200])
    table.add_row("Followers", str(profile.get("followerCount", "")))
    table.add_row("Connections", str(profile.get("connectionCount", "")))

    console.print(table)


@app.command()
def contact(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """Show contact info for a profile."""
    from auth import get_client
    api = get_client()
    info = api.get_profile_contact_info(public_id=username)

    table = Table(title=f"Contact: {username}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Email", str(info.get("email_address", "")))
    table.add_row("Phone", str(info.get("phone_numbers", [])))
    table.add_row("Twitter", str(info.get("twitter", [])))
    table.add_row("Websites", str(info.get("websites", [])))

    console.print(table)


@app.command()
def skills(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """List skills of a profile."""
    from auth import get_client
    api = get_client()
    result = api.get_profile_skills(public_id=username)

    table = Table(title=f"Skills: {username}")
    table.add_column("#", style="dim")
    table.add_column("Skill", style="green")

    for i, skill in enumerate(result, 1):
        table.add_row(str(i), skill.get("name", ""))

    console.print(table)


@app.command()
def experiences(
    username: str = typer.Argument(..., help="LinkedIn public profile ID or URN ID"),
):
    """List experiences of a profile."""
    from auth import get_client
    api = get_client()
    result = api.get_profile_experiences(urn_id=username)

    if not result:
        console.print("[dim]No experiences found.[/dim]")
        return

    for exp in result:
        company = exp.get("companyName", "")
        title = exp.get("title", "")
        period = exp.get("timePeriod", "")
        location = exp.get("location", "")
        console.print(f"[bold]{title}[/bold] at [cyan]{company}[/cyan]")
        if period:
            console.print(f"  {period}")
        if location:
            console.print(f"  [dim]{location}[/dim]")
        console.print()


@app.command()
def connections(
    urn_id: str = typer.Argument(..., help="LinkedIn URN ID"),
):
    """List connections of a profile."""
    from auth import get_client
    api = get_client()
    result = api.get_profile_connections(urn_id=urn_id)

    table = Table(title="Connections")
    table.add_column("Name", style="green")
    table.add_column("Headline")
    table.add_column("Public ID", style="dim")

    for conn in result[:50]:
        table.add_row(
            f"{conn.get('firstName', '')} {conn.get('lastName', '')}",
            (conn.get("headline", "") or "")[:60],
            conn.get("public_id", ""),
        )

    console.print(table)
    console.print(f"[dim]Showing {min(50, len(result))} of {len(result)} connections[/dim]")


@app.command()
def posts(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
    count: int = typer.Option(10, "--count", "-n", help="Number of posts"),
):
    """List posts from a profile."""
    from auth import get_client
    api = get_client()
    result = api.get_profile_posts(public_id=username, post_count=count)

    if not result:
        console.print("[dim]No posts found.[/dim]")
        return

    for i, post in enumerate(result, 1):
        text = post.get("text", "")
        console.print(f"[bold cyan]Post {i}[/bold cyan]")
        console.print(text[:300] if text else "[dim]No text[/dim]")
        console.print(
            f"[dim]Reactions: {post.get('reactions', '0')} | "
            f"Comments: {post.get('comments', '0')}[/dim]"
        )
        if post.get("urn"):
            console.print(f"[dim]URN: {post['urn']}[/dim]")
        console.print("---")


@app.command()
def views():
    """Show who viewed your profile."""
    from auth import get_client
    api = get_client()
    result = api.get_current_profile_views()

    table = Table(title="Profile Views")
    table.add_column("Name", style="green")
    table.add_column("Headline")
    table.add_column("Viewed At", style="dim")

    for card in result:
        value = card.get("value", {})
        inner = value.get("com.linkedin.voyager.identity.me.wvmpOverview.WvmpViewersCard", {})
        for insight in inner.get("insightCards", []):
            summary = insight.get("value", {}).get("com.linkedin.voyager.identity.me.wvmpOverview.WvmpSummaryInsightCard", {})
            for c in summary.get("cards", []):
                viewer_data = c.get("value", {}).get("com.linkedin.voyager.identity.me.WvmpProfileViewCard", {})
                viewer = viewer_data.get("viewer", {})
                full = viewer.get("com.linkedin.voyager.identity.me.FullProfileViewer", {})
                mini = full.get("profile", {}).get("miniProfile", {})
                if not mini:
                    continue
                name = f"{mini.get('firstName', '')} {mini.get('lastName', '')}"
                headline = mini.get("occupation", "")
                viewed_at = viewer_data.get("viewedAt", "")
                if viewed_at:
                    from datetime import datetime
                    try:
                        viewed_at = datetime.fromtimestamp(viewed_at / 1000).strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        pass
                table.add_row(name, headline[:60], str(viewed_at))

    console.print(table)


@app.command()
def network(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """Show network info for a profile."""
    from auth import get_client
    api = get_client()
    profile = api.get_profile(public_id=username)

    table = Table(title=f"Network: {username}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Followers", str(profile.get("followerCount", "")))
    table.add_row("Connections", str(profile.get("connectionCount", "")))

    console.print(table)


@app.command()
def raw(
    username: str = typer.Argument(..., help="LinkedIn public profile ID"),
):
    """Dump raw profile JSON."""
    from auth import get_client
    api = get_client()
    profile = api.get_profile(public_id=username)
    console.print_json(data=profile)
