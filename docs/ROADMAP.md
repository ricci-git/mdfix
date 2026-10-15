---
Title:  "mdfix Roadmap"
Code:   "RM-MDFIX-001"
Version: "1.0.0"
Status:  "active"
Description: "Strategic development plan for the mdfix project."
Owner:  "Ricci"
Layer:  "Project Management"
Type:   "Planning"
Document Class: "Public"
Audience: "Developers, Contributors, Users"
Canonical Language: uk
Translations: en
Created: 2026-10-15
Last Updated: 2026-10-15
Reviewers: ["AI Assistant"]
Approved By: ["Ricci"]
Related Documents: ["docs/BACKLOG.md", "docs/TASKS.md", "CHANGELOG.md"]
Related ADRs: []
---

## mdfix Roadmap

## Українська версія

### Візія

Створити найнадійніший, швидкий та сумісний із стандартами інструмент для автоматичного виправлення Markdown-документів, який полегшує життя розробникам та технічним письменникам.

### Поточний статус

**Версія:** v0.9.0 (Stable MVP)
**Етап:** Завершено Milestone 4 (Product Polish & CI/CD).

### Milestones

#### ✅ Milestone 0: Repo Hygiene (Завершено)

* Синхронізація версій.
* Фікс сканера (виключення кешів).
* Базова структура тестів.

#### ✅ Milestone 1: Diagnostics Core (Завершено)

* Модель `Diagnostic`.
* Рушій `Linter`.
* Перші правила: MD001, MD009, MD047, MD055.
* Команда CLI `lint`.

#### ✅ Milestone 2: Auto-fix Engine (Завершено)

* Модуль `Patcher` (bottom-up logic).
* Підтримка мультилайнових замін (таблиці).
* Команда CLI `fix` з `--dry-run`.

#### ✅ Milestone 3: Rule Registry & Stability (Завершено)

* Рефакторинг правил через `registry.py`.
* Стабілізація ядра парсингу.
* Dogfooding на власній документації.

#### ✅ Milestone 4: Product Polish & Infrastructure (Завершено)

* Unified Diff View для безпеки.
* Конфігурація через `pyproject.toml`.
* JSON Output для CI/CD.
* GitHub Actions Pipeline.
* Нові правила: MD018, MD030.

#### 🚀 Milestone 5: Standard Compliance (Поточний етап)

* **Мета:** Досягти максимальної сумісності зі стандартом `markdownlint`.
* **Ключові задачі:**
  * Імплементація Групи A правил (Easy Wins): MD012, MD022, MD026, MD031, MD032, MD034, MD037-039, MD058, MD060.
  * Розширення конфігурації для налаштування параметрів правил (напр., довжина рядка для MD013).
  * Покриття тестами нових правил (>200 тестів).
* **Результат:** mdfix стає альтернативою markdownlint для автофіксу.

#### 🔮 Milestone 6: Performance & DX (Планується)

* Оптимізація парсингу великих документів (>1MB).
* Паралельна обробка файлів у директоріях.
* Інтеграція з редакторами коду (VS Code Extension prototype).
* Prettier-like форматування (повна переформатація стилю, а не лише виправлення помилок).

#### 🏁 Milestone 7: Release v1.0.0 (Планується)

* Повна документація API.
* Стабілізація після тривалого використання.
* Публікація на PyPI.
* Маркетинг та залучення перших контріб'юторів.

---

## English Translation

## en mdfix Roadmap

### en Vision

To create the most reliable, fast, and standards-compliant tool for automatic Markdown fixing, easing life for developers and technical writers.

### en Current Status

**Version:** v0.9.0 (Stable MVP)
**Stage:** Completed Milestone 4 (Product Polish & CI/CD).

### en Milestones

#### ✅ Milestone 0: Repo Hygiene (Done)

* Version synchronization.
* Scanner fix (cache exclusions).
* Basic test structure.

#### ✅ Milestone 1: Diagnostics Core (Done)

* `Diagnostic` model.
* `Linter` engine.
* First rules: MD001, MD009, MD047, MD055.
* CLI command `lint`.

#### ✅ Milestone 2: Auto-fix Engine (Done)

* `Patcher` module (bottom-up logic).
* Multi-line replacement support (tables).
* CLI command `fix` with `--dry-run`.

#### ✅ Milestone 3: Rule Registry & Stability (Done)

* Refactoring rules via `registry.py`.
* Parsing core stabilization.
* Dogfooding on own documentation.

#### ✅ Milestone 4: Product Polish & Infrastructure (Done)

* Unified Diff View for safety.
* Configuration via `pyproject.toml`.
* JSON Output for CI/CD.
* GitHub Actions Pipeline.
* New rules: MD018, MD030.

#### 🚀 Milestone 5: Standard Compliance (Current)

* **Goal:** Achieve maximum compatibility with `markdownlint` standard.
* **Key Tasks:**
  * Implement Group A rules (Easy Wins): MD012, MD022, MD026, MD031, MD032, MD034, MD037-039, MD058, MD060.
  * Extend configuration for rule parameters (e.g., line length for MD013).
  * Test coverage for new rules (>200 tests).
* **Result:** mdfix becomes an alternative to markdownlint for auto-fixing.

#### 🔮 Milestone 6: Performance & DX (Planned)

* Optimize parsing for large documents (>1MB).
* Parallel file processing in directories.
* Editor integration (VS Code Extension prototype).
* Prettier-like formatting (full style reformatting, not just error fixing).

#### 🏁 Milestone 7: Release v1.0.0 (Planned)

* Full API documentation.
* Stabilization after long-term usage.
* Publication on PyPI.
* Marketing and attracting first contributors.

---

### Version History

| Version | Date       | Author      | Changes                                                                 |
| ------- | ---------- | ----------- | ----------------------------------------------------------------------- |
| 1.0.0   | 2026-10-15 | Ricci/AI    | Initial roadmap creation reflecting v0.9.0 state and future plans.      |
