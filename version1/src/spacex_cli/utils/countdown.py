import time
from datetime import datetime, timezone
from rich.console import Console
from rich.live import Live
from rich.text import Text


def countdown_to_launch(target: datetime, console: Console) -> None:
    """Live countdown to target datetime using Rich Live display."""
    with Live(console=console, refresh_per_second=1) as live:
        while True:
            now = datetime.now(tz=timezone.utc)
            delta = target - now
            if delta.total_seconds() <= 0:
                live.update(Text("🚀 Launch time!", style="bold green"))
                break
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            live.update(
                Text(f"⏳ T-{hours:02d}:{minutes:02d}:{seconds:02d}", style="bold yellow")
            )
            time.sleep(1)
