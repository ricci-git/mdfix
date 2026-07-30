from pathlib import Path

from .document import Document
from .elements import Element, Heading, Paragraph, SourcePosition


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

    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        if not stripped:
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

            continue

        if stripped.startswith("#"):
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

        if paragraph_start_line is None:
            paragraph_start_line = line_number

        paragraph_lines.append(stripped)

    if paragraph_lines:
        elements.append(
            Paragraph(
                text="\n".join(paragraph_lines),
                position=SourcePosition(
                    line=paragraph_start_line,
                ),
            )
        )

    return elements