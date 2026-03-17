import typer
from enum import Enum


from spacex_cli.utils.console import console
from spacex_cli.utils.logging import setup_logging


app = typer.Typer(
    name="spacex2",
    help="🚀 SpaceX launch intelligence from your terminal made by Mina Nabil.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


class OutputFormat(str, Enum):
    TABLE = "table"
    JSON = "json"
    JSON_PRETTY = "json-pretty"


class _State:
    output: OutputFormat = OutputFormat.TABLE
    verbose: bool = False


state = _State()


@app.callback()
def main(
    output: OutputFormat = typer.Option(
        OutputFormat.TABLE, "--output", "-o", help="Output format"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
) -> None:
    state.output = output
    state.verbose = verbose
    setup_logging(verbose=verbose)


# Lazy import/add subtypers to avoid circular imports
from spacex_cli.cli import launches, rockets, capsules, company, export  # noqa: E402

app.add_typer(launches.app, name="launches")
app.add_typer(rockets.app, name="rockets")
app.add_typer(capsules.app, name="capsules")
app.add_typer(company.app, name="company")
app.add_typer(export.app, name="export")


@app.command(name="exit")
def exit_cmd() -> None:
    """Выход из SpaceX CLI / Exit the SpaceX CLI."""
    console.print("[bold green]👋 Goodbye! Thanks for using SpaceX CLI.[/bold green]")
    raise SystemExit(0)
