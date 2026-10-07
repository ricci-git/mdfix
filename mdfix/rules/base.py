from abc import ABC, abstractmethod

from mdfix.diagnostics import Diagnostic
from mdfix.document import Document


class Rule(ABC):
    """
    Abstract base class for all Markdown linting rules.
    Each rule must implement the `check` method which accepts a parsed Document
    and returns a list of Diagnostics.
    """
    id: str
    description: str

    @abstractmethod
    def check(self, document: Document) -> list[Diagnostic]:
        """Analyze the document and return found issues."""
