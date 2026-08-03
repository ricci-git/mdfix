from mdfix.inline_elements import Text
from mdfix.inline_parser import parse_inline


def test_parse_plain_text():
    result = parse_inline("Hello world")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "Hello world"


def test_parse_empty_text():
    result = parse_inline("")

    assert result == []


def test_parse_whitespace_text():
    result = parse_inline("   ")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "   "


def test_parse_text_with_newline():
    result = parse_inline("Hello\nWorld")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "Hello\nWorld"