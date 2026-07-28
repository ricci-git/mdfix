# mdfix

Markdown document fixer and formatter.

`mdfix` is a CLI tool designed to analyze, validate and automatically fix Markdown documents according to predefined rules.

The project focuses on reliable document maintenance through structured parsing instead of direct text replacement.

## Current Status

Version: `0.5.0`

- *Implemented:

- Markdown file scanner
- Document model
- Markdown parser foundation
- Basic test coverage

## Architecture

- *Current processing pipeline:

```text

Markdown file
|
v
Scanner
|
v
MarkdownFile
|
v
Parser
|
v
Document

```

- *Future architecture:

```text

Markdown file
|
v
Parser
|
v
Markdown AST
|
+----------------+
| |
v v
Validators Fixers
| |
+-------+--------+
|
v
Updated Markdown

```

## Features Roadmap

Planned features:

- Heading hierarchy validation
- Automatic heading level correction
- Section numbering validation
- Markdown lint fixes
- Table formatting
- Separator cleanup
- Unknown word dictionary management
- Custom project dictionaries

## Installation

- *Development installation:

```bash

git clone <repository>
cd mdfix

python -m venv .venv
source .venv/bin/activate

pip install -e .

```

## Usage

- *Scan Markdown files:

mdfix scan .

- *Show version:

mdfix version

## Development

- *Run tests:

pytest

## Project Structure

mdfix/
├── cli.py
├── models.py
├── document.py
├── elements.py
├── scanner.py
├── parser.py
└── version.py

tests/
├── test_scanner.py
├── test_document.py
└── test_parser.py

## Design Principles

- Small isolated components
- Test-driven development
- Explicit document structure
- Safe automated modifications
- Extensible validation rules

## License

MIT License
