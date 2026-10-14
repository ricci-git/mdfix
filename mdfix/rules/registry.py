from mdfix.rules.base import Rule
from mdfix.rules.md001_heading_skip import Md001HeadingSkipRule
from mdfix.rules.md009_trailing_whitespace import Md009TrailingWhitespaceRule
from mdfix.rules.md047_newline_eof import Md047NewlineEofRule
from mdfix.rules.md055_table_format import Md055TableFormatRule


def get_default_rules() -> list[Rule]:
    """
    Returns a fresh instance of all default linting rules.
    Using a factory function allows for easier configuration and testing later.
    """
    return [
        Md001HeadingSkipRule(),
        Md009TrailingWhitespaceRule(),
        Md047NewlineEofRule(),
        Md055TableFormatRule(),
    ]
