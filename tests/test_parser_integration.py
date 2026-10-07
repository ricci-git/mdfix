import pytest
from pathlib import Path
from mdfix.parser import parse_markdown
from mdfix.elements import Paragraph
from mdfix.inline_elements import Strong, Text

def test_paragraph_contains_inline_ast(tmp_path: Path):
    """
    Verify that parsing a paragraph with bold text results in an Inline AST.
    Currently, Paragraph.text is populated, but Paragraph.inline is None.
    This test expects it to be populated after integration.
    """
    md_file = tmp_path / "test.md"
    # Simple markdown with bold text
    content = "# Header\nThis is **bold** text.\n"
    md_file.write_text(content)
    
    document = parse_markdown(md_file)
    
    # Find the paragraph element (index 1, since index 0 is Heading)
    assert len(document.elements) >= 2
    para = document.elements[1]
    
    assert isinstance(para, Paragraph)
    
    # CURRENT STATE: para.inline is likely None or missing
    # EXPECTED STATE: para.inline should contain [Text("This is "), Strong([Text("bold")]), Text(" text.")]
    
    assert hasattr(para, 'inline'), "Paragraph should have an 'inline' attribute"
    assert para.inline is not None, "Paragraph.inline should not be None"
    
    # Check structure loosely for now
    assert len(para.inline) > 0
    
    # Look for Strong element
    strong_found = False
    for node in para.inline:
        if isinstance(node, Strong):
            strong_found = True
            # Check child of Strong
            assert len(node.children) == 1
            assert isinstance(node.children[0], Text)
            assert node.children[0].text == "bold"
            
    assert strong_found, "Expected to find a Strong element inside Paragraph.inline"
