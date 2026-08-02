---
Title: mdfix — Markdown Document Fixer and Formatter
Code: README
Version: 0.7.0
Status: Active

Owner: mdfix Project
Layer: Project Documentation
Type: Overview
Document Class: Public Documentation
Audience: Users, Developers, Contributors

Canonical Language: uk
Translations: en

Created: 2026-08-02
Last Updated: 2026-08-02

Related Documents:
- docs/INLINE_AST_DESIGN.md

Related ADRs:
- None
---

## mdfix

- **Українська версія**

## Призначення

`mdfix` — це CLI-інструмент для аналізу, перевірки та автоматичного виправлення Markdown-документів відповідно до визначених правил.

Проєкт використовує структурний підхід до обробки документів через побудову моделей документа та AST замість прямої заміни тексту.

Основна мета — створити безпечний, розширюваний та передбачуваний інструмент для підтримки якості Markdown-документів.

---

## Поточний статус

Версія:

0.7.0

**Реалізовано:**

- Markdown file scanner
- Document model
- Markdown parser foundation
- Block AST elements
- Heading parsing
- Paragraph parsing
- Lists
- Block quotes
- Code blocks
- Horizontal rules
- Tables
- Inline AST foundation
- Automated test coverage

**Поточний стан тестів:**

45 tests passed

---

## Архітектура

**Поточний pipeline:**

```text
Markdown file
      |
      v
   Scanner
      |
      v
    Parser
      |
      v
  Document Model
      |
      +----------------+
      |                |
      v                v
 Block AST        Inline AST
```

Block AST відповідає за структурні елементи документа.

Inline AST відповідає за внутрішній вміст текстових елементів:

```text

    text

    strong

    emphasis

    inline code

    links
```

**Детальний опис:**

- docs/INLINE_AST_DESIGN.md

## Заплановані можливості

Roadmap:

```text

    Heading hierarchy validation

    Automatic heading correction

    Section numbering validation

    Markdown lint fixes

    Table formatting

    Separator cleanup

    Unknown word dictionary management

    Custom project dictionaries

    Full inline Markdown parser

    AST-based document transformations
```

## Встановлення

**Development installation:**

```bash

git clone <https://github.com/ricci-git/mdfix.git>

cd mdfix

python -m venv .venv

source .venv/bin/activate

pip install -e .

```

## Використання

**Сканування Markdown-файлів:**

```bash

mdfix scan .
```

**Перевірка версії:**

```bash

mdfix version

```

## Розробка

**Запуск тестів:**

```bash

pytest

```

**Перевірка стилю:**

```bash

ruff check .

```

## Структура проєкту

```text

mdfix/
├── cli.py
├── document.py
├── elements.py
├── inline_elements.py
├── models.py
├── parser.py
├── scanner.py
└── version.py
```

**Тести:**

```text

tests/
├── test_document.py
├── test_elements.py
├── test_inline_elements.py
├── test_parser.py
└── test_scanner.py
```

## Принципи дизайну

```text

    Small isolated components

    Test-driven development

    Explicit document structure

    Safe automated modifications

    Extensible validation rules

    Documentation as part of development process
```

## Ліцензія

MIT License

---

## English Translation

## Purpose

mdfix is a CLI tool for analyzing, validating and automatically fixing Markdown documents according to predefined rules.

The project uses a structured document processing approach based on document models and AST instead of direct text replacement.

The main goal is to provide a safe, extensible and predictable tool for maintaining Markdown document quality.

## Current Status

**Version:**

0.7.0

**Implemented:**

```text

    Markdown file scanner

    Document model

    Markdown parser foundation

    Block AST elements

    Heading parsing

    Paragraph parsing

    Lists

    Block quotes

    Code blocks

    Horizontal rules

    Tables

    Inline AST foundation

    Automated test coverage
```

**Current test status:**

45 tests passed

## Architecture

**Current pipeline:**

```text

Markdown file
      |
      v
   Scanner
      |
      v
    Parser
      |
      v
 Document Model
      |
      +----------------+
      |                |
      v                v
 Block AST        Inline AST

```

Block AST represents document-level structures.

**Inline AST represents internal content of text elements:**

```text

    text

    strong

    emphasis

    inline code

    links

```

**Detailed design:**

- docs/INLINE_AST_DESIGN.md

## Planned Features

**Roadmap:**

```text

    Heading hierarchy validation

    Automatic heading correction

    Section numbering validation

    Markdown lint fixes

    Table formatting

    Separator cleanup

    Unknown word dictionary management

    Custom project dictionaries

    Full inline Markdown parser

    AST-based document transformations

```

## Installation

**Development installation:**

```bash

git clone <https://github.com/ricci-git/mdfix.git>

cd mdfix

python -m venv .venv

source .venv/bin/activate

pip install -e .

```

## Usage

**Scan Markdown files:**

```bash

mdfix scan .

```

**Show version:**

```bash

mdfix version

```

## Development

**Run tests:**

```bash

pytest

```

**Check code quality:**

```bash

ruff check .

```

## Project Structure

```text

mdfix/
├── cli.py
├── document.py
├── elements.py
├── inline_elements.py
├── models.py
├── parser.py
├── scanner.py
└── version.py

```

**Tests:**

```text

tests/
├── test_document.py
├── test_elements.py
├── test_inline_elements.py
├── test_parser.py
└── test_scanner.py

```

## Design Principles

``` text

    Small isolated components

    Test-driven development

    Explicit document structure

    Safe automated modifications

    Extensible validation rules

    Documentation as part of development process

```

## License

MIT License
