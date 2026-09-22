# mdfix Project State

## Current Version

Version: v0.8.2

Status:

Stable

Last Completed:

Recursive Inline Parsing

## Repository State

Branch:

master

Latest Commit:

c479bd1

Latest Tag:

v0.8.2

Remote:

origin/master

Working Tree:

clean

## Validation

pytest:

118 passed

ruff:

passed

git diff --check:

passed

## Architecture Progress

Current pipeline:

```text
Markdown
    |
    v
Block Parser
    |
    v
Block AST
    |
    v
Inline Tokenizer
    |
    v
Inline Token Stream
    |
    v
Recursive Inline Parser
    |
    v
Inline AST
```

Current Inline Parser architecture:

```text
Markdown text
    |
    v
Inline Tokenizer
    |
    v
Token Stream
    |
    v
Recursive Inline Parser
    |
    v
Inline AST
```

The inline parsing architecture has transitioned from single-match detection to a tokenizer-based recursive parser.

The existing Inline AST model is preserved.

## Completed Milestones

### v0.7.0

Inline AST Foundation

Implemented:

- InlineElement base class
- Text
- Strong
- Emphasis
- InlineCode
- Link
- Paragraph inline representation
- Inline AST tests

### v0.7.1

Inline Parser Contract

Implemented:

- parse_inline()
- plain text parsing
- empty input handling
- initial parser contract

### v0.7.2

Strong Inline Parsing

Implemented:

- **strong**
- `__strong__`
- mixed text handling
- invalid syntax handling

### v0.7.3

Emphasis Inline Parsing

Implemented:

- *italic*
- `_italic_`
- mixed text handling
- unclosed emphasis handling
- empty emphasis handling

### v0.7.4

Inline Code Parsing

Implemented:

- `code`
- inline code within text
- unclosed inline code handling
- empty inline code handling

### v0.7.5

Link Parsing Support

Implemented:

- [label](url)
- links within surrounding text
- empty label handling
- empty URL handling
- unclosed link handling

### v0.7.6

Inline Parser Refactoring

Implemented:

- separated link detection
- separated marker detection
- inline element creation helper
- link element creation helper
- improved marker handling
- regression coverage for nested inline cases

### v0.7.7

Recursive Link Children Parsing

Implemented:

- inline parsing inside link labels
- Strong children inside links
- Emphasis children inside links
- InlineCode children inside links
- recursive construction of link children

This was limited recursive parsing for link labels.

It was not a general recursive inline parser.

### v0.7.8

Inline Parser Edge Cases

Implemented and validated:

- unmatched Strong markers
- unmatched Emphasis markers
- link trailing text
- mixed inline children inside links
- additional inline parser regression coverage

Validation:

- 79 tests passed
- ruff passed

### v0.8.1

Inline Tokenizer Foundation

Implemented:

- inline tokenizer module
- inline token model
- token types for inline syntax
- source-order tokenization
- tokenizer test coverage
- inline token test coverage

The tokenizer establishes a separate tokenization layer between Markdown text and inline AST construction.

Validation:

- 96 tests passed
- ruff passed
- git diff --check passed

### v0.8.2

Recursive Inline Parsing

Implemented:

- Inline Tokenizer integration
- Inline Token Stream
- recursive inline parser
- nested inline token parsing
- nested inline content inside links
- underscore Strong tokens
- underscore Emphasis tokens
- parser migration from direct text matching to token stream
- removal of obsolete inline parser helpers
- nested Strong inside Emphasis
- regression test coverage for nested inline parsing

Validation:

- 118 tests passed
- ruff passed
- git diff --check passed

Current implementation:

```text
Markdown text
    |
    v
Inline Tokenizer
    |
    v
Inline Token Stream
    |
    v
Recursive Inline Parser
    |
    v
Inline AST
```

The recursive parser replaces the previous single-match parsing approach.

## Current Inline AST

Supported elements:

- Text
- Strong
- Emphasis
- InlineCode
- Link

Examples:

```markdown
plain text
Text("plain text")
**important**
Strong(
    Text("important")
)
*note*
Emphasis(
    Text("note")
)
`python`
InlineCode("python")
[mdfix](https://example.com)
Link(
    children=[
        Text("mdfix")
    ],
    url="https://example.com"
)
```

Nested inline structures are supported:

```markdown
**bold *italic***
Strong(
    children=[
        Text("bold "),
        Emphasis(
            children=[
                Text("italic")
            ]
        )
    ]
)
```

The parser also supports recursive inline parsing inside link labels:

```markdown
[hello **world**](https://example.com)
Link(
    children=[
        Text("hello "),
        Strong(
            children=[
                Text("world")
            ]
        )
    ],
    url="https://example.com"
)
```

## Current Architecture

The parser is now divided into distinct responsibilities:

- **Inline Tokenizer**

Responsible for:

- reading Markdown inline source;
- recognizing inline syntax;
- producing tokens;
- preserving source order;
- separating lexical recognition from AST construction.

- **Inline Parser**

Responsible for:

- consuming the token stream;
- recognizing structural relationships between tokens;
- constructing Inline AST nodes;
- recursively constructing child nodes;
- preserving nesting and element order.

- **Inline AST**

Responsible for representing parsed inline structure:

- Text
- Strong
- Emphasis
- InlineCode
- Link

The tokenizer does not construct AST elements.

The parser does not perform lexical tokenization directly.

## Architectural Limitations

The general recursive parsing architecture is now established, but the v0.8.x cycle is not yet complete.

The following areas remain intentionally deferred:

- complete sequential inline expression coverage;
- broader mixed inline structure handling;
- malformed syntax policy refinement;
- parser cleanup;
- regression suite consolidation;
- final architecture stabilization.

These areas define the remaining scope of the v0.8.x development cycle.

## Next Development Cycle

Version:

v0.8.x

Title:

Recursive Inline Parser Architecture

Goal:

Complete the transition to a tokenizer-based recursive inline parser while preserving the existing Inline AST model and current behavior.

- **Planned Subversions**

- **v0.8.3**

Sequential Inline Elements

Goal:

Support multiple inline structures within the same text.

Examples:

```markdonw
**one** and *two*
Hello `code` and [link](https://example.com)
```

The parser must preserve element order.

- **v0.8.4**

Mixed Structures and Edge Cases

Goal:

Expand parser behavior for combinations of supported inline elements and establish explicit handling of malformed syntax.

Focus:

- mixed nesting;
- adjacent elements;
- unmatched markers;
- empty structures;
- malformed links;
- regression cases.

- **v0.8.5**

Parser Cleanup and Regression Suite

Goal:

Stabilize the parser implementation after the architectural transition.

Focus:

- remove obsolete parsing paths;
- simplify parser responsibilities;
- strengthen parser contracts;
- consolidate regression tests;
- verify backward compatibility.

- **v0.8.6**

Stabilization

Goal:

Finalize the v0.8.x recursive parser architecture and prepare the next stable development milestone.

Validation:

- complete test suite;
- ruff;
- regression verification;
- documentation synchronization.

## Development Rules

Follow TDD:

1. Add failing test
2. Implement minimum code
3. Run pytest
4. Run ruff
5. Commit
6. Tag
7. Push

Architectural rules:

- preserve the existing Inline AST model unless a concrete requirement requires change;
- do not patch individual marker cases when the problem belongs to parser architecture;
- separate tokenization from AST construction;
- keep tokenizer and parser responsibilities distinct;
- introduce no external dependencies;
- maintain backward compatibility where practical;
- do not optimize prematurely.

Do not:

- introduce dependencies;
- mix tokenization and AST construction unnecessarily;
- expand v0.8.x into rendering or formatting;
- change unrelated Block AST behavior;
- rewrite working components without a concrete architectural reason.

## Documentation Rule

`docs/PROJECT_STATE.md` is the operational source of truth for the current development state.

Update it when:

- a milestone is completed;
- the current version changes;
- repository state changes materially;
- validation results establish a new baseline;
- the next development target is defined.

Architectural design documents should describe stable or intentionally adopted architecture.

Do not modify architectural documentation merely to reflect an unverified implementation idea.
