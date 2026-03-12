"""Search commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command()
def people(
    keywords: str = typer.Argument(None, help="Search keywords"),
    company: str = typer.Option(None, "--company", "-c", help="Current company filter"),
    title: str = typer.Option(None, "--title", "-t", help="Job title filter"),
    school: str = typer.Option(None, "--school", "-s", help="School filter"),
    location: str = typer.Option(None, "--location", "-l", help="Region filter"),
    network: str = typer.Option(None, "--network", "-n", help="Network depth: F(irst), S(econd), O(ther)"),
    limit: int = typer.Option(25, "--limit", help="Max results"),
):
    """Search for people on LinkedIn."""
    from auth import get_client
    api = get_client()

    kwargs = {}
    if keywords:
        kwargs["keywords"] = keywords
    if company:
        kwargs["keyword_company"] = company
    if title:
        kwargs["keyword_title"] = title
    if school:
        kwargs["keyword_school"] = school
    if location:
        kwargs["regions"] = [location]
    if network:
        kwargs["network_depths"] = [network]

    results = api.search_people(**kwargs, limit=limit)

    table = Table(title=f"People Search ({len(results)} results)")
    table.add_column("Name", style="green")
    table.add_column("Headline")
    table.add_column("Location", style="dim")
    table.add_column("Public ID", style="cyan")

    for person in results:
        table.add_row(
            person.get("name", ""),
            (person.get("headline", "") or "")[:50],
            person.get("location", ""),
            person.get("public_id", ""),
        )

    console.print(table)


@app.command()
def companies(
    keywords: str = typer.Argument(..., help="Search keywords"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
):
    """Search for companies."""
    from auth import get_client
    api = get_client()
    results = api.search_companies(keywords=[keywords], limit=limit)

    table = Table(title=f"Company Search ({len(results)} results)")
    table.add_column("Name", style="green")
    table.add_column("Industry")
    table.add_column("ID", style="dim")

    for c in results:
        url = c.get("url", "")
        slug = url.rstrip("/").rsplit("/", 1)[-1] if url else ""
        table.add_row(
            c.get("name", ""),
            c.get("headline", ""),
            slug,
        )

    console.print(table)


@app.command()
def jobs(
    keywords: str = typer.Argument(None, help="Search keywords"),
    companies: str = typer.Option(None, "--company", "-c", help="Company ID"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    remote: str = typer.Option(None, "--remote", "-r", help="1=onsite, 2=remote, 3=hybrid"),
    job_type: str = typer.Option(None, "--type", "-t", help="F=full, C=contract, P=part, T=temp, I=intern, V=volunteer"),
    limit: int = typer.Option(25, "--limit", help="Max results"),
):
    """Search for jobs."""
    from auth import get_client
    api = get_client()

    kwargs = {}
    if keywords:
        kwargs["keywords"] = keywords
    if companies:
        kwargs["companies"] = [companies]
    if location:
        kwargs["location_name"] = location
    if remote:
        kwargs["remote"] = [remote]
    if job_type:
        kwargs["job_type"] = [job_type]

    results = api.search_jobs(**kwargs, limit=limit)

    table = Table(title=f"Job Search ({len(results)} results)")
    table.add_column("Title", style="green")
    table.add_column("Company")
    table.add_column("Location", style="dim")
    table.add_column("Job ID", style="cyan")

    for job in results:
        table.add_row(
            job.get("name", ""),
            job.get("headline", ""),
            job.get("location", ""),
            job.get("urn_id", "").split(":")[-1] if job.get("urn_id") else "",
        )

    console.print(table)
