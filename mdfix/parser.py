from pathlib import Path

from .document import Document
from .elements import (
    Element,
    Heading,
    List,
    Paragraph,
    SourcePosition,
)


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

    lines = content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            flush_list()

            level = len(stripped) - len(stripped.lstrip("#"))

            if level > 6:
                continue

            title = stripped[level:].strip()

            elements.append(
                Heading(
                    level=level,
                    title=title,
                    position=SourcePosition(line=line_number),
                )
            )

            continue

        if stripped.startswith("- "):
            flush_paragraph()

            if list_start_line is None:
                list_start_line = line_number

            list_ordered = False
            list_items.append(stripped[2:].strip())

            continue

        if (
            len(stripped) > 2
            and stripped[0].isdigit()
            and stripped[1:3] == ". "
        ):
            flush_paragraph()

            if list_start_line is None:
                list_start_line = line_number

            list_ordered = True
            list_items.append(stripped[3:].strip())

            continue

        flush_list()

        if paragraph_start_line is None:
            paragraph_start_line = line_number

        paragraph_lines.append(stripped)

    flush_list()
    flush_paragraph()

    return elements