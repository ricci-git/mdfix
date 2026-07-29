from pathlib import Path

from .document import Document
from .elements import Element, Heading, SourcePosition


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

    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
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

    return elements