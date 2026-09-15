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
