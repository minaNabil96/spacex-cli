import csv
import json
from pathlib import Path
from typing import Any


def export_to_json(data: Any, dest: Path, pretty: bool = True) -> Path:
    with open(dest, "w", encoding="utf-8") as f:
        indent = 2 if pretty else None
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
    return dest


def export_to_csv(data: list[dict], dest: Path) -> Path:
    if not data:
        return dest
    with open(dest, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return dest


def export_to_markdown(data: Any, dest: Path, title: str = "SpaceX Report") -> Path:
    with open(dest, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"```json\n{json.dumps(data, indent=2, default=str)}\n```\n")
    return dest
