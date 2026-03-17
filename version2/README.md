# 🚀 Space Launch Tracker CLI (Gemini Version)

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AI](https://img.shields.io/badge/built%20by-Gemini%203.0%20Flash-purple)

## About

**Space Launch Tracker CLI** is a command-line tool for querying space launch data, rocket specifications, spacecraft configurations, and agency statistics. It was built entirely by **Gemini 3.0 Flash** (Antigravity) as part of a university study comparing AI-generated code.

The tool tracks space launches from **all providers** (SpaceX, NASA, Roscosmos, ESA, ISRO, and more) using the **Launch Library 2 API** by The Space Devs. By default, results are filtered to SpaceX launches (Agency ID 121).

**Key features:**
- 10 CLI commands across 5 command groups
- Rich terminal UI with tables, panels, and live countdown timer
- Multiple output formats (table, JSON, JSON-pretty)
- Export to JSON, CSV, and Markdown
- Custom exception hierarchy for error handling
- Russian-language docstrings on error classes

## REST API Used

| Property          | Value                                              |
|-------------------|----------------------------------------------------|
| **Name**          | Launch Library 2 API                               |
| **Provider**      | The Space Devs                                     |
| **Base URL (dev)**| `https://lldev.thespacedevs.com/2.2.0/`            |
| **Base URL (prod)**| `https://ll.thespacedevs.com/2.2.0/`              |
| **Authentication**| None required (anonymous: 15 req/hour; optional token for higher limits) |
| **Documentation** | https://ll.thespacedevs.com/docs/                  |

> **Note:** This project uses the development/staging server (`lldev.thespacedevs.com`) by default. For production use, update the base URL to `ll.thespacedevs.com/2.2.0/`.

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/minaNabil96/spacex-cli.git

# 2. Navigate to the Gemini version
cd spacex-cli/version2

# 3. Create a virtual environment (recommended)
python -m venv .venv
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate     # Linux/macOS

# 4. Install with development dependencies
pip install -e ".[dev]"

# 5. (Optional) Copy and configure environment
cp .env.example .env

# 6. Verify installation
spacex2 --help
```

## Configuration

| Variable           | Default                                        | Description                |
|--------------------|------------------------------------------------|----------------------------|
| `SPACEX_API_URL`   | `https://lldev.thespacedevs.com/2.2.0/`        | Launch Library 2 API base URL |
| `REQUEST_TIMEOUT`  | `30`                                           | HTTP request timeout (seconds) |

Configuration is loaded from a `.env` file via `python-dotenv`.

## Commands Reference

| Command                           | Flags                             | Description                        |
|-----------------------------------|-----------------------------------|------------------------------------|
| `spacex2 launches list`           | `--limit`, `--upcoming`, `--past` | List SpaceX launches               |
| `spacex2 launches info <id>`      |                                   | Detailed launch information        |
| `spacex2 launches countdown`      |                                   | Live countdown to next launch      |
| `spacex2 rockets list`            | `--limit`                         | List SpaceX launch vehicles        |
| `spacex2 rockets info <id>`       |                                   | Launcher specifications            |
| `spacex2 capsules list`           | `--limit`                         | List spacecraft configurations     |
| `spacex2 capsules info <id>`      |                                   | Spacecraft details                 |
| `spacex2 company info`            |                                   | SpaceX agency statistics           |
| `spacex2 export launches`         | `--dest`, `--format`, `--limit`   | Export launches to file            |
| `spacex2 exit`                    |                                   | Exit the SpaceX CLI                |

**Global options** (must come before the subcommand):

| Option             | Short | Description                      |
|--------------------|-------|----------------------------------|
| `--output`         | `-o`  | Output format: `table`, `json`, `json-pretty` |
| `--verbose`        | `-v`  | Enable verbose/debug logging     |

## Usage Examples

```bash
# List the 10 most recent SpaceX launches (default)
spacex2 launches list

# List 5 upcoming launches
spacex2 launches list --upcoming --limit 5

# List past launches (last 3)
spacex2 launches list --past --limit 3

# Get detailed info about a specific launch
spacex2 launches info "5fb40544-6569-42b6-b04b-32a1eb70d01a"

# Live countdown to the next SpaceX launch
spacex2 launches countdown

# List SpaceX rockets in table format
spacex2 rockets list

# Get rocket specifications by ID
spacex2 rockets info 164

# List spacecraft configurations
spacex2 capsules list --limit 5

# Get detailed spacecraft info
spacex2 capsules info 1

# View SpaceX company/agency statistics
spacex2 company info

# Output in JSON format
spacex2 -o json launches list --limit 3

# Output in pretty-printed JSON
spacex2 -o json-pretty company info

# Export launches to a JSON file
spacex2 export launches --dest ./launches.json --format json --limit 20

# Export launches to CSV
spacex2 export launches --dest ./launches.csv --format csv --limit 50

# Export launches to Markdown
spacex2 export launches --dest ./launches.md --format markdown --limit 10
```

## Output Formats

### Table (default)
Rich-formatted tables with emoji status indicators when `--output table` or no flag is used:
```
┌──────────┬──────────────────────────┬──────────────────┬─────────┐
│ ID       │ Name                     │ Date (UTC)       │ Success │
├──────────┼──────────────────────────┼──────────────────┼─────────┤
│ 5fb4054… │ Falcon 9 | Starlink G6-1 │ 2026-03-01 12:00 │ ✅      │
│ a1b2c3d… │ Falcon Heavy | GOES-U    │ 2026-02-28 09:30 │ ⏳      │
└──────────┴──────────────────────────┴──────────────────┴─────────┘
```

### JSON (`-o json`)
Compact JSON output on stdout for piping:
```json
[{"id":"5fb40544...","name":"Falcon 9 | Starlink","date_utc":"2026-03-01T12:00:00+00:00","success":true}]
```

### JSON Pretty (`-o json-pretty`)
Indented, human-readable JSON:
```json
[
  {
    "id": "5fb40544...",
    "name": "Falcon 9 | Starlink",
    "date_utc": "2026-03-01T12:00:00+00:00",
    "success": true
  }
]
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Verbose test output
pytest -v

# Generate HTML coverage report
pytest --cov=spacex_cli --cov-report=html

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Lint check
ruff check src/
```

## Project Structure

```
version2/
├── pyproject.toml
├── .env.example
├── README.md
├── src/
│   └── spacex_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── client.py          # SpaceXClient — HTTP wrapper
│       │   ├── endpoints.py       # Launch Library 2 endpoint constants
│       │   └── pagination.py      # Pagination helpers
│       ├── cli/
│       │   ├── __init__.py        # Typer app, OutputFormat, global state
│       │   ├── launches.py        # launches list/info/countdown
│       │   ├── rockets.py         # rockets list/info
│       │   ├── capsules.py        # capsules list/info
│       │   ├── company.py         # company info
│       │   └── export.py          # export launches
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py        # Environment config loader
│       ├── formatters/
│       │   ├── __init__.py
│       │   ├── table_fmt.py       # Rich Table formatters
│       │   ├── panel_fmt.py       # Rich Panel formatters
│       │   ├── json_fmt.py        # JSON output formatter
│       │   └── csv_fmt.py         # CSV export utility
│       ├── models/
│       │   ├── __init__.py
│       │   ├── launch.py          # Launch, LaunchDetails dataclasses
│       │   ├── rocket.py          # Rocket dataclass
│       │   ├── capsule.py         # Capsule dataclass
│       │   └── company.py         # CompanyInfo dataclass
│       ├── services/
│       │   ├── __init__.py
│       │   ├── launch_service.py  # Launch data fetching & parsing
│       │   ├── rocket_service.py  # Rocket data fetching & parsing
│       │   ├── capsule_service.py # Capsule data fetching & parsing
│       │   ├── company_service.py # Agency data fetching & parsing
│       │   └── export_service.py  # JSON/CSV/Markdown export logic
│       └── utils/
│           ├── __init__.py
│           ├── console.py         # Rich Console instances
│           ├── countdown.py       # Live countdown display
│           ├── errors.py          # Custom exception hierarchy (Russian docstrings)
│           └── logging.py         # Logging configuration
└── tests/
    ├── conftest.py                # Shared pytest fixtures
    ├── unit/
    │   ├── test_cli_commands.py
    │   ├── test_formatters.py
    │   ├── test_launch_service.py
    │   ├── test_models.py
    │   └── test_pagination.py
    └── integration/
        └── test_launches_cmd.py
```

---

## 🇷🇺 РУССКАЯ ВЕРСИЯ / RUSSIAN VERSION

---

# 🚀 Трекер космических запусков CLI (Версия Gemini)

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![AI](https://img.shields.io/badge/создан-Gemini%203.0%20Flash-purple)

## О проекте

**Space Launch Tracker CLI** — инструмент командной строки для получения данных о космических запусках, спецификаций ракет, конфигураций космических кораблей и статистики агентств. Проект полностью создан **Gemini 3.0 Flash** (Antigravity) в рамках университетского исследования по сравнению кода, сгенерированного ИИ.

Инструмент отслеживает космические запуски **всех провайдеров** (SpaceX, NASA, Роскосмос, ESA, ISRO и др.) через **Launch Library 2 API** от The Space Devs. По умолчанию результаты фильтруются для SpaceX (Agency ID 121).

**Основные возможности:**
- 10 CLI-команд в 5 командных группах
- Богатый терминальный UI с таблицами, панелями и живым обратным отсчётом
- Множественные форматы вывода (table, JSON, JSON-pretty)
- Экспорт в JSON, CSV и Markdown
- Иерархия пользовательских исключений для обработки ошибок
- Русскоязычные docstring-и в классах ошибок

## Используемый REST API

| Свойство              | Значение                                           |
|-----------------------|----------------------------------------------------|
| **Название**          | Launch Library 2 API                               |
| **Провайдер**         | The Space Devs                                     |
| **Базовый URL (dev)** | `https://lldev.thespacedevs.com/2.2.0/`            |
| **Базовый URL (prod)**| `https://ll.thespacedevs.com/2.2.0/`               |
| **Аутентификация**    | Не требуется (анонимно: 15 запросов/час; опциональный токен) |
| **Документация**      | https://ll.thespacedevs.com/docs/                  |

> **Примечание:** данный проект по умолчанию использует сервер разработки (`lldev.thespacedevs.com`). Для продакшена обновите базовый URL на `ll.thespacedevs.com/2.2.0/`.

## Установка

```bash
# 1. Клонирование репозитория
git clone https://github.com/minaNabil96/spacex-cli.git

# 2. Переход в директорию версии Gemini
cd spacex-cli/version2

# 3. Создание виртуального окружения (рекомендуется)
python -m venv .venv
source .venv/Scripts/activate   # Windows
# source .venv/bin/activate     # Linux/macOS

# 4. Установка с зависимостями для разработки
pip install -e ".[dev]"

# 5. (Опционально) Копирование и настройка окружения
cp .env.example .env

# 6. Проверка установки
spacex2 --help
```

## Конфигурация

| Переменная         | По умолчанию                                   | Описание                       |
|--------------------|------------------------------------------------|--------------------------------|
| `SPACEX_API_URL`   | `https://lldev.thespacedevs.com/2.2.0/`        | Базовый URL Launch Library 2 API |
| `REQUEST_TIMEOUT`  | `30`                                           | Тайм-аут HTTP-запроса (секунды) |

Конфигурация загружается из файла `.env` через `python-dotenv`.

## Справочник команд

| Команда                           | Флаги                             | Описание                         |
|-----------------------------------|-----------------------------------|----------------------------------|
| `spacex2 launches list`           | `--limit`, `--upcoming`, `--past` | Список запусков SpaceX           |
| `spacex2 launches info <id>`      |                                   | Подробная информация о запуске   |
| `spacex2 launches countdown`      |                                   | Живой обратный отсчёт до запуска |
| `spacex2 rockets list`            | `--limit`                         | Список ракет-носителей SpaceX    |
| `spacex2 rockets info <id>`       |                                   | Спецификации ракеты-носителя     |
| `spacex2 capsules list`           | `--limit`                         | Список конфигураций кораблей     |
| `spacex2 capsules info <id>`      |                                   | Подробности о корабле            |
| `spacex2 company info`            |                                   | Статистика агентства SpaceX      |
| `spacex2 export launches`         | `--dest`, `--format`, `--limit`   | Экспорт запусков в файл          |
| `spacex2 exit`                    |                                   | Выход из SpaceX CLI              |

**Глобальные опции** (указываются перед подкомандой):

| Опция              | Кратко | Описание                           |
|--------------------|--------|------------------------------------|
| `--output`         | `-o`   | Формат вывода: `table`, `json`, `json-pretty` |
| `--verbose`        | `-v`   | Включить подробное логирование     |

## Примеры использования

```bash
# Список 10 последних запусков SpaceX (по умолчанию)
spacex2 launches list

# Список 5 предстоящих запусков
spacex2 launches list --upcoming --limit 5

# Список прошлых запусков (последние 3)
spacex2 launches list --past --limit 3

# Подробная информация о конкретном запуске
spacex2 launches info "5fb40544-6569-42b6-b04b-32a1eb70d01a"

# Живой обратный отсчёт до следующего запуска SpaceX
spacex2 launches countdown

# Список ракет SpaceX в табличном формате
spacex2 rockets list

# Спецификации ракеты по ID
spacex2 rockets info 164

# Список конфигураций космических кораблей
spacex2 capsules list --limit 5

# Подробная информация о космическом корабле
spacex2 capsules info 1

# Статистика агентства SpaceX
spacex2 company info

# Вывод в формате JSON
spacex2 -o json launches list --limit 3

# Вывод в форматированном JSON
spacex2 -o json-pretty company info

# Экспорт запусков в JSON-файл
spacex2 export launches --dest ./launches.json --format json --limit 20

# Экспорт запусков в CSV
spacex2 export launches --dest ./launches.csv --format csv --limit 50

# Экспорт запусков в Markdown
spacex2 export launches --dest ./launches.md --format markdown --limit 10
```

## Форматы вывода

### Таблица (по умолчанию)
Форматированные Rich-таблицы с эмодзи-статусами при `--output table` или без флага:
```
┌──────────┬──────────────────────────┬──────────────────┬─────────┐
│ ID       │ Name                     │ Date (UTC)       │ Success │
├──────────┼──────────────────────────┼──────────────────┼─────────┤
│ 5fb4054… │ Falcon 9 | Starlink G6-1 │ 2026-03-01 12:00 │ ✅      │
│ a1b2c3d… │ Falcon Heavy | GOES-U    │ 2026-02-28 09:30 │ ⏳      │
└──────────┴──────────────────────────┴──────────────────┴─────────┘
```

### JSON (`-o json`)
Компактный JSON на stdout для перенаправления:
```json
[{"id":"5fb40544...","name":"Falcon 9 | Starlink","date_utc":"2026-03-01T12:00:00+00:00","success":true}]
```

### JSON Pretty (`-o json-pretty`)
Форматированный, читаемый JSON:
```json
[
  {
    "id": "5fb40544...",
    "name": "Falcon 9 | Starlink",
    "date_utc": "2026-03-01T12:00:00+00:00",
    "success": true
  }
]
```

## Запуск тестов

```bash
# Запуск всех тестов с покрытием
pytest

# Расширенный вывод тестов
pytest -v

# Генерация HTML-отчёта о покрытии
pytest --cov=spacex_cli --cov-report=html

# Запуск только модульных тестов
pytest tests/unit/

# Запуск только интеграционных тестов
pytest tests/integration/

# Проверка линтером
ruff check src/
```

## Структура проекта

```
version2/
├── pyproject.toml
├── .env.example
├── README.md
├── src/
│   └── spacex_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── api/
│       │   ├── client.py          # SpaceXClient — HTTP-обёртка
│       │   ├── endpoints.py       # Константы эндпоинтов Launch Library 2
│       │   └── pagination.py      # Помощники пагинации
│       ├── cli/
│       │   ├── __init__.py        # Приложение Typer, OutputFormat, глобальное состояние
│       │   ├── launches.py        # launches list/info/countdown
│       │   ├── rockets.py         # rockets list/info
│       │   ├── capsules.py        # capsules list/info
│       │   ├── company.py         # company info
│       │   └── export.py          # export launches
│       ├── config/
│       │   └── settings.py        # Загрузчик конфигурации окружения
│       ├── formatters/
│       │   ├── table_fmt.py       # Форматирование Rich-таблиц
│       │   ├── panel_fmt.py       # Форматирование Rich-панелей
│       │   ├── json_fmt.py        # Форматирование JSON-вывода
│       │   └── csv_fmt.py         # Утилита экспорта CSV
│       ├── models/
│       │   ├── launch.py          # Датаклассы Launch, LaunchDetails
│       │   ├── rocket.py          # Датакласс Rocket
│       │   ├── capsule.py         # Датакласс Capsule
│       │   └── company.py         # Датакласс CompanyInfo
│       ├── services/
│       │   ├── launch_service.py  # Получение и парсинг данных о запусках
│       │   ├── rocket_service.py  # Получение и парсинг данных о ракетах
│       │   ├── capsule_service.py # Получение и парсинг данных о кораблях
│       │   ├── company_service.py # Получение и парсинг данных об агентстве
│       │   └── export_service.py  # Логика экспорта JSON/CSV/Markdown
│       └── utils/
│           ├── console.py         # Экземпляры Rich Console
│           ├── countdown.py       # Живой обратный отсчёт
│           ├── errors.py          # Иерархия исключений (docstring на русском)
│           └── logging.py         # Конфигурация логирования
└── tests/
    ├── conftest.py                # Общие фикстуры pytest
    ├── unit/
    │   ├── test_cli_commands.py
    │   ├── test_formatters.py
    │   ├── test_launch_service.py
    │   ├── test_models.py
    │   └── test_pagination.py
    └── integration/
        └── test_launches_cmd.py
```
