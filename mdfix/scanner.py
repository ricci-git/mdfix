from pathlib import Path

from .models import MarkdownFile

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "node_modules",
    ".pytest_cache",  # Ignore pytest cache directory
    "__pycache__",    # Ignore Python bytecode cache directory
    "build",          # Standard build artifacts
    "dist"            # Standard distribution artifacts
}


def scan_markdown_files(
    root: Path,
) -> list[MarkdownFile]:
    files = []
    
    # Оптимізація: rglob повертає генератор, але ми збираємо в список
    # Логіка фільтрації залишається тією ж, але тепер вона ловить нові директорії
    for path in root.rglob("*.md"):
        if any(
            part in DEFAULT_EXCLUDES
            for part in path.parts
        ):
            continue
        
        files.append(
            MarkdownFile(
                path=path,
                size=path.stat().st_size,
            )
        )
        
    return files
