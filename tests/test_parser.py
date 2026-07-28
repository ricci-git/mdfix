from pathlib import Path

from mdfix.document import Document
from mdfix.parser import parse_markdown


def test_parse_markdown(tmp_path: Path):
    markdown_file = tmp_path / "README.md"
    markdown_file.write_text(
        "# Title\n\nContent",
        encoding="utf-8",
    )

    document = parse_markdown(markdown_file)

    assert isinstance(document, Document)
    assert document.path == markdown_file
    assert document.content == "# Title\n\nContent"
    assert document.elements == []