import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from mdfix.cli import app

runner = CliRunner()

def test_lint_json_format(tmp_path: Path):
    """
    Verify that 'lint --format json' outputs valid JSON with diagnostic details.
    """
    # Create a file with a known issue (MD009 Trailing Whitespace)
    md_file = tmp_path / "test.json.md"
    content = "# Title   \nSome text."
    md_file.write_text(content)

    # Run lint with --format json
    result = runner.invoke(app, ["lint", str(md_file), "--format", "json"])

    assert result.exit_code == 1, "Exit code should be 1 when issues are found"
    
    # Parse the output as JSON
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON:\n{result.stdout}")

    # Check structure
    assert isinstance(data, list), "Root element must be a list of diagnostics"
    assert len(data) >= 1, "Should find at least one issue"

    diag = data[0]
    assert diag["rule_id"] == "MD009"
    assert diag["message"] == "Trailing whitespace found"
    assert diag["severity"] == "warning"
    assert diag["file_path"].endswith("test.json.md")
    assert diag["line_start"] == 1
    assert diag["col_start"] == 8


def test_lint_json_no_issues(tmp_path: Path):
    """
    Verify that 'lint --format json' returns an empty list when no issues found.
    """
    md_file = tmp_path / "clean.md"
    content = "# Title\nSome text.\n"
    md_file.write_text(content)

    result = runner.invoke(app, ["lint", str(md_file), "--format", "json"])

    assert result.exit_code == 0
    
    data = json.loads(result.stdout)
    assert data == [], "Expected empty list for clean file"
