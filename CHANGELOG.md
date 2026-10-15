---
Title:  "Changelog for mdfix"
Code:   "CHANGELOG"
Version: "1.0.0"
Status:  "active"
Description: "Notable changes to this project, formatted according to Keep a Changelog."
Owner:  "Ricci"
Layer:  "Project Documentation"
Type:   "Reference"
Document Class: "Public"
Audience: "Users, Developers, Contributors"
Canonical Language: uk
Translations: en
Created: 2026-10-15
Last Updated: 2026-10-15
Reviewers: ["AI Assistant"]
Approved By: ["Ricci"]
Related Documents: ["README.md", "docs/PROJECT_STATE.md"]
Related ADRs: []
---

## Changelog

Усі помітні зміни в цьому проєкті документуються у цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
і цей проєкт дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-*(Порожній розділ для майбутніх змін)*

## [0.9.0] - 2026-10-15

### Added

- **Нові правила літингу:**
  - MD018: Відсутність пробілу після хеша в ATX-заголовках (`#Title` -> `# Title`). Підтримка автофіксу.
  - MD030: Пробіли навколо маркерів списків (`-Item` -> `- Item`). Підтримка автофіксу.
- **Конфігурація:**
  - Підтримка вимкнення правил через секцію `[tool.mdfix]` у файлі `pyproject.toml`.
  - Приклад: `disable = ["MD055"]`.
- **CLI Функціональність:**
  - Unified Diff view для команди `fix --dry-run`. Тепер користувач бачить точні зміни перед записом.
  - JSON output format для команди `lint --format json`. Інтеграція з CI/CD та редакторами коду.
- **Інфраструктура:**
  - GitHub Actions CI pipeline (автоматичний запуск `ruff check` та `pytest`).
  - Оновлення залежностей до безпечних версій (Typer >= 0.27, Rich >= 15.0, Pytest >= 9.1).

### Changed

- Рефакторинг Rule Registry (`registry.py`) для підтримки динамічної фільтрації правил.
- Покращена логіка Patcher'а (`patcher.py`) для багаторядкових замін (multi-line replacements), що дозволило коректно виправляти таблиці (MD055).

### Fixed

- Виправлено діапазон заміни для правил MD018 та MD030, щоб уникнути дублювання маркерів при автофіксі.
- Видалено зайві пробіли в кінцях рядків (trailing whitespace) у документації проєкту за допомогою самого `mdfix`.

## [0.8.3] - 2026-10-07

### Added (DUP HEADING)

- Початковий стабільний прототип із підтримкою Inline AST парсингу.
- Базовий Scanner та Block Parser.
- Перші правила літингу: MD001 (Heading Skip), MD009 (Trailing Whitespace), MD047 (Newline at EOF), MD055 (Table Format).
- Команди CLI `lint` та `fix` (базова реалізація).

---

## English Translation

## en Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## en [Unreleased]

-*(Empty section for future changes)*

## en [0.9.0] - 2026-10-15

### en Added

- **New Linting Rules:**
  - MD018: No space after hash on atx style heading (`#Title` -> `# Title`). Auto-fix supported.
  - MD030: Spaces around list markers (`-Item` -> `- Item`). Auto-fix supported.
- **Configuration:**
  - Support for disabling rules via `[tool.mdfix]` section in `pyproject.toml`.
  - Example: `disable = ["MD055"]`.
- **CLI Features:**
  - Unified Diff view for `fix --dry-run` command. Users can now see exact changes before writing to disk.
  - JSON output format for `lint --format json` command. Enables integration with CI/CD pipelines and code editors.
- **Infrastructure:**
  - GitHub Actions CI pipeline (automated `ruff check` and `pytest` execution).
  - Dependency updates to secure versions (Typer >= 0.27, Rich >= 15.0, Pytest >= 9.1).

### en Changed

- Refactored Rule Registry (`registry.py`) to support dynamic rule filtering.
- Improved Patcher logic (`patcher.py`) for multi-line replacements, enabling correct auto-fixing of tables (MD055).

### en Fixed

- Corrected replacement range for MD018 and MD030 rules to prevent marker duplication during auto-fix.
- Removed trailing whitespace from project documentation files using `mdfix` itself.

## en [0.8.3] - 2026-10-07

### en Added (DUP HEADING)

- Initial stable prototype with Inline AST parsing support.
- Basic Scanner and Block Parser implementation.
- First linting rules: MD001 (Heading Skip), MD009 (Trailing Whitespace), MD047 (Newline at EOF), MD055 (Table Format).
- CLI commands `lint` and `fix` (basic implementation).

---

### Version History

| Version | Date       | Author      | Changes                                                                          |
| ------- | ---------- | ----------- | -------------------------------------------------------------------------------- |
| 1.0.0   | 2026-10-15 | Ricci/AI    | Initial creation of changelog reflecting v0.9.0 state. Added UK/EN translations. |

---
