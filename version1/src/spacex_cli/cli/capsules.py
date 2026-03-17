import sys
from dataclasses import asdict
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_capsule_panel
from spacex_cli.formatters.table_fmt import format_capsules_table
from spacex_cli.services import capsule_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Capsule-related commands", no_args_is_help=True)


@app.command("list")
def list_capsules(
    limit: int = typer.Option(10, "--limit", "-l"),
) -> None:
    """List Dragon capsules."""
    try:
        with SpaceXClient() as client:
            capsules = capsule_service.get_capsules(client, limit=limit)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_capsules_table(capsules))
    else:
        out_console.print(
            format_json([asdict(c) for c in capsules], pretty=(state.output == OutputFormat.JSON_PRETTY))
        )


@app.command("info")
def capsule_info(
    capsule_id: str = typer.Argument(..., help="Capsule ID"),
) -> None:
    """Get detailed information about a capsule."""
    try:
        with SpaceXClient() as client:
            capsule = capsule_service.get_capsule_by_id(client, capsule_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_capsule_panel(capsule))
    else:
        out_console.print(format_json(asdict(capsule), pretty=(state.output == OutputFormat.JSON_PRETTY)))
