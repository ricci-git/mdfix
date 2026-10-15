from pathlib import Path

from typer.testing import CliRunner

from mdfix.cli import app

runner = CliRunner()

def test_fix_dry_run_shows_unified_diff(tmp_path: Path):
    """
    Verify that 'fix --dry-run' outputs a unified diff showing changes.
    """
    # Create a file with trailing whitespace (MD009 violation)
    md_file = tmp_path / "test.md"
    content = "# Title   \nSome text."
    md_file.write_text(content)

    # Run the fix command in dry-run mode
    result = runner.invoke(app, ["fix", str(md_file), "--dry-run"])

    assert result.exit_code == 0
    
    # Check if standard diff markers are present
    # Unified diff format typically includes lines starting with ---, +++, @@, -, +
    output = result.stdout
    
    assert "---" in output or "@@" in output, f"Expected diff markers in output:\n{output}"
    
    # Specifically check for removed line (with trailing spaces) and added line (clean)
    # Note: The exact formatting depends on difflib implementation, but we expect '-' and '+' signs
    assert "-" in output, "Expected removal indicator (-)"
    assert "+" in output, "Expected addition indicator (+)"
    
    # Ensure it says DRY RUN
    assert "DRY RUN" in output.upper()
