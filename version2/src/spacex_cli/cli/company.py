import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_company_panel
from spacex_cli.services import company_service
from spacex_cli.utils.console import console, out_console, error_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Company-related commands", no_args_is_help=True)


@app.command("info")
def company_info() -> None:
    """Get SpaceX company statistics."""
    try:
        with SpaceXClient() as client:
            info = company_service.get_company_info(client)
    except SpaceXCLIError as exc:
        error_console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_company_panel(info))
    else:
        import dataclasses
        out_console.print(format_json(dataclasses.asdict(info), pretty=(state.output == OutputFormat.JSON_PRETTY)))
