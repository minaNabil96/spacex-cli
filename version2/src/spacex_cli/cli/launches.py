import dataclasses
import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_launch_panel
from spacex_cli.formatters.table_fmt import format_launches_table
from spacex_cli.services import launch_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.countdown import countdown_to_launch
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Launch-related commands", no_args_is_help=True)


@app.command("list")
def list_launches(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results"),
    upcoming: bool = typer.Option(False, "--upcoming", help="Only upcoming"),
    past: bool = typer.Option(False, "--past", help="Only past"),
) -> None:
    """List SpaceX launches."""
    try:
        with SpaceXClient() as client:
            launches = launch_service.get_launches(
                client, limit=limit, upcoming=upcoming, past=past
            )
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_launches_table(launches))
    else:
        data = [dataclasses.asdict(la) for la in launches]
        out_console.print(format_json(data, pretty=(state.output == OutputFormat.JSON_PRETTY)))


@app.command("info")
def launch_info(
    launch_id: str = typer.Argument(..., help="Launch ID"),
) -> None:
    """Get detailed information about a specific launch."""
    try:
        with SpaceXClient() as client:
            details = launch_service.get_launch_by_id(client, launch_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_launch_panel(details))
    else:
        out_console.print(format_json(dataclasses.asdict(details), pretty=(state.output == OutputFormat.JSON_PRETTY)))


@app.command("countdown")
def launch_countdown() -> None:
    """Live countdown to the next SpaceX launch."""
    try:
        with SpaceXClient() as client:
            nxt = launch_service.get_next_launch(client)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    console.print(f"[bold blue]Next Mission:[/bold blue] {nxt.name}")
    countdown_to_launch(nxt.date_utc, console)
