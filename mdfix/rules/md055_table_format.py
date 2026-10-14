from mdfix.diagnostics import Diagnostic, Severity
from mdfix.document import Document
from mdfix.elements import Table
from mdfix.rules.base import Rule
from mdfix.table_formatter import format_table


class Md055TableFormatRule(Rule):
    id = "MD055"
    description = "Tables should be consistently formatted."

    def check(self, document: Document) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        
        all_lines = document.content.splitlines()
        
        for element in document.elements:
            if isinstance(element, Table):
                try:
                    # Generate canonical version using the Table object
                    formatted_str = format_table(element)
                except ValueError:
                    # If formatting fails due to structural issues (e.g., mismatched cells),
                    # skip auto-fix for safety and let other rules handle it or report manually.
                    continue
                
                # Determine the exact range of lines occupied by this table in the source
                start_idx = element.position.line - 1
                
                # Calculate how many lines the table takes:
                # 1 line for headers + 1 line for separator + N lines for rows
                num_data_rows = len(element.rows)
                total_table_lines = 1 + 1 + num_data_rows 
                
                end_idx = start_idx + total_table_lines
                
                # Extract raw text from source
                end_idx = min(end_idx, len(all_lines))
                    
                raw_table_lines = all_lines[start_idx:end_idx]
                raw_table_str = "\n".join(raw_table_lines)
                
                # Compare
                if raw_table_str != formatted_str:
                    diagnostics.append(
                        Diagnostic(
                            rule_id=self.id,
                            severity=Severity.WARNING,
                            message="Table format issue detected",
                            file_path=str(document.path),
                            line_start=element.position.line,
                            col_start=1,
                            line_end=end_idx,
                            col_end=len(raw_table_lines[-1]) + 1 if raw_table_lines else 1,
                            suggestion_diff=formatted_str,
                        )
                    )
                        
        return diagnostics
