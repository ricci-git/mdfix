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

    assert document.elements == []


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

def test_ignore_invalid_heading_level(tmp_path):
    md = tmp_path / "invalid.md"

    md.write_text(
        "####### Invalid\n",
        encoding="utf-8",
    )

    document = parse_markdown(md)

    assert document.elements == []