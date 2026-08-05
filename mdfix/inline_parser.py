from mdfix.inline_elements import (
    Emphasis,
    InlineCode,
    InlineElement,
    Strong,
    Text,
)


def parse_inline(text: str) -> list[InlineElement]:
    """Parse inline Markdown into Inline AST."""

    if not text:
        return []

    marker = None
    element_type = None

    for candidate, cls in (
        ("**", Strong),
        ("__", Strong),
        ("*", Emphasis),
        ("_", Emphasis),
        ("`", InlineCode),
    ):
        if candidate in text:
            marker = candidate
            element_type = cls
            break

    if marker is None:
        return [Text(text)]

    start = text.find(marker)

    end = text.find(marker, start + 2)

    if end == -1:
        return [Text(text)]

    content = text[start + len(marker):end]

    if not content:
        return [Text(text)]

    elements: list[InlineElement] = []

    if start > 0:
        elements.append(Text(text[:start]))

    if element_type is InlineCode:
        elements.append(InlineCode(code=content))
    else:
        elements.append(
            element_type(
                children=[
                    Text(content),
                ],
            )
        )

    if end + len(marker) < len(text):
        elements.append(Text(text[end + len(marker):]))

    return elements