from dataclasses import dataclass, field
from pathlib import Path

from .elements import Element


@dataclass(slots=True)
class Document:
    path: Path
    content: str
    elements: list[Element] = field(default_factory=list)