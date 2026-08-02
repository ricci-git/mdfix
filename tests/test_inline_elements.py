from mdfix.inline_elements import (
    Emphasis,
    InlineCode,
    Link,
    Strong,
    Text,
)


def test_text_element():
    text = Text("hello")

    assert text.text == "hello"


def test_strong_element():
    strong = Strong(
        children=[
            Text("bold"),
        ],
    )

    assert len(strong.children) == 1
    assert isinstance(strong.children[0], Text)
    assert strong.children[0].text == "bold"


def test_emphasis_element():
    emphasis = Emphasis(
        children=[
            Text("italic"),
        ],
    )

    assert emphasis.children[0].text == "italic"


def test_inline_code_element():
    code = InlineCode("print()")

    assert code.code == "print()"


def test_link_element():
    link = Link(
        children=[
            Text("OpenAI"),
        ],
        url="https://openai.com",
    )

    assert link.url == "https://openai.com"
    assert link.children[0].text == "OpenAI"