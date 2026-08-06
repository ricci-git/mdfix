from mdfix.inline_elements import (
    Emphasis,
    InlineCode,
    Link,
    Strong,
    Text,
)
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


def test_parse_strong_text():
    result = parse_inline("**hello**")

    assert len(result) == 1
    assert isinstance(result[0], Strong)

    strong = result[0]

    assert len(strong.children) == 1
    assert isinstance(strong.children[0], Text)
    assert strong.children[0].text == "hello"


def test_parse_text_with_strong():
    result = parse_inline("Hello **world**")

    assert len(result) == 2

    assert isinstance(result[0], Text)
    assert result[0].text == "Hello "

    assert isinstance(result[1], Strong)
    assert len(result[1].children) == 1
    assert isinstance(result[1].children[0], Text)
    assert result[1].children[0].text == "world"


def test_parse_unclosed_strong():
    result = parse_inline("Hello **world")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "Hello **world"


def test_parse_empty_strong():
    result = parse_inline("****")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "****"


def test_parse_strong_with_underscores():
    result = parse_inline("__hello__")

    assert len(result) == 1
    assert isinstance(result[0], Strong)

    assert len(result[0].children) == 1
    assert isinstance(result[0].children[0], Text)
    assert result[0].children[0].text == "hello"


def test_parse_text_with_strong_underscores():
    result = parse_inline("Hello __world__")

    assert len(result) == 2

    assert isinstance(result[0], Text)
    assert result[0].text == "Hello "

    assert isinstance(result[1], Strong)
    assert len(result[1].children) == 1
    assert isinstance(result[1].children[0], Text)
    assert result[1].children[0].text == "world"


def test_parse_emphasis_text():
    result = parse_inline("*hello*")

    assert len(result) == 1
    assert isinstance(result[0], Emphasis)

    emphasis = result[0]

    assert len(emphasis.children) == 1
    assert isinstance(emphasis.children[0], Text)
    assert emphasis.children[0].text == "hello"


def test_parse_text_with_emphasis():
    result = parse_inline("Hello *world*")

    assert len(result) == 2

    assert isinstance(result[0], Text)
    assert result[0].text == "Hello "

    assert isinstance(result[1], Emphasis)
    assert len(result[1].children) == 1
    assert isinstance(result[1].children[0], Text)
    assert result[1].children[0].text == "world"


def test_parse_emphasis_with_underscores():
    result = parse_inline("_hello_")

    assert len(result) == 1
    assert isinstance(result[0], Emphasis)

    assert len(result[0].children) == 1
    assert isinstance(result[0].children[0], Text)
    assert result[0].children[0].text == "hello"


def test_parse_unclosed_emphasis():
    result = parse_inline("Hello *world")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "Hello *world"


def test_parse_empty_emphasis():
    result = parse_inline("**")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "**"


def test_parse_inline_code():
    result = parse_inline("`hello`")

    assert len(result) == 1
    assert isinstance(result[0], InlineCode)
    assert result[0].code == "hello"


def test_parse_text_with_inline_code():
    result = parse_inline("Hello `world`")

    assert len(result) == 2

    assert isinstance(result[0], Text)
    assert result[0].text == "Hello "

    assert isinstance(result[1], InlineCode)
    assert result[1].code == "world"


def test_parse_unclosed_inline_code():
    result = parse_inline("Hello `world")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "Hello `world"


def test_parse_empty_inline_code():
    result = parse_inline("``")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "``"


def test_parse_link():
    result = parse_inline("[example](https://example.com)")

    assert len(result) == 1
    assert isinstance(result[0], Link)

    link = result[0]

    assert link.url == "https://example.com"
    assert len(link.children) == 1
    assert isinstance(link.children[0], Text)
    assert link.children[0].text == "example"


def test_parse_text_with_link():
    result = parse_inline("Visit [example](https://example.com)")

    assert len(result) == 2

    assert isinstance(result[0], Text)
    assert result[0].text == "Visit "

    assert isinstance(result[1], Link)
    assert result[1].url == "https://example.com"


def test_parse_empty_link_text():
    result = parse_inline("[](https://example.com)")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "[](https://example.com)"


def test_parse_unclosed_link():
    result = parse_inline("[example](https://example.com")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "[example](https://example.com"


def test_parse_link_without_url():
    result = parse_inline("[example]()")

    assert len(result) == 1
    assert isinstance(result[0], Text)
    assert result[0].text == "[example]()"


def test_parse_link_with_strong_child():
    result = parse_inline("[**bold**](https://example.com)")

    assert len(result) == 1
    assert isinstance(result[0], Link)

    link = result[0]

    assert len(link.children) == 1
    assert isinstance(link.children[0], Strong)

    strong = link.children[0]

    assert len(strong.children) == 1
    assert isinstance(strong.children[0], Text)
    assert strong.children[0].text == "bold"


def test_parse_link_with_emphasis_child():
    result = parse_inline("[*italic*](https://example.com)")

    assert len(result) == 1
    assert isinstance(result[0], Link)

    link = result[0]

    assert len(link.children) == 1
    assert isinstance(link.children[0], Emphasis)


def test_parse_link_with_inline_code_child():
    result = parse_inline("[`code`](https://example.com)")

    assert len(result) == 1
    assert isinstance(result[0], Link)

    link = result[0]

    assert len(link.children) == 1
    assert isinstance(link.children[0], InlineCode)

    assert link.children[0].code == "code"