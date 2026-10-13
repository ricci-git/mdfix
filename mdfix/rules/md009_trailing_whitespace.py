import re

from mdfix.diagnostics import Diagnostic, Severity
from mdfix.document import Document
from mdfix.rules.base import Rule


class Md009TrailingWhitespaceRule(Rule):
    id = "MD009"
    description = "Remove trailing whitespace."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        
        lines = document.content.splitlines(keepends=True)
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            # Strip newline chars to analyze horizontal whitespace only
            stripped_line = line.rstrip('\r\n')
            
            # Find trailing spaces/tabs
            match = re.search(r'[ \t]+$', stripped_line)
            
            if match:
                start_idx_in_stripped = match.start()
                length = len(match.group())
                
                # Calculate positions for Diagnostic and Patcher
                # col_start is 1-based index of the first offending char
                c_start_1_based = start_idx_in_stripped + 1
                
                # col_end is the exclusive upper bound for Python slicing [start:end]
                # In our patcher logic: slice(line[c_start-1 : c_end])
                # If we want to remove chars at indices X..Y (0-based), 
                # c_start should be X+1, c_end should be Y+1.
                y_exclusive_0_based = start_idx_in_stripped + length
                
                diagnostics.append(
                    Diagnostic(
                        rule_id=self.id,
                        severity=Severity.WARNING,
                        message="Trailing whitespace found",
                        file_path=str(document.path),
                        line_start=line_num,
                        col_start=c_start_1_based,
                        line_end=line_num,
                        col_end=y_exclusive_0_based, # This acts as the slice end
                        suggestion_diff="", 
                    )
                )
                
        return diagnostics
