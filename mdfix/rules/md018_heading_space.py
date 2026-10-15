import re

from mdfix.diagnostics import Diagnostic, Severity
from mdfix.document import Document
from mdfix.elements import Heading
from mdfix.rules.base import Rule


class Md018HeadingSpaceRule(Rule):
    id = "MD018"
    description = "No space after hash on atx style heading."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        
        for element in document.elements:
            if isinstance(element, Heading):
                # We need to inspect the raw text of the heading line.
                # However, our AST might have already parsed it. 
                # Safer approach: Iterate through lines directly or use position info.
                # Let's assume Heading element has 'level' and we can reconstruct or access raw.
                # For simplicity in this rule, let's scan the document content lines directly 
                # using regex, as it's faster for pattern matching than deep AST traversal for simple syntax errors.
                
                pass # Placeholder logic below uses direct string scanning for robustness
        
        # Direct string scanning implementation for MD018
        lines = document.content.splitlines()
        for i, line in enumerate(lines):
            # Regex to find ATX headings: optional leading spaces, hashes, NO space, then text
            # Pattern: ^\s*(#{1,6})([^ \t#\n].*)$
            match = re.match(r'^(\s*)(#{1,6})([^ \t#\n].*)$', line)
            if match:
                indent = match.group(1)
                hashes = match.group(2)
                rest_of_line = match.group(3)
                
                # Construct corrected line: indent + hashes + space + rest
                corrected_line = f"{indent}{hashes} {rest_of_line}"
                
                diagnostics.append(
                    Diagnostic(
                        rule_id=self.id,
                        severity=Severity.WARNING,
                        message="No space after hash on atx style heading",
                        file_path=str(document.path),
                        line_start=i + 1,
                        col_start=1,          # <--- ПОЧАТОК РЯДКА
                        line_end=i + 1,
                        col_end=len(line) + 1, # <--- КІНЕЦЬ РЯДКА (exclusive end for slice logic in patcher usually implies length+1 or similar depending on impl, but here we replace WHOLE LINE)
                        suggestion_diff=corrected_line, # <--- ПОВНИЙ НОВИЙ РЯДОК
                    )
                )
                        
        return diagnostics
