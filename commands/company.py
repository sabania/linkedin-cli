"""Company commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    public_id: str = typer.Argument(..., help="Company public ID (URL slug)"),
):
    """Show company details."""
    from auth import get_client
    api = get_client()
    company = api.get_company(public_id=public_id)

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
    limit: int = typer.Option(25, "--limit", "-n"),
):
    """Show recent company updates/posts."""
    from auth import get_client
    api = get_client()
    result = api.get_company_updates(public_id=public_id, limit=limit)

    if not result:
        console.print("[dim]No updates found.[/dim]")
        return

    for i, update in enumerate(result, 1):
        text = update.get("text", "").strip()
        urn = update.get("urn", "")
        rx = update.get("reactions", "0")
        cm = update.get("comments", "0")
        console.print(f"[bold cyan]Update {i}[/bold cyan]")
        console.print(text[:300] if text else "[dim]No text[/dim]")
        console.print(f"Reactions: {rx} | Comments: {cm}")
        console.print(f"[dim]{urn}[/dim]")
        console.print("---")


@app.command()
def follow(
    urn: str = typer.Argument(..., help="Company following state URN"),
):
    """Follow a company."""
    from auth import get_client
    api = get_client()
    api.follow_company(following_state_urn=urn, following=True)
    console.print("[green]Now following[/green]")


@app.command()
def unfollow(
    urn: str = typer.Argument(..., help="Entity URN to unfollow"),
):
    """Unfollow an entity."""
    from auth import get_client
    api = get_client()
    api.unfollow_entity(urn_id=urn)
    console.print("[yellow]Unfollowed[/yellow]")
