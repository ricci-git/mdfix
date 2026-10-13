from typing import List
from mdfix.diagnostics import Diagnostic


def apply_fixes(content: str, diagnostics: List[Diagnostic]) -> str:
    """
    Applies suggested fixes from diagnostics to the original content.
    
    Important: Fixes are applied in reverse order of their appearance in the file
    (bottom-up) to ensure that earlier replacements do not invalidate the 
    line/column indices of later replacements.
    
    Args:
        content: The original markdown string.
        diagnostics: A list of Diagnostic objects containing `suggestion_diff`.
        
    Returns:
        The modified markdown string.
    """
    if not diagnostics:
        return content
    
    # Filter out diagnostics without a suggestion
    fixable_diags = [d for d in diagnostics if d.suggestion_diff is not None]
    
    if not fixable_diags:
        return content
        
    # Sort diagnostics by start position DESCENDING (Bottom-Up)
    # Primary key: line_start (descending)
    # Secondary key: col_start (descending)
    sorted_diags = sorted(
        fixable_diags, 
        key=lambda d: (d.line_start, d.col_start), 
        reverse=True
    )
    
    # Split into lines WITHOUT keeping newlines initially for easier manipulation
    # Note: This assumes standard Unix-style line endings or handles them implicitly
    lines = content.split('\n')
    
    for diag in sorted_diags:
        # Convert 1-based line numbers to 0-based indices
        start_idx = diag.line_start - 1
        end_idx = diag.line_end - 1
        
        # Validate indices
        if start_idx < 0 or start_idx >= len(lines):
            continue
            
        # For MVP, we assume single-line fixes mostly. 
        # If multi-line, this simple logic might need expansion, but let's stick to single line replacement first.
        if start_idx != end_idx:
            # Skip multi-line ranges for now to avoid complexity bugs in MVP
            continue

        line_str = lines[start_idx]
        
        # Adjust cols to 0-based indices
        c_start = max(0, diag.col_start - 1)
        # col_end in Diagnostic is typically exclusive or inclusive depending on convention.
        # In our test: "Some text." (len 10). col_start=1, col_end=11.
        # So slice is [0:11]. But line_str has no \n here because we split by '\n'.
        # Wait, if we split by '\n', "Some text." becomes just "Some text.". Length 10.
        # Slice [0:11] would go out of bounds or take everything.
        # Let's clamp c_end to length of line_str to be safe.
        c_end = min(len(line_str), diag.col_end) 
        
        # Extract prefix and suffix
        prefix = line_str[:c_start]
        suffix = line_str[c_end:]
        
        # Clean suggestion (remove potential trailing newlines if any slipped in)
        clean_suggestion = diag.suggestion_diff.rstrip('\r\n')
        
        # Reconstruct line
        new_line = prefix + clean_suggestion + suffix
        
        lines[start_idx] = new_line

    # Join back with newlines
    return '\n'.join(lines)
