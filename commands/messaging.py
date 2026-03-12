"""Messaging commands."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("list")
def list_conversations():
    """List recent conversations."""
    from auth import get_client
    api = get_client()
    convos = api.get_conversations()

    table = Table(title="Conversations")
    table.add_column("Participants", style="green")
    table.add_column("Last Message")
    table.add_column("Date", style="dim")

    for convo in convos:
        name = convo.get("participants", "")
        last_msg = convo.get("lastMessage", "")[:80] if isinstance(convo.get("lastMessage"), str) else ""
        date = convo.get("date", "")

        table.add_row(name, last_msg, date)

    console.print(table)


@app.command()
def read(
    conversation_urn: str = typer.Argument(..., help="Conversation URN ID"),
):
    """Read messages in a conversation."""
    from auth import get_client
    api = get_client()
    convo = api.get_conversation(conversation_urn_id=conversation_urn)

    if isinstance(convo, dict):
        events = convo.get("events", [])
    elif isinstance(convo, list):
        events = convo
    else:
        events = []

    for msg in events:
        sender = msg.get("from", {})
        name = f"{sender.get('firstName', '')} {sender.get('lastName', '')}"
        text = msg.get("eventContent", {}).get("messageEvent", {}).get("body", "") if isinstance(msg.get("eventContent"), dict) else str(msg.get("eventContent", ""))

        console.print(f"[bold cyan]{name}[/bold cyan]")
        console.print(f"  {text}")
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
