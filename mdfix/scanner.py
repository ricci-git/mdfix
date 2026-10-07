from pathlib import Path

from .models import MarkdownFile

DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "node_modules",
    ".pytest_cache",  # Fixed in M0
    "__pycache__",    # Fixed in M0
    "build",          # Fixed in M0
    "dist"            # Fixed in M0
}


def scan_markdown_files(
    root: Path,
) -> list[MarkdownFile]:
    files = []
    
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
