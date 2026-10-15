---
Title:  "mdfix Active Tasks (Milestone 5)"
Code:   "TS-MDFIX-005"
Version: "1.0.0"
Status:  "active"
Description: "Specific actionable tasks for the current milestone."
Owner:  "Ricci"
Layer:  "Project Management"
Type:   "Execution"
Document Class: "Internal"
Audience: "Developer"
Canonical Language: uk
Translations: none
Created: 2026-10-15
Last Updated: 2026-10-15
Reviewers: ["AI Assistant"]
Approved By: ["Ricci"]
Related Documents: ["docs/ROADMAP.md", "docs/BACKLOG.md"]
Related ADRs: []
---

## mdfix Active Tasks: Milestone 5

## Статус: In Progress

### Фаза 1: Easy Wins (Simple Regex/String Fixes)

*Ці задачі можна виконати паралельно або послідовно. Вони не потребують складної інтеграції з AST, працюють на рівні рядків.*

- [ ] **Task 5.1: Implement MD012 (Multiple Blank Lines)**
  - [ ] Write tests `tests/rules/test_md012_blank_lines.py`.
  - [ ] Implement rule `mdfix/rules/md012_blank_lines.py`.
  - [ ] Add to `registry.py`.
  - [ ] Verify auto-fix works.
- [ ] **Task 5.2: Implement MD026 (Trailing Punctuation)**
  - [ ] Write tests `tests/rules/test_md026_trailing_punct.py`.
  - [ ] Implement rule `mdfix/rules/md026_trailing_punct.py`.
  - [ ] Add to `registry.py`.
- [ ] **Task 5.3: Implement MD034 (Bare URLs)**
  - [ ] Write tests `tests/rules/test_md034_bare_url.py`.
  - [ ] Implement rule using regex.
  - [ ] Add to `registry.py`.
- [ ] **Task 5.4: Implement MD037-039 (Spaces in Markers)**
  - [ ] Combine into one task or separate? Separate is cleaner.
  - [ ] Tests + Impl for MD037 (Emphasis).
  - [ ] Tests + Impl for MD038 (Code Span).
  - [ ] Tests + Impl for MD039 (Link Text).
  - [ ] Add all to `registry.py`.

### Фаза 2: Context-Aware Fixes (Requires Block Awareness)

*Ці задачі складніші, бо треба дивитись на сусідні елементи (перед заголовком, після списку).*

- [ ] **Task 5.5: Implement MD022 (Heading Blanks)**
  - [ ] Analyze AST neighbors.
  - [ ] Write tests covering edge cases (first/last element).
  - [ ] Implement rule.
- [ ] **Task 5.6: Implement MD031 (Code Block Blanks)**
  - [ ] Similar logic to MD022 but for CodeBlock elements.
  - [ ] Write tests.
  - [ ] Implement rule.
- [ ] **Task 5.7: Implement MD032 (List Blanks)**
  - [ ] Detect List elements.
  - [ ] Ensure blank lines around them.
  - [ ] Write tests.
  - [ ] Implement rule.
- [ ] **Task 5.8: Implement MD058 (Table Blanks)**
  - [ ] Detect Table elements.
  - [ ] Ensure blank lines around them.
  - [ ] Write tests.
  - [ ] Implement rule.

### Фаза 3: Formatting Consistency

- [ ] **Task 5.9: Implement MD060 (Table Pipe Spacing)**
  - [ ] Normalize spaces inside table cells.
  - [ ] Integrate with existing Table Formatter logic if possible.
  - [ ] Write tests.
  - [ ] Implement rule.

### Фаза 4: Integration & Cleanup

- [ ] **Task 5.10: Update Documentation**
  - [ ] Update `README.md` with new rules list.
  - [ ] Update `CHANGELOG.md` with v0.10.0 entry (draft).
  - [ ] Create `docs/RULES_REFERENCE.md` detailing each rule's behavior.
- [ ] **Task 5.11: Final Validation**
  - [ ] Run full test suite (`pytest -q`).
  - [ ] Run linter (`ruff check .`).
  - [ ] Dogfood: Run `mdfix fix .` on project docs.
  - [ ] Commit & Push.
  - [ ] Tag release v0.10.0-beta.

---

### Notes

- *Приоритет: Спочатку Фаза 1 (швидкі перемоги), потім Фаза 2.*
- *Якщо задача блокується (наприклад, складний кейс з inline-парсером), перенести її в Backlog P1 і рухатись далі. Не застрягати.*

---

### Version History

| Version | Date       | Author      | Changes                                                                 |
| ------- | ---------- | ----------- | ----------------------------------------------------------------------- |
| 1.0.0   | 2026-10-15 | Ricci/AI    | Initial task breakdown for Milestone 5.                                 |
