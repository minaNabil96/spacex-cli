import sys
from pathlib import Path

import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.services import export_service, launch_service
from spacex_cli.utils.console import console, error_console

app = typer.Typer(help="Export data to file", no_args_is_help=True)


@app.command("launches")
def export_launches(
    dest: Path = typer.Option(Path("./launches_export.json"), "--dest", "-d"),
    fmt: str = typer.Option("json", "--format", "-f", help="json | csv | markdown"),
    limit: int = typer.Option(10, "--limit", "-l"),
) -> None:
    """Export launches data to JSON, CSV or Markdown."""
    try:
        with SpaceXClient() as client:
            launches = launch_service.get_launches(client, limit=limit)
            import dataclasses
            data = [dataclasses.asdict(la) for la in launches]
    except Exception as exc:
        error_console.print(f"[red]Export failed:[/red] {exc}")
        sys.exit(1)

    match fmt:
        case "json":
            export_service.export_to_json(data, dest, pretty=True)
        case "csv":
            export_service.export_to_csv(data, dest)
        case "markdown":
            export_service.export_to_markdown(data, dest, title="SpaceX Launches")
        case _:
            console.print(f"[red]Unknown format:[/red] {fmt}. Use json | csv | markdown")
            sys.exit(2)

    console.print(f"[green]✓ Exported {len(data)} records → {dest}[/green]")
