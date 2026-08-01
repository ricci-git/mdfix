from mdfix.elements import (
    CodeBlock,
    Heading,
    List,
    Paragraph,
    SourcePosition,
    Table,
)


def test_heading():
    heading = Heading(
        level=2,
        title="Introduction",
        position=SourcePosition(line=1),
    )

    assert heading.level == 2
    assert heading.title == "Introduction"
    assert heading.position.line == 1
    assert heading.position.column == 1


def test_paragraph():
    paragraph = Paragraph(
        text="Hello",
        position=SourcePosition(line=3),
    )

    assert paragraph.text == "Hello"
    assert paragraph.position.line == 3
    assert paragraph.position.column == 1


def test_table():
    table = Table(
        headers=[
            "A",
            "B",
        ],
        rows=[
            [
                "1",
                "2",
            ],
        ],
        position=SourcePosition(line=5),
    )

    assert table.headers == [
        "A",
        "B",
    ]

    assert table.rows == [
        [
            "1",
            "2",
        ],
    ]

    assert table.position.line == 5


def test_code_block():
    block = CodeBlock(
        language="python",
        code="print('Hello')",
        position=SourcePosition(line=7),
    )

    assert block.language == "python"
    assert "print" in block.code
    assert block.position.line == 7


def test_list():
    lst = List(
        ordered=False,
        items=["One", "Two"],
        position=SourcePosition(line=10),
    )

    assert lst.ordered is False
    assert len(lst.items) == 2
    assert lst.position.line == 10