# DocOps Agent — decision_log

## Metadata
Project: docops-agent
Doc type: decision_log
ID: DOA-DEC-063
Date: 2026-04-25
Parent: DOA-OP-038
Status: accepted

---

## Title
Use fixed doc_type to folder mapping

---

## Context

В рамках стабилизации процесса создания документов необходимо устранить расползание структуры папок.

Сейчас документы могут создаваться в разных местах, если папка явно указана в prompt или выбрана вручную.

Это нарушает предсказуемость DocOps workflow и усложняет навигацию.

---

## Decision

Использовать правило:

один doc_type соответствует одной фиксированной папке.

Документ должен создаваться только в папке, соответствующей его doc_type.

---

## Mapping

| doc_type | folder |
|---|---|
| idea_to_mvp | docs/idea_to_mvp/ |
| architecture_draft | docs/architecture/ |
| decision_log | docs/decision_log/ |
| operational_plan | docs/operational_plan/ |
| implementation_snapshot | docs/implementation_snapshot/ |
| audit_check | docs/audit_check/ |
| longterm_plan | docs/longterm_plan/ |
| midterm_plan | docs/midterm_plan/ |

---

## Consequences

- структура репозитория становится предсказуемой
- пользователь больше не выбирает папку вручную
- Cursor должен определять папку по doc_type
- новые документы создаются только в канонической папке

---

## Non-goals

- не переносить существующие документы
- не изменять validator
- не добавлять автоматизацию
- не создавать aliases для папок

---

## Follow-up

Следующий шаг по DOA-OP-038:

T02 — Define ID generation rule.
