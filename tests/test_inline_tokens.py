from mdfix.inline_tokens import InlineToken, TokenType


def test_create_text_token():
    token = InlineToken(TokenType.TEXT, "hello")

    assert token.type is TokenType.TEXT
    assert token.value == "hello"


def test_create_marker_token_without_value():
    token = InlineToken(TokenType.STRONG_OPEN)

    assert token.type is TokenType.STRONG_OPEN
    assert token.value is None


def test_create_link_destination_token():
    token = InlineToken(
        TokenType.LINK_DESTINATION,
        "https://example.com",
    )

    assert token.type is TokenType.LINK_DESTINATION
    assert token.value == "https://example.com"


def test_tokens_are_immutable():
    token = InlineToken(TokenType.TEXT, "hello")

    try:
        token.value = "world"
    except AttributeError:
        pass
    else:
        raise AssertionError("InlineToken must be immutable")