import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_rocket_panel
from spacex_cli.formatters.table_fmt import format_rockets_table
from spacex_cli.services import rocket_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Rocket-related commands", no_args_is_help=True)


@app.command("list")
def list_rockets(
    limit: int = typer.Option(10, "--limit", "-l"),
) -> None:
    """List SpaceX rockets."""
    try:
        with SpaceXClient() as client:
            rockets = rocket_service.get_rockets(client, limit=limit)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_rockets_table(rockets))
    else:
        import dataclasses
        data = [dataclasses.asdict(r) for r in rockets]
        out_console.print(format_json(data, pretty=(state.output == OutputFormat.JSON_PRETTY)))


@app.command("info")
def rocket_info(
    rocket_id: str = typer.Argument(..., help="Rocket ID"),
) -> None:
    """Get detailed specifications of a rocket."""
    try:
        with SpaceXClient() as client:
            rocket = rocket_service.get_rocket_by_id(client, rocket_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_rocket_panel(rocket))
    else:
        import dataclasses
        out_console.print(format_json(dataclasses.asdict(rocket), pretty=(state.output == OutputFormat.JSON_PRETTY)))
