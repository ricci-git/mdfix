import pytest

from mdfix.elements import SourcePosition, Table
from mdfix.table_formatter import format_table


def test_format_simple_table():
    table = Table(
        headers=["Name", "Age", "City"],
        rows=[
            ["Alice", "30", "Amsterdam"],
            ["Bob", "25", "Rotterdam"],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| Name  | Age | City      |\n"
        "| ----- | --- | --------- |\n"
        "| Alice | 30  | Amsterdam |\n"
        "| Bob   | 25  | Rotterdam |"
    )


def test_format_table_aligns_columns():
    table = Table(
        headers=["Name", "Age", "City"],
        rows=[
            ["A", "100", "Amsterdam"],
            ["Alexander", "5", "Rome"],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| Name      | Age | City      |\n"
        "| --------- | --- | --------- |\n"
        "| A         | 100 | Amsterdam |\n"
        "| Alexander | 5   | Rome      |"
    )


def test_format_table_minimum_separator_width():
    table = Table(
        headers=["A", "B"],
        rows=[
            ["x", "y"],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| A   | B   |\n"
        "| --- | --- |\n"
        "| x   | y   |"
    )


def test_format_table_with_empty_cells():
    table = Table(
        headers=["Name", "Age", "City"],
        rows=[
            ["Alice", "", "Amsterdam"],
            ["", "25", ""],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| Name  | Age | City      |\n"
        "| ----- | --- | --------- |\n"
        "| Alice |     | Amsterdam |\n"
        "|       | 25  |           |"
    )


def test_format_table_preserves_inline_markdown():
    table = Table(
        headers=["Name", "Role"],
        rows=[
            ["**Alice**", "*Developer*"],
            ["`Bob`", "**Admin**"],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| Name      | Role        |\n"
        "| --------- | ----------- |\n"
        "| **Alice** | *Developer* |\n"
        "| `Bob`     | **Admin**   |"
    )


from mdfix.parser import parse_elements


def test_format_parsed_table():
    content = (
        "| Name|Age|City|\n"
        "|---|---|---|\n"
        "|Alice|30|Amsterdam|\n"
        "|Bob|25|Rotterdam|\n"
    )

    elements = parse_elements(content)

    table = elements[0]

    result = format_table(table)

    assert result == (
        "| Name  | Age | City      |\n"
        "| ----- | --- | --------- |\n"
        "| Alice | 30  | Amsterdam |\n"
        "| Bob   | 25  | Rotterdam |"
    )


def test_format_table_pads_missing_cells():
    table = Table(
        headers=["Name", "Age", "City"],
        rows=[
            ["Alice", "30"],
        ],
        position=SourcePosition(line=1),
    )

    result = format_table(table)

    assert result == (
        "| Name  | Age | City |\n"
        "| ----- | --- | ---- |\n"
        "| Alice | 30  |      |"
    )


def test_format_table_rejects_extra_cells():
    table = Table(
        headers=["Name", "Age"],
        rows=[
            ["Alice", "30", "Amsterdam"],
        ],
        position=SourcePosition(line=1),
    )

    with pytest.raises(ValueError, match="more cells than headers"):
        format_table(table)
