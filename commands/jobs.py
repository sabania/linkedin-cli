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

    company_details = job.get("companyDetails", {})
    if isinstance(company_details, dict):
        inner = company_details.get("com.linkedin.voyager.jobs.JobPostingCompany", company_details)
        company_name = inner.get("companyResolutionResult", {}).get("name", "")
        if not company_name:
            company_name = inner.get("company", "")
    else:
        company_name = str(company_details)

    listed_at = job.get("listedAt", "") or job.get("createdAt", "")
    if listed_at and isinstance(listed_at, (int, float)):
        from datetime import datetime
        try:
            listed_at = datetime.fromtimestamp(listed_at / 1000).strftime("%Y-%m-%d %H:%M")
        except Exception:
            listed_at = str(listed_at)

    table.add_row("Title", job.get("title", ""))
    table.add_row("Company", str(company_name))
    table.add_row("Location", job.get("formattedLocation", ""))
    table.add_row("Description", (job.get("description", {}).get("text", "") or "")[:500])
    table.add_row("Listed At", str(listed_at))

    console.print(table)


@app.command()
def skills(
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Show required skills for a job."""
    from auth import get_client
    api = get_client()
    result = api.get_job_skills(job_id=job_id)

    if not result:
        console.print("[dim]No skills found for this job.[/dim]")
        return

    table = Table(title=f"Skills: {job_id}")
    table.add_column("#", style="dim", width=3)
    table.add_column("Skill", style="green")

    for i, skill in enumerate(result, 1):
        name = skill.get("name", "") if isinstance(skill, dict) else str(skill)
        table.add_row(str(i), name)

    console.print(table)
