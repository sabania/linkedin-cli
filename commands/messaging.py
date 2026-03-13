"""Messaging commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("list")
def list_conversations(
    limit: int = typer.Option(25, "--limit", "-n", help="Number of conversations"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List recent conversations."""
    from auth import get_client
    api = get_client()
    convos = api.get_conversations(limit=limit)

    if json_output:
        from commands import output_json
        output_json(convos)
        return

    table = Table(title="Conversations")
    table.add_column("Participants", style="green")
    table.add_column("Last Message")
    table.add_column("Date", style="dim")
    table.add_column("Conversation URN", style="cyan")

    for convo in convos:
        name = convo.get("participants", "")
        last_msg = convo.get("lastMessage", "")[:80] if isinstance(convo.get("lastMessage"), str) else ""
        date = convo.get("date", "")
        conv_urn = convo.get("conversationUrn", "")

        table.add_row(name, last_msg, date, conv_urn)

    console.print(table)


@app.command()
def read(
    name: str = typer.Argument(..., help="Participant name to find conversation"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Read messages in a conversation by participant name."""
    from auth import get_client
    api = get_client()
    messages = api.get_conversation(name=name)

    if json_output:
        from commands import output_json
        output_json(messages)
        return

    if not messages:
        console.print(f"[yellow]No conversation found for '{name}'[/yellow]")
        return

    console.print(f"[bold]Conversation with '{name}'[/bold]\n")
    last_sender = ""
    for msg in messages:
        sender = msg.get("sender", "")
        body = msg.get("body", "")
        time_str = msg.get("time", "")
        if sender and sender != last_sender:
            console.print(f"[bold cyan]{sender}[/bold cyan]  [dim]{time_str}[/dim]")
            last_sender = sender
        elif not sender and time_str:
            console.print(f"  [dim]{time_str}[/dim]")
        console.print(f"  {body}")
        console.print()


@app.command()
def send(
    conversation_urn: str = typer.Option(None, "--conversation", "-c", help="Conversation URN"),
    recipient: str = typer.Option(None, "--to", "-t", help="Recipient URN ID (for new conversation)"),
    message: str = typer.Argument(..., help="Message text"),
):
    """Send a message."""
    from auth import get_client
    api = get_client()

    kwargs = {"message_body": message}
    if conversation_urn:
        kwargs["conversation_urn_id"] = conversation_urn
    elif recipient:
        kwargs["recipients"] = [recipient]
    else:
        console.print("[red]Provide either --conversation or --to[/red]")
        raise typer.Exit(1)

    api.send_message(**kwargs)
    console.print("[green]Message sent[/green]")


@app.command()
def seen(
    conversation_urn: str = typer.Argument(..., help="Conversation URN ID"),
):
    """Mark a conversation as seen."""
    from auth import get_client
    api = get_client()
    api.mark_conversation_as_seen(conversation_urn_id=conversation_urn)
    console.print("[green]Marked as seen[/green]")
