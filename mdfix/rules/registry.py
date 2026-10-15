from mdfix.rules.base import Rule
from mdfix.rules.md001_heading_skip import Md001HeadingSkipRule
from mdfix.rules.md009_trailing_whitespace import Md009TrailingWhitespaceRule
from mdfix.rules.md018_heading_space import Md018HeadingSpaceRule  # NEW
from mdfix.rules.md030_list_spacing import Md030ListSpacingRule  # NEW
from mdfix.rules.md047_newline_eof import Md047NewlineEofRule
from mdfix.rules.md055_table_format import Md055TableFormatRule


def get_all_rules() -> list[Rule]:
    """Returns instances of ALL available rules."""
    return [
        Md001HeadingSkipRule(),
        Md009TrailingWhitespaceRule(),
        Md018HeadingSpaceRule(),      # <-- ADD HERE
        Md030ListSpacingRule(),       # <-- ADD HERE
        Md047NewlineEofRule(),
        Md055TableFormatRule(),
    ]

def get_default_rules() -> list[Rule]:
    """Kept for backward compatibility."""
    return get_all_rules()

def filter_rules(rules: list[Rule], disabled_ids: set[str]) -> list[Rule]:
    """Filters out rules whose IDs are in disabled_ids."""
    return [r for r in rules if r.id not in disabled_ids]
