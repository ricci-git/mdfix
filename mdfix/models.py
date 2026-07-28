from dataclasses import dataclass
from pathlib import Path


@dataclass
class MarkdownFile:
    path: Path
    size: int
    