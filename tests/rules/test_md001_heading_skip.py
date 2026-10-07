from pathlib import Path

from mdfix.diagnostics import Severity
from mdfix.linter import Linter
from mdfix.rules.md001_heading_skip import Md001HeadingSkipRule


def test_md001_detects_heading_level_skip(tmp_path: Path):
    """
    Verify that MD001 flags a heading level skip (e.g., H1 -> H3).
    """
    md_file = tmp_path / "bad_headings.md"
    # Skips H2: # Title -> ### Subtitle
    content = "# Title\n### Subtitle\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md001HeadingSkipRule()])
    results = linter.lint(md_file)

    assert len(results) == 1, f"Expected 1 diagnostic, got {len(results)}"
    diag = results[0]
    assert diag.rule_id == "MD001"
    assert diag.severity == Severity.WARNING
    assert "Heading level skipped" in diag.message
    # The error should point to the line with ### (line 2)
    assert diag.line_start == 2


def test_md001_passes_valid_sequence(tmp_path: Path):
    """
    Verify that MD001 does not flag valid sequences (H1 -> H2 -> H3).
    """
    md_file = tmp_path / "good_headings.md"
    content = "# Title\n## Section\n### Subsection\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md001HeadingSkipRule()])
    results = linter.lint(md_file)

    assert len(results) == 0, f"Expected 0 diagnostics for valid sequence, got {len(results)}"
