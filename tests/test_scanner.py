import tempfile

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


def test_scanner_ignores_cache_directories():
    """
    Verify that scan_markdown_files ignores .pytest_cache and __pycache__.
    This prevents noise in linting results from cached markdown files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        
        # 1. Create a valid markdown file that SHOULD be found
        valid_md = root / "readme.md"
        valid_md.write_text("# Hello World\n")
        
        # 2. Create ignored directories with markdown/text files inside
        cache_dir = root / ".pytest_cache"
        cache_dir.mkdir()
        (cache_dir / "README.md").write_text("# Cache Readme\nShould be ignored.")
        
        pycache_dir = root / "__pycache__"
        pycache_dir.mkdir()
        # Note: Usually .pyc files aren't scanned by *.md glob, 
        # but let's ensure the directory itself is skipped if logic relies on path parts
        (pycache_dir / "dummy.txt").touch() 
        
        # Run scanner
        results = list(scan_markdown_files(root))
        
        # Assertions
        assert len(results) == 1, f"Expected exactly 1 file, got {len(results)}: {[str(r.path) for r in results]}"
        
        # Check that the found file is indeed our valid one
        found_path = results[0].path
        assert found_path.name == "readme.md", f"Found wrong file name: {found_path.name}"
        
        # Explicitly check that no result comes from excluded dirs
        for res in results:
            assert ".pytest_cache" not in str(res.path), f"Cache dir leaked: {res.path}"
            assert "__pycache__" not in str(res.path), f"Pycache dir leaked: {res.path}"
