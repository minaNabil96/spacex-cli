# Technical Specification (TZ)
# Space Launch Tracker CLI — SpaceX Launch Intelligence
# Версия / Version: 1.0

---

## Table of Contents / Содержание

1. [Overview / Обзор](#1-overview--обзор)
2. [Global Options / Глобальные опции](#2-global-options--глобальные-опции)
3. [Command Group: launches / launches](#3-command-group-launches--группа-команд-launches)
   - [launches list](#31-launches-list)
   - [launches info](#32-launches-info)
   - [launches countdown](#33-launches-countdown)
4. [Command Group: rockets / rockets](#4-command-group-rockets--группа-команд-rockets)
   - [rockets list](#41-rockets-list)
   - [rockets info](#42-rockets-info)
5. [Command Group: capsules / capsules](#5-command-group-capsules--группа-команд-capsules)
   - [capsules list](#51-capsules-list)
   - [capsules info](#52-capsules-info)
6. [Command Group: company / company](#6-command-group-company--группа-команд-company)
   - [company info](#61-company-info)
7. [Command Group: export / export](#7-command-group-export--группа-команд-export)
   - [export launches](#71-export-launches)
8. [Command: exit / exit](#8-command-exit--команда-exit)
9. [REST API Endpoints / Эндпоинты REST API](#9-rest-api-endpoints--эндпоинты-rest-api)
10. [Technical Requirements / Технические требования](#10-technical-requirements--технические-требования)
    - [10.1 Libraries / Библиотеки](#101-libraries--библиотеки)
    - [10.2 Project Structure / Структура проекта](#102-project-structure--структура-проекта)
    - [10.3 Error Handling / Обработка ошибок](#103-error-handling--обработка-ошибок)
    - [10.4 Configuration / Конфигурация](#104-configuration--конфигурация)
    - [10.5 Logging / Логирование](#105-logging--логирование)
    - [10.6 Testing / Тестирование](#106-testing--тестирование)
11. [Appendix: Exit Codes / Приложение: коды завершения](#appendix-exit-codes--приложение-коды-завершения)

---

## 1. Overview / Обзор

The **Space Launch Tracker CLI** is a command-line utility for querying real-time space launch data, rocket specifications, spacecraft configurations, and company statistics directly from the terminal. It integrates with the **Launch Library 2 API** by The Space Devs (`https://lldev.thespacedevs.com/2.2.0/`), automatically filtered for SpaceX launches (Launch Service Provider ID: 121).

The CLI supports three output formats (table, JSON, pretty JSON) and three export formats (JSON, CSV, Markdown). Output formatting is handled by the Rich library, which provides rich, colored terminal tables and panels.

**Трекер космических запусков CLI** — утилита командной строки для получения актуальных данных о космических запусках, характеристиках ракет, конфигурациях космических аппаратов и статистике компании непосредственно из терминала. Она интегрируется с **Launch Library 2 API** от The Space Devs (`https://lldev.thespacedevs.com/2.2.0/`), автоматически фильтруя данные по запускам SpaceX (ID поставщика услуг запуска: 121).

CLI поддерживает три формата вывода (таблица, JSON, форматированный JSON) и три формата экспорта (JSON, CSV, Markdown). Форматирование вывода выполняется библиотекой Rich, которая обеспечивает цветные таблицы и панели в терминале.

### Version / Версия

| Version / Версия | Directory / Директория | Entry Point / Точка входа |
|-----------------|------------------------|--------------------------|
| Claude Opus 4.6 Thinking | `version1/` | `spacex` |
| Gemini 3.0 Flash | `version2/` | `spacex2` |

---

## 2. Global Options / Глобальные опции

Global options must precede the subcommand. They are defined in the main Typer callback and apply to all commands.

Глобальные опции должны предшествовать подкоманде. Они определены в основном callback Typer и применяются ко всем командам.

| Option / Опция | Short / Кратко | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|---|
| `--output` | `-o` | `OutputFormat` (enum: `table`, `json`, `json-pretty`) | `table` | No / Нет | Output format for results. Default: table output to stderr. JSON formats are written to stdout. / Формат вывода результатов. По умолчанию: таблица в stderr. JSON-форматы записываются в stdout. |
| `--verbose` | `-v` | `bool` | `False` | No / Нет | Enable verbose (DEBUG level) logging. / Включить подробное логирование (уровень DEBUG). |

### OutputFormat enum values / Значения enum OutputFormat

| Value / Значение | Description / Описание |
|---|---|
| `table` | Rich-colored table output to stderr (default). Colored output does not interfere with stdout piping. / Цветная таблица в stderr (по умолчанию). Цветной вывод не мешает перенаправлению stdout. |
| `json` | Compact single-line JSON to stdout. / Компактный JSON в одну строку в stdout. |
| `json-pretty` | Indented, human-readable JSON to stdout. / Отформатированный JSON в stdout. |

---

## 3. Command Group: launches / launches

**Description / Описание:** Group of commands for querying SpaceX launch data. All launches are filtered by Launch Service Provider ID 121 (SpaceX). / Группа команд для запроса данных о запусках SpaceX. Все запуски фильтруются по ID поставщика услуг запуска 121 (SpaceX).

**Subcommands / Подкоманды:** `list`, `info`, `countdown`

---

### 3.1 launches list

**Команда / Command:** `launches list`

**Описание / Description:** Lists SpaceX launches with optional filtering by launch status (upcoming or past). Returns a table or JSON with launch name, date, flight number, and success status. / Выводит список запусков SpaceX с дополнительной фильтрацией по статусу (предстоящие или прошедшие). Возвращает таблицу или JSON с названием запуска, датой, номером рейса и статусом успеха.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Short / Кратко | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|---|
| `--limit` | `-l` | `int` | `10` | No / Нет | Maximum number of launch records to return. / Максимальное количество записей о запусках для возврата. |
| `--upcoming` | — | `bool` | `False` | No / Нет | If set, return only upcoming launches. Cannot be combined with `--past`. / Если установлено, возвращать только предстоящие запуски. Несовместимо с `--past`. |
| `--past` | — | `bool` | `False` | No / Нет | If set, return only past launches. Cannot be combined with `--upcoming`. / Если установлено, возвращать только прошедшие запуски. Несовместимо с `--upcoming`. |

**Example / Пример:**
```bash
# Default: list 10 most recent launches
$ spacex launches list
# Default / По умолчанию: список 10 последних запусков

# List 5 upcoming launches in JSON format
$ spacex -o json launches list --upcoming --limit 5
# Список 5 предстоящих запусков в формате JSON

# List 20 past launches
$ spacex launches list --past --limit 20
# Список 20 прошедших запусков
```

**Expected Output / Ожидаемый результат:**

*Table format (default) / Табличный формат (по умолчанию):*
```
🚀 SpaceX Launches
╭════════════╬═════════════════════════════╬══════════════════╬═══════════╮
║ Flight #  ║ Name                         ║ Date (UTC)       ║ Success  ║
╠════════════╬═════════════════════════════╬══════════════════╬═══════════╡
║     123   ║ Starlink Group 6-1          ║ 2026-03-19 12:00 ║ ⏳       ║
║     122   ║ Crew-10                      ║ 2026-03-15 08:30 ║ ⏳       ║
║     121   ║ Starlink 5-12               ║ 2026-03-10 14:22 ║ ✅       ║
╚════════════╩═════════════════════════════╩══════════════════╩═══════════╝
```

*JSON format / Формат JSON:*
```json
[{"id":"...","name":"Starlink Group 6-1","date_utc":"2026-03-19T12:00:00Z","success":null,"flight_number":123,...}]
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/launch/
Parameters:
  limit     = <int>    (required, default 10)
  lsp__id   = 121      (always sent, SpaceX filter)
  upcoming  = true     (sent only if --upcoming flag is set)
  past      = true     (sent only if --past flag is set)
```

---

### 3.2 launches info

**Команда / Command:** `launches info <launch_id>`

**Описание / Description:** Retrieves detailed information about a specific launch by its ID. Returns a Rich panel with mission name, date, status, payload details (mass, orbit, customers), mission description, and links to webcast and articles. / Получает подробную информацию о конкретном запуске по его ID. Возвращает Rich-панель с названием миссии, датой, статусом, деталями полезной нагрузки (масса, орбита, клиенты), описанием миссии и ссылками на вебкаст и статьи.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|
| `<launch_id>` | `str` | — | **Yes / Да** | Unique identifier of the launch (UUID format, e.g., `5eb87cd9ffd86e000604b32a`). / Уникальный идентификатор запуска (формат UUID, например `5eb87cd9ffd86e000604b32a`). |

**Example / Пример:**
```bash
$ spacex launches info 5eb87cd9ffd86e000604b32a
$ spacex -o json-pretty launches info 5eb87cd9ffd86e000604b32a
```

**Expected Output / Ожидаемый результат:**

*Table format (Rich Panel) / Табличный формат (Rich-панель):*
```
╔══════════════════════════════════════════════════════════════════════════╗
║                        🚀 Launch Details                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║ **Mission:** Crew-10                                                     ║
║ **Date (UTC):** 2026-03-15 08:30                                        ║
║ **Status:** ⏳ Pending                                                   ║
║                                                                          ║
║ **Payload:**                                                              ║
║ - Mass: 12,570 kg / 27,710 lbs                                           ║
║ - Orbit: ISS (International Space Station)                              ║
║ - Customers: NASA                                                       ║
║                                                                          ║
║ **Details:**                                                              ║
║ SpaceX's tenth operational Commercial Crew mission to the ISS...          ║
║                                                                          ║
║ **Links:**                                                                ║
║ - Webcast: https://www.youtube.com/watch?v=...                           ║
║ - Article: https://www.nasa.gov/...                                      ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/launch/<launch_id>/
Parameters: (none besides path parameter)
```

---

### 3.3 launches countdown

**Команда / Command:** `launches countdown`

**Описание / Description:** Displays a live countdown timer to the next upcoming SpaceX launch. The countdown updates every second using Rich's Live display widget. The command blocks until the target time is reached and then prints "🚀 Launch time!" / Отображает живой таймер обратного отсчёта до следующего предстоящего запуска SpaceX. Обратный отсчёт обновляется каждую секунду с использованием виджета Live библиотеки Rich. Команда блокируется до достижения целевого времени, затем выводит "🚀 Launch time!".

**Arguments and Options / Аргументы и опции:** None / Нет.

**Example / Пример:**
```bash
$ spacex launches countdown
Next Mission: Starlink Group 6-1
⏳ T-00:45:23
⏳ T-00:45:22
⏳ T-00:45:21
...
🚀 Launch time!
```

**Expected Output / Ожидаемый результат:**
Line 1: Bold blue "Next Mission:" label followed by mission name.
Lines 2+: Live-updating line showing countdown in `T-HH:MM:SS` format (bold yellow), or "🚀 Launch time!" (bold green) when countdown reaches zero. / Строка 1: Жирная синяя метка "Next Mission:" с названием миссии.
Строки 2+: Обновляемая строка с обратным отсчётом в формате `T-HH:MM:SS` (жирный жёлтый) или "🚀 Launch time!" (жирный зелёный) при достижении нуля.

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/launch/upcoming/
Parameters:
  limit   = 1
  lsp__id = 121
  ordering = net
```

---

## 4. Command Group: rockets / rockets

**Description / Описание:** Group of commands for querying SpaceX rocket/launch vehicle configurations. / Группа команд для запроса конфигураций ракет-носителей SpaceX.

**Subcommands / Подкоманды:** `list`, `info`

---

### 4.1 rockets list

**Команда / Command:** `rockets list`

**Описание / Description:** Lists SpaceX rocket configurations. Returns a table or JSON with rocket name, active status, number of stages, success rate percentage, and first flight date. / Выводит список конфигураций ракет SpaceX. Возвращает таблицу или JSON с названием ракеты, статусом активности, количеством ступеней, процентом успешных запусков и датой первого полёта.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Short / Кратко | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|---|
| `--limit` | `-l` | `int` | `10` | No / Нет | Maximum number of rocket records to return. / Максимальное количество записей о ракетах для возврата. |

**Example / Пример:**
```bash
$ spacex rockets list
$ spacex -o json rockets list --limit 5
$ spacex rockets list -l 3 -o json-pretty
```

**Expected Output / Ожидаемый результат:**

*Table format / Табличный формат:*
```
🛰️ SpaceX Rockets
╭═══════════════╬════════════════╬════════╬════════════╬════════════════╮
║ Name          ║ Active        ║ Stages ║ Success %   ║ First Flight  ║
╠═══════════════╬════════════════╬════════╬════════════╬════════════════╡
║ Falcon 9      ║ ✅             ║ 2      ║ 98.9%       ║ 2010-06-04    ║
║ Falcon Heavy  ║ ✅             ║ 3      ║ 100%        ║ 2018-02-06    ║
║ Starship      ║ ✅             ║ 2      ║ 50%         ║ 2023-04-20    ║
╚═══════════════╩════════════════╩════════╩════════════╩════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/config/launcher/
Parameters:
  limit         = <int>  (required, default 10)
  manufacturer__id = 121  (always sent, SpaceX filter)
```

---

### 4.2 rockets info

**Команда / Command:** `rockets info <rocket_id>`

**Описание / Description:** Retrieves detailed specifications of a specific rocket configuration by its ID. Returns a Rich panel with full name, type, active status, stages, boosters, cost per launch, success rate, first flight date, country, dimensions (height, diameter, mass), and description. / Получает подробные характеристики конкретной конфигурации ракеты по её ID. Возвращает Rich-панель с полным названием, типом, статусом активности, ступенями, ускорителями, стоимостью запуска, процентом успешных запусков, датой первого полёта, страной, размерами (высота, диаметр, масса) и описанием.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|
| `<rocket_id>` | `str` | — | **Yes / Да** | Unique identifier of the rocket configuration (e.g., `falcon9`, `falconheavy`, `starship`). / Уникальный идентификатор конфигурации ракеты (например, `falcon9`, `falconheavy`, `starship`). |

**Example / Пример:**
```bash
$ spacex rockets info falcon9
$ spacex -o json rockets info starship
```

**Expected Output / Ожидаемый результат:**

*Table format (Rich Panel) / Табличный формат (Rich-панель):*
```
╔══════════════════════════════════════════════════════════════════════════╗
║                        🛰️ Rocket Specs                                    ║
╠══════════════════════════════════════════════════════════════════════════╣
║ **Name:** Falcon 9 Block 5 | **Type:** rocket                            ║
║ **Active:** ✅ | **Stages:** 2 | **Boosters:** 1                          ║
║ **Success Rate:** 98.9% | **Cost/Launch:** $67,000,000                    ║
║ **First Flight:** 2010-06-04 | **Country:** United States                 ║
║                                                                          ║
║ **Dimensions:**                                                          ║
║ - Height: 70.0 m                                                         ║
║ - Diameter: 3.7 m                                                        ║
║ - Mass: 549,054 kg                                                       ║
║                                                                          ║
║ **Description:**                                                         ║
║ Falcon 9 is a reusable, two-stage rocket...                              ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/config/launcher/<rocket_id>/
Parameters: (none besides path parameter)
```

---

## 5. Command Group: capsules / capsules

**Description / Описание:** Group of commands for querying SpaceX spacecraft (Dragon capsule) configurations. / Группа команд для запроса конфигураций космических аппаратов (капсул Dragon) компании SpaceX.

**Subcommands / Подкоманды:** `list`, `info`

---

### 5.1 capsules list

**Команда / Command:** `capsules list`

**Описание / Description:** Lists SpaceX spacecraft (Dragon capsule) configurations. Returns a table or JSON with serial number, status, type, reuse count, and number of water landings. / Выводит список конфигураций космических аппаратов SpaceX (капсул Dragon). Возвращает таблицу или JSON с серийным номером, статусом, типом, количеством использований и количеством приводнений.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Short / Кратко | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|---|
| `--limit` | `-l` | `int` | `10` | No / Нет | Maximum number of capsule records to return. / Максимальное количество записей о капсулах для возврата. |

**Example / Пример:**
```bash
$ spacex capsules list
$ spacex -o json capsules list --limit 5
```

**Expected Output / Ожидаемый результат:**

*Table format / Табличный формат:*
```
🐉 Dragon Capsules
╭══════════╦═══════════════════╦═══════════════════╦══════════════╦═════════════════╮
║ Serial   ║ Status            ║ Type              ║ Reuse Count  ║ Water Landings  ║
╠══════════╬═══════════════════╬═══════════════════╬══════════════╬═════════════════╡
║ C212     ║ active            ║ Dragon 2.0        ║ 4            ║ 4               ║
║ C210     ║ retired           ║ Dragon 2.0        ║ 6            ║ 6               ║
║ C106     ║ active            ║ Dragon 2.0        ║ 3            ║ 3               ║
╚══════════╩═══════════════════╩═══════════════════╩══════════════╩═════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/config/spacecraft/
Parameters:
  limit           = <int>  (required, default 10)
  manufacturer__id = 121   (always sent, SpaceX filter)
```

---

### 5.2 capsules info

**Команда / Command:** `capsules info <capsule_id>`

**Описание / Description:** Retrieves detailed information about a specific spacecraft configuration by its ID. Returns a Rich panel with serial number, type, status, reuse count, water and land landings, last update, and associated launches. / Получает подробную информацию о конкретной конфигурации космического аппарата по её ID. Возвращает Rich-панель с серийным номером, типом, статусом, количеством использований, приводнениями и посадками на сушу, последним обновлением и связанными запусками.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|
| `<capsule_id>` | `str` | — | **Yes / Да** | Unique identifier of the spacecraft configuration (e.g., `dragon-v2`). / Уникальный идентификатор конфигурации космического аппарата (например, `dragon-v2`). |

**Example / Пример:**
```bash
$ spacex capsules info dragon-v2
$ spacex -o json-pretty capsules info dragon-v2
```

**Expected Output / Ожидаемый результат:**

*Table format (Rich Panel) / Табличный формат (Rich-панель):*
```
╔══════════════════════════════════════════════════════════════════════════╗
║                        🐉 Capsule Details                                  ║
╠══════════════════════════════════════════════════════════════════════════╣
║ **Serial:** C212 | **Type:** Dragon 2.0                                     ║
║ **Status:** active                                                         ║
║ **Reuse Count:** 4                                                         ║
║ **Water Landings:** 4 | **Land Landings:** 0                               ║
║                                                                          ║
║ **Last Update:**                                                           ║
║ Capsule completed its fourth mission, returning from the ISS...           ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/config/spacecraft/<capsule_id>/
Parameters: (none besides path parameter)
```

---

## 6. Command Group: company / company

**Description / Описание:** Group of commands for querying SpaceX company/agency information. / Группа команд для запроса информации о компании SpaceX / агентстве.

**Subcommands / Подкоманды:** `info`

---

### 6.1 company info

**Команда / Command:** `company info`

**Описание / Description:** Retrieves SpaceX company statistics and general information. Returns a Rich panel with company name, founder, founding year, number of employees, vehicles, launch sites, test sites, CEO/CTO/COO, valuation, headquarters address, summary, and links. / Получает статистику и общую информацию о компании SpaceX. Возвращает Rich-панель с названием компании, основателем, годом основания, количеством сотрудников, транспортных средств, стартовых площадок, испытательных площадок, CEO/CTO/COO, оценкой стоимости, адресом штаб-квартиры, резюме и ссылками.

**Arguments and Options / Аргументы и опции:** None / Нет.

**Example / Пример:**
```bash
$ spacex company info
$ spacex -o json company info
```

**Expected Output / Ожидаемый результат:**

*Table format (Rich Panel) / Табличный формат (Rich-панель):*
```
╔══════════════════════════════════════════════════════════════════════════╗
║                        🏢 SpaceX Company Info                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║ **Company:** SpaceX | **Founded:** 2002 by Elon Musk                      ║
║ **Employees:** 13,000 | **Valuation:** $350,000,000,000                   ║
║                                                                          ║
║ **Leadership:** CEO Elon Musk | CTO Elon Musk | COO Gwynne Shotwell      ║
║                                                                          ║
║ **Infrastructure:**                                                       ║
║ - Vehicles: 3                                                            ║
║ - Launch Sites: 4                                                        ║
║ - Test Sites: 3                                                           ║
║                                                                          ║
║ **HQ:** Hawthorne, California, 1 Rocket Road                              ║
║                                                                          ║
║ **Summary:**                                                              ║
║ SpaceX designs, manufactures and launches advanced rockets and spacecraft ║
╚══════════════════════════════════════════════════════════════════════════╝
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/agencies/121/
Parameters: (none)
```

---

## 7. Command Group: export / export

**Description / Описание:** Group of commands for exporting SpaceX data to files. / Группа команд для экспорта данных SpaceX в файлы.

**Subcommands / Подкоманды:** `launches`

---

### 7.1 export launches

**Команда / Command:** `export launches`

**Описание / Description:** Exports SpaceX launch data to a file in the specified format. Supports JSON (formatted with indentation), CSV (with headers), and Markdown (JSON embedded in a fenced code block under a heading). After successful export, prints a green confirmation message with the file path and number of records exported. / Экспортирует данные о запусках SpaceX в файл в указанном формате. Поддерживает JSON (с отступами), CSV (с заголовками) и Markdown (JSON в блоке кода под заголовком). После успешного экспорта выводит зелёное подтверждение с путём к файлу и количеством экспортированных записей.

**Arguments and Options / Аргументы и опции:**

| Argument / Option | Short / Кратко | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|---|
| `--dest` | `-d` | `Path` | `./launches_export.json` | No / Нет | Destination file path. The file extension does not need to match the format; the `--format` option determines the serialization method. / Путь к файлу назначения. Расширение файла не обязательно должно соответствовать формату; формат сериализации определяется опцией `--format`. |
| `--format` | `-f` | `str` | `json` | No / Нет | Export format. Allowed values: `json`, `csv`, `markdown`. If an unknown value is provided, the command prints an error and exits with code 2. / Формат экспорта. Допустимые значения: `json`, `csv`, `markdown`. Если указано неизвестное значение, команда выводит ошибку и завершается с кодом 2. |
| `--limit` | `-l` | `int` | `10` | No / Нет | Number of launch records to fetch and export. / Количество записей о запусках для получения и экспорта. |

**Example / Пример:**
```bash
# Export 10 launches to JSON (default)
$ spacex export launches
# Exports: 10 records → ./launches_export.json

# Export 20 launches to CSV
$ spacex export launches --format csv --dest ./my_launches.csv --limit 20
# Exports: 20 records → ./my_launches.csv

# Export 5 upcoming launches to Markdown
$ spacex export launches --format markdown --dest ./report.md --limit 5
# Exports: 5 records → ./report.md

# Export in pretty JSON format
$ spacex export launches --format json --dest ./launches.json
# Exports: 10 records → ./launches.json
```

**Expected Output / Ожидаемый результат:**

*Success message (always printed to stderr) / Сообщение об успехе (всегда выводится в stderr):*
```
✓ Exported 10 records → ./launches_export.json
```

*JSON file content example / Пример содержимого JSON-файла:*
```json
[
  {
    "id": "5eb87cd9-...",
    "name": "Starlink Group 6-1",
    "date_utc": "2026-03-19T12:00:00Z",
    "success": null,
    "flight_number": 123,
    "details": "...",
    "links_webcast": "...",
    "links_article": "..."
  }
]
```

*CSV file content example / Пример содержимого CSV-файла:*
```csv
id,name,date_utc,success,flight_number,details,links_webcast,links_article
5eb87cd9-...,Starlink Group 6-1,2026-03-19T12:00:00Z,,123,...
```

*Markdown file content example / Пример содержимого Markdown-файла:*
```markdown
# SpaceX Launches

```json
[
  {
    "id": "5eb87cd9-...",
    "name": "Starlink Group 6-1",
    ...
  }
]
```
```

**Used API Endpoint / Используемый эндпоинт API:**
```
GET https://lldev.thespacedevs.com/2.2.0/launch/
Parameters:
  limit     = <int>   (required, default 10)
  lsp__id   = 121     (always sent, SpaceX filter)
```

---

## 8. Command: exit / exit

**Команда / Command:** `exit`

**Описание / Description:** Exits the SpaceX CLI gracefully. Prints a goodbye message to the console and terminates the process with exit code 0. Can be invoked at any point in the interactive session. / Завершает работу SpaceX CLI корректно. Выводит прощальное сообщение в консоль и завершает процесс с кодом выхода 0. Может быть вызвана в любой момент интерактивной сессии.

**Arguments and Options / Аргументы и опции:** None / Нет.

**Example / Пример:**
```bash
$ spacex exit
```

**Expected Output / Ожидаемый результа:**
```
👋 Goodbye! Thanks for using SpaceX CLI.
```
Process terminates with exit code 0. / Процесс завершается с кодом выхода 0.

---

## 9. REST API Endpoints / Эндпоинты REST API

### 9.1 API Overview / Обзор API

| Property / Свойство | Value / Значение |
|---|---|
| **API Name / Название** | Launch Library 2 API |
| **Provider / Провайдер** | The Space Devs |
| **Base URL (dev)** | `https://lldev.thespacedevs.com/2.2.0/` |
| **Base URL (prod)** | `https://ll.thespacedevs.com/2.2.0/` |
| **Authentication / Аутентификация** | None required (anonymous: 15 req/hour; with token: higher) / Не требуется (анонимно: 15 запросов/час; с токеном: больше) |
| **Documentation** | `https://ll.thespacedevs.com/docs/` |

### 9.2 Complete Endpoint Mapping / Полная карта эндпоинтов

| CLI Command / Команда CLI | HTTP Method / Метод | Full URL / Полный URL | Query Parameters / Параметры запроса |
|---|---|---|---|
| `launches list` | `GET` | `https://lldev.thespacedevs.com/2.2.0/launch/` | `limit` (int), `lsp__id=121` (fixed), `upcoming=true` (optional), `past=true` (optional) |
| `launches info <id>` | `GET` | `https://lldev.thespacedevs.com/2.2.0/launch/{id}/` | — |
| `launches countdown` | `GET` | `https://lldev.thespacedevs.com/2.2.0/launch/upcoming/` | `limit=1`, `lsp__id=121`, `ordering=net` |
| `rockets list` | `GET` | `https://lldev.thespacedevs.com/2.2.0/config/launcher/` | `limit` (int), `manufacturer__id=121` (fixed) |
| `rockets info <id>` | `GET` | `https://lldev.thespacedevs.com/2.2.0/config/launcher/{id}/` | — |
| `capsules list` | `GET` | `https://lldev.thespacedevs.com/2.2.0/config/spacecraft/` | `limit` (int), `manufacturer__id=121` (fixed) |
| `capsules info <id>` | `GET` | `https://lldev.thespacedevs.com/2.2.0/config/spacecraft/{id}/` | — |
| `company info` | `GET` | `https://lldev.thespacedevs.com/2.2.0/agencies/121/` | — |
| `export launches` | `GET` | `https://lldev.thespacedevs.com/2.2.0/launch/` | `limit` (int), `lsp__id=121` (fixed) |

### 9.3 Pagination / Пагинация

Paginated endpoints return a wrapper object with the following structure:

Эндпоинты с пагинацией возвращают объект-обёртку следующей структуры:

```json
{
  "count": 123,
  "next": "https://lldev.thespacedevs.com/2.2.0/launch/?limit=10&offset=10",
  "previous": null,
  "results": [...]
}
```

The client extracts the `results` array for processing. The CLI uses server-side limiting (via `limit` parameter) rather than offset-based pagination. Offset-based pagination support exists in `api/pagination.py` for future extension. / Клиент извлекает массив `results` для обработки. CLI использует ограничение на стороне сервера (через параметр `limit`), а не пагинацию со смещением. Поддержка пагинации со смещением существует в `api/pagination.py` для будущего расширения.

### 9.4 Error Responses / Ответы об ошибках

| HTTP Status / Статус HTTP | Meaning / Значение | CLI Behaviour / Поведение CLI |
|---|---|---|
| `200` | Success / Успех | Parse JSON response / Парсинг JSON-ответа |
| `404` | Resource not found / Ресурс не найден | Raise `NotFoundError`, print red error message, exit code 1 / Вызов `NotFoundError`, вывод красного сообщения об ошибке, код завершения 1 |
| `429` | Rate limit exceeded / Превышен лимит запросов | Raise `APIError`, print message, exit code 1 / Вызов `APIError`, вывод сообщения, код завершения 1 |
| `500` | Server error / Ошибка сервера | Raise `APIError`, print message, exit code 1 / Вызов `APIError`, вывод сообщения, код завершения 1 |

---

## 10. Technical Requirements / Технические требования

### 10.1 Libraries / Библиотеки

The project uses the following Python libraries across both versions. All are specified as dependencies in `pyproject.toml`.

Проект использует следующие библиотеки Python в обеих версиях. Все они указаны как зависимости в `pyproject.toml`.

| Library / Библиотека | Version / Версия | Purpose / Назначение |
|---|---|---|
| **typer** `[all]` | `>=0.12, <1` | CLI framework — declarative command definitions, automatic `--help` generation, type-safe argument parsing. `all` extras include Rich integration. / Фреймворк CLI — декларативные определения команд, автогенерация `--help`, типобезопасный парсинг аргументов. Дополнения `all` включают интеграцию с Rich. |
| **requests** | `>=2.31, <3` | HTTP client — session management, timeouts, connection pooling. Used as the underlying transport for all REST API calls. / HTTP-клиент — управление сессиями, тайм-ауты, пул соединений. Используется как базовый транспорт для всех вызовов REST API. |
| **rich** | `>=13, <14` | Terminal formatting — colored tables (`Table`), rich panels (`Panel`), live display (`Live`), Markdown rendering, console output with style tags. / Форматирование терминала — цветные таблицы (`Table`), богатые панели (`Panel`), живой отображение (`Live`), рендеринг Markdown, вывод в консоль со стилевыми тегами. |
| **python-dotenv** | `>=1, <2` | Environment variable loading from `.env` files. Loads `SPACEX_API_URL` and `REQUEST_TIMEOUT` on application startup. / Загрузка переменных окружения из файлов `.env`. Загружает `SPACEX_API_URL` и `REQUEST_TIMEOUT` при запуске приложения. |
| **pytest** | `>=7, <8` | Testing framework — test discovery, fixtures, parametrization, assertions. / Фреймворк тестирования — обнаружение тестов, фикстуры, параметризация, проверки. |
| **pytest-cov** | `>=4, <5` | Coverage reporting — measures test coverage of `spacex_cli` source code. Configured with `--cov-fail-under=60` to enforce minimum coverage threshold. / Отчётность о покрытии — измеряет покрытие исходного кода `spacex_cli` тестами. Настроено с `--cov-fail-under=60` для обеспечения минимального порога покрытия. |
| **responses** | `>=0.24, <1` | HTTP mocking for tests — intercepts `requests` calls without monkey-patching. Used in integration tests to mock API responses from fixture JSON files. / Мокирование HTTP для тестов — перехватывает вызовы `requests` без monkey-patching. Используется в интеграционных тестах для мокирования ответов API из файлов-фикстур JSON. |
| **ruff** | `>=0.3, <1` | Linter and formatter — enforces PEP 8, checks imports (`isort`), runs static analysis (`pyflakes`). Single tool replacing flake8, isort, pyupgrade. / Линтер и форматтер — обеспечивает соблюдение PEP 8, проверяет импорты (`isort`), выполняет статический анализ (`pyflakes`). Единый инструмент, заменяющий flake8, isort, pyupgrade. |

### 10.2 Project Structure / Структура проекта

Both versions (`version1/` and `version2/`) share the same architectural structure. The only differences are the package name and entry point script name.

Обе версии (`version1/` и `version2/`) имеют одинаковую архитектурную структуру. Единственные различия — название пакета и имя скрипта точки входа.

```
spacex_cli/                        # Source package / Исходный пакет
│
├── __init__.py                    # Package init — exports __version__ / Инициализация пакета — экспорт __version__
├── __main__.py                    # Entry point: python -m spacex_cli / Точка входа: python -m spacex_cli
│
├── api/                           # HTTP layer / HTTP-слой
│   ├── __init__.py
│   ├── client.py                  # SpaceXClient — requests.Session wrapper / Обёртка над requests.Session
│   ├── endpoints.py               # API endpoint URL constants / URL-константы эндпоинтов API
│   └── pagination.py              # Offset-based pagination iterator / Итератор пагинации со смещением
│
├── cli/                           # Command layer / Слой команд
│   ├── __init__.py                # Typer app, OutputFormat enum, state, global callback, exit command
│   ├── launches.py                # launches list / info / countdown
│   ├── rockets.py                 # rockets list / info
│   ├── capsules.py                # capsules list / info
│   ├── company.py                 # company info
│   └── export.py                  # export launches
│
├── config/                        # Configuration / Конфигурация
│   ├── __init__.py
│   └── settings.py                # .env loader: get_api_url(), get_timeout()
│
├── formatters/                    # Output formatting / Форматирование вывода
│   ├── __init__.py
│   ├── json_fmt.py                # JSON serialization (compact / pretty) / Сериализация JSON (компактная / красивая)
│   ├── table_fmt.py               # Rich Table formatters / Форматтеры Rich-таблиц
│   ├── panel_fmt.py               # Rich Panel formatters / Форматтеры Rich-панелей
│   └── csv_fmt.py                 # CSV formatting utility / Утилита форматирования CSV
│
├── models/                        # Data models / Модели данных
│   ├── __init__.py
│   ├── launch.py                  # Launch, LaunchDetails (frozen dataclasses, slots) / Замороженные датаклассы со слотами
│   ├── rocket.py                  # Rocket (frozen, slots)
│   ├── capsule.py                 # Capsule (frozen, slots)
│   └── company.py                 # CompanyInfo (frozen, slots)
│
├── services/                      # Business logic layer / Слой бизнес-логики
│   ├── __init__.py
│   ├── launch_service.py          # get_launches(), get_launch_by_id(), get_next_launch() + parsers
│   ├── rocket_service.py          # get_rockets(), get_rocket_by_id() + parser
│   ├── capsule_service.py         # get_capsules(), get_capsule_by_id() + parser
│   ├── company_service.py         # get_company_info() + parser
│   └── export_service.py          # export_to_json(), export_to_csv(), export_to_markdown()
│
└── utils/                         # Shared utilities / Общие утилиты
    ├── __init__.py
    ├── console.py                 # Rich Console instances (console → stderr, out_console → stdout)
    ├── countdown.py               # Live countdown with Rich Live widget / Живой обратный отсчёт с виджетом Rich Live
    ├── errors.py                  # Custom exception hierarchy / Иерархия пользовательских исключений
    └── logging.py                 # setup_logging() — DEBUG/WARNING level based on --verbose flag

tests/
├── version1/                          # Version 1 tests / Тесты версии 1
│   ├── conftest.py                    # Shared pytest fixtures / Общие фикстуры pytest
│   ├── fixtures/                      # Static JSON fixture files / Статические файлы-фикстуры JSON
│   │   ├── __init__.py
│   │   ├── launches_response.json     # 2 sample launches / 2 примера запусков
│   │   ├── rockets_response.json      # 2 sample rockets / 2 примера ракет
│   │   ├── capsules_response.json     # 2 sample capsules / 2 примера капсул
│   │   ├── company_response.json      # 1 sample company / 1 пример компании
│   │   └── api_responses.py           # Python fixture data / Python-данные фикстур
│   ├── unit/                          # Unit tests / Юнит-тесты
│   │   ├── test_models.py             # Dataclass creation, frozen behavior, field values
│   │   ├── test_pagination.py         # paginate() returns correct number of items
│   │   ├── test_formatters.py         # JSON compact/pretty output, table headers, panel presence
│   │   ├── test_launch_service.py     # Parser functions, None-field handling
│   │   └── test_cli_commands.py       # CLI runner tests, exit codes
│   └── integration/                   # Integration tests / Интеграционные тесты
│       ├── test_launches_cmd.py       # launches list/info/countdown
│       ├── test_rockets_cmd.py        # rockets list/info
│       ├── test_capsules_cmd.py       # capsules list/info
│       ├── test_company_cmd.py        # company info
│       └── test_export_cmd.py         # export to JSON/CSV/Markdown
│
└── version2/                          # Version 2 tests / Тесты версии 2
    ├── conftest.py                    # Shared pytest fixtures / Общие фикстуры pytest
    ├── fixtures/                      # Static JSON fixture files / Статические файлы-фикстуры JSON
    │   ├── launches_response.json     # 2 sample launches / 2 примера запусков
    │   ├── rockets_response.json      # 2 sample rockets / 2 примера ракет
    │   ├── capsules_response.json     # 2 sample capsules / 2 примера капсул
    │   └── company_response.json      # 1 sample company / 1 пример компании
    ├── unit/                          # Unit tests / Юнит-тесты
    │   ├── test_models.py             # Dataclass creation, frozen behavior, field values
    │   ├── test_pagination.py         # paginate() returns correct number of items
    │   ├── test_formatters.py         # JSON compact/pretty output, table headers, panel presence
    │   ├── test_launch_service.py     # Parser functions, None-field handling
    │   └── test_cli_commands.py       # CLI runner tests, exit codes
    └── integration/                   # Integration tests / Интеграционные тесты
        ├── test_launches_cmd.py       # launches list/info/countdown
        ├── test_rockets_cmd.py        # rockets list/info
        ├── test_capsules_cmd.py       # capsules list/info
        ├── test_company_cmd.py        # company info
        └── test_export_cmd.py          # export to JSON/CSV/Markdown
```

### 10.3 Error Handling / Обработка ошибок

The CLI implements a custom exception hierarchy rooted at `SpaceXCLIError`. All CLI commands wrap their business logic in a `try/except` block that catches `SpaceXCLIError` and its subclasses, prints a red error message to the console, and exits with code 1. Network errors are caught and re-raised as `NetworkError` with a descriptive message.

CLI реализует пользовательскую иерархию исключений с корнем `SpaceXCLIError`. Все команды CLI оборачивают свою бизнес-логику в блок `try/except`, который перехватывает `SpaceXCLIError` и её подклассы, выводит красное сообщение об ошибке в консоль и завершается с кодом 1. Сетевые ошибки перехватываются и повторно вызываются как `NetworkError` с описательным сообщением.

#### Exception Hierarchy / Иерархия исключений

```
Exception
└── SpaceXCLIError                          # Base exception — all CLI errors inherit from here / Базовое исключение — все ошибки CLI наследуются отсюда
    ├── NetworkError                        # Network failures: connection refused, timeout, DNS resolution / Сетевые сбои: отказ соединения, тайм-аут, разрешение DNS
    │       └── Raised by: SpaceXClient.get() on requests.exceptions.RequestException
    ├── NotFoundError(spacexCLIError)       # HTTP 404 — resource does not exist / HTTP 404 — ресурс не существует
    │       └── Attributes: resource (str), identifier (str)
    │       └── Raised by: SpaceXClient._raise_for_status() on status 404
    ├── APIError(spacexCLIError)            # Unexpected HTTP errors (5xx, 4xx other than 404) / Непредвиденные HTTP-ошибки (5xx, 4xx кроме 404)
    │       └── Attributes: status_code (int)
    │       └── Raised by: SpaceXClient._raise_for_status() on unexpected status codes
    └── ValidationError(spacexCLIError)     # Invalid user input / Неверный ввод пользователя
            └── Currently not raised by any command (reserved for future use) / В настоящее время не вызывается ни одной командой (зарезервировано для будущего использования)
```

#### Error Flow Diagram / Схема обработки ошибок

```
User Input / Ввод пользователя
       │
       ▼
CLI Command Handler / Обработчик команд CLI
       │
       ▼
┌─────────────────────────────────────────┐
│  try:                                    │
│      with SpaceXClient() as client:     │
│          data = service_function(client) │
│  except SpaceXCLIError as exc:          │
│      console.print(f"[red]Error:[/red] {exc}") │
│      sys.exit(1)                         │
└─────────────────────────────────────────┘
       │
       ▼
Error Message Printed / Сообщение об ошибке напечатано
       │
       ▼
Process Exits with Code 1 / Процесс завершается с кодом 1
```

#### Error Scenarios / Сценарии ошибок

| Scenario / Сценарий | Cause / Причина | Exception / Исключение | Message / Сообщение | Exit Code / Код |
|---|---|---|---|---|
| Network unreachable / Сеть недоступна | No internet connection / Нет подключения к интернету | `NetworkError` | `Network error: ...` | 1 |
| Request timeout / Тайм-аут запроса | Server takes too long / Сервер слишком долго отвечает | `NetworkError` | `Network error: ...` | 1 |
| Resource not found / Ресурс не найден | Invalid ID passed / Передан неверный ID | `NotFoundError` | `Not found: <resource>/<id>` | 1 |
| Rate limit / Лимит запросов | Too many requests / Слишком много запросов | `APIError` | `SpaceX API error 429: ...` | 1 |
| Server error / Ошибка сервера | LL2 API internal error / Внутренняя ошибка LL2 API | `APIError` | `SpaceX API error 500: ...` | 1 |
| Unknown export format / Неизвестный формат экспорта | Invalid `--format` value / Неверное значение `--format` | (handled directly) | `Unknown format: <value>. Use json | csv | markdown` | 2 |

### 10.4 Configuration / Конфигурация

Configuration is managed through environment variables, loaded via `python-dotenv` from a `.env` file in the project root. The configuration module (`config/settings.py`) provides typed getter functions.

Конфигурация управляется через переменные окружения, загружаемые через `python-dotenv` из файла `.env` в корне проекта. Модуль конфигурации (`config/settings.py`) предоставляет типизированные функции получения значений.

#### Configuration Files / Файлы конфигурации

| File / Файл | Purpose / Назначение | Created by / Создаётся |
|---|---|---|
| `.env` | Runtime configuration — actual values (API URL, timeout). Must be created by the user from `.env.example`. Never committed to version control. / Конфигурация времени выполнения — фактические значения (URL API, тайм-аут). Создаётся пользователем из `.env.example`. Никогда не коммитится в систему контроля версий. |
| `.env.example` | Configuration template — documents all available environment variables with default values. / Шаблон конфигурации — документирует все доступные переменные окружения со значениями по умолчанию. |

#### Environment Variables / Переменные окружения

| Variable / Переменная | Type / Тип | Default / По умолчанию | Required / Обязательный | Description / Описание |
|---|---|---|---|---|
| `SPACEX_API_URL` | `str` | `https://lldev.thespacedevs.com/2.2.0/` | No / Нет | Base URL of the Launch Library 2 API. Use the development URL (`lldev.thespacedevs.com`) for testing or the production URL (`ll.thespacedevs.com`) for live data. / Базовый URL Launch Library 2 API. Используйте URL разработки (`lldev.thespacedevs.com`) для тестирования или производственный URL (`ll.thespacedevs.com`) для актуальных данных. |
| `REQUEST_TIMEOUT` | `str` (int at runtime) | `30` | No / Нет | HTTP request timeout in seconds. Passed directly to `requests.Session.get(timeout=...)`. / Тайм-аут HTTP-запроса в секундах. Передаётся напрямую в `requests.Session.get(timeout=...)`. |

#### Configuration Loading / Загрузка конфигурации

```python
# config/settings.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file into environment / Загружает .env файл в окружение

def get_api_url() -> str:
    return os.getenv("SPACEX_API_URL", "https://lldev.thespacedevs.com/2.2.0/")

def get_timeout() -> int:
    return int(os.getenv("REQUEST_TIMEOUT", "30"))
```

### 10.5 Logging / Логирование

The CLI uses Python's standard `logging` module. Logging is configured once at startup (in the global callback) based on the `--verbose` flag. No log files are created by default; logs are written to stderr.

CLI использует стандартный модуль Python `logging`. Логирование настраивается один раз при запуске (в глобальном callback) на основе флага `--verbose`. Файлы логов по умолчанию не создаются; логи записываются в stderr.

#### Logging Configuration / Конфигурация логирования

| Verbose Mode / Режим | Logging Level / Уровень логирования | What's Logged / Что логируется |
|---|---|---|
| Default (`-v` not set) / По умолчанию (`-v` не установлен) | `WARNING` | Only error messages from the standard library and third-party libraries. No CLI-level logs. / Только сообщения об ошибках от стандартной библиотеки и сторонних библиотек. Без логов уровня CLI. |
| Verbose (`-v` set) / Подробный (`-v` установлен) | `DEBUG` | All HTTP requests (URL, method, params), all CLI function calls, full exception stack traces. / Все HTTP-запросы (URL, метод, параметры), все вызовы функций CLI, полные трассировки исключений. |

#### Logging Code / Код логирования

```python
# utils/logging.py
import logging

def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
```

#### Debug Output Example / Пример отладочного вывода

```
DEBUG: GET https://lldev.thespacedevs.com/2.2.0/launch/?limit=10&lsp__id=121
DEBUG: Response 200 OK (1245 bytes, 87 ms)
DEBUG: Parsed 10 launch records
DEBUG: Formatting output as TABLE
```

### 10.6 Testing / Тестирование

#### Overview / Обзор

The test suite covers both unit tests (isolated components) and integration tests (full command pipelines with mocked HTTP). All tests run offline using fixture JSON files and the `responses` library to mock `requests.Session.get()` calls.

Набор тестов включает как юнит-тесты (изолированные компоненты), так и интеграционные тесты (полные конвейеры команд с замокированным HTTP). Все тесты запускаются офлайн с использованием файлов-фикстур JSON и библиотеки `responses` для мокирования вызовов `requests.Session.get()`.

#### Test Requirements / Требования к тестированию

| Requirement / Требование | Value / Значение |
|---|---|
| Minimum coverage / Минимальное покрытие | 60% (enforced by `pytest --cov-fail-under=60`) |
| Version 1 (Claude) achieved / Достигнуто в версии 1 (Claude) | 88.73% (59 tests) |
| Version 2 (Gemini) achieved / Достигнуто в версии 2 (Gemini) | 81.58% (22 tests) |
| Minimum test count / Минимальное количество тестов | 5–10 unit tests |

#### Test Files / Файлы тестов

| Test File / Файл тестов | Type / Тип | What Is Tested / Что тестируется | Example Tests / Примеры тестов |
|---|---|---|---|
| `tests/unit/test_models.py` | Unit | Dataclass instantiation, frozen immutability, field values, optional fields handling (None values). / Создание датаклассов, неизменность frozen, значения полей, обработка опциональных полей (значения None). | `test_launch_creation`, `test_launch_frozen`, `test_optional_fields_none`, `test_company_info_fields` |
| `tests/unit/test_pagination.py` | Unit | `paginate()` yields correct number of items, handles empty results, correct offset/limit. / `paginate()` возвращает правильное количество элементов, обрабатывает пустые результаты, корректное смещение/лимит. | `test_pagination_items_count`, `test_pagination_empty`, `test_pagination_with_params` |
| `tests/unit/test_formatters.py` | Unit | JSON compact vs pretty output, table column headers, panel title presence, CSV headers. / Компактный vs красивый вывод JSON, заголовки столбцов таблицы, наличие заголовков панелей, заголовки CSV. | `test_json_pretty_indent`, `test_json_compact_separators`, `test_table_has_columns`, `test_csv_has_headers` |
| `tests/unit/test_launch_service.py` | Unit | Parser functions (`_parse_launch`, `_parse_launch_details`), datetime parsing, nested field extraction, None handling. / Функции парсинга (`_parse_launch`, `_parse_launch_details`), парсинг datetime, извлечение вложенных полей, обработка None. | `test_parse_launch`, `test_parse_launch_details`, `test_missing_optional_fields`, `test_datetime_parsing` |
| `tests/unit/test_cli_commands.py` | Unit | CLI runner — basic command invocation, exit code 0 for help, argument validation. / Запуск CLI — базовый вызов команды, код завершения 0 для help, валидация аргументов. | `test_app_help`, `test_launches_help`, `test_exit_command` |
| `tests/integration/test_launches_cmd.py` | Integration | Full `launches list`, `launches info`, `launches countdown` commands with mocked HTTP responses. / Полные команды `launches list`, `launches info`, `launches countdown` с замокированными HTTP-ответами. | `test_list_launches_table`, `test_list_launches_json`, `test_launch_info_found`, `test_launch_info_not_found` |
| `tests/integration/test_rockets_cmd.py` | Integration | Full `rockets list`, `rockets info` commands with mocked HTTP responses. / Полные команды `rockets list`, `rockets info` с замокированными HTTP-ответами. | `test_rockets_list_table`, `test_rockets_list_json`, `test_rocket_info` |
| `tests/integration/test_capsules_cmd.py` | Integration | Full `capsules list`, `capsules info` commands with mocked HTTP responses. / Полные команды `capsules list`, `capsules info` с замокированными HTTP-ответами. | `test_capsules_list_table`, `test_capsule_info` |
| `tests/integration/test_company_cmd.py` | Integration | Full `company info` command with mocked HTTP response. / Полная команда `company info` с замокированным HTTP-ответом. | `test_company_info_table`, `test_company_info_json` |
| `tests/integration/test_export_cmd.py` | Integration | Full `export launches` command — verifies correct file creation and content in JSON, CSV formats. / Полная команда `export launches` — проверяет корректное создание файлов и содержимое в форматах JSON, CSV. | `test_export_launches_json`, `test_export_launches_csv` |

#### Fixture Files / Файлы-фикстуры

Both versions use the same fixture structure, with separate directories for each version. / Обе версии используют одинаковую структуру фикстур, с отдельными директориями для каждой версии.

| Fixture File / Файл-фикстура | Contents / Содержимое |
|---|---|
| `tests/version1/fixtures/launches_response.json` / `tests/version2/fixtures/launches_response.json` | Array of 2 sample launch objects (one upcoming, one past) with all fields used by parsers. / Массив из 2 примеров объектов запуска (один предстоящий, один прошедший) со всеми полями, используемыми парсерами. |
| `tests/version1/fixtures/rockets_response.json` / `tests/version2/fixtures/rockets_response.json` | Array of 2 rocket configuration objects with dimensions, mass, cost, and description. / Массив из 2 объектов конфигурации ракет с размерами, массой, стоимостью и описанием. |
| `tests/version1/fixtures/capsules_response.json` / `tests/version2/fixtures/capsules_response.json` | Array of 2 spacecraft configuration objects with serial, status, reuse_count, landings. / Массив из 2 объектов конфигурации космических аппаратов с серийным номером, статусом, количеством использований, посадками. |
| `tests/version1/fixtures/company_response.json` / `tests/version2/fixtures/company_response.json` | Single company/agency object with all fields: name, founder, employees, CEO, CTO, COO, valuation, headquarters, links, summary. / Один объект компании/агентства со всеми полями. |
| `tests/version1/fixtures/api_responses.py` | Python dictionaries mirroring the JSON fixtures — used for programmatic fixture access in tests (version1 only). / Python-словари, зеркалирующие JSON-фикстуры — используются для программного доступа к фикстурам в тестах (только версия 1). |

#### Running Tests / Запуск тестов

```bash
# Run all tests for version 1 with coverage / Запуск всех тестов версии 1 с покрытием
$ cd version1 && pytest

# Run all tests for version 2 with coverage / Запуск всех тестов версии 2 с покрытием
$ cd version2 && pytest

# Run with HTML coverage report / С HTML-отчётом о покрытии
$ pytest --cov=spacex_cli --cov-report=html
# Open: htmlcov/index.html

# Run unit tests only (version 2) / Только юнит-тесты (версия 2)
$ pytest tests/version2/unit/

# Run integration tests only (version 2) / Только интеграционные тесты (версия 2)
$ pytest tests/version2/integration/

# Run with verbose output / С подробным выводом
$ pytest -v

# Stop on first failure / Остановиться на первой ошибке
$ pytest -x
```

---

## Appendix: Exit Codes / Приложение: коды завершения

| Exit Code / Код | Meaning / Значение | Cause / Причина |
|---|---|---|
| `0` | Success / Успех | Normal command execution completed. Also used by the `exit` command. / Нормальное выполнение команды завершено. Также используется командой `exit`. |
| `1` | Error / Ошибка | Any `SpaceXCLIError` (network failure, not found, API error). / Любая `SpaceXCLIError` (сетевой сбой, не найдено, ошибка API). |
| `2` | Invalid argument / Неверный аргумент | Unknown export format value passed to `export launches --format`. / Неизвестное значение формата экспорта, переданное в `export launches --format`. |
