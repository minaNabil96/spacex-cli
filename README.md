# 🚀 Space Launch Tracker CLI — AI Comparison Study

![CI](https://github.com/minaNabil96/spacex-cli/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

University assignment comparing two AI coding assistants. The same CLI application — a **Space Launch Tracker** — was built independently by **Claude Opus 4.6 Thinking** and **Gemini 3.0 Flash**. Both versions track space launches from all providers via the **Launch Library 2 API** (`https://lldev.thespacedevs.com/2.2.0/`), filtered for SpaceX (Agency ID 121).

Results are compared analytically in [comparison.md](comparison.md).

## The Two Versions

| Aspect           | Claude Opus 4.6 Thinking     | Gemini 3.0 Flash              |
|------------------|------------------------------|-------------------------------|
| Directory        | `version1/`            | `version2/`             |
| Entry Point      | `spacex`                     | `spacex2`                     |
| Commands         | 10                            | 10                             |
| Test Coverage    | 88.73% (59 tests)           | 81.58% (22 tests)            |
| REST API         | Launch Library 2 API         | Launch Library 2 API          |

## Quick Start

### Claude Version
```bash
cd version1
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -e ".[dev]"
spacex --help
```

### Gemini Version
```bash
cd version2
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -e ".[dev]"
spacex2 --help
```

## Repository Structure

```
spacex-cli/
├── README.md                         # This file
├── comparison.md                     # Full comparison report (EN + RU)
├── conversations/
│   ├── ...claude.md                  # Claude development session log
│   └── ...gemini_flash.md            # Gemini development session log
├── version1/
│   ├── pyproject.toml
│   ├── README.md                     # Claude version docs (EN + RU)
│   ├── DEVELOPMENT_SESSION_LOG.md
│   ├── src/spacex_cli/              # Source code
│   └── tests/                       # Unit + Integration tests
├── version2/
│   ├── pyproject.toml
│   ├── README.md                     # Gemini version docs (EN + RU)
│   ├── src/spacex_cli/              # Source code
│   └── tests/                       # Unit + Integration tests
└── .github/workflows/
    └── ci.yml                        # CI for both versions
```

## Features

- **10 CLI commands** across 5 command groups (launches, rockets, capsules, company, export), plus an `exit` command
- **Rich terminal UI** with tables, panels, and live countdown timer
- **3 output formats**: table, JSON, JSON-pretty
- **3 export formats**: JSON, CSV, Markdown
- **Launch Library 2 API** integration with SpaceX filtering
- **Comprehensive error handling** with custom exception hierarchy
- **80%+ test coverage** in both versions

## Documentation

- [Claude Version README](version1/README.md)
- [Gemini Version README](version2/README.md)
- [AI Comparison Report](comparison.md)

## License

MIT

---

## 🇷🇺 РУССКАЯ ВЕРСИЯ / RUSSIAN VERSION

---

# 🚀 Трекер космических запусков CLI — Сравнение инструментов ИИ

![CI](https://github.com/minaNabil96/spacex-cli/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Обзор проекта

Университетское задание по сравнению двух ИИ-помощников для программирования. Одно и то же CLI-приложение — **Трекер космических запусков** — было создано независимо **Claude Opus 4.6 Thinking** и **Gemini 3.0 Flash**. Обе версии отслеживают космические запуски всех провайдеров через **Launch Library 2 API** (`https://lldev.thespacedevs.com/2.2.0/`), с фильтрацией для SpaceX (Agency ID 121).

Результаты аналитически сравниваются в [comparison.md](comparison.md).

## Две версии

| Аспект           | Claude Opus 4.6 Thinking     | Gemini 3.0 Flash              |
|------------------|------------------------------|-------------------------------|
| Директория       | `version1/`            | `version2/`             |
| Точка входа      | `spacex`                     | `spacex2`                     |
| Команды          | 10                            | 10                             |
| Покрытие тестов  | 88,73% (59 тестов)           | 81,58% (22 теста)             |
| REST API         | Launch Library 2 API         | Launch Library 2 API          |

## Быстрый старт

### Версия Claude
```bash
cd version1
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -e ".[dev]"
spacex --help
```

### Версия Gemini
```bash
cd version2
python -m venv .venv && source .venv/Scripts/activate  # Windows
pip install -e ".[dev]"
spacex2 --help
```

## Структура репозитория

```
spacex-cli/
├── README.md                         # Этот файл
├── comparison.md                     # Отчёт о сравнении (EN + RU)
├── conversations/
│   ├── ...claude.md                  # Журнал сессии разработки Claude
│   └── ...gemini_flash.md            # Журнал сессии разработки Gemini
├── version1/
│   ├── pyproject.toml
│   ├── README.md                     # Документация Claude (EN + RU)
│   ├── src/spacex_cli/              # Исходный код
│   └── tests/                       # Юнит- + интеграционные тесты
├── version2/
│   ├── pyproject.toml
│   ├── README.md                     # Документация Gemini (EN + RU)
│   ├── src/spacex_cli/              # Исходный код
│   └── tests/                       # Юнит- + интеграционные тесты
└── .github/workflows/
    └── ci.yml                        # CI для обеих версий
```

## Возможности

- **10 CLI-команд** в 5 командных группах (launches, rockets, capsules, company, export), плюс команда `exit`
- **Богатый терминальный UI** с таблицами, панелями и живым обратным отсчётом
- **3 формата вывода**: table, JSON, JSON-pretty
- **3 формата экспорта**: JSON, CSV, Markdown
- **Интеграция с Launch Library 2 API** с фильтрацией SpaceX
- **Комплексная обработка ошибок** с иерархией исключений
- **80%+ покрытие тестами** в обеих версиях

## Документация

- [README версии Claude](version1/README.md)
- [README версии Gemini](version2/README.md)
- [Отчёт о сравнении ИИ](comparison.md)

## Лицензия

MIT
