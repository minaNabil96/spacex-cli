import json
from typing import Any


def format_json(data: Any, pretty: bool = False) -> str:
    """Serialize data to a JSON string (compact or indented)."""
    if pretty:
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), default=str, ensure_ascii=False)
