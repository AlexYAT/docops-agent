# operational_plan — DOA-OP-006

## Metadata
- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-006
- Status: draft
- Date: 2026-04-08
- Parent: DOA-ARCH-012

---

## Goal
Выполнить архитектурное расширение DocOps Agent:
добавить doc_types `other` и `rules`, создать соответствующие каталоги и подготовить систему к использованию новых типов документов.

---

## Scope

### Includes
- фиксацию decision_log
- выпуск новой версии architecture_draft
- создание каталогов `docs/other`, `docs/rules`
- создание каталогов `templates/other`, `templates/rules`
- подготовку шаблонов для `other` и `rules`
- проверку naming и metadata для новых типов

### Excludes
- миграцию всех существующих документов в новые типы
- полную переработку README / WORKFLOW
- автоматизацию валидации

---

## Tasks

### DOA-OP-006-T01 — Принять decision о новых doc_types
**Description**
Зафиксировать решение о введении `other` и `rules`.

**Done when**
- создан `DOA-DEC-030`
- decision описывает назначение и guardrails

---

### DOA-OP-006-T02 — Выпустить новую версию architecture_draft
**Description**
Зафиксировать архитектурное изменение в новой версии ARCH.

**Done when**
- создан `DOA-ARCH-012`
- в ARCH зафиксированы новые doc_types и naming mapping

---

### DOA-OP-006-T03 — Создать каталоги docs и templates
**Description**
Добавить:
- `docs/other`
- `docs/rules`
- `templates/other`
- `templates/rules`

**Done when**
- каталоги созданы
- существующая структура не нарушена

---

### DOA-OP-006-T04 — Создать шаблоны для новых doc_types
**Description**
Подготовить markdown templates для `other` и `rules`.

**Done when**
- существует template для `other`
- существует template для `rules`
- шаблоны используют стандартную metadata model

---

### DOA-OP-006-T05 — Проверить naming и traceability
**Description**
Проверить новые типы на соответствие naming, metadata и parent-links.

**Done when**
- подтверждены `DOA-OTH-XXX` и `DOA-RUL-XXX`
- не выявлено конфликтов с текущей архитектурой

---

### DOA-OP-006-T06 — Зафиксировать snapshot цикла
**Description**
После выполнения изменений создать implementation_snapshot.

**Done when**
- создан новый implementation_snapshot
- зафиксирован результат цикла расширения архитектуры

---

## Dependencies
- T02 depends on T01
- T03 depends on T02
- T04 depends on T03
- T05 depends on T04
- T06 depends on T05

---

## Definition of Done
План считается выполненным, если:
- введены doc_types `other` и `rules`
- создана новая версия architecture_draft
- созданы каталоги docs/templates
- существуют шаблоны новых типов
- naming и metadata согласованы
- создан implementation_snapshot

---

## Notes
- это отдельный архитектурный цикл, а не исправление старых документов
- существующие legacy документы не трогаются без отдельного решения
- новые типы вводятся минимально и под guardrails
