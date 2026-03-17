from rich.table import Table

from spacex_cli.models.capsule import Capsule
from spacex_cli.models.launch import Launch
from spacex_cli.models.rocket import Rocket


def format_launches_table(launches: list[Launch]) -> Table:
    table = Table(title="🚀 SpaceX Launches", show_lines=True)
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="magenta")
    table.add_column("Date (UTC)", style="green")
    table.add_column("Success", justify="center")

    for la in launches:
        icon = "✅" if la.success else ("❌" if la.success is False else "⏳")
        table.add_row(
            str(la.id[:8]), # Shorten ID for table
            la.name,
            la.date_utc.strftime("%Y-%m-%d %H:%M"),
            icon,
        )
    return table


def format_rockets_table(rockets: list[Rocket]) -> Table:
    table = Table(title="🛰️ SpaceX Rockets", show_lines=True)
    table.add_column("Name", style="magenta")
    table.add_column("Active", justify="center")
    table.add_column("Stages", justify="right")
    table.add_column("Success %", justify="right")
    table.add_column("First Flight")

    for r in rockets:
        table.add_row(
            r.name,
            "✅" if r.active else "❌",
            str(r.stages),
            f"{r.success_rate_pct}%",
            r.first_flight or "N/A",
        )
    return table


def format_capsules_table(capsules: list[Capsule]) -> Table:
    table = Table(title="🐉 Dragon Capsules", show_lines=True)
    table.add_column("Serial", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Type", style="blue")
    table.add_column("Reuse Count", justify="right")
    table.add_column("Water Landings", justify="right")

    for c in capsules:
        table.add_row(c.serial, c.status, c.type, str(c.reuse_count), str(c.water_landings))
    return table
