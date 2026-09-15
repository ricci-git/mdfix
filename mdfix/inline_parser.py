from mdfix.inline_elements import (
    Emphasis,
    InlineCode,
    InlineElement,
    Link,
    Strong,
    Text,
)
from mdfix.inline_tokenizer import tokenize
from mdfix.inline_tokens import InlineToken, TokenType


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
    markers = (
        ("**", Strong),
        ("__", Strong),
        ("*", Emphasis),
        ("_", Emphasis),
        ("`", InlineCode),
    )

    found: list[tuple[int, str, type[InlineElement]]] = []

    for marker, cls in markers:
        position = text.find(marker)

        if position != -1:
            found.append((position, marker, cls))

    if not found:
        return None

    _, marker, cls = min(found, key=lambda item: item[0])

    return marker, cls


def find_matching_marker(
    text: str,
    start: int,
    marker: str,
) -> int | None:
    position = start + len(marker)
    nested = 0

    while position < len(text):
        if marker == "**":
            if text.startswith("***", position):
                position += 1
                continue

            if text.startswith("**", position):
                return position

            position += 1
            continue

        if marker == "*":
            if text.startswith("***", position) and nested > 0:
                nested -= 1
                position += 2
                continue

            if text.startswith("**", position):
                nested += 1
                position += 2
                continue

            if text.startswith("*", position):
                if nested > 0:
                    position += 1
                    continue

                return position

            position += 1
            continue

        if text.startswith(marker, position):
            return position

        position += 1

    return None


def create_link_element(
    label: str,
    url: str,
) -> Link:
    return Link(
        children=parse_inline(label),
        url=url,
    )


def create_inline_element(
    element_type: type[InlineElement],
    content: str,
) -> InlineElement:
    if element_type is InlineCode:
        return InlineCode(
            code=content,
        )

    return element_type(
        children=parse_inline(content),
    )


def parse_tokens(tokens: list[InlineToken]) -> list[InlineElement]:
    elements, _ = _parse_token_sequence(tokens, 0, None)
    return elements


def _parse_token_sequence(
    tokens: list[InlineToken],
    position: int,
    closing_type: TokenType | None,
) -> tuple[list[InlineElement], int]:
    elements: list[InlineElement] = []

    while position < len(tokens):
        token = tokens[position]

        if closing_type is not None and token.type is closing_type:
            return elements, position + 1

        if token.type is TokenType.TEXT:
            elements.append(Text(token.value or ""))
            position += 1
            continue

        if token.type is TokenType.STRONG_OPEN:
            children, position = _parse_token_sequence(
                tokens,
                position + 1,
                TokenType.STRONG_CLOSE,
            )

            if children:
                elements.append(Strong(children=children))

            continue

        if token.type is TokenType.EMPHASIS_OPEN:
            children, position = _parse_token_sequence(
                tokens,
                position + 1,
                TokenType.EMPHASIS_CLOSE,
            )

            if children:
                elements.append(Emphasis(children=children))

            continue

        if token.type is TokenType.LINK_OPEN:
            children, position = _parse_token_sequence(
                tokens,
                position + 1,
                TokenType.LINK_DESTINATION,
            )

            destination = tokens[position - 1].value

            elements.append(
                Link(
                    children=children,
                    url=destination or "",
                )
            )

            if position < len(tokens) and tokens[position].type is TokenType.LINK_CLOSE:
                position += 1

            continue

        if token.type is TokenType.CODE_OPEN:
            end = position + 1

            while end < len(tokens):
                if tokens[end].type is TokenType.CODE_CLOSE:
                    code = "".join(
                        token.value or ""
                        for token in tokens[position + 1:end]
                    )

                    if code:
                        elements.append(
                            InlineCode(code=code)
                        )

                    position = end + 1
                    break

                end += 1
            else:
                position += 1

            continue

        position += 1

    return elements, position


def parse_inline(text: str) -> list[InlineElement]:
    """Parse inline Markdown into Inline AST."""

    return parse_tokens(tokenize(text))
