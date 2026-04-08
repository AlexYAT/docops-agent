# operational_plan — DOA-OP-005

## Metadata
- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-005
- Status: draft
- Date: 2026-04-08
- Parent: DOA-DEC-029

---

## Goal
Создать README.md как публичную точку входа для внешнего пользователя и аудита.

---

## Scope

### Includes
- определение структуры README
- написание README
- добавление README в репозиторий

### Excludes
- переработка всей документации
- изменение существующих doc_types
- автоматизация документации

---

## Tasks

### DOA-OP-005-T01 — Определить структуру README
**Description**
Определить структуру README.md как entry point.

**Done when**
- структура README определена

---

### DOA-OP-005-T02 — Написать README
**Description**
Создать README.md с описанием системы.

**Done when**
- README содержит описание, концепции и how-to

---

### DOA-OP-005-T03 — Добавить README в репозиторий
**Description**
Добавить README.md в корень репозитория.

**Done when**
- README добавлен и доступен в GitHub

---

## Dependencies
- T02 depends on T01
- T03 depends on T02

---

## Definition of Done
План выполнен если:
- README создан
- README добавлен в репозиторий
- README понятен внешнему пользователю
