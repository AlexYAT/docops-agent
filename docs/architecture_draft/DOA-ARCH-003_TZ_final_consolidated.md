# architecture_draft — DOA-ARCH-003

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-003
- Status: draft
- Date: 2026-04-08
- Parent: DOA-DOC-IDEA

---

## 0. Summary
DocOps Agent — система управления разработкой через документацию (docs-first).
ТЗ фиксирует структуру системы, правила и planning layer для MVP.

## 0.1 Goal
Определить непротиворечивую архитектуру, достаточную для перехода к реализации.

## 0.2 Scope (MVP)
Входит:
- doc_types
- planning layer
- правила системы
- metadata
- naming convention
- связи документов

Не входит:
- update/sync
- auto-detection шаблонов
- внешние интеграции
- сложная агентность

---

## 1. Назначение системы

### 1.1 Проблема
- хаос в документации
- потеря связей
- зависимость от контекста в голове

### 1.2 Цель
Создать систему, где вся разработка управляется через документы.

### 1.3 Границы
Система ограничена документацией и planning layer.

---

## 2. Роли и сценарии

### 2.1 Роли
- Пользователь — создаёт документы и ведёт проект

### 2.2 Сценарии
1. Создание проекта
2. Выбор шаблона
3. Создание документа
4. decision_log
5. operational_plan
6. implementation_snapshot

### 2.3 Ограничения
Запрещены действия вне operational_plan

---

## 3. Модель документов

### Core
- idea_to_mvp
- architecture_draft
- decision_log
- implementation_snapshot
- audit_check

### Planning
- longterm_plan
- midterm_plan
- operational_plan

### Create-only
Документы не изменяются — создаются новые версии

---

## 4. Planning layer

### Уровни
- longterm
- midterm
- operational

### Связи
longterm → midterm → operational

### Правила
- нельзя работать вне operational_plan
- результат фиксируется snapshot

---

## 5. Правила системы

### docs-first
Сначала документ, потом код

### planning-first
Любая работа через план

### create-only
Без обновления

### explicit decisions
Все решения фиксируются

### traceability
Все связано

---

## 6. Metadata

Обязательные поля:
- project
- doc_type
- id
- status
- date
- parent

Status:
draft | review | accepted | obsolete

---

## 7. Naming

Формат:
PROJECT-TYPE-NUMBER

---

## 8. Связи

- idea → midterm
- midterm → operational
- decision → влияет на всё
- snapshot → фиксирует

---

## 9. Ограничения

- no sync
- no automation
- limited templates

---

## 10. DoD

ТЗ готово если:
- все разделы заполнены
- нет противоречий
- можно начать реализацию
