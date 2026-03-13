"""Company commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    public_id: str = typer.Argument(..., help="Company public ID (URL slug)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show company details."""
    from auth import get_client
    api = get_client()
    company = api.get_company(public_id=public_id)

    if json_output:
        from commands import output_json
        output_json(company)
        return

    table = Table(title=f"Company: {public_id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    industries = company.get("companyIndustries", [])
    industry_str = ", ".join(i.get("localizedName", "") for i in industries if isinstance(i, dict)) if industries else ""
    hq = company.get("headquarter", {})
    if isinstance(hq, dict):
        hq_parts = [hq.get("line1", ""), hq.get("city", ""), hq.get("geographicArea", ""), hq.get("postalCode", ""), hq.get("country", "")]
        hq_str = ", ".join(p for p in hq_parts if p)
    else:
        hq_str = str(hq)

    table.add_row("Name", company.get("name", ""))
    table.add_row("Industry", industry_str)
    table.add_row("Size", str(company.get("staffCount", "")))
    table.add_row("HQ", hq_str)
    table.add_row("Description", (company.get("description", "") or "")[:300])
    table.add_row("Website", company.get("callToAction", {}).get("url", ""))

    console.print(table)


@app.command()
def updates(
    public_id: str = typer.Argument(..., help="Company public ID"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Show recent company updates/posts."""
    from auth import get_client
    api = get_client()
    result = api.get_company_updates(public_id=public_id, limit=limit)

    if json_output:
        from commands import output_json
        output_json(result)
        return

    if not result:
        console.print("[dim]No updates found.[/dim]")
        return

    for i, update in enumerate(result, 1):
        text = update.get("text", "").strip()
        urn = update.get("urn", "")
        rx = update.get("reactions", "0")
        cm = update.get("comments", "0")
        posted_at = update.get("posted_at", "")
        console.print(f"[bold cyan]Update {i}[/bold cyan]  [dim]{posted_at}[/dim]")
        console.print(text[:300] if text else "[dim]No text[/dim]")
        console.print(f"Reactions: {rx} | Comments: {cm}")
        console.print(f"[dim]{urn}[/dim]")
        console.print("---")


@app.command()
def follow(
    public_id: str = typer.Argument(..., help="Company public ID (URL slug)"),
):
    """Follow a company."""
    from auth import get_client
    api = get_client()
    result = api.follow_company(public_id=public_id, following=True)
    action = result.get("action", "") if isinstance(result, dict) else ""
    if action == "followed":
        console.print(f"[green]Now following {public_id}[/green]")
    elif action == "already following":
        console.print(f"[dim]Already following {public_id}[/dim]")
    else:
        console.print(f"[red]Could not follow {public_id}: {action}[/red]")


@app.command()
def unfollow(
    public_id: str = typer.Argument(..., help="Company public ID (URL slug)"),
):
    """Unfollow a company."""
    from auth import get_client
    api = get_client()
    result = api.follow_company(public_id=public_id, following=False)
    action = result.get("action", "") if isinstance(result, dict) else ""
    if action == "unfollowed":
        console.print(f"[yellow]Unfollowed {public_id}[/yellow]")
    elif action == "not following":
        console.print(f"[dim]Not following {public_id}[/dim]")
    else:
        console.print(f"[red]Could not unfollow {public_id}: {action}[/red]")
