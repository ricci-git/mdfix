from mdfix.elements import (
    Heading,
    HorizontalRule,
    Paragraph,
    Table,
)
from mdfix.parser import parse_markdown


def test_parse_headings(tmp_path):
    md = tmp_path / "test.md"

    md.write_text(
        "# Title\n"
        "\n"
        "## Section\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 2

    heading1 = document.elements[0]
    assert heading1.level == 1
    assert heading1.title == "Title"
    assert heading1.position.line == 1
    assert heading1.position.column == 1

    heading2 = document.elements[1]
    assert heading2.level == 2
    assert heading2.title == "Section"
    assert heading2.position.line == 3
    assert heading2.position.column == 1


def test_parse_empty_document(tmp_path):
    md = tmp_path / "empty.md"
    md.write_text("", encoding="utf-8")

    document = parse_markdown(md)

    assert document.elements == []


def test_parse_without_headings(tmp_path):
    md = tmp_path / "text.md"

    md.write_text(
        "Hello\n"
        "World\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]

    assert paragraph.text == "Hello\nWorld"
    assert paragraph.position.line == 1
    assert paragraph.position.column == 1


def test_parse_all_heading_levels(tmp_path):
    md = tmp_path / "levels.md"

    md.write_text(
        "# H1\n"
        "## H2\n"
        "### H3\n"
        "#### H4\n"
        "##### H5\n"
        "###### H6\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 6

    for index, heading in enumerate(document.elements, start=1):
        assert heading.level == index
        assert heading.title == f"H{index}"
        assert heading.position.line == index
        assert heading.position.column == 1


def test_invalid_heading_is_paragraph(tmp_path):
    md = tmp_path / "invalid.md"

    md.write_text(
        "####### Invalid\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]

    assert paragraph.text == "####### Invalid"
    assert paragraph.position.line == 1
    assert paragraph.position.column == 1


def test_parse_single_paragraph(tmp_path):
    md = tmp_path / "paragraph.md"

    md.write_text(
        "Hello world.\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]
    assert paragraph.text == "Hello world."
    assert paragraph.position.line == 1
    assert paragraph.position.column == 1


def test_parse_multiline_paragraph(tmp_path):
    md = tmp_path / "paragraph.md"

    md.write_text(
        "Hello\n"
        "world\n"
        "\n"
        "Second paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 2

    first = document.elements[0]
    assert first.text == "Hello\nworld"
    assert first.position.line == 1

    second = document.elements[1]
    assert second.text == "Second paragraph"
    assert second.position.line == 4


def test_parse_unordered_list(tmp_path):
    md = tmp_path / "list.md"

    md.write_text(
        "- First\n"
        "- Second\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    lst = document.elements[0]

    assert lst.ordered is False
    assert lst.items == [
        "First",
        "Second",
    ]
    assert lst.position.line == 1
    assert lst.position.column == 1


def test_parse_ordered_list(tmp_path):
    md = tmp_path / "list.md"

    md.write_text(
        "1. First\n"
        "2. Second\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    lst = document.elements[0]

    assert lst.ordered is True
    assert lst.items == [
        "First",
        "Second",
    ]
    assert lst.position.line == 1
    assert lst.position.column == 1


def test_parse_mixed_document(tmp_path):
    md = tmp_path / "mixed.md"

    md.write_text(
        "# Title\n"
        "\n"
        "First paragraph\n"
        "continues here\n"
        "\n"
        "- First\n"
        "- Second\n"
        "\n"
        "Last paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 4

    heading = document.elements[0]
    assert heading.level == 1
    assert heading.title == "Title"

    paragraph = document.elements[1]
    assert paragraph.text == (
        "First paragraph\n"
        "continues here"
    )

    lst = document.elements[2]
    assert lst.ordered is False
    assert lst.items == [
        "First",
        "Second",
    ]

    paragraph = document.elements[3]
    assert paragraph.text == "Last paragraph"


def test_parse_python_code_block(tmp_path):
    md = tmp_path / "code.md"

    md.write_text(
        "```python\n"
        "print('Hello')\n"
        "```\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    block = document.elements[0]

    assert block.language == "python"
    assert block.code == "print('Hello')"
    assert block.position.line == 1


def test_parse_plain_code_block(tmp_path):
    md = tmp_path / "code.md"

    md.write_text(
        "```\n"
        "Hello\n"
        "World\n"
        "```\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    block = document.elements[0]

    assert block.language is None
    assert block.code == "Hello\nWorld"

    assert block.position.line == 1


def test_parse_document_with_code_block(tmp_path):
    md = tmp_path / "mixed.md"

    md.write_text(
        "# Title\n"
        "\n"
        "```python\n"
        "print(1)\n"
        "```\n"
        "\n"
        "Paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 3

    assert document.elements[0].title == "Title"

    block = document.elements[1]
    assert block.language == "python"
    assert block.code == "print(1)"

    paragraph = document.elements[2]
    assert paragraph.text == "Paragraph"


def test_parse_blockquote(tmp_path):
    md = tmp_path / "quote.md"

    md.write_text(
        "> Hello\n"
        "> World\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    quote = document.elements[0]

    assert quote.text == (
        "Hello\n"
        "World"
    )

    assert quote.position.line == 1


def test_parse_single_blockquote(tmp_path):
    md = tmp_path / "quote.md"

    md.write_text(
        "> Hello world\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    quote = document.elements[0]

    assert quote.text == "Hello world"
    assert quote.position.line == 1


def test_parse_multiline_blockquote(tmp_path):
    md = tmp_path / "quote.md"

    md.write_text(
        "> First line\n"
        "> Second line\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    quote = document.elements[0]

    assert quote.text == (
        "First line\n"
        "Second line"
    )


def test_parse_document_with_blockquote(tmp_path):
    md = tmp_path / "mixed.md"

    md.write_text(
        "# Title\n"
        "\n"
        "> Quote text\n"
        "\n"
        "Paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 3

    assert document.elements[0].title == "Title"

    quote = document.elements[1]
    assert quote.text == "Quote text"

    paragraph = document.elements[2]
    assert paragraph.text == "Paragraph"


def test_parse_blockquote_with_paragraph(tmp_path):
    md = tmp_path / "quote.md"

    md.write_text(
        "> Quote\n"
        "\n"
        "Paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 2

    assert document.elements[0].text == "Quote"
    assert document.elements[1].text == "Paragraph"


def test_parse_horizontal_rule_dash(tmp_path):
    md = tmp_path / "hr.md"

    md.write_text(
        "---\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    rule = document.elements[0]

    assert isinstance(rule, HorizontalRule)
    assert rule.position.line == 1


def test_parse_horizontal_rule_asterisk(tmp_path):
    md = tmp_path / "hr.md"

    md.write_text(
        "***\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    rule = document.elements[0]

    assert isinstance(rule, HorizontalRule)
    assert rule.position.line == 1


def test_parse_horizontal_rule_underscore(tmp_path):
    md = tmp_path / "hr.md"

    md.write_text(
        "___\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    rule = document.elements[0]

    assert isinstance(rule, HorizontalRule)
    assert rule.position.line == 1


def test_parse_horizontal_rule_with_spaces(tmp_path):
    md = tmp_path / "hr.md"

    md.write_text(
        "- - -\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    rule = document.elements[0]

    assert isinstance(rule, HorizontalRule)
    assert rule.position.line == 1


def test_document_with_horizontal_rule(tmp_path):
    md = tmp_path / "mixed.md"

    md.write_text(
        "# Title\n"
        "\n"
        "---\n"
        "\n"
        "Paragraph\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 3

    assert document.elements[0].title == "Title"

    rule = document.elements[1]

    assert isinstance(rule, HorizontalRule)
    assert rule.position.line == 3

    assert document.elements[2].text == "Paragraph"


def test_invalid_horizontal_rule_is_paragraph(tmp_path):
    md = tmp_path / "invalid_hr.md"

    md.write_text(
        "----\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]

    assert paragraph.text == "----"


def test_parse_simple_table(tmp_path):
    md = tmp_path / "table.md"

    md.write_text(
        "| Name | Age |\n"
        "| ---- | --- |\n"
        "| Bob  | 20  |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    table = document.elements[0]

    assert isinstance(table, Table)

    assert table.headers == [
        "Name",
        "Age",
    ]

    assert table.rows == [
        [
            "Bob",
            "20",
        ]
    ]

    assert table.position.line == 1


def test_parse_table_multiple_rows(tmp_path):
    md = tmp_path / "table.md"

    md.write_text(
        "| Name | Age |\n"
        "| ---- | --- |\n"
        "| Bob  | 20  |\n"
        "| Ann  | 25  |\n"
        "| Tom  | 31  |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    table = document.elements[0]

    assert isinstance(table, Table)

    assert table.headers == [
        "Name",
        "Age",
    ]

    assert table.rows == [
        [
            "Bob",
            "20",
        ],
        [
            "Ann",
            "25",
        ],
        [
            "Tom",
            "31",
        ],
    ]


def test_parse_table_empty_cells(tmp_path):
    md = tmp_path / "table.md"

    md.write_text(
        "| Name | Age | City |\n"
        "| ---- | --- | ---- |\n"
        "| Bob  | 20  |      |\n"
        "| Ann  |     | Paris |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    table = document.elements[0]

    assert isinstance(table, Table)

    assert table.headers == [
        "Name",
        "Age",
        "City",
    ]

    assert table.rows == [
        [
            "Bob",
            "20",
            "",
        ],
        [
            "Ann",
            "",
            "Paris",
        ],
    ]


def test_parse_table_inside_document(tmp_path):
    md = tmp_path / "table.md"

    md.write_text(
        "# Users\n"
        "\n"
        "User list:\n"
        "\n"
        "| Name | Age |\n"
        "| ---- | --- |\n"
        "| Bob  | 20  |\n"
        "\n"
        "End.\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 4

    assert isinstance(document.elements[0], Heading)
    assert document.elements[0].title == "Users"

    assert isinstance(document.elements[1], Paragraph)
    assert document.elements[1].text == "User list:"

    assert isinstance(document.elements[2], Table)
    assert document.elements[2].headers == [
        "Name",
        "Age",
    ]

    assert isinstance(document.elements[3], Paragraph)
    assert document.elements[3].text == "End."


def test_invalid_table_without_separator_is_paragraph(tmp_path):
    md = tmp_path / "invalid_table.md"

    md.write_text(
        "| Name | Age |\n"
        "| Bob  | 20  |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]

    assert isinstance(paragraph, Paragraph)

    assert paragraph.text == (
        "| Name | Age |\n"
        "| Bob  | 20  |"
    )


def test_invalid_table_without_header_is_paragraph(tmp_path):
    md = tmp_path / "invalid_table.md"

    md.write_text(
        "| ---- | --- |\n"
        "| Bob  | 20  |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    paragraph = document.elements[0]

    assert isinstance(paragraph, Paragraph)

    assert paragraph.text == (
        "| ---- | --- |\n"
        "| Bob  | 20  |"
    )


def test_parse_table_inconsistent_columns(tmp_path):
    md = tmp_path / "table.md"

    md.write_text(
        "| Name | Age |\n"
        "| ---- | --- |\n"
        "| Bob |\n"
        "| Ann | 25 | City |\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert len(document.elements) == 1

    table = document.elements[0]

    assert isinstance(table, Table)

    assert table.headers == [
        "Name",
        "Age",
    ]

    assert table.rows == [
        [
            "Bob",
        ],
        [
            "Ann",
            "25",
            "City",
        ],
    ]

    assert table.position.line == 1