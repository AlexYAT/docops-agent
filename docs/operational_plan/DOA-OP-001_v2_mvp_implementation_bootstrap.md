# operational_plan — DOA-OP-001

## Metadata
- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-001
- Status: accepted
- Date: 2026-04-08
- Parent: DOA-ARCH-010
- Replaces: DOA-OP-001 (draft)

---

# 1. Goal

Запустить MVP DocOps системы на основе утвержденного ТЗ (DOA-ARCH-010).

---

# 2. Scope

Включает:
- создание структуры проекта
- создание шаблонов документов
- создание примеров документов
- описание базового workflow
- первичный аудит

Не включает:
- автоматизацию
- UI/API
- сложную логику

---

# 3. Tasks

## DOA-OP-001-T01 — Создать структуру репозитория

**Описание**
Создать базовую структуру папок:

- docs/
  - decision_log/
  - architecture_draft/
  - operational_plan/
  - implementation_snapshot/
  - audit_check/

**Done when**
- структура создана
- README добавлен

---

## DOA-OP-001-T02 — Создать шаблоны doc_types

**Описание**
Создать markdown-шаблоны для:

- idea_to_mvp
- architecture_draft
- decision_log
- implementation_snapshot
- audit_check
- longterm_plan
- midterm_plan
- operational_plan

Шаблон включает:
- Metadata блок
- Основные секции doc_type

**Done when**
- для каждого doc_type есть шаблон
- шаблоны соответствуют metadata + naming

---

## DOA-OP-001-T03 — Создать примеры документов

**Описание**
Создать минимум по одному заполненному документу каждого типа.

**Done when**
- документы осмысленные (не пустые)
- naming валиден
- metadata валидна

---

## DOA-OP-001-T04 — Описать workflow пользователя

**Описание**
Создать WORKFLOW.md (вне doc_types)

Содержит:
- создание документов
- принятие решений
- выполнение задач

**Dependencies**
- зависит от DOA-OP-001-T03

**Done when**
- workflow покрывает все doc_types
- понятен пользователю

---

## DOA-OP-001-T05 — Провести audit_check

**Описание**
Проверить систему:
- naming
- metadata
- связи

**Done when**
- создан audit_check
- выявленные проблемы зафиксированы
- создан decision_log при нарушениях

---

## DOA-OP-001-T06 — Зафиксировать implementation_snapshot

**Описание**
Сделать снапшот состояния системы

**Done when**
- создан implementation_snapshot
- отражает структуру и документы

---

## DOA-OP-001-T07 — Зафиксировать решения

**Описание**
Зафиксировать решения, принятые в процессе

**Done when**
- созданы decision_log записи
- покрыты ключевые решения

---

# 4. Dependencies

- T02 зависит от T01
- T03 зависит от T02
- T04 зависит от T03
- T05 зависит от T03
- T06 зависит от T05
- T07 выполняется параллельно

---

# 5. Definition of Done

План выполнен если:

- создана структура docs
- есть шаблоны всех doc_types
- есть примеры документов
- соблюдены naming и metadata
- выполнен audit_check
- все критичные проблемы исправлены ИЛИ задокументированы
- есть implementation_snapshot
- есть decision_log для значимых решений

---

# 6. Notes

- все задачи выполняются вручную
- любые решения фиксируются через decision_log
- workflow документ не является doc_type (исключение MVP)
