from pathlib import Path

from mdfix.diagnostics import Severity
from mdfix.linter import Linter
from mdfix.rules.md009_trailing_whitespace import Md009TrailingWhitespaceRule


def test_md009_detects_trailing_spaces(tmp_path: Path):
    """
    Verify that MD009 flags lines ending with spaces.
    """
    md_file = tmp_path / "bad_ws.md"
    # Line 1 has trailing space, Line 2 is clean
    content = "# Title \nClean line\n" 
    md_file.write_text(content)

    linter = Linter(rules=[Md009TrailingWhitespaceRule()])
    results = linter.lint(md_file)

    assert len(results) == 1, f"Expected 1 diagnostic, got {len(results)}"
    diag = results[0]
    assert diag.rule_id == "MD009"
    assert diag.severity == Severity.WARNING
    assert "Trailing whitespace" in diag.message
    # Should point to line 1
    assert diag.line_start == 1
    
    # CRITICAL: Check if it suggests a fix
    assert diag.suggestion_diff is not None, "MD009 should provide an auto-fix suggestion"
    # The suggestion should be empty string to remove the whitespace at the end of the detected range
    # Or specifically the replacement text for the offending part.
    # For simplicity in our patcher logic which replaces [col_start:col_end], 
    # if we detect "Title ", col_start=7, col_end=8 (assuming 1-based inclusive/exclusive mix needs care).
    # Let's assume the rule identifies the exact span of whitespace.
    

def test_md009_passes_clean_lines(tmp_path: Path):
    """
    Verify that MD009 does not flag lines without trailing whitespace.
    """
    md_file = tmp_path / "good_ws.md"
    content = "# Title\nClean line\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md009TrailingWhitespaceRule()])
    results = linter.lint(md_file)

    assert len(results) == 0
