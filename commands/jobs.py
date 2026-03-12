"""Job commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def show(
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Show job details."""
    from auth import get_client
    api = get_client()
    job = api.get_job(job_id=job_id)

    table = Table(title=f"Job: {job_id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Title", job.get("title", ""))
    table.add_row("Company", str(job.get("companyDetails", {}).get("company", "")))
    table.add_row("Location", job.get("formattedLocation", ""))
    table.add_row("Description", (job.get("description", {}).get("text", "") or "")[:500])
    table.add_row("Listed At", str(job.get("listedAt", "")))

    console.print(table)


@app.command()
def skills(
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Show required skills for a job."""
    from auth import get_client
    api = get_client()
    result = api.get_job_skills(job_id=job_id)
    console.print_json(data=result)
