from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Document:
    path: Path
    content: str
    elements: list = field(default_factory=list)