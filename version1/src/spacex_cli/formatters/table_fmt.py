from rich.table import Table

from spacex_cli.models.capsule import Capsule
from spacex_cli.models.launch import Launch
from spacex_cli.models.rocket import Rocket


def format_launches_table(launches: list[Launch]) -> Table:
    table = Table(title="🚀 SpaceX Launches", show_lines=True)
    table.add_column("Flight #", style="cyan", justify="right")
    table.add_column("Name", style="magenta")
    table.add_column("Date (UTC)", style="green")
    table.add_column("Status", justify="center")

    for la in launches:
        # LL2 Status: Success, Failure, TBD, Partial Failure, etc.
        status_colors = {
            "Success": "green",
            "Failure": "red",
            "Partial Failure": "yellow",
            "TBD": "blue",
        }
        color = status_colors.get(la.status_name, "white")
        table.add_row(
            str(la.flight_number or "N/A"),
            la.name,
            la.date_utc.strftime("%Y-%m-%d %H:%M"),
            f"[{color}]{la.status_abbrev}[/{color}]",
        )
    return table


def format_rockets_table(rockets: list[Rocket]) -> Table:
    table = Table(title="🛰️ SpaceX Rockets", show_lines=True)
    table.add_column("Name", style="magenta")
    table.add_column("Variant", style="blue")
    table.add_column("Active", justify="center")
    table.add_column("Reusable", justify="center")
    table.add_column("Maiden Flight")

    for r in rockets:
        table.add_row(
            r.name,
            r.variant,
            "✅" if r.active else "❌",
            "♻️" if r.reusable else "❌",
            r.maiden_flight or "N/A",
        )
    return table


def format_capsules_table(capsules: list[Capsule]) -> Table:
    table = Table(title="🐉 Spacecraft Versions", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="blue")
    table.add_column("Agency", style="magenta")
    table.add_column("Crew Cap", justify="right")
    table.add_column("Human Rated", justify="center")

    for c in capsules:
        table.add_row(
            c.name,
            c.type,
            c.agency,
            str(c.crew_capacity or 0),
            "👤" if c.human_rated else "❌",
        )
    return table
