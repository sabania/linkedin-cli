"""Company commands."""

import typer
from rich.console import Console
from rich.table import Table

from auth import get_client

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    public_id: str = typer.Argument(..., help="Company public ID (URL slug)"),
):
    """Show company details."""
    api = get_client()
    company = api.get_company(public_id=public_id)

    table = Table(title=f"Company: {public_id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Name", company.get("name", ""))
    table.add_row("Industry", str(company.get("companyIndustries", [])))
    table.add_row("Size", str(company.get("staffCount", "")))
    table.add_row("HQ", str(company.get("headquarter", "")))
    table.add_row("Description", (company.get("description", "") or "")[:300])
    table.add_row("Website", company.get("callToAction", {}).get("url", ""))

    console.print(table)


@app.command()
def updates(
    public_id: str = typer.Argument(..., help="Company public ID"),
    limit: int = typer.Option(10, "--limit", "-n"),
):
    """Show recent company updates/posts."""
    api = get_client()
    result = api.get_company_updates(public_id=public_id, max_results=limit)

    for i, update in enumerate(result, 1):
        console.print(f"[bold cyan]Update {i}[/bold cyan]")
        console.print_json(data=update)
        console.print("---")


@app.command()
def follow(
    urn: str = typer.Argument(..., help="Company following state URN"),
):
    """Follow a company."""
    api = get_client()
    api.follow_company(following_state_urn=urn, following=True)
    console.print("[green]Now following[/green]")


@app.command()
def unfollow(
    urn: str = typer.Argument(..., help="Entity URN to unfollow"),
):
    """Unfollow an entity."""
    api = get_client()
    api.unfollow_entity(urn_id=urn)
    console.print("[yellow]Unfollowed[/yellow]")
