from pathlib import Path

from mdfix.models import MarkdownFile
from mdfix.scanner import scan_markdown_files


def test_scan_markdown_files(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Test")

    files = scan_markdown_files(tmp_path)

    assert len(files) == 1
    assert isinstance(files[0], MarkdownFile)
    assert files[0].path.name == "README.md"


def test_scan_ignores_git_directory(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()

    (git_dir / "hidden.md").write_text("# Hidden")
    (tmp_path / "visible.md").write_text("# Visible")

    files = scan_markdown_files(tmp_path)

    names = [file.path.name for file in files]

    assert "visible.md" in names
    assert "hidden.md" not in names