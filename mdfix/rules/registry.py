from mdfix.rules.base import Rule
from mdfix.rules.md001_heading_skip import Md001HeadingSkipRule
from mdfix.rules.md009_trailing_whitespace import Md009TrailingWhitespaceRule
from mdfix.rules.md047_newline_eof import Md047NewlineEofRule
from mdfix.rules.md055_table_format import Md055TableFormatRule


def get_all_rules() -> list[Rule]:
    """Returns instances of ALL available rules."""
    return [
        Md001HeadingSkipRule(),
        Md009TrailingWhitespaceRule(),
        Md047NewlineEofRule(),
        Md055TableFormatRule(),
    ]

def get_default_rules() -> list[Rule]:
    """
    Returns a fresh instance of all default linting rules.
    Kept for backward compatibility if needed, but preferably use filter_rules.
    """
    return get_all_rules()

def filter_rules(rules: list[Rule], disabled_ids: set[str]) -> list[Rule]:
    """Filters out rules whose IDs are in disabled_ids."""
    return [r for r in rules if r.id not in disabled_ids]
