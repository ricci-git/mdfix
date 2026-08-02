from dataclasses import dataclass


@dataclass(slots=True)
class InlineElement:
    """Base class for inline Markdown AST elements."""


@dataclass(slots=True)
class Text(InlineElement):
    text: str


@dataclass(slots=True)
class Strong(InlineElement):
    children: list[InlineElement]


@dataclass(slots=True)
class Emphasis(InlineElement):
    children: list[InlineElement]


@dataclass(slots=True)
class InlineCode(InlineElement):
    code: str


@dataclass(slots=True)
class Link(InlineElement):
    children: list[InlineElement]
    url: str