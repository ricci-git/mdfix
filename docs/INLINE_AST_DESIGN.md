---

Title: Inline AST Design
Code: DESIGN-001
Version: 0.7.0
Status: Active

Owner: mdfix Project
Layer: Architecture
Type: Design Document
Document Class: Technical Design
Audience: Developers, Contributors, Maintainers

Canonical Language: uk
Translations: en

Created: 2026-08-02
Last Updated: 2026-08-02

Related Documents:

* README.md

Related ADRs:

---

## Inline AST Design

* **Українська версія**

## 1. Призначення документа

Цей документ описує архітектуру Inline AST (Abstract Syntax Tree) у проєкті `mdfix`.

Inline AST є внутрішнім представленням текстових елементів Markdown всередині блокових елементів документа.

Основна мета Inline AST:

* відокремити структуру тексту від простого рядка;
* забезпечити безпечний аналіз та модифікацію Markdown;
* створити основу для майбутніх форматерів, валідаторів та автоматичних виправлень.

## 2. Контекст

Початкова архітектура `mdfix` працювала на рівні блокових елементів Markdown.

Поточний рівень представлення:

```text
Markdown file
    |
    v
Scanner
    |
    v
Parser
    |
    v
Document
    |
    v
Block AST
```

Block AST представляє великі структурні елементи:

* Heading;
* Paragraph;
* List;
* Table;
* BlockQuote;
* CodeBlock;
* HorizontalRule.

Однак текст всередині блоків залишався простим рядком.

Наприклад:

```markdown
This is **important** text.
```

на рівні Paragraph раніше представлялося як:

```text
Paragraph(
    text="This is **important** text."
)
```

Така модель не дозволяла безпечно працювати з окремими частинами тексту.

---

## 3. Проблема

Markdown текст може містити вкладені inline конструкції:

* звичайний текст;
* жирний текст;
* курсив;
* inline code;
* посилання;
* майбутні розширення.

При роботі тільки зі строкою виникають проблеми:

* складно виконувати точкові зміни;
* складно зберігати структуру форматування;
* складно створювати автоматичні виправлення без пошкодження документа.

Тому необхідний окремий рівень представлення.

---

## 4. Архітектурна модель

Після додавання Inline AST структура документа має вигляд:

```text
Markdown file
    |
    v
Scanner
    |
    v
Parser
    |
    v
Document
    |
    +----------------+
    |                |
    v                v
 Block AST       Inline AST
```

Block AST відповідає за структуру документа.

Inline AST відповідає за структуру тексту всередині блоків.

---

## 5. Inline AST Elements

Початкова версія v0.7.0 визначає базові inline елементи.

### Text

Представляє звичайний текст.

Приклад:

```markdown
hello world
```

Модель:

```text
Text("hello world")
```

---

### Strong

Представляє жирний текст.

Markdown:

```markdown
**important**
```

Модель:

```text
Strong(
    Text("important")
)
```

---

### Emphasis

Представляє курсив.

Markdown:

```markdown
*note*
```

Модель:

```text
Emphasis(
    Text("note")
)
```

---

### InlineCode

Представляє код всередині рядка.

Markdown:

```markdown
`python`
```

Модель:

```text
InlineCode("python")
```

---

### Link

Представляє посилання.

Markdown:

```markdown
[mdfix](https://example.com)
```

Модель:

```text
Link(
    text="mdfix",
    url="https://example.com"
)
```

---

## 6. Інтеграція з Block AST

У версії v0.7.0 клас Paragraph отримує підтримку inline структури.

До:

```python
Paragraph(
    text="hello"
)
```

Після:

```python
Paragraph(
    text="hello",
    inline=None
)
```

Механізм зворотно сумісний.

Старий код може використовувати поле `text`.

Новий код може використовувати поле `inline`.

---

## 7. Відповідальність компонентів

### Block Parser

Відповідає за:

* визначення блокових елементів;
* створення Document структури;
* визначення меж блоків.

Не відповідає за:

* розбір форматування тексту.

---

### Inline Parser

Майбутній компонент.

Відповідатиме за:

* аналіз текстового вмісту;
* створення Inline AST;
* вкладені inline конструкції.

---

## 8. Поточний стан реалізації

Версія 0.7.0 містить:

* моделі Inline AST;
* базові inline елементи;
* інтеграцію з Paragraph;
* автоматичні тести.

Не реалізовано:

* inline parser;
* inline rendering;
* автоматичне відновлення Markdown syntax;
* складні вкладені структури.

---

## 9. Майбутній розвиток

Наступні можливі етапи:

1. Inline Parser
2. Inline AST integration into Parser pipeline
3. Inline validation rules
4. Safe Markdown transformations
5. Formatting engine

---

* **English Translation**

## en. Inline AST Design

## 1. Document Purpose

This document describes the Inline AST (Abstract Syntax Tree) architecture in the `mdfix` project.

Inline AST is an internal representation of Markdown text elements inside document blocks.

The main goals:

* separate text structure from plain strings;
* enable safe Markdown analysis and modification;
* provide a foundation for future formatters, validators and automated fixes.

---

## 2. Context

The initial `mdfix` architecture operated on Markdown block elements.

Current representation:

```text
Markdown file
    |
    v
Scanner
    |
    v
Parser
    |
    v
Document
    |
    v
Block AST
```

Block AST represents:

* Heading;
* Paragraph;
* List;
* Table;
* BlockQuote;
* CodeBlock;
* HorizontalRule.

Text inside blocks was previously stored as plain strings.

---

## 3. Problem

Markdown text contains inline structures:

* plain text;
* strong emphasis;
* emphasis;
* inline code;
* links;
* future extensions.

String-only representation makes:

* precise modifications difficult;
* formatting preservation difficult;
* safe automatic fixes difficult.

Inline AST introduces a dedicated representation layer.

---

## 4. Architecture

After introducing Inline AST:

```text
Markdown file
    |
    v
Scanner
    |
    v
Parser
    |
    v
Document
    |
    +----------------+
    |                |
    v                v
 Block AST       Inline AST
```

Block AST manages document structure.

Inline AST manages text structure inside blocks.

---

## en. 5. Inline AST Elements

Version 0.7.0 defines initial inline elements:

* Text
* Strong
* Emphasis
* InlineCode
* Link

These elements provide the foundation for future parsing and transformation.

---

## 6. Integration with Block AST

In version 0.7.0, Paragraph supports inline representation.

Previous model:

```python
Paragraph(
    text="hello"
)
```

New model:

```python
Paragraph(
    text="hello",
    inline=None
)
```

The change remains backward compatible.

---

## 7. Component Responsibilities

Block Parser:

* identifies block elements;
* builds document structure;
* manages block boundaries.

Inline Parser:

* analyzes text content;
* creates Inline AST;
* handles nested inline structures.

---

## 8. Current Implementation Status

Implemented:

* Inline AST models;
* basic inline elements;
* Paragraph integration;
* automated tests.

Not implemented:

* inline parser;
* inline rendering;
* Markdown reconstruction;
* complex nested inline structures.

---

## 9. Future Development

Possible next stages:

1. Inline Parser
2. Parser pipeline integration
3. Inline validation rules
4. Safe Markdown transformations
5. Formatting engine
