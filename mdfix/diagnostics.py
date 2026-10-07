from dataclasses import dataclass
from enum import Enum
from typing import Optional

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass(frozen=True)
class Diagnostic:
    """
    Represents a single issue found in a Markdown document.
    Frozen to ensure immutability during processing pipelines.
    """
    rule_id: str
    severity: Severity
    message: str
    file_path: str
    
    # Location information
    line_start: int
    col_start: int
    line_end: int
    col_end: int
    
    # Optional suggestion for auto-fix (e.g., unified diff string)
    suggestion_diff: Optional[str] = None
