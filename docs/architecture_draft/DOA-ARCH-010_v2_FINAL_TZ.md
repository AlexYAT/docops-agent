# architecture_draft — DOA-ARCH-010 (FINAL)

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-010
- Status: accepted
- Date: 2026-04-08
- Parent: DOA-ARCH-003

---

# 1. Overview

Единый документ ТЗ для DocOps Agent (MVP).
Объединяет архитектурные разделы 005–009.
Является **single source of truth верхнего уровня**.

---

# 2. Scope (MVP)

- markdown-only система
- один пользователь
- ручное соблюдение правил
- отсутствие автоматизации, UI и API

---

# 3. Roles & Scenarios

Роль:
- User — оператор системы

Сценарии:
- создание документа
- фиксация решения (decision_log)
- планирование (midterm → operational)
- выполнение (implementation_snapshot)
- проверка (audit_check)

---

# 4. Document Model

Doc types:
- idea_to_mvp
- architecture_draft
- decision_log
- implementation_snapshot
- audit_check
- longterm_plan (optional)
- midterm_plan
- operational_plan

---

# 5. Metadata Model

Обязательные поля:
- project
- doc_type
- id
- status
- date
- parent (может быть null)

Связи:
- parent
- replaces

---

# 6. Naming Convention

Формат:
<PROJECT>-<TYPE>-<NNN>

Правила:
- уникальность ID
- сквозная нумерация внутри TYPE
- соответствие project prefix

---

# 7. System Rules

1. Docs-first — всё фиксируется в документах  
2. Planning-first — работа только через план  
3. Create-only — смысловые изменения только через новый документ  
4. Explicit decisions — решения через decision_log  
5. Traceability — все связи прослеживаемы  

Контроль:
- manual enforcement
- validation + audit_check

---

# 8. Validation

Валидация выполняется вручную пользователем:

- metadata validation
- naming validation
- link validation

Документ без валидации считается невалидным.

---

# 9. Workflow (MVP)

1. идея → idea_to_mvp  
2. архитектура → architecture_draft  
3. решения → decision_log  
4. планирование → midterm_plan → operational_plan  
5. выполнение → implementation_snapshot  
6. проверка → audit_check  

---

# 10. Definition of Done

Система считается готовой если:
- используются все doc_types
- соблюдается naming
- metadata валидна
- применяются system rules
- есть traceability
- для всех значимых изменений есть decision_log + связь с планом/снапшотом

---

# 11. Итог

DOA-ARCH-010 является:
- canonical документом
- базой для реализации
- источником для operational_plan
