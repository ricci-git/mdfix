from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    TEXT = auto()
    STRONG_OPEN = auto()
    STRONG_CLOSE = auto()
    EMPHASIS_OPEN = auto()
    EMPHASIS_CLOSE = auto()
    CODE_OPEN = auto()
    CODE_CLOSE = auto()
    LINK_OPEN = auto()
    LINK_DESTINATION = auto()
    LINK_CLOSE = auto()


@dataclass(frozen=True)
class InlineToken:
    type: TokenType
    value: str | None = None