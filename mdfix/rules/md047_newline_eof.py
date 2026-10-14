from mdfix.document import Document
from mdfix.diagnostics import Diagnostic, Severity
from mdfix.rules.base import Rule


class Md047NewlineEofRule(Rule):
    id = "MD047"
    description = "Files should end with a single newline character."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        
        content = document.content
        
        if not content:
            return diagnostics
            
        if content.endswith("\n"):
            return diagnostics
            
        lines = content.splitlines()
        if not lines:
            return diagnostics
            
        last_line_index = len(lines) - 1
        last_line_number = last_line_index + 1 # 1-based
        last_line_text = lines[last_line_index]
        last_line_length = len(last_line_text)
        
        # Strategy: Replace the ENTIRE last line content with itself + newline.
        # This avoids complex insertion logic in the patcher for zero-width ranges.
        col_start = 1
        col_end = last_line_length + 1 # Exclusive end for slice [0:length]
        
        new_content_for_line = last_line_text + "\n"
        
        diagnostics.append(
            Diagnostic(
                rule_id=self.id,
                severity=Severity.WARNING,
                message="Missing newline at end of file",
                file_path=str(document.path),
                line_start=last_line_number,
                col_start=col_start,
                line_end=last_line_number,
                col_end=col_end,
                suggestion_diff=new_content_for_line,
            )
        )
        
        return diagnostics
