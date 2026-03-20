import responses
import json
from pathlib import Path
from typer.testing import CliRunner
import traceback
import sys

# Add src to sys.path at the beginning to ensure it's picked over any other installed versions
sys.path.insert(0, str(Path("src").absolute()))

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://lldev.thespacedevs.com/2.2.0"
FIXTURES = Path("../tests/version2/fixtures").absolute()

def debug_rockets_list():
    rockets_response = json.loads((FIXTURES / "rockets_response.json").read_text())
    rockets_data = rockets_response["results"]
    
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{BASE}/config/launcher/",
            json={"results": rockets_data, "count": len(rockets_data)},
            status=200,
            match_querystring=False
        )
        
        print("Running 'rockets list'...")
        result = runner.invoke(app, ["rockets", "list"], catch_exceptions=False)
        print(f"Exit code: {result.exit_code}")
        print(f"Stdout: {result.stdout}")

if __name__ == "__main__":
    try:
        debug_rockets_list()
    except Exception:
        traceback.print_exc()
