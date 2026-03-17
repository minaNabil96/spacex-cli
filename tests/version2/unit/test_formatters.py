from datetime import datetime
from rich.table import Table
from rich.panel import Panel
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.table_fmt import format_launches_table
from spacex_cli.models.launch import Launch


def test_format_json():
    data = {"key": "value"}
    compact = format_json(data, pretty=False)
    pretty = format_json(data, pretty=True)
    
    assert compact == '{"key":"value"}'
    assert '"key": "value"' in pretty


def test_format_launches_table():
    launches = [
        Launch(
            id="1",
            name="L1",
            date_utc=datetime.now(),
            success=True,
            rocket="R1",
            launchpad="P1",
            flight_number=1,
            details=None,
            links_webcast=None,
            links_article=None
        )
    ]
    table = format_launches_table(launches)
    assert isinstance(table, Table)
    assert table.title == "🚀 SpaceX Launches"
