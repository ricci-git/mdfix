from abc import ABC, abstractmethod
from typing import List
from mdfix.document import Document
from mdfix.diagnostics import Diagnostic

class Rule(ABC):
    """
    Abstract base class for all Markdown linting rules.
    Each rule must implement the `check` method which accepts a parsed Document
    and returns a list of Diagnostics.
    """
    id: str
    description: str

    @abstractmethod
    def check(self, document: Document) -> List[Diagnostic]:
        """Analyze the document and return found issues."""
        pass
