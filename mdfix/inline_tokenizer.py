from mdfix.inline_tokens import InlineToken, TokenType


def _find_link(
    text: str,
    start: int,
) -> tuple[int, int, str, str] | None:
    label_end = text.find("](", start)

    if label_end == -1:
        return None

    url_end = text.find(")", label_end + 2)

    if url_end == -1:
        return None

    label = text[start + 1:label_end]
    url = text[label_end + 2:url_end]

    if not label or not url:
        return None

    return start, url_end, label, url


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
                if nested > 0:
                    position += 1
                    nested -= 1
                    continue

                return position

            if text.startswith("**", position):
                return position

            if text.startswith("*", position):
                nested += 1
                position += 1
                continue

            position += 1
            continue

        if marker == "*":
            if text.startswith("***", position) and nested > 0:
                nested -= 1
                position += 2
                continue

            if text.startswith("**", position):
                if nested > 0:
                    nested -= 1
                else:
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


def tokenize(text: str) -> list[InlineToken]:
    if not text:
        return []

    tokens: list[InlineToken] = []

    markers = {
        "**": (
            TokenType.STRONG_OPEN,
            TokenType.STRONG_CLOSE,
        ),
        "__": (
            TokenType.STRONG_OPEN,
            TokenType.STRONG_CLOSE,
        ),
        "*": (
            TokenType.EMPHASIS_OPEN,
            TokenType.EMPHASIS_CLOSE,
        ),
        "_": (
            TokenType.EMPHASIS_OPEN,
            TokenType.EMPHASIS_CLOSE,
        ),
        "`": (
            TokenType.CODE_OPEN,
            TokenType.CODE_CLOSE,
        ),
    }

    position = 0
    text_start = 0

    while position < len(text):
        if text[position] == "[":
            link = _find_link(text, position)

            if link is not None:
                start, end, label, url = link

                if start > text_start:
                    tokens.append(
                        InlineToken(
                            TokenType.TEXT,
                            text[text_start:start],
                        )
                    )

                tokens.append(
                    InlineToken(TokenType.LINK_OPEN)
                )

                tokens.extend(tokenize(label))

                tokens.append(
                    InlineToken(
                        TokenType.LINK_DESTINATION,
                        url,
                    )
                )

                tokens.append(
                    InlineToken(TokenType.LINK_CLOSE)
                )

                position = end + 1
                text_start = position
                continue

        marker = None

        for candidate in markers:
            if text.startswith(candidate, position):
                marker = candidate
                break

        if marker is None:
            position += 1
            continue

        if position > text_start:
            tokens.append(
                InlineToken(
                    TokenType.TEXT,
                    text[text_start:position],
                )
            )

        open_type, close_type = markers[marker]

        tokens.append(InlineToken(open_type))

        close_position = find_matching_marker(
            text,
            position,
            marker,
        )

        if close_position is None:
            return [InlineToken(TokenType.TEXT, text)]

        if close_position == position + len(marker):
            return [InlineToken(TokenType.TEXT, text)]

        if close_position > position + len(marker):
            tokens.extend(
                tokenize(
                    text[position + len(marker):close_position]
                )
            )

        tokens.append(InlineToken(close_type))

        position = close_position + len(marker)
        text_start = position

    if text_start < len(text):
        tokens.append(
            InlineToken(
                TokenType.TEXT,
                text[text_start:],
            )
        )

    return tokens