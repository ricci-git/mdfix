from pathlib import Path

from mdfix.diagnostics import Severity
from mdfix.linter import Linter
from mdfix.rules.md030_list_spacing import Md030ListSpacingRule


def test_md030_detects_missing_space_in_unordered_list(tmp_path: Path):
    """
    Verify that MD030 flags unordered list items without a space after the marker.
    Examples: '-Item', '*Item', '+Item'.
    """
    md_file = tmp_path / "bad_list.md"
    content = "-Item\n*Another\n+Third\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md030ListSpacingRule()])
    results = linter.lint(md_file)

    assert len(results) == 3, f"Expected 3 diagnostics, got {len(results)}"
    
    for i, diag in enumerate(results):
        assert diag.rule_id == "MD030"
        assert diag.severity == Severity.WARNING
        assert "Missing space after list marker" in diag.message
        
        # Expected corrections
        expected_suggestions = ["- Item", "* Another", "+ Third"]
        assert diag.suggestion_diff == expected_suggestions[i]


def test_md030_passes_correct_lists(tmp_path: Path):
    """
    Verify that MD030 passes lists with proper spacing.
    """
    md_file = tmp_path / "good_list.md"
    content = "- Item\n* Another\n+ Third\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md030ListSpacingRule()])
    results = linter.lint(md_file)

    assert len(results) == 0
