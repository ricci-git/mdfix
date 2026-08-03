from mdfix.inline_elements import InlineElement, Text


def parse_inline(text: str) -> list[InlineElement]:
    """Parse inline Markdown into Inline AST."""

    if not text:
        return []

    return [Text(text)]