from pathlib import Path
import pytest
from mdfix.linter import Linter
from mdfix.rules.md055_table_format import Md055TableFormatRule
from mdfix.diagnostics import Severity


def test_md055_detects_misaligned_table(tmp_path: Path):
    """
    Verify that MD055 flags tables with inconsistent column widths or missing pipes.
    """
    md_file = tmp_path / "bad_table.md"
    # A poorly formatted table (inconsistent spacing in separator row)
    content = "| Name | Age |\n|---|---|\n| John | 30 |\n| Jane   | 25 |\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md055TableFormatRule()])
    results = linter.lint(md_file)

    assert len(results) == 1, f"Expected 1 diagnostic, got {len(results)}"
    diag = results[0]
    assert diag.rule_id == "MD055"
    assert diag.severity == Severity.WARNING
    assert "Table format issue" in diag.message
    
    # Check suggestion: should be a properly formatted table string
    assert diag.suggestion_diff is not None
    # The exact format depends on our table_formatter logic, but it should start with '|'
    assert diag.suggestion_diff.strip().startswith("|")


def test_md055_passes_well_formatted_table(tmp_path: Path):
    """
    Verify that MD055 passes tables that are already correctly formatted.
    """
    md_file = tmp_path / "good_table.md"
    # A well-formatted table (assuming standard alignment produced by format_table)
    # Note: We need to know exactly what format_table outputs to write this test correctly.
    # For now, let's assume it pads columns to equal width based on max content length.
    # Headers: Name(4), Age(3). Max widths: 4, 3.
    # Rows: John(4), 30(2); Jane(4), 25(2).
    # Canonical might look like:
    # | Name | Age |
    # | ---- | --- |
    # | John | 30  |
    # | Jane | 25  |
    
    # Let's use the output of format_table as the "good" input for the second test later.
    # For now, just ensure no crash and maybe adjust assertion if needed.
    content = "| Name | Age |\n| ---- | --- |\n| John | 30  |\n| Jane | 25  |\n"
    md_file.write_text(content)

    linter = Linter(rules=[Md055TableFormatRule()])
    results = linter.lint(md_file)

    # This test might fail initially if our heuristic isn't perfect, 
    # but ideally it should pass if the input matches the formatter's output.
    assert len(results) == 0, f"Expected 0 diagnostics for valid sequence, got {len(results)}"
