from pathlib import Path

from mdfix.cli import run_lint_logic
from mdfix.diagnostics import Severity


def test_run_lint_logic_finds_errors(tmp_path: Path):
    """
    Verify that the core linting logic returns diagnostics for bad markdown.
    """
    md_file = tmp_path / "bad.md"
    # H1 -> H3 skip (MD001 violation)
    content = "# Title\n### Subtitle\n"
    md_file.write_text(content)
    
    results = run_lint_logic(md_file)
    
    assert len(results) == 1
    assert results[0].rule_id == "MD001"
    assert results[0].severity == Severity.WARNING
    assert str(md_file.resolve()) in results[0].file_path

def test_run_lint_logic_clean_file(tmp_path: Path):
    """
    Verify that the core linting logic returns empty list for good markdown.
    """
    md_file = tmp_path / "good.md"
    content = "# Title\n## Section\n"
    md_file.write_text(content)
    
    results = run_lint_logic(md_file)
    
    assert len(results) == 0
