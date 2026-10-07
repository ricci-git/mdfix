from mdfix.document import Document
from mdfix.diagnostics import Diagnostic, Severity
from mdfix.elements import Heading
from mdfix.rules.base import Rule


class Md001HeadingSkipRule(Rule):
    id = "MD001"
    description = "Heading levels should increment by one."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        last_level = 0

        for element in document.elements:
            if isinstance(element, Heading):
                current_level = element.level

                # Check if there is a gap greater than 1
                # Note: First heading usually starts at 1, so we handle initial state carefully
                if last_level > 0 and current_level > last_level + 1:
                    diagnostics.append(
                        Diagnostic(
                            rule_id=self.id,
                            severity=Severity.WARNING,
                            message=f"Heading level skipped from {last_level} to {current_level}",
                            file_path=str(document.path),
                            line_start=element.position.line,
                            col_start=element.position.column or 1,
                            line_end=element.position.line,
                            col_end=element.position.column or 1,
                        )
                    )

                # Update last seen level regardless of whether it was an error
                # This allows detecting subsequent skips relative to the *actual* structure found
                last_level = current_level

        return diagnostics
