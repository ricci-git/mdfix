# Chat Handover

Project:
mdfix

Purpose:
Markdown parser and automatic fixer.

Current focus:
Inline parsing architecture completed.

Current milestone:
v0.8.2 completed.

Current architecture:

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

Important context:

- Use Ukrainian for explanations.
Keep English technical terms unchanged.
Work step-by-step.
Use TDD.
Do not skip tests.
Keep commits small.
Every feature gets its own version tag.
Do not start a new feature before the next milestone is defined.

Current validation:

118 tests passed
ruff passed
git diff --check passed

Current repository state:

Branch: master
Latest commit: c479bd1
Latest tag: v0.8.2
Remote: origin/master

Next step:

Review the current architecture and documentation.

Determine the next development problem and milestone before starting implementation.

Do not write code until the next milestone is agreed.
