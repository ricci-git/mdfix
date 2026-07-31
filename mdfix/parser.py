from pathlib import Path

from .document import Document
from .elements import (
    CodeBlock,
    Element,
    Heading,
    List,
    Paragraph,
    SourcePosition,
)


def heading_level(line: str) -> int | None:
    if not line.startswith("#"):
        return None

    level = len(line) - len(line.lstrip("#"))

    if level > 6:
        return None

    return level


def parse_unordered_list_item(line: str) -> str | None:
    if line.startswith("- "):
        return line[2:].strip()

    return None


def parse_ordered_list_item(line: str) -> str | None:
    if (
        len(line) > 2
        and line[0].isdigit()
        and line[1:3] == ". "
    ):
        return line[3:].strip()

    return None


def is_code_fence(line: str) -> bool:
    return line.startswith("```")


def code_fence_language(line: str) -> str | None:
    if not is_code_fence(line):
        return None

    language = line[3:].strip()

    if not language:
        return None

    return language


def parse_markdown(path: Path) -> Document:
    content = path.read_text(encoding="utf-8")

    document = Document(
        path=path,
        content=content,
    )

    document.elements = parse_elements(content)

    return document


def parse_elements(content: str) -> list[Element]:
    elements: list[Element] = []

    paragraph_lines: list[str] = []
    paragraph_start_line: int | None = None

    list_items: list[str] = []
    list_ordered: bool | None = None
    list_start_line: int | None = None

    in_code_block = False
    code_language: str | None = None
    code_lines: list[str] = []
    code_start_line: int | None = None

    def flush_paragraph():
        nonlocal paragraph_lines, paragraph_start_line

        if paragraph_lines:
            elements.append(
                Paragraph(
                    text="\n".join(paragraph_lines),
                    position=SourcePosition(
                        line=paragraph_start_line,
                    ),
                )
            )

            paragraph_lines = []
            paragraph_start_line = None

    def flush_list():
        nonlocal list_items, list_ordered, list_start_line

        if list_items:
            elements.append(
                List(
                    ordered=list_ordered is True,
                    items=list_items,
                    position=SourcePosition(
                        line=list_start_line,
                    ),
                )
            )

            list_items = []
            list_ordered = None
            list_start_line = None

    def flush_code_block():
        nonlocal in_code_block, code_language, code_lines, code_start_line

        if code_start_line is None:
            return

        elements.append(
            CodeBlock(
                language=code_language,
                code="\n".join(code_lines),
                position=SourcePosition(
                    line=code_start_line,
                ),
            )
        )

        in_code_block = False
        code_language = None
        code_lines = []
        code_start_line = None

    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        if in_code_block:
            if is_code_fence(stripped):
                flush_code_block()
            else:
                code_lines.append(line)

            continue

        if is_code_fence(stripped):
            flush_paragraph()
            flush_list()

            in_code_block = True
            code_language = code_fence_language(stripped)
            code_lines = []
            code_start_line = line_number

            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        level = heading_level(stripped)

        if level is not None:
            flush_paragraph()
            flush_list()

            elements.append(
                Heading(
                    level=level,
                    title=stripped[level:].strip(),
                    position=SourcePosition(
                        line=line_number,
                    ),
                )
            )

            continue

        item = parse_unordered_list_item(stripped)

        if item is not None:
            flush_paragraph()

            if list_start_line is None:
                list_start_line = line_number

            list_ordered = False
            list_items.append(item)

            continue

        item = parse_ordered_list_item(stripped)

        if item is not None:
            flush_paragraph()

            if list_start_line is None:
                list_start_line = line_number

            list_ordered = True
            list_items.append(item)

            continue

        flush_list()

        if paragraph_start_line is None:
            paragraph_start_line = line_number

        paragraph_lines.append(stripped)

    if in_code_block:
        flush_code_block()

    flush_list()
    flush_paragraph()

    return elements