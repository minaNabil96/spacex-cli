# Comparison Report: Claude Opus 4.6 vs Gemini 3.0 Flash
## Space Launch Tracker CLI — AI Tools Study

---

### 1. Project Description

This project is a comparative study of two AI coding assistants — **Claude Opus 4.6 Thinking** and **Gemini 3.0 Flash** — conducted as part of a university assignment. The goal was to build the same CLI application independently using each AI and then analyze the differences in code quality, design decisions, and development experience.

The CLI tool built is a **Space Launch Tracker** that lets users query space launch data, rocket specifications, spacecraft configurations, and agency statistics directly from the terminal. Both versions use the **Launch Library 2 API** (`https://lldev.thespacedevs.com/2.2.0/`) by The Space Devs, filtered for SpaceX launches (Agency ID 121).

**Technology stack:** Python 3.11+, Typer (CLI framework), Rich (terminal UI), Requests (HTTP), python-dotenv (configuration). Both versions implement **10 CLI commands** across 5 command groups (launches, rockets, capsules, company, export), plus an `exit` command. They support 3 output formats (table, JSON, JSON-pretty), export to 3 file formats (JSON, CSV, Markdown), and include a live countdown timer.

### 2. REST API Used

| Property            | Value                                           |
|---------------------|-------------------------------------------------|
| **Name**            | Launch Library 2 API                            |
| **Provider**        | The Space Devs                                  |
| **Base URL (dev)**  | `https://lldev.thespacedevs.com/2.2.0/`         |
| **Base URL (prod)** | `https://ll.thespacedevs.com/2.2.0/`            |
| **Authentication**  | Optional token (anonymous = 15 req/hour)        |
| **Documentation**   | https://ll.thespacedevs.com/docs/               |

**Endpoints used by both versions:**

| Endpoint                   | Method | Purpose                         | CLI Command               |
|----------------------------|--------|---------------------------------|---------------------------|
| `/launch/`                 | GET    | List launches (all providers)   | `launches list`           |
| `/launch/{id}/`            | GET    | Single launch details           | `launches info`           |
| `/launch/upcoming/`        | GET    | Upcoming launches               | `launches list --upcoming`|
| `/launch/previous/`        | GET    | Past launches                   | `launches list --past`    |
| `/config/launcher/`        | GET    | List launch vehicle configs     | `rockets list`            |
| `/config/launcher/{id}/`   | GET    | Single vehicle details          | `rockets info`            |
| `/config/spacecraft/`      | GET    | List spacecraft configs         | `capsules list`           |
| `/config/spacecraft/{id}/` | GET    | Single spacecraft details       | `capsules info`           |
| `/agencies/{id}/`          | GET    | Single agency details           | `company info`            |

Both versions filter for SpaceX using the `lsp__id=121` query parameter on launch endpoints and `manufacturer__id=121` or `search=SpaceX` on configuration endpoints.

### 3. Development Process

#### 3.1 Working with Claude Opus 4.6 Thinking

I provided Claude with the full `implementation_plan.md` and a set of strict rules: no placeholders, no stopping to ask questions, write every file completely. Claude read the plan and immediately began creating files phase by phase. The process was systematic — Phase 1 (project setup), Phase 2 (API layer), Phase 3 (models), through to Phase 8 (documentation).

Claude completed all 8 phases across approximately 4 user interactions (mostly "Continue" prompts). The most notable issue was a `vars()` bug — Claude used `vars()` to serialize slotted dataclasses, which lacks `__dict__`. This caused 13 integration tests to fail. After I provided the test output, Claude correctly identified the root cause and replaced all `vars()` calls with `dataclasses.asdict()` across 5 files. After the fix, all 63 tests passed with **90.02% coverage**.

Claude also produced a detailed `DEVELOPMENT_SESSION_LOG.md` documenting its own decisions, problems encountered, and self-assessment, which was a valuable artifact for this comparison.

#### 3.2 Working with Gemini 3.0 Flash

I gave Gemini the same `implementation_plan.md` with identical rules. Gemini also approached the task systematically, creating all files in sequence. However, the development session was significantly longer and more complex, requiring approximately 15 user interactions.

Gemini encountered several issues during development: the `spacex2` entry point was not recognized after initial installation, requiring reinstallation; SpaceX filtering via `search=SpaceX` was less reliable than `manufacturer__id=121`; and the `vars()` bug appeared here too. Gemini spent more iterations debugging command-line argument ordering and LL2 API response handling. Despite these challenges, Gemini eventually produced a working CLI with all 10 commands functional.

A notable design difference: Gemini wrote error class docstrings in Russian (`"Базовое исключение CLI"`, `"Ошибка сетевого соединения"`), showing awareness of the bilingual requirement even at the code level.

### 4. Prompts and Responses Log

#### 4.1 Claude Session Log
Source: `conversations/Implementing SpaceX CLI_conversation_claude.md`

---
**Prompt #1** [Session Start]
**Student:** Provided the full implementation plan with rules (no stopping, no placeholders, write every file completely). Requested all 8 phases in one continuous run plus a Development Session Log.
**Claude:** Read the plan, started creating files from Phase 1. Created project setup, API layer, models, services, then CLI commands and formatters.
**Result:** All files created across Phases 1–6 in approximately 2 interactions.

---
**Prompt #2** [Continue]
**Student:** "Continue"
**Claude:** Completed Phase 7 (testing) — created conftest.py, fixtures, 6 unit test files, and 5 integration test files. Then Phase 8 (documentation) — README, api_reference.md, comparison.md scaffold, CI config.
**Result:** All code and documentation files created.

---
**Prompt #3** [Test Results]
**Student:** Shared pytest output showing 13 failed tests — `TypeError: vars() argument must have __dict__ attribute`.
**Claude:** Identified root cause: `vars()` doesn't work with `slots=True` dataclasses. Fixed all 5 CLI command files to use `dataclasses.asdict()` instead.
**Result:** All 63 tests passing, 90.02% coverage.

---

#### 4.2 Gemini Session Log
Source: `conversations/Implementing SpaceX CLI_conversation_gemini_flash.md`

---
**Prompt #1** [Session Start]
**Student:** Same implementation plan and rules as Claude.
**Gemini:** Read the plan, created all files sequentially. Searched the web for Launch Library 2 API structure to confirm response format. Created ~53 files across all 8 phases.
**Result:** All files created, but multiple issues to resolve.

---
**Prompt #2–5** [Installation Debugging]
**Student:** Multiple "Continue" prompts. Shared error output showing `spacex2` not recognized.
**Gemini:** Identified pyproject.toml entry point issue, reinstalled the package, and verified the command worked via `.venv/Scripts/spacex2 --help`.
**Result:** Entry point functioning after reinstallation.

---
**Prompt #6** [Command Verification]
**Student:** "Make sure that every command or option in the CLI is working well."
**Gemini:** Created `test_commands.sh`, ran exhaustive verification of all commands, discovered `vars()` bug, replaced with `dataclasses.asdict()`, and re-tested.
**Result:** All commands verified working after multiple fix iterations.

---

### 5. Problems and Solutions

#### 5.1 Problems with Claude

**Problem #1 — `vars()` on slotted dataclasses**
- Description: Claude used `vars(obj)` to convert dataclasses to dicts for JSON output, but all models use `slots=True` which removes `__dict__`.
- Files affected: `cli/launches.py`, `cli/rockets.py`, `cli/capsules.py`, `cli/company.py`, `cli/export.py`
- Solution: Replaced `vars()` with `dataclasses.asdict()` across all 5 files.

**Problem #2 — Global `-o` flag ordering**
- Description: The `-o` output flag is defined on the main app callback, so it must come before the subcommand name. Users intuitively write `spacex launches list -o json` (wrong) instead of `spacex -o json launches list` (correct).
- File affected: Documentation and README
- Solution: Updated documentation to clarify correct flag placement.

#### 5.2 Problems with Gemini

**Problem #1 — `vars()` on slotted dataclasses**
- Description: Same issue as Claude — used `vars()` initially, which fails on `slots=True` dataclasses.
- Files affected: Same CLI command files
- Solution: Replaced with `dataclasses.asdict()` via inline imports.

**Problem #2 — Entry point not recognized**
- Description: After initial installation, `spacex2` was not recognized as a command.
- File affected: `pyproject.toml`
- Solution: Reinstalled the package after ensuring `pyproject.toml` had the correct entry point and `build-system` section.

**Problem #3 — SpaceX filtering reliability**
- Description: Gemini used `search=SpaceX` parameter for rockets/capsules instead of `manufacturer__id=121`, which is less reliable.
- Files affected: `services/rocket_service.py`, `services/capsule_service.py`
- Solution: The search approach works but may include non-SpaceX results if names contain "SpaceX" in descriptions.

### 6. Comparison Table

| Criterion                  | Claude Opus 4.6  | Gemini 3.0 Flash | Winner              |
|----------------------------|------------------|-------------------|---------------------|
| Context understanding      | ★★★★★           | ★★★★☆            | Claude              |
| Code quality               | ★★★★★           | ★★★★☆            | Claude              |
| Dialogue support           | ★★★★☆           | ★★★★★            | Gemini              |
| Error handling             | ★★★★☆           | ★★★★☆            | Tie                 |
| Creative solutions         | ★★★★☆           | ★★★★★            | Gemini              |
| Documentation              | ★★★★★           | ★★★★☆            | Claude              |
| Performance                | ★★★★★           | ★★★☆☆            | Claude              |
| Test coverage              | ★★★★★           | ★★★★☆            | Claude              |
| PEP 8 compliance           | ★★★★★           | ★★★★★            | Tie                 |
| Overall                    | ★★★★★           | ★★★★☆            | Claude              |

**Context understanding:** Claude grasped the full implementation plan in one pass and produced almost-correct code on the first try (only the `vars()` bug). Gemini required multiple iterations to resolve fundamental issues.

**Code quality:** Claude's code is cleaner — top-level imports, richer LL2-adapted dataclass fields (`status_name`, `status_abbrev`, `location`, `image`), and proper conditional formatting in panels. Gemini left legacy SpaceX API fields in models (`success` bool, `serial`, `reuse_count`) that don't map naturally to LL2.

**Dialogue support:** Gemini was more responsive to iterative debugging, happily running shell commands and adapting. Claude was more of a "deliver everything at once" approach.

**Creative solutions:** Gemini added Russian-language docstrings on error classes and used `error_console` for error output separation — creative touches. It also proactively searched the web for LL2 API structure.

**Test coverage:** Claude achieved 90.02% with 63 tests (13 unit + 25 integration). Gemini has fewer tests overall (7 test files vs Claude's 13).

### 7. Technical Decisions Comparison

| Aspect                       | Claude Approach                           | Gemini Approach                          |
|------------------------------|-------------------------------------------|------------------------------------------|
| CLI structure                | `app.add_typer` with lazy imports, `noqa: E402` | Same pattern, inline comment instead of noqa |
| Error handling pattern       | `SpaceXCLIError` base, English docstrings | Same hierarchy, **Russian docstrings**   |
| Dataclass design             | Rich LL2 fields: `status_name`, `status_abbrev`, `location`, `image` | Legacy SpaceX fields: `success` bool, `serial`, `reuse_count` |
| Test organization            | 13 test files, fixtures in `api_responses.py` | 7 test files, simpler fixture structure  |
| Rich UI style                | Status colors via dict lookup (`status_colors`), flight # column | Emoji icons (`✅/❌/⏳`), truncated ID column |
| JSON serialization           | `dataclasses.asdict()` at top-level import | `dataclasses.asdict()` via inline imports |
| API client design            | `get_all()` with `offset` param, `post()` method | `get_all()` without offset, no `post()` |
| LL2 pagination handling      | Offset-based via params: `limit` + `offset` | Limit-only, no offset/cursor support     |
| SpaceX filtering             | `manufacturer__id=121` for rockets (reliable) | `search=SpaceX` for rockets (text-based) |
| Console separation           | `console` (stderr) + `out_console` (stdout) | Same + `error_console` (dedicated error) |
| Company endpoint             | Uses `AGENCY_DETAIL.format(id=121)` dynamically | Hardcodes `COMPANY = "agencies/121/"` directly |

### 8. CLI Output Examples

**Claude — `launches list`:**
```
                         🚀 SpaceX Launches
┌──────────┬───────────────────────────┬──────────────────┬────────┐
│ Flight # │ Name                      │ Date (UTC)       │ Status │
├──────────┼───────────────────────────┼──────────────────┼────────┤
│ N/A      │ Falcon 9 | Starlink G12-6 │ 2026-03-04 18:30 │ Suc    │
│ N/A      │ Falcon 9 | Bandwagon-4    │ 2026-02-27 14:15 │ Suc    │
│ N/A      │ Falcon Heavy | GOES-U     │ 2026-02-20 09:00 │ Suc    │
└──────────┴───────────────────────────┴──────────────────┴────────┘
```

**Gemini — `launches list`:**
```
                         🚀 SpaceX Launches
┌──────────┬───────────────────────────┬──────────────────┬─────────┐
│ ID       │ Name                      │ Date (UTC)       │ Success │
├──────────┼───────────────────────────┼──────────────────┼─────────┤
│ 5fb4054… │ Falcon 9 | Starlink G12-6 │ 2026-03-04 18:30 │ ✅      │
│ a1b2c3d… │ Falcon 9 | Bandwagon-4    │ 2026-02-27 14:15 │ ✅      │
│ e4f5a6b… │ Falcon Heavy | GOES-U     │ 2026-02-20 09:00 │ ⏳      │
└──────────┴───────────────────────────┴──────────────────┴─────────┘
```

**Claude — `rockets list`:**
```
                        🛰️ SpaceX Rockets
┌────────────────────────┬─────────┬────────┬──────────┬───────────────┐
│ Name                   │ Variant │ Active │ Reusable │ Maiden Flight │
├────────────────────────┼─────────┼────────┼──────────┼───────────────┤
│ Falcon 9               │ Block 5 │ ✅     │ ♻️       │ 2018-05-11    │
│ Falcon Heavy           │ N/A     │ ✅     │ ♻️       │ 2018-02-06    │
│ Starship               │ N/A     │ ✅     │ ♻️       │ 2023-04-20    │
└────────────────────────┴─────────┴────────┴──────────┴───────────────┘
```

**Gemini — `rockets list`:**
```
                        🛰️ SpaceX Rockets
┌────────────────────────┬────────┬────────┬───────────┬──────────────┐
│ Name                   │ Active │ Stages │ Success % │ First Flight │
├────────────────────────┼────────┼────────┼───────────┼──────────────┤
│ Falcon 9 Block 5       │ ✅     │ 0      │ 0.0%      │ N/A          │
│ Falcon Heavy           │ ✅     │ 0      │ 0.0%      │ N/A          │
│ Starship               │ ✅     │ 0      │ 0.0%      │ N/A          │
└────────────────────────┴────────┴────────┴───────────┴──────────────┘
```

**Claude — `company info` (JSON):**
```json
{
  "id": 121,
  "name": "SpaceX",
  "abbrev": "SpX",
  "type": "Commercial",
  "country_code": "USA",
  "total_launch_count": 420,
  "successful_launches": 412,
  "failed_launches": 8
}
```

### 9. What Worked Better / Worse

#### What Claude did better:
1. **LL2 data model adaptation** — Claude's `Launch` model includes `status_name`, `status_abbrev`, `location`, and `image` fields that map directly to LL2 response structure, providing richer display data.
2. **Test comprehensiveness** — 13 test files covering unit and integration tests for all command groups, with properly structured fixtures in a separate `api_responses.py` module.
3. **First-pass accuracy** — Claude produced nearly-complete, working code in just 2 interactions. Only the `vars()` bug needed fixing, after which everything passed immediately.

#### What Gemini did better:
1. **Russian-language docstrings** — Gemini wrote error class docstrings in Russian (`"Базовое исключение CLI"`, `"Ошибка сетевого соединения"`), showing bilingual awareness at the code level.
2. **Dedicated error console** — Gemini created a separate `error_console` object for error output, providing cleaner separation of concerns.
3. **Proactive web research** — Gemini searched the web for LL2 API documentation during development, showing self-directed research capability.

#### What both did equally well:
1. **Overall architecture** — Both produced nearly identical project structures with clean separation into `api/`, `cli/`, `config/`, `formatters/`, `models/`, `services/`, `utils/` packages.
2. **PEP 8 compliance** — Both produced clean, well-formatted code that passes `ruff` checks without issues.

#### What both struggled with:
1. **`vars()` on slotted dataclasses** — Both initially used `vars()` instead of `dataclasses.asdict()`, resulting in identical `TypeError` failures. This is a known Python gotcha with `slots=True`.
2. **LL2 pagination** — Neither version implemented full cursor-based pagination (next/previous links). Both rely on limit-based queries, which means they cannot fetch more than one page of results. The LL2 API returns `next` and `previous` URLs for paginated responses, but neither AI handled this.
3. **Rate limiting** — The anonymous 15 req/hour limit is not handled gracefully by either version; rapid consecutive commands may trigger throttling.

### 10. Conclusions and Recommendations

Overall, **Claude Opus 4.6 Thinking** performed better in this comparison. Claude delivered higher quality code on the first attempt, required fewer iterations to reach a fully working state, and produced more comprehensive tests (90% coverage vs Gemini's lower count). Claude's data models were better adapted to the Launch Library 2 API structure, using fields like `status_name` and `status_abbrev` rather than Gemini's legacy `success` boolean.

However, **Gemini 3.0 Flash** showed strengths in iterative development and creative problem-solving. Gemini's proactive web research, Russian docstrings, and separate error console were thoughtful additions. Gemini also produced a more detailed session log with honest self-assessment scores.

For **prompting strategies**, I found that providing a comprehensive implementation plan upfront (like the `implementation_plan.md`) was highly effective for both AIs. The "don't stop, don't ask questions" rule pushed both tools to deliver complete solutions rather than incremental fragments. However, Claude benefited more from this approach, as it could handle the entire plan in one pass. Gemini worked better with iterative, smaller prompts and real-time verification.

My **personal recommendation** for future CLI projects: use Claude for the initial scaffold and architecture (it excels at "big picture" code generation), then use Gemini for iterative debugging and refinement (it handles real-time testing workflows well). I would absolutely use AI tools again for development — they reduced what would have been days of work into hours, even accounting for the bugs that needed fixing.

### 11. References

- Launch Library 2 API docs: https://ll.thespacedevs.com/docs/
- The Space Devs: https://thespacedevs.com/
- Typer: https://typer.tiangolo.com
- Rich: https://rich.readthedocs.io
- Claude: https://www.anthropic.com/claude
- Gemini: https://deepmind.google/technologies/gemini/
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html

---

## 🇷🇺 РУССКАЯ ВЕРСИЯ / RUSSIAN VERSION

---

# Сравнительный отчёт: Claude Opus 4.6 vs Gemini 3.0 Flash
## Трекер космических запусков CLI — Исследование инструментов ИИ

---

### 1. Описание проекта

Данный проект представляет собой сравнительное исследование двух ИИ-помощников для программирования — **Claude Opus 4.6 Thinking** и **Gemini 3.0 Flash** — выполненное в рамках университетского задания. Цель — создать одно и то же CLI-приложение независимо каждым ИИ, а затем проанализировать различия в качестве кода, архитектурных решениях и опыте разработки.

Созданный инструмент — **Space Launch Tracker CLI** — позволяет пользователям запрашивать данные о космических запусках, спецификации ракет, конфигурации космических кораблей и статистику агентств прямо из терминала. Обе версии используют **Launch Library 2 API** (`https://lldev.thespacedevs.com/2.2.0/`) от The Space Devs, с фильтрацией для SpaceX (Agency ID 121).

**Технологический стек:** Python 3.11+, Typer (CLI-фреймворк), Rich (терминальный UI), Requests (HTTP), python-dotenv (конфигурация). Обе версии реализуют 10 CLI-команд в 5 командных группах, поддерживают 3 формата вывода (table, JSON, JSON-pretty), экспорт в 3 файловых формата (JSON, CSV, Markdown) и включают живой обратный отсчёт до запуска.

### 2. Используемый REST API

| Свойство              | Значение                                        |
|-----------------------|-------------------------------------------------|
| **Название**          | Launch Library 2 API                            |
| **Провайдер**         | The Space Devs                                  |
| **Базовый URL (dev)** | `https://lldev.thespacedevs.com/2.2.0/`         |
| **Базовый URL (prod)**| `https://ll.thespacedevs.com/2.2.0/`            |
| **Аутентификация**    | Необязательна (анонимно: 15 запросов/час)       |
| **Документация**      | https://ll.thespacedevs.com/docs/               |

**Используемые эндпоинты:**

| Эндпоинт                  | Метод | Назначение                      | CLI-команда                 |
|----------------------------|-------|---------------------------------|-----------------------------|
| `/launch/`                 | GET   | Список запусков                 | `launches list`             |
| `/launch/{id}/`            | GET   | Детали запуска                  | `launches info`             |
| `/launch/upcoming/`        | GET   | Предстоящие запуски             | `launches list --upcoming`  |
| `/launch/previous/`        | GET   | Прошедшие запуски               | `launches list --past`      |
| `/config/launcher/`        | GET   | Конфигурации ракет-носителей    | `rockets list`              |
| `/config/launcher/{id}/`   | GET   | Детали ракеты-носителя          | `rockets info`              |
| `/config/spacecraft/`      | GET   | Конфигурации космических кораблей | `capsules list`           |
| `/config/spacecraft/{id}/` | GET   | Детали космического корабля     | `capsules info`             |
| `/agencies/{id}/`          | GET   | Детали агентства                | `company info`              |

Обе версии фильтруют запуски для SpaceX через параметр `lsp__id=121`, а конфигурации — через `manufacturer__id=121` (Claude) или `search=SpaceX` (Gemini).

### 3. Процесс разработки

#### 3.1 Работа с Claude Opus 4.6 Thinking

Я предоставил Claude полный `implementation_plan.md` со строгими правилами: без заглушек, без остановок для вопросов, каждый файл написать полностью. Claude прочитал план и сразу начал создавать файлы фаза за фазой. Процесс был систематическим — от фазы 1 (настройка проекта) до фазы 8 (документация).

Claude завершил все 8 фаз за примерно 4 взаимодействия с пользователем. Главная проблема — баг с `vars()`: Claude использовал `vars()` для сериализации слотовых датаклассов, у которых нет `__dict__`. После предоставления вывода тестов Claude верно определил причину и заменил все вызовы `vars()` на `dataclasses.asdict()` в 5 файлах. После исправления все 63 теста прошли с **покрытием 90,02%**.

#### 3.2 Работа с Gemini 3.0 Flash

Gemini получил тот же `implementation_plan.md` с идентичными правилами. Gemini также подошёл к задаче систематически, создавая все файлы последовательно. Однако сессия разработки была значительно длиннее — около 15 взаимодействий.

Gemini столкнулся с несколькими проблемами: точка входа `spacex2` не распознавалась после установки, фильтрация SpaceX через `search=SpaceX` была менее надёжной, и тот же баг с `vars()`. Gemini потратил больше итераций на отладку аргументов командной строки и обработку ответов LL2 API. Несмотря на это, Gemini в итоге создал рабочий CLI со всеми 10 командами.

Примечательное отличие: Gemini написал docstring-и классов ошибок на русском языке (`"Базовое исключение CLI"`, `"Ошибка сетевого соединения"`), проявив осведомлённость о двуязычном требовании даже на уровне кода.

### 4. Журнал промптов и ответов

#### 4.1 Сессия с Claude

---
**Промпт #1** [Начало сессии]
**Студент:** Предоставил полный план реализации со строгими правилами.
**Claude:** Прочитал план и начал создание файлов с фазы 1. Создал настройку проекта, API-слой, модели, сервисы, CLI-команды и форматировщики.
**Результат:** Все файлы фаз 1–6 созданы за 2 взаимодействия.

---
**Промпт #2** [Продолжение]
**Студент:** «Continue»
**Claude:** Завершил фазу 7 (тестирование) — conftest.py, фикстуры, 6 файлов юнит-тестов и 5 файлов интеграционных тестов. Затем фаза 8 (документация).
**Результат:** Все файлы кода и документации созданы.

---
**Промпт #3** [Результаты тестов]
**Студент:** Предоставил вывод pytest с 13 неудачными тестами — `TypeError: vars() argument must have __dict__ attribute`.
**Claude:** Определил причину: `vars()` не работает с датаклассами `slots=True`. Исправил все 5 файлов CLI-команд на `dataclasses.asdict()`.
**Результат:** Все 63 теста пройдены, покрытие 90,02%.

---

#### 4.2 Сессия с Gemini

---
**Промпт #1** [Начало сессии]
**Студент:** Тот же план реализации и правила.
**Gemini:** Прочитал план, создал все файлы последовательно. Провёл веб-поиск структуры LL2 API. Создал ~53 файла.
**Результат:** Все файлы созданы, но требовалось исправление ряда проблем. Все 10 команд работают.

---
**Промпты #2–5** [Отладка установки]
**Студент:** Множественные промпты «Continue». Ошибка: `spacex2` не распознаётся.
**Gemini:** Исправил точку входа в pyproject.toml, переустановил пакет.
**Результат:** Точка входа заработала после переустановки.

---
**Промпт #6** [Верификация команд]
**Студент:** «Убедись, что каждая команда работает правильно.»
**Gemini:** Создал `test_commands.sh`, провёл исчерпывающую проверку, обнаружил баг `vars()`, исправил на `dataclasses.asdict()`.
**Результат:** Все команды проверены и работают после нескольких итераций исправлений.

---

### 5. Проблемы и решения

#### 5.1 Проблемы с Claude

**Проблема #1 — `vars()` на слотовых датаклассах**
- Описание: Claude использовал `vars(obj)` для конвертации датаклассов в словари, но все модели используют `slots=True`, что удаляет `__dict__`.
- Затронутые файлы: `cli/launches.py`, `cli/rockets.py`, `cli/capsules.py`, `cli/company.py`, `cli/export.py`
- Решение: Замена `vars()` на `dataclasses.asdict()` во всех 5 файлах.

**Проблема #2 — Порядок глобального флага `-o`**
- Описание: Флаг `-o` определён в main callback, поэтому должен стоять перед подкомандой.
- Решение: Обновление документации с правильным порядком флагов.

#### 5.2 Проблемы с Gemini

**Проблема #1 — `vars()` на слотовых датаклассах**
- Описание: Та же проблема, что и у Claude.
- Решение: Замена на `dataclasses.asdict()` через инлайн-импорты.

**Проблема #2 — Точка входа не распознаётся**
- Описание: После установки `spacex2` не работал как команда.
- Решение: Переустановка пакета с корректным pyproject.toml.

**Проблема #3 — Надёжность фильтрации SpaceX**
- Описание: Gemini использовал `search=SpaceX` вместо `manufacturer__id=121`, что менее надёжно.
- Решение: Подход через поиск работает, но может включать нерелевантные результаты.

### 6. Таблица сравнения

| Критерий                   | Claude Opus 4.6  | Gemini 3.0 Flash | Победитель          |
|----------------------------|------------------|-------------------|---------------------|
| Понимание контекста        | ★★★★★           | ★★★★☆            | Claude              |
| Качество кода              | ★★★★★           | ★★★★☆            | Claude              |
| Поддержка диалога          | ★★★★☆           | ★★★★★            | Gemini              |
| Обработка ошибок           | ★★★★☆           | ★★★★☆            | Ничья               |
| Креативные решения         | ★★★★☆           | ★★★★★            | Gemini              |
| Документация               | ★★★★★           | ★★★★☆            | Claude              |
| Производительность         | ★★★★★           | ★★★☆☆            | Claude              |
| Покрытие тестами           | ★★★★★           | ★★★★☆            | Claude              |
| Соответствие PEP 8         | ★★★★★           | ★★★★★            | Ничья               |
| Общая оценка               | ★★★★★           | ★★★★☆            | Claude              |

**Понимание контекста:** Claude осознал весь план реализации за один проход и создал почти корректный код с первой попытки. Gemini потребовались множественные итерации.

**Качество кода:** Код Claude чище: импорты на верхнем уровне, более богатые поля датаклассов для LL2 (`status_name`, `status_abbrev`, `location`, `image`), корректное условное форматирование в панелях.

**Поддержка диалога:** Gemini был более отзывчив к итеративной отладке, с готовностью запускал shell-команды и адаптировался.

**Креативные решения:** Gemini добавил русскоязычные docstring-и и отдельный `error_console` — продуманные решения. Также провёл веб-поиск документации LL2 API.

**Покрытие тестами:** Claude — 90,02% с 63 тестами. У Gemini меньше тестов (7 файлов против 13 у Claude).

### 7. Сравнение технических решений

| Аспект                     | Подход Claude                             | Подход Gemini                            |
|----------------------------|-------------------------------------------|------------------------------------------|
| Структура CLI              | `app.add_typer` с lazy imports, `noqa: E402` | Тот же паттерн, инлайн-комментарий      |
| Обработка ошибок           | `SpaceXCLIError`, английские docstring-и  | Та же иерархия, **русские docstring-и**  |
| Дизайн датаклассов         | Поля LL2: `status_name`, `status_abbrev`, `location`, `image` | Поля SpaceX API: `success`, `serial`, `reuse_count` |
| Организация тестов         | 13 файлов, фикстуры в `api_responses.py`  | 7 файлов, простая структура фикстур     |
| Стиль Rich UI              | Цвета статуса через словарь, колонка Flight # | Эмодзи (`✅/❌/⏳`), укороченные ID  |
| JSON-сериализация          | `dataclasses.asdict()` — импорт на верхнем уровне | `dataclasses.asdict()` — инлайн-импорты |
| Клиент API                 | `get_all()` с параметром `offset`, метод `post()` | `get_all()` без offset, нет `post()`   |
| Обработка пагинации LL2    | На основе offset: `limit` + `offset`       | Только limit, без поддержки offset      |
| Фильтрация SpaceX          | `manufacturer__id=121` (надёжно)           | `search=SpaceX` (текстовый поиск)       |
| Разделение console         | `console` (stderr) + `out_console` (stdout) | То же + `error_console` (для ошибок)   |
| Эндпоинт компании          | `AGENCY_DETAIL.format(id=121)` динамически  | Хардкод `COMPANY = "agencies/121/"`     |

### 8. Примеры работы CLI

**Claude — `launches list`:**
```
                         🚀 SpaceX Launches
┌──────────┬───────────────────────────┬──────────────────┬────────┐
│ Flight # │ Name                      │ Date (UTC)       │ Status │
├──────────┼───────────────────────────┼──────────────────┼────────┤
│ N/A      │ Falcon 9 | Starlink G12-6 │ 2026-03-04 18:30 │ Suc    │
│ N/A      │ Falcon 9 | Bandwagon-4    │ 2026-02-27 14:15 │ Suc    │
│ N/A      │ Falcon Heavy | GOES-U     │ 2026-02-20 09:00 │ Suc    │
└──────────┴───────────────────────────┴──────────────────┴────────┘
```

**Gemini — `launches list`:**
```
                         🚀 SpaceX Launches
┌──────────┬───────────────────────────┬──────────────────┬─────────┐
│ ID       │ Name                      │ Date (UTC)       │ Success │
├──────────┼───────────────────────────┼──────────────────┼─────────┤
│ 5fb4054… │ Falcon 9 | Starlink G12-6 │ 2026-03-04 18:30 │ ✅      │
│ a1b2c3d… │ Falcon 9 | Bandwagon-4    │ 2026-02-27 14:15 │ ✅      │
│ e4f5a6b… │ Falcon Heavy | GOES-U     │ 2026-02-20 09:00 │ ⏳      │
└──────────┴───────────────────────────┴──────────────────┴─────────┘
```

**Claude — `rockets list`:**
```
                        🛰️ SpaceX Rockets
┌────────────────────────┬─────────┬────────┬──────────┬───────────────┐
│ Name                   │ Variant │ Active │ Reusable │ Maiden Flight │
├────────────────────────┼─────────┼────────┼──────────┼───────────────┤
│ Falcon 9               │ Block 5 │ ✅     │ ♻️       │ 2018-05-11    │
│ Falcon Heavy           │ N/A     │ ✅     │ ♻️       │ 2018-02-06    │
│ Starship               │ N/A     │ ✅     │ ♻️       │ 2023-04-20    │
└────────────────────────┴─────────┴────────┴──────────┴───────────────┘
```

**Gemini — `rockets list`:**
```
                        🛰️ SpaceX Rockets
┌────────────────────────┬────────┬────────┬───────────┬──────────────┐
│ Name                   │ Active │ Stages │ Success % │ First Flight │
├────────────────────────┼────────┼────────┼───────────┼──────────────┤
│ Falcon 9 Block 5       │ ✅     │ 0      │ 0.0%      │ N/A          │
│ Falcon Heavy           │ ✅     │ 0      │ 0.0%      │ N/A          │
│ Starship               │ ✅     │ 0      │ 0.0%      │ N/A          │
└────────────────────────┴────────┴────────┴───────────┴──────────────┘
```

### 9. Что получилось лучше / хуже

#### Что Claude сделал лучше:
1. **Адаптация модели данных LL2** — модель `Launch` у Claude включает `status_name`, `status_abbrev`, `location` и `image`, которые точно соответствуют структуре ответов LL2.
2. **Полнота тестов** — 13 файлов тестов с покрытием юнит- и интеграционных тестов для всех групп команд.
3. **Точность первого прохода** — Claude создал почти полностью рабочий код за 2 взаимодействия.

#### Что Gemini сделал лучше:
1. **Русскоязычные docstring-и** — классы ошибок имеют docstring-и на русском: `"Базовое исключение CLI"`, `"Ошибка сетевого соединения"`.
2. **Выделенная error_console** — отдельный объект `error_console` для вывода ошибок.
3. **Самостоятельное исследование** — Gemini провёл веб-поиск документации LL2 API во время разработки.

#### Что оба сделали одинаково хорошо:
1. **Общая архитектура** — практически идентичная структура проекта с чистым разделением на подпакеты.
2. **Соответствие PEP 8** — оба создали чистый, хорошо отформатированный код, проходящий проверку `ruff`.

#### С чем оба столкнулись:
1. **`vars()` на слотовых датаклассах** — оба использовали `vars()` вместо `dataclasses.asdict()`, получив идентичные `TypeError`.
2. **Пагинация LL2** — ни одна версия не реализовала полную курсорную пагинацию (ссылки next/previous). Обе используют запросы с limit.
3. **Ограничение скорости** — анонимный лимит 15 запросов/час не обрабатывается корректно ни одной версией.

### 10. Выводы и рекомендации

В целом **Claude Opus 4.6 Thinking** показал лучшие результаты в этом сравнении. Claude доставил код более высокого качества с первой попытки, потребовал меньше итераций для достижения полностью рабочего состояния и создал более полные тесты (90% покрытия). Модели данных Claude были лучше адаптированы к структуре Launch Library 2 API.

Однако **Gemini 3.0 Flash** продемонстрировал сильные стороны в итеративной разработке и творческом решении проблем. Веб-исследование Gemini, русские docstring-и и отдельная error_console были продуманными дополнениями.

По **стратегиям промптинга**: предоставление полного плана реализации было высокоэффективным для обоих ИИ. Правило «не останавливайся, не задавай вопросов» подтолкнуло обоих к доставке полных решений. Claude извлёк больше пользы из этого подхода, обработав весь план за один проход. Gemini работал лучше с итеративными промптами и верификацией в реальном времени.

Моя **личная рекомендация** для будущих CLI-проектов: использовать Claude для начального каркаса и архитектуры, а затем Gemini для итеративной отладки. Я однозначно буду использовать ИИ-инструменты снова — они сократили работу на несколько дней до нескольких часов, даже с учётом исправления багов.

### 11. Список литературы

- Документация Launch Library 2: https://ll.thespacedevs.com/docs/
- The Space Devs: https://thespacedevs.com/
- Typer: https://typer.tiangolo.com
- Rich: https://rich.readthedocs.io
- Claude: https://www.anthropic.com/claude
- Gemini: https://deepmind.google/technologies/gemini/
- Датаклассы Python: https://docs.python.org/3/library/dataclasses.html
