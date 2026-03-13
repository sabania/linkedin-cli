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
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
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

    if json_output:
        from commands import output_json
        output_json(results)
        return

    table = Table(title=f"People Search ({len(results)} results)")
    table.add_column("Name", style="green")
    table.add_column("Headline")
    table.add_column("Location", style="dim")
    table.add_column("Degree", style="yellow", width=5)
    table.add_column("Public ID", style="cyan")

    for person in results:
        table.add_row(
            person.get("name", ""),
            (person.get("headline", "") or "")[:50],
            person.get("location", ""),
            person.get("connection_degree", ""),
            person.get("public_id", ""),
        )

    console.print(table)


@app.command()
def companies(
    keywords: str = typer.Argument(..., help="Search keywords"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for companies."""
    from auth import get_client
    api = get_client()
    results = api.search_companies(keywords=[keywords], limit=limit)

    if json_output:
        from commands import output_json
        output_json(results)
        return

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
def posts(
    keywords: str = typer.Argument(..., help="Search keywords"),
    sort: str = typer.Option(None, "--sort", "-s", help="relevance (default) or date_posted"),
    date: str = typer.Option(None, "--date", "-d", help="past-24h, past-week, past-month"),
    content: str = typer.Option(None, "--content", help="videos, images, documents, job-postings, liveVideos"),
    from_member: str = typer.Option(None, "--from-member", help="Member URN (ACoAAB...)"),
    from_company: str = typer.Option(None, "--from-company", help="Company URN or ID"),
    posted_by: str = typer.Option(None, "--posted-by", help="me, first (1st connections), or following"),
    mentioning: str = typer.Option(None, "--mentioning", help="Member URN"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results (~3 per page load)"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for posts/content with filters.

    Examples:
      search posts "AI" --date past-week --sort date_posted
      search posts "python" --content videos --limit 15
      search posts "NLP" --from-company apostroph --posted-by first
    """
    from auth import get_client
    api = get_client()
    results = api.search_posts(
        keywords=keywords, limit=limit, sort_by=sort,
        date_posted=date, content_type=content,
        from_member=from_member, from_company=from_company,
        posted_by=posted_by, mentioning=mentioning,
    )

    if json_output:
        from commands import output_json
        output_json(results)
        return

    table = Table(title=f"Post Search ({len(results)} results)")
    table.add_column("#", style="dim", width=3)
    table.add_column("Author", style="green", width=20)
    table.add_column("Text", width=45)
    table.add_column("Posted", style="dim", width=11)
    table.add_column("Rx", style="yellow", justify="right", width=6)
    table.add_column("Cm", style="yellow", justify="right", width=6)
    table.add_column("Activity ID", style="cyan", width=20)

    for i, p in enumerate(results, 1):
        posted = p.get("posted_at", "")[:10]  # date only
        table.add_row(
            str(i),
            p.get("author", ""),
            p.get("text", "")[:80],
            posted,
            p.get("reactions", "0"),
            p.get("comments", "0"),
            p.get("activity_id", ""),
        )

    console.print(table)


@app.command()
def groups(
    keywords: str = typer.Argument(..., help="Search keywords"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for groups."""
    from auth import get_client
    api = get_client()
    results = api.search_groups(keywords=keywords, limit=limit)

    if json_output:
        from commands import output_json
        output_json(results)
        return

    table = Table(title=f"Group Search ({len(results)} results)")
    table.add_column("Name", style="green")
    table.add_column("Description")
    table.add_column("URL", style="dim")

    for g in results:
        table.add_row(
            g.get("name", ""),
            (g.get("headline", "") or "")[:60],
            g.get("url", ""),
        )

    console.print(table)


@app.command()
def events(
    keywords: str = typer.Argument(..., help="Search keywords"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search for events."""
    from auth import get_client
    api = get_client()
    results = api.search_events(keywords=keywords, limit=limit)

    if json_output:
        from commands import output_json
        output_json(results)
        return

    table = Table(title=f"Event Search ({len(results)} results)")
    table.add_column("Name", style="green")
    table.add_column("Details")
    table.add_column("URL", style="dim")

    for e in results:
        table.add_row(
            e.get("name", ""),
            (e.get("headline", "") or "")[:60],
            e.get("url", ""),
        )

    console.print(table)


@app.command()
def jobs(
    keywords: str = typer.Argument(None, help="Search keywords"),
    companies: str = typer.Option(None, "--company", "-c", help="Company ID"),
    location: str = typer.Option(None, "--location", "-l", help="Location name"),
    remote: str = typer.Option(None, "--remote", "-r", help="1=onsite, 2=remote, 3=hybrid"),
    job_type: str = typer.Option(None, "--type", "-t", help="F=full, C=contract, P=part, T=temp, I=intern, V=volunteer"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
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

    if json_output:
        from commands import output_json
        output_json(results)
        return

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
