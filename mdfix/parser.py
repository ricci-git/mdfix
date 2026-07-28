from pathlib import Path

from .document import Document


def parse_markdown(path: Path) -> Document:
    content = path.read_text(encoding="utf-8")

    return Document(
        path=path,
        content=content,
    )