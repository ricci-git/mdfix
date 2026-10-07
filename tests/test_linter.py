import pytest
from pathlib import Path
from mdfix.linter import Linter
from mdfix.rules.base import Rule
from mdfix.diagnostics import Diagnostic, Severity
# parse_markdown імпортується всередині Linter, тут нам не потрібен для тесту правила

class DummyRule(Rule):
    id = "TEST001"
    description = "A dummy rule for testing"
    
    def check(self, document) -> list[Diagnostic]:
        diagnostics = []
        
        # Просто беремо перший елемент зі списку, якщо він є
        if not document.elements:
            return diagnostics
            
        first_element = document.elements[0]
        
        # Генеруємо діагностику без прив'язки до конкретного типу елемента
        # Використовуємо getattr для безпеки, щоб отримати текст/label, якщо вони є
        element_repr = repr(first_element)[:50] 
        
        diagnostics.append(
            Diagnostic(
                rule_id=self.id,
                severity=Severity.ERROR,
                message=f"Found element: {element_repr}",
                file_path=str(document.path),
                line_start=1, # Hardcoded for simplicity in this test
                col_start=1,
                line_end=1,
                col_end=1,
            )
        )
        return diagnostics

def test_linter_runs_rules_and_returns_diagnostics(tmp_path: Path):
    """
    Verify that Linter executes registered rules and collects their diagnostics.
    """
    # Create a simple markdown file with at least one block element
    md_file = tmp_path / "test.md"
    content = "# Hello World\nSome text.\n"
    md_file.write_text(content)
    
    # Initialize linter with the dummy rule
    linter = Linter(rules=[DummyRule()])
    
    # Run linting
    results = linter.lint(md_file)
    
    # Assertions
    assert len(results) == 1, f"Expected 1 diagnostic, got {len(results)}"
    assert results[0].rule_id == "TEST001"
    assert "Found element" in results[0].message
    assert results[0].file_path == str(md_file.resolve())
