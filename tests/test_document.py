from pathlib import Path

from mdfix.document import Document


def test_document_creation():
    document = Document(
        path=Path("README.md"),
        content="# Title",
    )

    assert document.path.name == "README.md"
    assert document.content == "# Title"
    assert document.elements == []