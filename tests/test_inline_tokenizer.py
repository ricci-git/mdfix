from mdfix.inline_tokenizer import (
    find_matching_marker,
    tokenize,
)
from mdfix.inline_tokens import InlineToken, TokenType


def test_tokenize_plain_text():
    result = tokenize("hello")

    assert result == [
        InlineToken(TokenType.TEXT, "hello"),
    ]


def test_tokenize_strong():
    result = tokenize("**bold**")

    assert result == [
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold"),
        InlineToken(TokenType.STRONG_CLOSE),
    ]


def test_tokenize_emphasis():
    result = tokenize("*italic*")

    assert result == [
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "italic"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_tokenize_inline_code():
    result = tokenize("`code`")

    assert result == [
        InlineToken(TokenType.CODE_OPEN),
        InlineToken(TokenType.TEXT, "code"),
        InlineToken(TokenType.CODE_CLOSE),
    ]


def test_tokenize_link():
    result = tokenize("[example](https://example.com)")

    assert result == [
        InlineToken(TokenType.LINK_OPEN),
        InlineToken(TokenType.TEXT, "example"),
        InlineToken(
            TokenType.LINK_DESTINATION,
            "https://example.com",
        ),
        InlineToken(TokenType.LINK_CLOSE),
    ]


def test_tokenize_link_with_spaces():
    result = tokenize("[hello world](https://example.com)")

    assert result == [
        InlineToken(TokenType.LINK_OPEN),
        InlineToken(TokenType.TEXT, "hello world"),
        InlineToken(
            TokenType.LINK_DESTINATION,
            "https://example.com",
        ),
        InlineToken(TokenType.LINK_CLOSE),
    ]


def test_tokenize_text_with_link():
    result = tokenize("Visit [example](https://example.com)")

    assert result == [
        InlineToken(TokenType.TEXT, "Visit "),
        InlineToken(TokenType.LINK_OPEN),
        InlineToken(TokenType.TEXT, "example"),
        InlineToken(
            TokenType.LINK_DESTINATION,
            "https://example.com",
        ),
        InlineToken(TokenType.LINK_CLOSE),
    ]


def test_tokenize_invalid_link_as_text():
    result = tokenize("[example](https://example.com")

    assert result == [
        InlineToken(TokenType.TEXT, "[example](https://example.com"),
    ]


def test_tokenize_strong_with_underscores():
    result = tokenize("__hello__")

    assert result == [
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "hello"),
        InlineToken(TokenType.STRONG_CLOSE),
    ]


def test_tokenize_emphasis_with_underscores():
    result = tokenize("_hello_")

    assert result == [
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "hello"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_tokenize_sequential_inline_elements():
    result = tokenize("**bold** _italic_")

    assert result == [
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold"),
        InlineToken(TokenType.STRONG_CLOSE),
        InlineToken(TokenType.TEXT, " "),
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "italic"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_tokenize_nested_strong_and_emphasis():
    result = tokenize("**bold *italic***")

    assert result == [
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold "),
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "italic"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
        InlineToken(TokenType.STRONG_CLOSE),
    ]


def test_tokenize_nested_emphasis_and_strong():
    result = tokenize("*italic **bold***")

    assert result == [
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "italic "),
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold"),
        InlineToken(TokenType.STRONG_CLOSE),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_find_matching_marker_for_nested_strong():

    text = "**bold *italic***"

    assert find_matching_marker(text, 0, "**") == 15


def test_find_matching_marker_for_nested_emphasis():

    text = "*italic **bold***"

    assert find_matching_marker(text, 0, "*") == 16


def test_find_matching_marker_for_strong():

    text = "**bold**"

    assert find_matching_marker(text, 0, "**") == 6


def test_tokenize_link_with_nested_strong():
    result = tokenize("[**bold**](https://example.com)")

    assert result == [
        InlineToken(TokenType.LINK_OPEN),
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold"),
        InlineToken(TokenType.STRONG_CLOSE),
        InlineToken(
            TokenType.LINK_DESTINATION,
            "https://example.com",
        ),
        InlineToken(TokenType.LINK_CLOSE),
    ]


def test_tokenize_link_with_destination_token():
    result = tokenize("[link](https://example.com)")

    assert result == [
        InlineToken(TokenType.LINK_OPEN),
        InlineToken(TokenType.TEXT, "link"),
        InlineToken(TokenType.LINK_DESTINATION, "https://example.com"),
        InlineToken(TokenType.LINK_CLOSE),
    ]


def test_tokenize_empty_strong_as_text():
    result = tokenize("****")

    assert result == [
        InlineToken(TokenType.TEXT, "****"),
    ]


def test_tokenize_empty_strong_underscore_as_text():
    result = tokenize("____")

    assert result == [
        InlineToken(TokenType.TEXT, "____"),
    ]


def test_tokenize_empty_inline_code_as_text():
    result = tokenize("``")

    assert result == [
        InlineToken(TokenType.TEXT, "``"),
    ]


def test_tokenize_nested_strong_in_emphasis():
    tokens = tokenize("*italic **bold** text*")

    assert tokens == [
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "italic "),
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "bold"),
        InlineToken(TokenType.STRONG_CLOSE),
        InlineToken(TokenType.TEXT, " text"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_tokenize_adjacent_inline_elements():
    tokens = tokenize("**one***two*")

    assert tokens == [
        InlineToken(TokenType.STRONG_OPEN),
        InlineToken(TokenType.TEXT, "one"),
        InlineToken(TokenType.STRONG_CLOSE),
        InlineToken(TokenType.EMPHASIS_OPEN),
        InlineToken(TokenType.TEXT, "two"),
        InlineToken(TokenType.EMPHASIS_CLOSE),
    ]


def test_find_matching_marker_for_adjacent_emphasis():
    text = "**one***two*"

    assert find_matching_marker(text, 7, "*") == 11
