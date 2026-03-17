from rich.console import Console

console = Console(stderr=True)   # Rich output → stderr (doesn't interfere with JSON in stdout)
out_console = Console()          # Clean stdout for JSON
