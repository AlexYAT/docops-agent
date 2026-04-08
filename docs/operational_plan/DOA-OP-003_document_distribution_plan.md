# operational_plan — DOA-OP-003

## Metadata
- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-003
- Status: draft
- Date: 2026-04-08
- Parent: DOA-DEC-026

---

## Goal
Разложить документы из временного каталога `tz/` по канонической структуре `docs/<doc_type>/`
без потери traceability и с фиксацией legacy-артефактов.

---

## Scope

### Includes
- инвентаризация файлов в `tz/`
- классификация по doc_type
- раскладка по каноническим каталогам `docs/`
- фиксация конфликтов, дублей и legacy
- audit_check после раскладки

### Excludes
- переписывание содержания документов
- ретроспективное исправление исторических файлов без отдельного decision_log
- изменение утверждённой архитектуры DocOps

---

## Tasks

### DOA-OP-003-T01 — Инвентаризация файлов в tz
**Description**
Составить список всех файлов в `tz/` и определить для каждого предполагаемый doc_type.

**Done when**
- создана таблица/список всех файлов
- каждому файлу назначен doc_type или статус `unclassified`

---

### DOA-OP-003-T02 — Определить правила раскладки
**Description**
Для каждой группы файлов определить целевой каталог:
- ARCH → docs/architecture_draft/
- DEC → docs/decision_log/
- IMP → docs/implementation_snapshot/
- OP → docs/operational_plan/
- IDEA → docs/idea_to_mvp/
- LT → docs/longterm_plan/
- MT → docs/midterm_plan/
- AUD → docs/audit_check/

**Done when**
- для всех классифицированных файлов определён целевой каталог
- отдельно отмечены legacy/conflict files

---

### DOA-OP-003-T03 — Разложить документы по каноническим каталогам
**Description**
Переместить или скопировать файлы из `tz/` в соответствующие каталоги `docs/`
по принятой политике проекта.

**Done when**
- все классифицированные файлы размещены в `docs/<doc_type>/`
- ни один файл не потерян
- изменения выполнены согласованно с create-only подходом

---

### DOA-OP-003-T04 — Зафиксировать конфликты и legacy
**Description**
Выявить:
- дубли
- несколько версий одного документа
- неканоничные размещения
- файлы, которые не нужно исправлять ретроспективно

**Done when**
- создан decision_log при необходимости
- составлен список legacy/conflict files

---

### DOA-OP-003-T05 — Провести audit_check после раскладки
**Description**
Проверить:
- правильность размещения
- naming
- metadata
- parent-links
- наличие legacy-исключений

**Done when**
- создан audit_check
- нарушения либо исправлены, либо явно зафиксированы

---

### DOA-OP-003-T06 — Зафиксировать snapshot состояния
**Description**
После завершения раскладки создать implementation_snapshot текущего состояния документации.

**Done when**
- создан implementation_snapshot
- snapshot описывает новую каноническую структуру и known legacy

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
- все документы из `tz/` проинвентаризированы
- классифицированные документы размещены в `docs/<doc_type>/`
- legacy и конфликты зафиксированы
- выполнен audit_check
- создан implementation_snapshot

---

## Notes
- `tz/` рассматривается как staging/import зона, а не source of truth
- любые спорные случаи фиксируются через decision_log
- ретроспективные исправления без явной фиксации не выполняются
