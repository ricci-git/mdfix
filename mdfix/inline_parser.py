from mdfix.inline_elements import (
    Emphasis,
    InlineCode,
    InlineElement,
    Link,
    Strong,
    Text,
)


def find_link(text: str) -> tuple[int, int, str, str] | None:
    start = text.find("[")

    if start == -1:
        return None

    label_end = text.find("](", start)

    if label_end == -1:
        return None

    url_end = text.find(")", label_end)

    if url_end == -1:
        return None

    label = text[start + 1:label_end]
    url = text[label_end + 2:url_end]

    if not label or not url:
        return None

    return start, url_end, label, url


def find_marker(text: str) -> tuple[str, type[InlineElement]] | None:
    for candidate, cls in (
        ("**", Strong),
        ("__", Strong),
        ("*", Emphasis),
        ("_", Emphasis),
        ("`", InlineCode),
    ):
        if candidate in text:
            return candidate, cls

    return None


def parse_inline(text: str) -> list[InlineElement]:
    """Parse inline Markdown into Inline AST."""

    if not text:
        return []

    link = find_link(text)

    if link:
        start, end, label, url = link

        elements: list[InlineElement] = []

        if start > 0:
            elements.append(Text(text[:start]))

        elements.append(
            Link(
                children=[
                    Text(label),
                ],
                url=url,
            )
        )

        if end + 1 < len(text):
            elements.append(Text(text[end + 1:]))

        return elements

    marker_result = find_marker(text)

    if marker_result is None:
        return [Text(text)]

    marker, element_type = marker_result

    start = text.find(marker)

    end = text.find(marker, start + len(marker))

    if end == -1:
        return [Text(text)]

    content = text[start + len(marker):end]

    if not content:
        return [Text(text)]

    elements: list[InlineElement] = []

    if start > 0:
        elements.append(Text(text[:start]))

    if element_type is InlineCode:
        elements.append(
            InlineCode(
                code=content,
            )
        )
    else:
        elements.append(
            element_type(
                children=[
                    Text(content),
                ],
            )
        )

    if end + len(marker) < len(text):
        elements.append(
            Text(text[end + len(marker):])
        )

    return elements