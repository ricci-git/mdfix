from mdfix.diagnostics import Diagnostic, Severity


def test_diagnostic_creation():
    """
    Verify that a Diagnostic object can be created with all required fields.
    """
    diag = Diagnostic(
        rule_id="MD001",
        severity=Severity.ERROR,
        message="Heading level skipped",
        file_path="/path/to/file.md",
        line_start=10,
        col_start=5,
        line_end=10,
        col_end=20,
    )
    
    assert diag.rule_id == "MD001"
    assert diag.severity == Severity.ERROR
    assert diag.message == "Heading level skipped"
    assert diag.file_path == "/path/to/file.md"
    assert diag.line_start == 10
    assert diag.col_start == 5
    assert diag.suggestion_diff is None 

def test_severity_enum_values():
    """
    Ensure Severity enum has expected levels.
    """
    assert Severity.ERROR.value == "error"
    assert Severity.WARNING.value == "warning"
    assert Severity.INFO.value == "info"
