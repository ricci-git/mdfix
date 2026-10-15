---
Title:  "mdfix Backlog"
Code:   "BL-MDFIX-001"
Version: "1.0.0"
Status:  "active"
Description: "Prioritized list of features, improvements, and technical debt items."
Owner:  "Ricci"
Layer:  "Project Management"
Type:   "Planning"
Document Class: "Internal"
Audience: "Developers, Maintainers"
Canonical Language: uk
Translations: en
Created: 2026-10-15
Last Updated: 2026-10-15
Reviewers: ["AI Assistant"]
Approved By: ["Ricci"]
Related Documents: ["docs/ROADMAP.md", "docs/TASKS.md", "proposal-2026-10-07.md"]
Related ADRs: []
---

## mdfix Backlog

## Українська версія

### P0: Critical / Must-Have (Milestone 5 Focus)

*Ці задачі блокують досягнення сумісності зі стандартом.*

1. **[Rule] MD012 Multiple Consecutive Blank Lines.**
    * *Опис:* Забороняти більше одного порожнього рядка підряд.
    * *Автофікс:* Так (замінити `\n\n+` на `\n\n`).
    * *Складність:* Низька.
2. **[Rule] MD022 Headings Surrounded by Blank Lines.**
    * *Опис:* Перед і після заголовка має бути порожній рядок.
    * *Автофікс:* Так (вставка `\n`).
    * *Складність:* Середня (потрібно знати тип попереднього/наступного елемента).
3. **[Rule] MD026 Trailing Punctuation in Heading.**
    * *Опис:* Заголовки не повинні закінчуватися на `.`, `,`, `;`, `:`, `!`, `?`.
    * *Автофікс:* Так (видалення символу).
    * *Складність:* Низька.
4. **[Rule] MD031 Fenced Code Blocks Surrounded by Blank Lines.**
    * *Опис:* Аналогічно MD022, але для блоків коду.
    * *Автофікс:* Так.
    * *Складність:* Середня.
5. **[Rule] MD032 Lists Surrounded by Blank Lines.**
    * *Опис:* Списки мають бути відокремлені порожніми рядками від тексту.
    * *Автофікс:* Так.
    * *Складність:* Середня.
6. **[Rule] MD034 Bare URL Used.**
    * *Опис:* Знаходити HTTP/HTTPS посилання без обрамлення `<...>` або `[text](url)`.
    * *Автофікс:* Так (загорнути в `<URL>`).
    * *Складність:* Низька (Regex).
7. **[Rule] MD037 Spaces Inside Emphasis Markers.**
    * *Опис:* `** Bold **` -> `**Bold**`.
    * *Автофікс:* Так.
    * *Складність:* Низька.
8. **[Rule] MD038 Spaces Inside Code Span Elements.**
    * *Опис:* `` ` code ` `` -> `` `code` ``.
    * *Автофікс:* Так.
    * *Складність:* Низька.
9. **[Rule] MD039 Spaces Inside Link Text.**
    * *Опис:* `[ text ](url)` -> `[text](url)`.
    * *Автофікс:* Так.
    * *Складність:* Низька.
10. **[Rule] MD058 Tables Surrounded by Blank Lines.**
    * *Опис:* Таблиці мають бути відокремлені порожніми рядками.
    * *Автофікс:* Так.
    * *Складність:* Середня.
11. **[Rule] MD060 Table Pipe Spacing.**
    * *Опис:* Пробіли всередині комірок `| a | b |` vs `|a|b|`.
    * *Автофікс:* Так.
    * *Складність:* Низька.

### P1: High Value / Should-Have (Milestone 6+)

*Покращення UX та гнучкості.*

1. **[Config] Rule Parameters Support.**
    * *Опис:* Дозволити налаштовувати параметри правил у `pyproject.toml` (напр., `line_length = 80` для MD013).
    * *Складність:* Висока (архітектурний зміни в Registry/Linter).
2. **[Rule] MD013 Line Length.**
    * *Опис:* Перевірка довжини рядка.
    * *Автофікс:* Ні (Manual only).
    * *Складність:* Низька для детекту, висока для коректного ігнорування коду/таблиць.
3. **[Perf] Parallel Processing.**
    * *Опис:* Використовувати `multiprocessing` або `asyncio` для сканування великих директорій.
    * *Складність:* Середня.
4. **[DX] VS Code Extension Prototype.**
    * *Опис:* Проста інтеграція для підсвічування помилок в реальному часі.
    * *Складність:* Висока.

### P2: Nice-to-Have / Future Ideas

1. **[Rule] MD040 Fenced Code Blocks Should Have Language.**
    * *Автофікс:* Ні (не можна вгадати мову).
2. **[Feature] Custom Rules Plugin System.**
    * *Опис:* Дозволити користувачам писати свої правила на Python.
3. **[Docs] Interactive Playground.**
    * *Опис:* Веб-сайт, де можна вставити Markdown і побачити результат фіксу онлайн.

### Technical Debt (From Proposal & State)

1. **[Refactor] Inline Parser Edge Cases.**
    * *Опис:* Покращити обробку екранованих символів (`\*`, `\``) та вкладених конструкцій.
    * *Джерело:* proposal-2026-10-07.md (Section 3).
2. **[Test] Property-Based Testing.**
    * *Опис:* Додати тести, які генерують випадкові Markdown-документи і перевіряють, чи не ламається парсер.
    * *Джерело:* proposal-2026-10-07.md (Section 4).

---

## English Translation

## en mdfix Backlog

### en P0: Critical / Must-Have (Milestone 5 Focus)

*These tasks block achieving standard compliance.*

1. **[Rule] MD012 Multiple Consecutive Blank Lines.**
    * *Desc:* Forbid more than one blank line in a row.
    * *Auto-fix:* Yes (replace `\n\n+` with `\n\n`).
    * *Complexity:* Low.
2. **[Rule] MD022 Headings Surrounded by Blank Lines.**
    * *Desc:* Require blank lines before and after headings.
    * *Auto-fix:* Yes (insert `\n`).
    * *Complexity:* Medium (needs context awareness).
3. **[Rule] MD026 Trailing Punctuation in Heading.**
    * *Desc:* Headings shouldn't end with `.`, `,`, `;`, `:`, `!`, `?`.
    * *Auto-fix:* Yes (remove char).
    * *Complexity:* Low.
4. **[Rule] MD031 Fenced Code Blocks Surrounded by Blank Lines.**
    * *Desc:* Similar to MD022 but for code blocks.
    * *Auto-fix:* Yes.
    * *Complexity:* Medium.
5. **[Rule] MD032 Lists Surrounded by Blank Lines.**
    * *Desc:* Lists must be separated from text by blank lines.
    * *Auto-fix:* Yes.
    * *Complexity:* Medium.
6. **[Rule] MD034 Bare URL Used.**
    * *Desc:* Find HTTP/HTTPS links without `<...>` or `[text](url)` wrapping.
    * *Auto-fix:* Yes (wrap in `<URL>`).
    * *Complexity:* Low (Regex).
7. **[Rule] MD037 Spaces Inside Emphasis Markers.**
    * *Desc:* `** Bold **` -> `**Bold**`.
    * *Auto-fix:* Yes.
    * *Complexity:* Low.
8. **[Rule] MD038 Spaces Inside Code Span Elements.**
    * *Desc:* `` ` code ` `` -> `` `code` ``.
    * *Auto-fix:* Yes.
    * *Complexity:* Low.
9. **[Rule] MD039 Spaces Inside Link Text.**
    * *Desc:* `[ text ](url)` -> `[text](url)`.
    * *Auto-fix:* Yes.
    * *Complexity:* Low.
10. **[Rule] MD058 Tables Surrounded by Blank Lines.**
    * *Desc:* Tables must be separated by blank lines.
    * *Auto-fix:* Yes.
    * *Complexity:* Medium.
11. **[Rule] MD060 Table Pipe Spacing.**
    * *Desc:* Enforce spacing inside cells `| a | b |`.
    * *Auto-fix:* Yes.
    * *Complexity:* Low.

### en P1: High Value / Should-Have (Milestone 6+)

*UX and flexibility improvements.*

1. **[Config] Rule Parameters Support.**
    * *Desc:* Allow configuring rule params in `pyproject.toml` (e.g., `line_length = 80`).
    * *Complexity:* High (architectural changes).
2. **[Rule] MD013 Line Length.**
    * *Desc:* Check line length limits.
    * *Auto-fix:* No (Manual).
    * *Complexity:* Low detection, high false-positive avoidance.
3. **[Perf] Parallel Processing.**
    * *Desc:* Use multiprocessing/asyncio for large dirs.
    * *Complexity:* Medium.
4. **[DX] VS Code Extension Prototype.**
    * *Desc:* Real-time error highlighting.
    * *Complexity:* High.

### en P2: Nice-to-Have / Future Ideas

1. **[Rule] MD040 Fenced Code Blocks Should Have Language.**
    * *Auto-fix:* No.
2. **[Feature] Custom Rules Plugin System.**
3. **[Docs] Interactive Playground.**

### en Technical Debt

1. **[Refactor] Inline Parser Edge Cases.**
    * *Source:* proposal-2026-10-07.md.
2. **[Test] Property-Based Testing.**
    * *Source:* proposal-2026-10-07.md.

---

### Version History

| Version | Date       | Author      | Changes                                                                      |
| ------- | ---------- | ----------- | ---------------------------------------------------------------------------- |
| 1.0.0   | 2026-10-15 | Ricci/AI    | Initial backlog creation consolidating ideas from proposals and discussions. |
