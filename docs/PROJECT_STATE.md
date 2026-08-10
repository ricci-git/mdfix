# mdfix Project State

## Current Version

Version: v0.7.8

Status:

Stable

Last Completed:

Inline Parser Edge Cases and Link Children Parsing

## Repository State

Branch:

master

Latest Commit:

8f8e65c

Latest Tag:

v0.7.8

Remote:

origin/master

Working Tree:

clean

## Validation

pytest:

79 passed

ruff:

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
Inline Parser
    |
    v
Inline AST
```

Current Inline Parser architecture:

```text
Markdown text
    |
    v
Link detection
    |
    v
Marker detection
    |
    v
Inline element creation
    |
    v
Inline AST
```

The current parser supports the defined inline structures but is not yet a general tokenizer-based recursive parser.

## Completed Milestones

### v0.7.0

Inline AST Foundation

Implemented:

* InlineElement base class
* Text
* Strong
* Emphasis
* InlineCode
* Link
* Paragraph inline representation
* Inline AST tests

### v0.7.1

Inline Parser Contract

Implemented:

* `parse_inline()`
* plain text parsing
* empty input handling
* initial parser contract

### v0.7.2

Strong Inline Parsing

Implemented:

* `**strong**`
* `__strong__`
* mixed text handling
* invalid syntax handling

### v0.7.3

Emphasis Inline Parsing

Implemented:

* `*italic*`
* `_italic_`
* mixed text handling
* unclosed emphasis handling
* empty emphasis handling

### v0.7.4

Inline Code Parsing

Implemented:

* `` `code` ``
* inline code within text
* unclosed inline code handling
* empty inline code handling

### v0.7.5

Link Parsing Support

Implemented:

* `[label](url)`
* links within surrounding text
* empty label handling
* empty URL handling
* unclosed link handling

### v0.7.6

Inline Parser Refactoring

Implemented:

* separated link detection
* separated marker detection
* inline element creation helper
* link element creation helper
* improved marker handling
* regression coverage for nested inline cases

### v0.7.7

Recursive Link Children Parsing

Implemented:

* inline parsing inside link labels
* Strong children inside links
* Emphasis children inside links
* InlineCode children inside links
* recursive construction of link children

This is limited recursive parsing for link labels.

It is not a general recursive inline parser.

### v0.7.8

Inline Parser Edge Cases

Implemented and validated:

* unmatched Strong markers
* unmatched Emphasis markers
* link trailing text
* mixed inline children inside links
* additional inline parser regression coverage

Current validation:

* 79 tests passed
* ruff passed

## Current Inline AST

Supported elements:

```text
Text
Strong
Emphasis
InlineCode
Link
```

Examples:

```markdown
plain text
```

```text
Text("plain text")
```

```markdown
**important**
```

```text
Strong(
    Text("important")
)
```

```markdown
*note*
```

```text
Emphasis(
    Text("note")
)
```

```markdown
`python`
```

```text
InlineCode("python")
```

```markdown
[mdfix](https://example.com)
```

```text
Link(
    children=[
        Text("mdfix")
    ],
    url="https://example.com"
)
```

Link children may contain supported inline structures:

```markdown
[hello **world**](https://example.com)
```

```text
Link(
    children=[
        Text("hello "),
        Strong(
            Text("world")
        )
    ],
    url="https://example.com"
)
```

## Current Architectural Limitation

The current `parse_inline()` implementation is based on single-match detection.

It can recognize and construct individual inline elements and supports limited recursive parsing inside link labels.

It does not yet provide a general recursive inline parsing architecture.

The following capabilities are intentionally deferred:

* general tokenizer;
* token stream;
* recursive parser;
* arbitrary nested inline structures;
* multiple sequential inline structures;
* complete mixed inline expression parsing.

These limitations define the scope of the `v0.8.x` development cycle.

## Next Development Cycle

Version:

v0.8.0

Title:

Recursive Inline Parser Foundation

Goal:

Replace the current single-match inline parsing approach with a tokenizer-based recursive parser architecture while preserving the existing Inline AST model and current behavior.

The `v0.8.0` development cycle is divided into smaller implementation milestones.

### Planned Subversions

#### v0.8.1

Inline Tokenization Foundation

Goal:

Introduce an internal tokenization layer for inline Markdown syntax.

Planned responsibilities:

* recognize inline markers;
* recognize text segments;
* recognize link boundaries;
* represent opening and closing markers;
* preserve source order;
* establish tokenizer tests.

#### v0.8.2

Recursive Inline Parsing

Goal:

Build Inline AST recursively from the token stream.

Planned capabilities:

* nested Strong;
* nested Emphasis;
* nested InlineCode where valid;
* nested structures inside Link;
* recursive child parsing.

#### v0.8.3

Sequential Inline Elements

Goal:

Support multiple inline structures within the same text.

Examples:

```markdown
**one** and *two*
```

```markdown
Hello `code` and [link](https://example.com)
```

The parser must preserve element order.

#### v0.8.4

Mixed Structures and Edge Cases

Goal:

Expand parser behavior for combinations of supported inline elements and establish explicit handling of malformed syntax.

Focus:

* mixed nesting;
* adjacent elements;
* unmatched markers;
* empty structures;
* malformed links;
* regression cases.

#### v0.8.5

Parser Cleanup and Regression Suite

Goal:

Stabilize the parser implementation after the architectural transition.

Focus:

* remove obsolete parsing paths;
* simplify parser responsibilities;
* strengthen parser contracts;
* consolidate regression tests;
* verify backward compatibility.

#### v0.8.6

Stabilization

Goal:

Finalize the `v0.8.x` recursive parser architecture and prepare the next stable development milestone.

Validation:

* complete test suite;
* ruff;
* regression verification;
* documentation synchronization.

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

* preserve the existing Inline AST model unless a concrete requirement requires change;
* do not patch individual marker cases when the problem belongs to parser architecture;
* separate tokenization from AST construction;
* keep tokenizer and parser responsibilities distinct;
* introduce no external dependencies;
* maintain backward compatibility where practical;
* do not optimize prematurely.

Do not:

* introduce dependencies;
* mix tokenization and AST construction unnecessarily;
* expand `v0.8.x` into rendering or formatting;
* change unrelated Block AST behavior;
* rewrite working components without a concrete architectural reason.

## Documentation Rule

`docs/PROJECT_STATE.md` is the operational source of truth for the current development state.

Update it when:

* a milestone is completed;
* the current version changes;
* repository state changes materially;
* validation results establish a new baseline;
* the next development target is defined.

Architectural design documents should describe stable or intentionally adopted architecture.

Do not modify architectural documentation merely to reflect an unverified implementation idea.
