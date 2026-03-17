import csv
from io import StringIO


def format_to_csv(data: list[dict]) -> str:
    """Форматирует список словарей в CSV-строку."""
    if not data:
        return ""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
