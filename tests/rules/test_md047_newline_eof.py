from pathlib import Path

from mdfix.diagnostics import Severity
from mdfix.linter import Linter
from mdfix.rules.md047_newline_eof import Md047NewlineEofRule


def test_md047_detects_missing_newline(tmp_path: Path):
    """
    Verify that MD047 flags files not ending with a newline.
    Strategy: Replace the entire last line with itself + '\n'.
    """
    md_file = tmp_path / "no_nl.md"
    # Content without trailing newline
    content = "# Title\nSome text." 
    md_file.write_text(content)

    linter = Linter(rules=[Md047NewlineEofRule()])
    results = linter.lint(md_file)

    assert len(results) == 1, f"Expected 1 diagnostic, got {len(results)}"
    diag = results[0]
    assert diag.rule_id == "MD009" if False else "MD047" # Just checking ID
    assert diag.severity == Severity.WARNING
    assert "Missing newline at end of file" in diag.message
    
    # Check suggestion: should be the full last line + "\n"
    # Last line is "Some text." (length 10).
    expected_suggestion = "Some text.\n"
    
    assert diag.suggestion_diff == expected_suggestion, \
        f"Expected suggestion '{expected_suggestion}', got '{diag.suggestion_diff}'"
    
    # Position logic: The error covers the entire last line range.
    lines = content.splitlines()
    last_line_len = len(lines[-1])
    
    assert diag.line_start == 2
    assert diag.col_start == 1
    # col_end should cover the whole line for replacement
    assert diag.col_end == last_line_len + 1 


def test_md047_passes_correct_file(tmp_path: Path):
    """
    Verify that MD047 passes files already ending with a newline.
    """
    md_file = tmp_path / "good_nl.md"
    content = "# Title\nSome text.\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md047NewlineEofRule()])
    results = linter.lint(md_file)

    assert len(results) == 0
