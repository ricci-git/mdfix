from pathlib import Path

from mdfix.diagnostics import Severity
from mdfix.linter import Linter
from mdfix.rules.md018_heading_space import Md018HeadingSpaceRule


def test_md018_detects_missing_space_after_hash(tmp_path: Path):
    """
    Verify that MD018 flags headings without a space after the hash symbols.
    Example: '#Title' should be flagged.
    """
    md_file = tmp_path / "bad_heading.md"
    content = "#Title\n##Subheading\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md018HeadingSpaceRule()])
    results = linter.lint(md_file)

    assert len(results) == 2, f"Expected 2 diagnostics, got {len(results)}"
    
    # Check first diagnostic (#Title)
    diag1 = results[0]
    assert diag1.rule_id == "MD018"
    assert diag1.severity == Severity.WARNING
    assert "No space after hash" in diag1.message
    assert diag1.line_start == 1
    
    # Suggestion should add a space: "# Title"
    assert diag1.suggestion_diff == "# Title"

    # Check second diagnostic (##Subheading)
    diag2 = results[1]
    assert diag2.line_start == 2
    assert diag2.suggestion_diff == "## Subheading"


def test_md018_passes_correct_headings(tmp_path: Path):
    """
    Verify that MD018 passes headings with proper spacing.
    """
    md_file = tmp_path / "good_heading.md"
    content = "# Title\n## Subheading\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md018HeadingSpaceRule()])
    results = linter.lint(md_file)

    assert len(results) == 0
