# architecture_draft — DOA-ARCH-001

## Summary
Полное техническое задание (ТЗ) для DocOps Agent (MVP)

## Goal
Определить полную структуру системы до начала реализации,
чтобы исключить хаос и ошибки при работе с документацией.

---

## 1. Назначение системы
DocOps Agent — система управления разработкой через документацию (docs-first).

Цель:
- убрать зависимость от контекста "в голове"
- структурировать разработку через документы
- обеспечить трассируемость всех действий

---

## 2. Роли и сценарии

### Пользователь:
- создаёт проект
- выбирает шаблон
- создаёт документы
- ведёт проект через planning layer

### Основные сценарии:
1. Создание проекта
2. Выбор шаблона
3. Создание документа
4. Фиксация решения (decision_log)
5. Планирование задач (operational_plan)
6. Фиксация реализации (implementation_snapshot)

---

## 3. Состав документов

### Core:
- idea_to_mvp
- architecture_draft
- decision_log
- implementation_snapshot
- audit_check

### Planning:
- longterm_plan
- midterm_plan
- operational_plan

---

## 4. Правила системы

- docs-first
- planning-first
- create-only
- explicit decisions
- traceability

---

## 5. Metadata структура

Обязательные поля:
- project
- doc_type
- id
- status
- date
- parent (опционально)

---

## 6. Naming convention

Формат:
<PROJECT>-<TYPE>-<NUMBER>

Пример:
DOA-DEC-003

---

## 7. Связи документов

- idea_to_mvp → midterm_plan
- midterm_plan → operational_plan
- decision_log → влияет на планы и архитектуру
- implementation_snapshot → фиксирует факт реализации

---

## 8. Ограничения MVP

- только create-only
- без update/sync
- без сложной автоматизации
- ограниченное количество шаблонов
