import re

from mdfix.diagnostics import Diagnostic, Severity
from mdfix.document import Document
from mdfix.rules.base import Rule


class Md030ListSpacingRule(Rule):
    id = "MD030"
    description = "Spaces around list markers."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        
        lines = document.content.splitlines()
        # Regex for unordered list markers (-, *, +) followed immediately by non-space/non-tab char
        # Allows for indentation
        pattern = re.compile(r'^(\s*)([-*+])([^ \t\n\r].*)$')
        
        for i, line in enumerate(lines):
            match = pattern.match(line)
            if match:
                indent = match.group(1)
                marker = match.group(2)
                content_part = match.group(3)
                
                # Corrected line: indent + marker + space + content
                corrected_line = f"{indent}{marker} {content_part}"
                
                diagnostics.append(
                    Diagnostic(
                        rule_id=self.id,
                        severity=Severity.WARNING,
                        message="Missing space after list marker",
                        file_path=str(document.path),
                        line_start=i + 1,
                        col_start=1,           # <--- ПОЧАТОК РЯДКА
                        line_end=i + 1,
                        col_end=len(line) + 1, # <--- КІНЕЦЬ РЯДКА
                        suggestion_diff=corrected_line, # <--- ПОВНИЙ НОВИЙ РЯДОК
                    )
                )
                        
        return diagnostics
