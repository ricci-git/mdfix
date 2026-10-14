from mdfix.diagnostics import Diagnostic


def apply_fixes(content: str, diagnostics: list[Diagnostic]) -> str:
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
    sorted_diags = sorted(
        fixable_diags, 
        key=lambda d: (d.line_start, d.col_start), 
        reverse=True
    )
    
    # Split into lines WITHOUT keeping newlines initially for easier manipulation
    lines = content.split('\n')
    
    for diag in sorted_diags:
        # Convert 1-based line numbers to 0-based indices
        start_idx = diag.line_start - 1
        end_idx = diag.line_end - 1
        
        # Validate indices
        if start_idx < 0 or start_idx >= len(lines):
            continue
            
        # Adjust cols to 0-based indices
        c_start = max(0, diag.col_start - 1)
        
        # Ensure end_idx is valid before accessing lines[end_idx]
        if end_idx >= len(lines):
            end_idx = len(lines) - 1
            
        c_end = min(len(lines[end_idx]), diag.col_end) 
        
        clean_suggestion = diag.suggestion_diff

        if start_idx == end_idx:
            # Single line replacement logic
            line_str = lines[start_idx]
            prefix = line_str[:c_start]
            suffix = line_str[c_end:]
            new_line = prefix + clean_suggestion + suffix
            lines[start_idx] = new_line
        else:
            # Multi-line replacement logic
            # We need to replace lines[start_idx : end_idx + 1] with new content derived from suggestion
            
            # 1. Get prefix from the first line involved
            first_line_prefix = lines[start_idx][:c_start]
            
            # 2. Get suffix from the last line involved
            last_line_suffix = lines[end_idx][c_end:]
            
            # 3. Split suggestion into lines
            suggestion_lines = clean_suggestion.split('\n')
            
            # 4. Construct the new block of lines
            new_block = []
            
            # Handle case where suggestion has only 1 line but replaces multiple
            if len(suggestion_lines) == 1:
                merged_line = first_line_prefix + suggestion_lines[0] + last_line_suffix
                new_block.append(merged_line)
            else:
                # First line of suggestion merges with prefix
                new_block.append(first_line_prefix + suggestion_lines[0])
                
                # Middle lines are added as-is using extend for efficiency
                new_block.extend(suggestion_lines[1:-1])
                    
                # Last line of suggestion merges with suffix
                new_block.append(suggestion_lines[-1] + last_line_suffix)
            
            # 5. Replace the old slice in 'lines' list with the new block
            lines[start_idx : end_idx + 1] = new_block

    return '\n'.join(lines)
