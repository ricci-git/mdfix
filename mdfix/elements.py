from dataclasses import dataclass


@dataclass(slots=True)
class SourcePosition:
    line: int
    column: int = 1


@dataclass(slots=True)
class Element:
    """Base class for all Markdown AST elements."""

    position: SourcePosition


@dataclass(slots=True)
class Heading(Element):
    level: int
    title: str


@dataclass(slots=True)
class Paragraph(Element):
    text: str


@dataclass(slots=True)
class BlockQuote(Element):
    text: str


@dataclass(slots=True)
class Table(Element):
    rows: list[list[str]]


@dataclass(slots=True)
class CodeBlock(Element):
    language: str | None
    code: str


@dataclass(slots=True)
class List(Element):
    ordered: bool
    items: list[str]