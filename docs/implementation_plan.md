# implementation_plan.md

```markdown
# SpaceX Launch Tracker CLI — Implementation Plan

> **Контекст задания:** Практическая работа по разработке CLI-утилит с использованием
> ИИ-инструментов. Проект реализуется **параллельно в двух нейросетях** (ChatGPT + Claude),
> результаты сравниваются и публикуются на GitHub.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Assignment Compliance Map](#2-assignment-compliance-map)
3. [Technology Stack](#3-technology-stack)
4. [Repository Structure](#4-repository-structure)
5. [Implementation Phases](#5-implementation-phases)
   - [Phase 1: Project Setup & Configuration](#phase-1-project-setup--configuration)
   - [Phase 2: Core API Layer](#phase-2-core-api-layer)
   - [Phase 3: Data Models](#phase-3-data-models)
   - [Phase 4: Service Layer](#phase-4-service-layer)
   - [Phase 5: CLI Commands](#phase-5-cli-commands)
   - [Phase 6: Formatters](#phase-6-formatters)
   - [Phase 7: Testing (coverage > 60%)](#phase-7-testing)
   - [Phase 8: Documentation & GitHub Publication](#phase-8-documentation--github-publication)
6. [Verification & Build](#6-verification--build)
7. [Running the CLI](#7-running-the-cli)
8. [Pre-Submission Checklist](#8-pre-submission-checklist)

---

## 1. Project Overview

**SpaceX CLI** — утилита командной строки для получения актуальной информации о запусках
SpaceX, ракетах, капсулах и данных компании прямо из терминала.

Инструмент использует **The Space Devs' Launch Library 2 API** (development version), фильтруя данные по SpaceX (Agency ID 121), форматирует вывод
в виде JSON или Rich-таблиц и поддерживает интерактивный обратный отсчёт до запуска.

### Core Features

| Feature          | Command                       | Description                              |
|------------------|-------------------------------|------------------------------------------|
| Launch List      | `spacex launches list`        | Список запусков с фильтрами              |
| Launch Details   | `spacex launches info <id>`   | Детали одного запуска                    |
| Launch Countdown | `spacex launches countdown`   | Живой обратный отсчёт до следующего      |
| Rocket Fleet     | `spacex rockets list`         | Все ракеты SpaceX                        |
| Rocket Details   | `spacex rockets info <id>`    | Спецификации ракеты                      |
| Capsules         | `spacex capsules list`        | Список капсул Dragon                     |
| Capsule Details  | `spacex capsules info <id>`   | Детали капсулы                           |
| Company Info     | `spacex company info`         | Статистика компании                      |
| Export Reports   | `spacex export launches`      | Экспорт в JSON / CSV / Markdown          |

> ✅ Минимум **9 команд/подкоманд** — требование (≥ 7) выполнено с запасом (10 команд).

### Output Formats

| Format      | Flag value   | Поведение                         |
|-------------|--------------|-----------------------------------|
| Table       | `table`      | Rich-таблица в stderr (по умолч.) |
| JSON        | `json`       | Компактный JSON в stdout          |
| Pretty JSON | `json-pretty`| Форматированный JSON в stdout     |

---

## 2. Assignment Compliance Map

Сопоставление требований задания с решениями в проекте.

| Требование задания                              | Реализация в проекте                                      |
|-------------------------------------------------|-----------------------------------------------------------|
| REST API обязателен                             | Launch Library 2 API — данные через HTTP GET             |
| Минимум 7 команд/подкоманд                      | 10 команд (launches×3, rockets×2, capsules×2, company, export, exit) |
| Средняя/высокая сложность                       | Вложенные Typer-группы, пагинация, countdown, экспорт     |
| Параллельная разработка в 2 нейросетях          | `version1/` (ChatGPT) + `version2/` (Claude)              |
| Сохранение всех промптов                        | `docs/prompts/` — полные логи диалогов с таймстампами     |
| Unit-тесты (покрытие > 60%)                     | pytest + responses; цель ≥ 65%                            |
| PEP 8                                           | ruff (линтер + форматтер)                                 |
| README с описанием API, установкой, примерами   | README.md + docs/api_reference.md                         |
| comparison.md в репозитории                     | `comparison.md` — сравнительный анализ двух версий        |
| Правильная структура репозитория                | version1/, version2/, docs/, tests/, comparison.md        |
| Badges, лицензия, .gitignore                    | MIT, GitHub Actions badge, .gitignore                     |

---

## 3. Technology Stack

| Слой            | Выбор              | Обоснование                                          |
|-----------------|--------------------|------------------------------------------------------|
| Язык            | Python ≥ 3.11      | match-выражения, зрелые type hints, slots             |
| CLI Framework   | Typer 0.12+        | Декларативный, автогенерация `--help`, type-safe      |
| HTTP Client     | Requests 2.31+     | Стандарт де-факто, поддержка Session                  |
| Terminal UI     | Rich 13+           | Таблицы, панели, прогресс-бары, Markdown              |
| JSON            | stdlib `json`      | Нет лишних зависимостей                               |
| Дата/время      | stdlib `datetime`  | Обратный отсчёт, форматирование                       |
| Тестирование    | pytest + responses | Мокирование HTTP без monkey-patching                  |
| Пакетирование   | pyproject.toml     | PEP 621, современный стандарт                         |
| Линтинг         | ruff               | PEP 8, isort, pyflakes в одном инструменте            |
| CI              | GitHub Actions     | Автоматический запуск тестов при push                 |

---

## 4. Repository Structure

```
spacex-cli/                          # Корень публичного репозитория
│
├── version1/                        # Версия от нейросети 1 (ChatGPT)
│   ├── pyproject.toml
│   ├── README.md
│   ├── .env.example
│   ├── .gitignore
│   ├── src/
│   │   └── spacex_cli/
│   │       ├── __init__.py
│   │       ├── __main__.py
│   │       ├── cli/
│   │       │   ├── __init__.py      # Typer app + callback + OutputFormat enum
│   │       │   ├── launches.py
│   │       │   ├── rockets.py
│   │       │   ├── capsules.py
│   │       │   ├── company.py
│   │       │   └── export.py
│   │       ├── api/
│   │       │   ├── __init__.py
│   │       │   ├── client.py        # SpaceXClient (requests.Session)
│   │       │   ├── endpoints.py     # URL-константы
│   │       │   └── pagination.py    # Итератор пагинации
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   ├── launch.py
│   │       │   ├── rocket.py
│   │       │   ├── capsule.py
│   │       │   └── company.py
│   │       ├── services/
│   │       │   ├── __init__.py
│   │       │   ├── launch_service.py
│   │       │   ├── rocket_service.py
│   │       │   ├── capsule_service.py
│   │       │   ├── company_service.py
│   │       │   └── export_service.py
│   │       ├── formatters/
│   │       │   ├── __init__.py
│   │       │   ├── json_fmt.py
│   │       │   ├── table_fmt.py
│   │       │   ├── panel_fmt.py
│   │       │   └── csv_fmt.py
│   │       ├── config/
│   │       │   ├── __init__.py
│   │       │   └── settings.py
│   │       └── utils/
│   │           ├── __init__.py
│   │           ├── console.py
│   │           ├── errors.py
│   │           ├── logging.py
│   │           └── countdown.py
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       │   ├── test_models.py
│       │   ├── test_pagination.py
│       │   ├── test_formatters.py
│       │   ├── test_launch_service.py
│       │   └── test_cli_commands.py
│       ├── integration/
│       │   ├── test_launches_cmd.py
│       │   ├── test_rockets_cmd.py
│       │   ├── test_capsules_cmd.py
│       │   ├── test_company_cmd.py
│       │   └── test_export_cmd.py
│       └── fixtures/
│           ├── __init__.py
│           ├── launches_response.json
│           ├── rockets_response.json
│           ├── capsules_response.json
│           ├── company_response.json
│           └── api_responses.py
│
├── version2/                        # Версия от нейросети 2 (Claude)
│   └── ...                          # Аналогичная структура
│
├── docs/
│   ├── prompts/
│   │   ├── chatgpt_session.md       # Все промпты ChatGPT с таймстампами
│   │   └── claude_session.md        # Все промпты Claude с таймстампами
│   └── api_reference.md             # Описание SpaceX API endpoints
│
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions: lint + test
│
├── README.md                        # Описание проекта, установка, примеры
└── comparison.md                    # Сравнительный анализ двух версий
```

---

## 5. Implementation Phases

### Phase 1: Project Setup & Configuration

#### 1.1 pyproject.toml

```toml
[project]
name = "spacex-cli"
version = "0.1.0"
description = "SpaceX launch intelligence from your terminal"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [{name = "Your Name", email = "you@example.com"}]
dependencies = [
    "typer[all] >=0.12, <1",
    "requests >=2.31, <3",
    "rich >=13, <14",
    "python-dotenv >=1, <2",
]

[project.optional-dependencies]
dev = [
    "pytest >=7, <8",
    "pytest-cov >=4, <5",
    "responses >=0.24, <1",
    "ruff >=0.3, <1",
]

[project.scripts]
spacex = "spacex_cli.cli:app"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=spacex_cli --cov-report=term-missing --cov-fail-under=60"
```

#### 1.2 .env.example

```bash
# SpaceX API Base URL (Launch Library 2)
SPACEX_API_URL=https://lldev.thespacedevs.com/2.2.0/

# Request timeout in seconds
REQUEST_TIMEOUT=30
```

#### 1.3 .gitignore

```
__pycache__/
*.pyc
.env
.venv/
dist/
*.egg-info/
.coverage
htmlcov/
.ruff_cache/
```

#### 1.4 Package Entry Points

`src/spacex_cli/__init__.py`:
```python
__version__ = "0.1.0"
```

`src/spacex_cli/__main__.py`:
```python
from spacex_cli.cli import app

if __name__ == "__main__":
    app()
```

#### 1.5 Settings

`src/spacex_cli/config/settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()


def get_api_url() -> str:
    return os.getenv("SPACEX_API_URL", "https://lldev.thespacedevs.com/2.2.0/")


def get_timeout() -> int:
    return int(os.getenv("REQUEST_TIMEOUT", "30"))
```

#### 1.6 Utility Layer

`src/spacex_cli/utils/console.py`:
```python
from rich.console import Console

console = Console(stderr=True)   # Rich-вывод → stderr (не мешает JSON в stdout)
out_console = Console()          # Чистый stdout для JSON
```

`src/spacex_cli/utils/errors.py`:
```python
class SpaceXCLIError(Exception):
    """Базовое исключение CLI."""


class NetworkError(SpaceXCLIError):
    """Ошибка сетевого соединения."""


class NotFoundError(SpaceXCLIError):
    """Ресурс не найден (404)."""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"Not found: {resource}/{identifier}")


class APIError(SpaceXCLIError):
    """Непредвиденная HTTP-ошибка."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"SpaceX API error {status_code}: {message}")


class ValidationError(SpaceXCLIError):
    """Некорректный ввод пользователя."""
```

`src/spacex_cli/utils/logging.py`:
```python
import logging


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
```

`src/spacex_cli/utils/countdown.py`:
```python
import time
from datetime import datetime, timezone
from rich.console import Console
from rich.live import Live
from rich.text import Text


def countdown_to_launch(target: datetime, console: Console) -> None:
    """Живой обратный отсчёт до target (Rich Live)."""
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
```

---

### Phase 2: Core API Layer

#### 2.1 SpaceXClient (`src/spacex_cli/api/client.py`)

```python
import requests
from typing import Optional

from spacex_cli.config.settings import get_api_url, get_timeout
from spacex_cli.utils.errors import APIError, NetworkError, NotFoundError


class SpaceXClient:
    """Тонкая обёртка вокруг requests.Session для Launch Library 2 API."""

    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {"Accept": "application/json", "User-Agent": "SpaceX-CLI/0.1"}
        )
        self._base_url = get_api_url()
        self._timeout = get_timeout()

    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        url = f"{self._base_url}{endpoint}"
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.exceptions.RequestException as exc:
            raise NetworkError(f"Network error: {exc}") from exc
        self._raise_for_status(response)
        return response

    def get_all(
        self, endpoint: str, params: Optional[dict] = None, limit: int = 100
    ) -> list[dict]:
        params = {**(params or {}), "limit": limit}
        return self.get(endpoint, params=params).json()

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        match response.status_code:
            case 200 | 201 | 204:
                return
            case 404:
                raise NotFoundError("resource", response.url)
            case _:
                try:
                    msg = response.json().get("message", "Unknown error")
                except Exception:
                    msg = response.text
                raise APIError(response.status_code, msg)

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "SpaceXClient":
        return self

    def __exit__(self, *exc) -> None:
        self.close()
```

#### 2.2 Endpoints (`src/spacex_cli/api/endpoints.py`)

```python
# Launches
LAUNCHES = "/launch"
LAUNCH_UPCOMING = "/launch/upcoming"
LAUNCH_PREVIOUS = "/launch/previous"
LAUNCH_DETAIL = "/launch/{id}"

# Agency (Company)
COMPANY = "/agencies/121"

# Rockets & Capsules (Configurations)
ROCKETS = "/config/launcher"
CAPSULES = "/config/spacecraft"
```

#### 2.3 Pagination (`src/spacex_cli/api/pagination.py`)

```python
from typing import Generator, Optional
from spacex_cli.api.client import SpaceXClient


def paginate(
    client: SpaceXClient,
    endpoint: str,
    params: Optional[dict] = None,
    limit: int = 100,
) -> Generator[dict, None, None]:
    """Возвращает отдельные объекты из постраничного ответа API."""
    for item in client.get_all(endpoint, params=params, limit=limit):
        yield item
```

---

### Phase 3: Data Models

#### 3.1 Launch (`src/spacex_cli/models/launch.py`)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True, slots=True)
class Launch:
    id: str
    name: str
    date_utc: datetime
    success: Optional[bool]
    rocket: str
    launchpad: str
    flight_number: int
    details: Optional[str]
    links_webcast: Optional[str]
    links_article: Optional[str]


@dataclass(frozen=True, slots=True)
class LaunchDetails:
    launch: Launch
    payload_mass_kg: Optional[float]
    payload_mass_lbs: Optional[float]
    orbit: Optional[str]
    customers: list[str]
```

#### 3.2 Rocket (`src/spacex_cli/models/rocket.py`)

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Rocket:
    id: str
    name: str
    type: str
    active: bool
    stages: int
    boosters: int
    cost_per_launch: int
    success_rate_pct: float
    first_flight: Optional[str]
    country: str
    company: str
    height: dict
    diameter: dict
    mass: dict
    description: str
```

#### 3.3 Capsule (`src/spacex_cli/models/capsule.py`)

```python
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Capsule:
    id: str
    serial: str
    status: str
    type: str
    reuse_count: int
    water_landings: int
    land_landings: int
    last_update: Optional[str]
    launches: list[str]
```

#### 3.4 Company (`src/spacex_cli/models/company.py`)

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CompanyInfo:
    name: str
    founder: str
    founded: int
    employees: int
    vehicles: int
    launch_sites: int
    test_sites: int
    ceo: str
    cto: str
    coo: str
    valuation: int
    headquarters: dict
    links: dict
    summary: str
```

---

### Phase 4: Service Layer

#### 4.1 Launch Service (`src/spacex_cli/services/launch_service.py`)

```python
from datetime import datetime
from typing import Optional

from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import LAUNCH_DETAIL, LAUNCH_NEXT, LAUNCHES
from spacex_cli.models.launch import Launch, LaunchDetails


def get_launches(
    client: SpaceXClient,
    limit: int = 10,
    upcoming: bool = False,
    past: bool = False,
) -> list[Launch]:
    params: dict = {"limit": limit}
    if upcoming:
        params["upcoming"] = True
    if past:
        params["past"] = True
    data = client.get_all(LAUNCHES, params=params)
    return [_parse_launch(item) for item in data]


def get_launch_by_id(client: SpaceXClient, launch_id: str) -> LaunchDetails:
    data = client.get(LAUNCH_DETAIL.format(id=launch_id)).json()
    return _parse_launch_details(data)


def get_next_launch(client: SpaceXClient) -> Launch:
    data = client.get(LAUNCH_NEXT).json()
    return _parse_launch(data)


def _parse_launch(data: dict) -> Launch:
    return Launch(
        id=data["id"],
        name=data["name"],
        date_utc=datetime.fromisoformat(data["date_utc"].replace("Z", "+00:00")),
        success=data.get("success"),
        rocket=data.get("rocket", ""),
        launchpad=data.get("launchpad", ""),
        flight_number=data.get("flight_number", 0),
        details=data.get("details"),
        links_webcast=data.get("links", {}).get("webcast"),
        links_article=data.get("links", {}).get("article"),
    )


def _parse_launch_details(data: dict) -> LaunchDetails:
    payload = data.get("payloads", [{}])[0] if data.get("payloads") else {}
    return LaunchDetails(
        launch=_parse_launch(data),
        payload_mass_kg=payload.get("mass_kg"),
        payload_mass_lbs=payload.get("mass_lbs"),
        orbit=payload.get("orbit"),
        customers=payload.get("customers", []),
    )
```

#### 4.2 Rocket Service (`src/spacex_cli/services/rocket_service.py`)

```python
from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import ROCKET_DETAIL, ROCKETS
from spacex_cli.models.rocket import Rocket


def get_rockets(client: SpaceXClient, limit: int = 10) -> list[Rocket]:
    return [_parse_rocket(item) for item in client.get_all(ROCKETS, params={"limit": limit})]


def get_rocket_by_id(client: SpaceXClient, rocket_id: str) -> Rocket:
    return _parse_rocket(client.get(ROCKET_DETAIL.format(id=rocket_id)).json())


def _parse_rocket(data: dict) -> Rocket:
    return Rocket(
        id=data["id"],
        name=data["name"],
        type=data["type"],
        active=data["active"],
        stages=data["stages"],
        boosters=data["boosters"],
        cost_per_launch=data["cost_per_launch"],
        success_rate_pct=data["success_rate_pct"],
        first_flight=data.get("first_flight"),
        country=data["country"],
        company=data["company"],
        height=data["height"],
        diameter=data["diameter"],
        mass=data["mass"],
        description=data["description"],
    )
```

#### 4.3 Capsule Service (`src/spacex_cli/services/capsule_service.py`)

```python
from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import CAPSULE_DETAIL, CAPSULES
from spacex_cli.models.capsule import Capsule


def get_capsules(client: SpaceXClient, limit: int = 10) -> list[Capsule]:
    return [_parse_capsule(item) for item in client.get_all(CAPSULES, params={"limit": limit})]


def get_capsule_by_id(client: SpaceXClient, capsule_id: str) -> Capsule:
    return _parse_capsule(client.get(CAPSULE_DETAIL.format(id=capsule_id)).json())


def _parse_capsule(data: dict) -> Capsule:
    return Capsule(
        id=data["id"],
        serial=data["serial"],
        status=data["status"],
        type=data["type"],
        reuse_count=data["reuse_count"],
        water_landings=data["water_landings"],
        land_landings=data["land_landings"],
        last_update=data.get("last_update"),
        launches=data.get("launches", []),
    )
```

#### 4.4 Company Service (`src/spacex_cli/services/company_service.py`)

```python
from spacex_cli.api.client import SpaceXClient
from spacex_cli.api.endpoints import COMPANY
from spacex_cli.models.company import CompanyInfo


def get_company_info(client: SpaceXClient) -> CompanyInfo:
    data = client.get(COMPANY).json()
    return CompanyInfo(
        name=data["name"],
        founder=data["founder"],
        founded=data["founded"],
        employees=data["employees"],
        vehicles=data["vehicles"],
        launch_sites=data["launch_sites"],
        test_sites=data["test_sites"],
        ceo=data["ceo"],
        cto=data["cto"],
        coo=data["coo"],
        valuation=data["valuation"],
        headquarters=data["headquarters"],
        links=data["links"],
        summary=data["summary"],
    )
```

#### 4.5 Export Service (`src/spacex_cli/services/export_service.py`)

```python
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
```

---

### Phase 5: CLI Commands

#### 5.1 App Entry Point (`src/spacex_cli/cli/__init__.py`)

```python
import typer

from spacex_cli.utils.console import console
from spacex_cli.utils.logging import setup_logging
from spacex_cli.utils.errors import SpaceXCLIError
from enum import Enum

app = typer.Typer(
    name="spacex",
    help="🚀 SpaceX launch intelligence from your terminal.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


class OutputFormat(str, Enum):
    TABLE = "table"
    JSON = "json"
    JSON_PRETTY = "json-pretty"


class _State:
    output: OutputFormat = OutputFormat.TABLE
    verbose: bool = False


state = _State()


@app.callback()
def main(
    output: OutputFormat = typer.Option(
        OutputFormat.TABLE, "--output", "-o", help="Output format"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose logging"),
) -> None:
    state.output = output
    state.verbose = verbose
    setup_logging(verbose=verbose)


# ── подключение групп команд ─────────────────────────────────────────────────
from spacex_cli.cli import launches, rockets, capsules, company, export  # noqa: E402

app.add_typer(launches.app, name="launches")
app.add_typer(rockets.app, name="rockets")
app.add_typer(capsules.app, name="capsules")
app.add_typer(company.app, name="company")
app.add_typer(export.app, name="export")
```

> **Единый обработчик ошибок** добавляется через декоратор `@app.command()` или общую
> обёртку, чтобы ловить `SpaceXCLIError` и выводить понятное сообщение + `sys.exit(1)`.

#### 5.2 Launches (`src/spacex_cli/cli/launches.py`)

```python
import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_launch_panel
from spacex_cli.formatters.table_fmt import format_launches_table
from spacex_cli.services import launch_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.countdown import countdown_to_launch
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Launch-related commands", no_args_is_help=True)


@app.command("list")
def list_launches(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of results"),
    upcoming: bool = typer.Option(False, "--upcoming", help="Only upcoming"),
    past: bool = typer.Option(False, "--past", help="Only past"),
) -> None:
    """List SpaceX launches."""
    try:
        with SpaceXClient() as client:
            launches = launch_service.get_launches(
                client, limit=limit, upcoming=upcoming, past=past
            )
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_launches_table(launches))
    else:
        data = [vars(la) for la in launches]
        out_console.print(format_json(data, pretty=(state.output == OutputFormat.JSON_PRETTY)))


@app.command("info")
def launch_info(
    launch_id: str = typer.Argument(..., help="Launch ID"),
) -> None:
    """Get detailed information about a specific launch."""
    try:
        with SpaceXClient() as client:
            details = launch_service.get_launch_by_id(client, launch_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_launch_panel(details))
    else:
        out_console.print(format_json(vars(details), pretty=(state.output == OutputFormat.JSON_PRETTY)))


@app.command("countdown")
def launch_countdown() -> None:
    """Live countdown to the next SpaceX launch."""
    try:
        with SpaceXClient() as client:
            nxt = launch_service.get_next_launch(client)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    console.print(f"[bold blue]Next Mission:[/bold blue] {nxt.name}")
    countdown_to_launch(nxt.date_utc, console)
```

#### 5.3 Rockets (`src/spacex_cli/cli/rockets.py`)

```python
import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_rocket_panel
from spacex_cli.formatters.table_fmt import format_rockets_table
from spacex_cli.services import rocket_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Rocket-related commands", no_args_is_help=True)


@app.command("list")
def list_rockets(
    limit: int = typer.Option(10, "--limit", "-l"),
) -> None:
    """List SpaceX rockets."""
    try:
        with SpaceXClient() as client:
            rockets = rocket_service.get_rockets(client, limit=limit)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_rockets_table(rockets))
    else:
        out_console.print(
            format_json([vars(r) for r in rockets], pretty=(state.output == OutputFormat.JSON_PRETTY))
        )


@app.command("info")
def rocket_info(
    rocket_id: str = typer.Argument(..., help="Rocket ID"),
) -> None:
    """Get detailed specifications of a rocket."""
    try:
        with SpaceXClient() as client:
            rocket = rocket_service.get_rocket_by_id(client, rocket_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_rocket_panel(rocket))
    else:
        out_console.print(format_json(vars(rocket), pretty=(state.output == OutputFormat.JSON_PRETTY)))
```

#### 5.4 Capsules (`src/spacex_cli/cli/capsules.py`)

```python
import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_capsule_panel
from spacex_cli.formatters.table_fmt import format_capsules_table
from spacex_cli.services import capsule_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Capsule-related commands", no_args_is_help=True)


@app.command("list")
def list_capsules(
    limit: int = typer.Option(10, "--limit", "-l"),
) -> None:
    """List Dragon capsules."""
    try:
        with SpaceXClient() as client:
            capsules = capsule_service.get_capsules(client, limit=limit)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_capsules_table(capsules))
    else:
        out_console.print(
            format_json([vars(c) for c in capsules], pretty=(state.output == OutputFormat.JSON_PRETTY))
        )


@app.command("info")
def capsule_info(
    capsule_id: str = typer.Argument(..., help="Capsule ID"),
) -> None:
    """Get detailed information about a capsule."""
    try:
        with SpaceXClient() as client:
            capsule = capsule_service.get_capsule_by_id(client, capsule_id)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_capsule_panel(capsule))
    else:
        out_console.print(format_json(vars(capsule), pretty=(state.output == OutputFormat.JSON_PRETTY)))
```

#### 5.5 Company (`src/spacex_cli/cli/company.py`)

```python
import sys
import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.cli import OutputFormat, state
from spacex_cli.formatters.json_fmt import format_json
from spacex_cli.formatters.panel_fmt import format_company_panel
from spacex_cli.services import company_service
from spacex_cli.utils.console import console, out_console
from spacex_cli.utils.errors import SpaceXCLIError

app = typer.Typer(help="Company-related commands", no_args_is_help=True)


@app.command("info")
def company_info() -> None:
    """Get SpaceX company statistics."""
    try:
        with SpaceXClient() as client:
            info = company_service.get_company_info(client)
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        sys.exit(1)

    if state.output == OutputFormat.TABLE:
        console.print(format_company_panel(info))
    else:
        out_console.print(format_json(vars(info), pretty=(state.output == OutputFormat.JSON_PRETTY)))
```

#### 5.6 Export (`src/spacex_cli/cli/export.py`)

```python
import sys
from pathlib import Path

import typer

from spacex_cli.api.client import SpaceXClient
from spacex_cli.services import export_service, launch_service, rocket_service
from spacex_cli.utils.console import console
from spacex_cli.utils.errors import SpaceXCLIError

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
            data = [vars(la) for la in launches]
    except SpaceXCLIError as exc:
        console.print(f"[red]Error:[/red] {exc}")
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
```

---

### Phase 6: Formatters

#### 6.1 JSON Formatter (`src/spacex_cli/formatters/json_fmt.py`)

```python
import json
from typing import Any


def format_json(data: Any, pretty: bool = False) -> str:
    """Сериализует данные в JSON-строку (compact или indented)."""
    if pretty:
        return json.dumps(data, indent=2, default=str, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), default=str, ensure_ascii=False)
```

#### 6.2 Table Formatter (`src/spacex_cli/formatters/table_fmt.py`)

```python
from rich.table import Table

from spacex_cli.models.capsule import Capsule
from spacex_cli.models.launch import Launch
from spacex_cli.models.rocket import Rocket


def format_launches_table(launches: list[Launch]) -> Table:
    table = Table(title="🚀 SpaceX Launches", show_lines=True)
    table.add_column("Flight #", style="cyan", justify="right")
    table.add_column("Name", style="magenta")
    table.add_column("Date (UTC)", style="green")
    table.add_column("Success", justify="center")

    for la in launches:
        icon = "✅" if la.success else ("❌" if la.success is False else "⏳")
        table.add_row(
            str(la.flight_number),
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
```

#### 6.3 Panel Formatter (`src/spacex_cli/formatters/panel_fmt.py`)

```python
from rich.markdown import Markdown
from rich.panel import Panel

from spacex_cli.models.capsule import Capsule
from spacex_cli.models.company import CompanyInfo
from spacex_cli.models.launch import LaunchDetails
from spacex_cli.models.rocket import Rocket


def format_launch_panel(d: LaunchDetails) -> Panel:
    la = d.launch
    content = f"""
**Mission:** {la.name}
**Date (UTC):** {la.date_utc.strftime("%Y-%m-%d %H:%M")}
**Status:** {"✅ Success" if la.success else ("❌ Failure" if la.success is False else "⏳ Pending")}

**Payload:**
- Mass: {d.payload_mass_kg or "N/A"} kg / {d.payload_mass_lbs or "N/A"} lbs
- Orbit: {d.orbit or "N/A"}
- Customers: {", ".join(d.customers) if d.customers else "N/A"}

**Details:**
{la.details or "No details available."}

**Links:**
- Webcast: {la.links_webcast or "N/A"}
- Article: {la.links_article or "N/A"}
"""
    return Panel(Markdown(content), title="🚀 Launch Details", border_style="blue")


def format_rocket_panel(r: Rocket) -> Panel:
    content = f"""
**Name:** {r.name} | **Type:** {r.type}
**Active:** {"✅" if r.active else "❌"} | **Stages:** {r.stages} | **Boosters:** {r.boosters}
**Success Rate:** {r.success_rate_pct}% | **Cost/Launch:** ${r.cost_per_launch:,}
**First Flight:** {r.first_flight or "N/A"} | **Country:** {r.country}

**Dimensions:**
- Height: {r.height.get("meters", "N/A")} m
- Diameter: {r.diameter.get("meters", "N/A")} m
- Mass: {r.mass.get("kg", "N/A")} kg

**Description:**
{r.description}
"""
    return Panel(Markdown(content), title="🛰️ Rocket Specs", border_style="cyan")


def format_capsule_panel(c: Capsule) -> Panel:
    content = f"""
**Serial:** {c.serial} | **Type:** {c.type}
**Status:** {c.status}
**Reuse Count:** {c.reuse_count}
**Water Landings:** {c.water_landings} | **Land Landings:** {c.land_landings}

**Last Update:**
{c.last_update or "No updates available."}
"""
    return Panel(Markdown(content), title="🐉 Capsule Details", border_style="magenta")


def format_company_panel(c: CompanyInfo) -> Panel:
    content = f"""
**Company:** {c.name} | **Founded:** {c.founded} by {c.founder}
**Employees:** {c.employees:,} | **Valuation:** ${c.valuation:,}

**Leadership:** CEO {c.ceo} | CTO {c.cto} | COO {c.coo}

**Infrastructure:**
- Vehicles: {c.vehicles}
- Launch Sites: {c.launch_sites}
- Test Sites: {c.test_sites}

**HQ:** {c.headquarters.get("city", "")}, {c.headquarters.get("state", "")},
{c.headquarters.get("address", "")}

**Summary:**
{c.summary}
"""
    return Panel(Markdown(content), title="🏢 SpaceX Company Info", border_style="green")
```

#### 6.4 CSV Formatter (`src/spacex_cli/formatters/csv_fmt.py`)

```python
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
```

---

### Phase 7: Testing

**Цель:** покрытие кода тестами **> 60%** (настроено в pyproject.toml через `--cov-fail-under=60`).

#### 7.1 conftest.py (`tests/conftest.py`)

```python
import json
from pathlib import Path

import pytest
import responses as resp_lib

from spacex_cli.api.client import SpaceXClient

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def launches_data():
    return json.loads((FIXTURES / "launches_response.json").read_text())


@pytest.fixture
def rockets_data():
    return json.loads((FIXTURES / "rockets_response.json").read_text())


@pytest.fixture
def capsules_data():
    return json.loads((FIXTURES / "capsules_response.json").read_text())


@pytest.fixture
def company_data():
    return json.loads((FIXTURES / "company_response.json").read_text())
```

#### 7.2 Unit Tests

| Файл                      | Что тестируем                                                 |
|---------------------------|---------------------------------------------------------------|
| `test_models.py`          | Создание dataclass, корректность полей, frozen behaviour      |
| `test_pagination.py`      | `paginate()` возвращает правильное число объектов             |
| `test_formatters.py`      | JSON compact/pretty, заголовки таблиц, наличие панелей        |
| `test_launch_service.py`  | `_parse_launch`, `_parse_launch_details`, обработка None-полей |
| `test_cli_commands.py`    | Exit code 0 для базовых команд через `CliRunner`              |

#### 7.3 Integration Tests

```python
# tests/integration/test_launches_cmd.py
import responses
from typer.testing import CliRunner

from spacex_cli.cli import app

runner = CliRunner()
BASE = "https://api.spacexdata.com/v4"


@responses.activate
def test_list_launches_table(launches_data):
    responses.add(responses.GET, f"{BASE}/launches", json=launches_data)
    result = runner.invoke(app, ["launches", "list", "--limit", "2"])
    assert result.exit_code == 0


@responses.activate
def test_list_launches_json(launches_data):
    responses.add(responses.GET, f"{BASE}/launches", json=launches_data)
    result = runner.invoke(app, ["-o", "json", "launches", "list"])
    assert result.exit_code == 0


@responses.activate
def test_launch_info_not_found():
    responses.add(responses.GET, f"{BASE}/launches/bad-id", status=404)
    result = runner.invoke(app, ["launches", "info", "bad-id"])
    assert result.exit_code == 1
```

#### 7.4 Fixture Files

Минимальные JSON-фикстуры для offline-тестирования:

- `tests/fixtures/launches_response.json` — массив из 2 запусков
- `tests/fixtures/rockets_response.json` — массив из 2 ракет
- `tests/fixtures/capsules_response.json` — массив из 2 капсул
- `tests/fixtures/company_response.json` — объект компании

---

### Phase 8: Documentation & GitHub Publication

#### 8.1 README.md (корень репозитория)

Структура:

```markdown
# SpaceX Launch Tracker CLI

![CI](https://github.com/minaNabil96/spacex-cli/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## About
## REST API Used
## Installation
## Usage (all commands + examples)
## Output Formats
## Configuration (.env)
## Running Tests
## Project Structure
## AI Development Comparison → see comparison.md
```

#### 8.2 comparison.md

```markdown
# AI Tools Comparison Report

## 1. Introduction
## 2. Methodology
## 3. Development with ChatGPT
   - All prompts (with timestamps)
   - Problems encountered
   - Solutions found
## 4. Development with Claude
   - All prompts (with timestamps)
   - Problems encountered
   - Solutions found
## 5. Comparative Analysis

| Criterion            | ChatGPT | Claude |
|----------------------|---------|--------|
| Context understanding|         |        |
| Code quality         |         |        |
| Dialogue support     |         |        |
| Response speed       |         |        |
| Error handling       |         |        |
| Creativity           |         |        |
| Documentation        |         |        |

## 6. Conclusions & Recommendations
```

#### 8.3 GitHub Actions (`.github/workflows/ci.yml`)

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          cd version1
          pip install -e ".[dev]"
      - name: Lint
        run: ruff check version1/src/
      - name: Test
        run: |
          cd version1
          pytest
```

#### 8.4 docs/api_reference.md

Описание используемых SpaceX API endpoints:

```markdown
# Launch Library 2 API Reference (SpaceX Filtered)

Base URL: `https://lldev.thespacedevs.com/2.2.0`

| Endpoint             | Method | Description                   |
|----------------------|--------|-------------------------------|
| /launch              | GET    | All SpaceX launches           |
| /launch/upcoming     | GET    | Upcoming SpaceX launches      |
| /launch/previous     | GET    | Past SpaceX launches          |
| /launch/{id}         | GET    | Single launch details         |
| /config/launcher     | GET    | Rocket configurations         |
| /config/spacecraft   | GET    | Spacecraft (capsule) configs  |
| /agencies/121        | GET    | SpaceX agency info            |
```

#### 8.5 docs/prompts/

- `chatgpt_session.md` — полный лог диалога с ChatGPT (промпт → ответ → таймстамп)
- `claude_session.md` — полный лог диалога с Claude (промпт → ответ → таймстамп)

---

## 6. Verification & Build

```bash
# ── Клонировать и перейти в нужную версию ────────────────────────────────────
git clone https://github.com/minaNabil96/spacex-cli.git
cd spacex-cli/version1

# ── Установить в режиме разработки ───────────────────────────────────────────
pip install -e ".[dev]"

# ── Проверить установку ───────────────────────────────────────────────────────
spacex --help

# ── Линтинг ──────────────────────────────────────────────────────────────────
ruff check src/
ruff format src/

# ── Тесты с покрытием ────────────────────────────────────────────────────────
pytest                                        # запустит все тесты
pytest --cov=spacex_cli --cov-report=html    # HTML-отчёт → htmlcov/index.html
pytest tests/unit/                            # только unit
pytest tests/integration/                     # только integration

# ── Сборка дистрибутива ──────────────────────────────────────────────────────
pip install build
python -m build
pip install dist/spacex_cli-*.whl
```

---

## 7. Running the CLI

```bash
# ── Launches ─────────────────────────────────────────────────────────────────
spacex launches list                          # последние 10 запусков
spacex launches list --upcoming --limit 5     # 5 предстоящих
spacex launches list --past -o json           # прошедшие в JSON
spacex launches info 5eb87cd9ffd86e000604b32a # детали запуска
spacex launches countdown                     # живой обратный отсчёт

# ── Rockets ──────────────────────────────────────────────────────────────────
spacex rockets list                           # все ракеты
spacex rockets list -o json-pretty            # форматированный JSON
spacex rockets info falcon9                   # спецификации Falcon 9

# ── Capsules ─────────────────────────────────────────────────────────────────
spacex capsules list --limit 5
spacex capsules info C201

# ── Company ──────────────────────────────────────────────────────────────────
spacex company info
spacex company info -o json

# ── Export ───────────────────────────────────────────────────────────────────
spacex export launches --dest ./out.json --format json --limit 20
spacex export launches --dest ./out.csv  --format csv
spacex export launches --dest ./out.md   --format markdown

# ── Глобальные флаги ─────────────────────────────────────────────────────────
spacex --verbose launches list                # включить debug-лог
spacex -o json-pretty rockets list            # форматированный вывод
```

---

## 8. Pre-Submission Checklist

На основе чек-листа задания:

### Техническая часть (40%)
- [ ] CLI использует SpaceX REST API (внешний, публичный, v4)
- [ ] Обе версии (`version1/`, `version2/`) запускаются без ошибок
- [ ] Реализованы все 9 команд согласно ТЗ
- [ ] Код соответствует PEP 8 (проверено `ruff check`)
- [ ] Написаны unit-тесты, покрытие > 60%
- [ ] Обработка ошибок: NetworkError, NotFoundError, APIError → exit code 1
- [ ] Exit code 0 при успехе, 1 при ошибке API, 2 при неверных аргументах

### Процесс разработки (30%)
- [ ] Сохранены все промпты и ответы с таймстампами → `docs/prompts/`
- [ ] Зафиксировано время и количество итераций для каждой нейросети
- [ ] Отмечены проблемы и способы их решения

### Аналитическая часть (20%)
- [ ] `comparison.md` содержит таблицу по 8 критериям
- [ ] Даны конкретные выводы и рекомендации по промпт-инжинирингу
- [ ] Анализ объективен, подкреплён примерами кода

### Документация (10%)
- [ ] README содержит: описание API, установку, примеры всех команд
- [ ] Репозиторий: `version1/`, `version2/`, `docs/`, `comparison.md`
- [ ] Добавлены GitHub Actions badge, лицензия MIT, `.gitignore`
- [ ] `docs/api_reference.md` описывает все используемые endpoints

---

## Notes

| Пункт | Статус |
|-------|--------|
| REST API обязателен | ✅ Launch Library 2 API — все данные через HTTP |
| Минимум 7 команд | ✅ 9 команд реализовано |
| Typer: вложенные группы | ✅ launches / rockets / capsules / company / export |
| Typer: аргументы и опции | ✅ Argument + Option с типами и валидацией |
| Rich: таблицы | ✅ `format_launches/rockets/capsules_table()` |
| Rich: панели | ✅ `format_launch/rocket/capsule/company_panel()` |
| Rich: прогресс/Live | ✅ `countdown_to_launch()` через `rich.live.Live` |
| Type annotations | ✅ Все функции аннотированы |
| PEP 8 | ✅ ruff |
| UTF-8 | ✅ `ensure_ascii=False` во всех JSON-выводах |
| Параллельная разработка | ✅ version1/ + version2/ |
| Промпты сохранены | ✅ docs/prompts/ |
| Публикация на GitHub | ✅ Публичный репозиторий |
```