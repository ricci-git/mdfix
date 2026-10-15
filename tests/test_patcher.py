from mdfix.diagnostics import Diagnostic, Severity
from mdfix.patcher import apply_fixes


def test_apply_single_line_replacement():
    """
    Verify that a single line replacement works correctly.
    """
    original_content = "# Title\nSome text.\nAnother line."
    
    # Simulate a diagnostic suggesting to replace line 2 ("Some text.") with "Fixed text."
    diag = Diagnostic(
        rule_id="TEST001",
        severity=Severity.ERROR,
        message="Fix this line",
        file_path="/fake/path.md",
        line_start=2,
        col_start=1,
        line_end=2,
        col_end=11, # Length of "Some text." + newline handling logic might vary
        suggestion_diff="Fixed text.", # Simplified for test: just the new content for the range
    )
    
    # We need a way to pass fixes. Let's assume apply_fixes takes content and list of diagnostics with suggestions.
    # But wait, our current Diagnostic model doesn't strictly enforce how the fix is represented.
    # For MVP, let's say suggestion_diff contains the NEW TEXT for the specified range.
    
    fixed_content = apply_fixes(original_content, [diag])
    
    assert fixed_content == "# Title\nFixed text.\nAnother line."

def test_apply_multiple_fixes_bottom_up_order():
    """
    Verify that applying multiple fixes preserves indices by processing bottom-up.
    If we processed top-down, changing line 2 would shift line 3, making its old index invalid.
    """
    original_content = "Line 1\nLine 2\nLine 3"
    
    # Fix Line 3 first (in terms of position), then Line 1
    # But in the list, they can be in any order. The patcher MUST sort them or process reverse.
    
    diag_3 = Diagnostic(
        rule_id="T1", severity=Severity.ERROR, message="",
        file_path="/f", line_start=3, col_start=1, line_end=3, col_end=7,
        suggestion_diff="Line 3 FIXED"
    )
    
    diag_1 = Diagnostic(
        rule_id="T2", severity=Severity.ERROR, message="",
        file_path="/f", line_start=1, col_start=1, line_end=1, col_end=7,
        suggestion_diff="Line 1 FIXED"
    )
    
    # Pass them in arbitrary order (top-down visually, but random in list)
    fixed_content = apply_fixes(original_content, [diag_1, diag_3])
    
    assert fixed_content == "Line 1 FIXED\nLine 2\nLine 3 FIXED"


def test_apply_multi_line_replacement():
    """
    Verify that the patcher can replace a block of multiple lines with new content.
    This is required for rules like MD055 (Table Formatting).
    """
    original_content = "Line 1\nLine 2 Bad\nLine 3 Also Bad\nLine 4 Good"
    
    # Simulate a diagnostic covering lines 2-3
    diag = Diagnostic(
        rule_id="TEST_MULTI",
        severity=Severity.ERROR,
        message="Replace block",
        file_path="/fake/path.md",
        line_start=2,
        col_start=1,
        line_end=3,
        col_end=17, # End of "Line 3 Also Bad"
        suggestion_diff="Line 2 Fixed\nLine 3 Fixed", # New multi-line content
    )
    
    fixed_content = apply_fixes(original_content, [diag])
    
    expected = "Line 1\nLine 2 Fixed\nLine 3 Fixed\nLine 4 Good"
    assert fixed_content == expected, f"Got:\n{fixed_content!r}\nExpected:\n{expected!r}"
