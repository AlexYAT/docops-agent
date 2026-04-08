# architecture_draft — DOA-ARCH-012

## Metadata
- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-012
- Status: draft
- Date: 2026-04-08
- Parent: DOA-DEC-030

---

## Summary
Новая версия архитектуры расширяет модель DocOps Agent двумя дополнительными doc_types:
`other` и `rules`.

## Goal
Устранить разрыв между фактической практикой проекта и текущей архитектурой, сохранив docs-first, create-only и traceability.

## Scope of change
Изменение затрагивает:
- модель документов (doc_types)
- структуру каталогов `docs/` и `templates/`
- naming convention
- правила использования вспомогательных и нормативных документов

Не затрагивает:
- базовую planning model
- create-only стратегию
- существующие core/planning doc_types

---

## 1. New doc_types

### 1.1 `other`
Назначение:
- вспомогательные документы проекта
- contextual/project-support файлы
- артефакты, на которые можно ссылаться, но которые не являются core/planning/rules

Примеры:
- `PROJECT_CONTEXT.md`
- дополнительные guides
- supporting notes
- catalog/index документы

Правила использования:
- применять только если документ не подходит ни под один существующий doc_type
- документ должен иметь metadata
- документ может быть родительским или ссылочным артефактом, если это логично

### 1.2 `rules`
Назначение:
- нормативные документы проекта
- process rules
- commit rules
- working discipline / operational rules

Примеры:
- commit rules
- pre-commit checklist
- process discipline rules

Правила использования:
- использовать только для норм и правил работы
- не смешивать с решениями (`decision_log`)
- изменение правил оформляется create-only через новый документ и/или decision_log

---

## 2. Updated document groups

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

### Support
- other
- rules

---

## 3. Updated repository structure

### docs/
- docs/architecture_draft/
- docs/audit_check/
- docs/decision_log/
- docs/idea_to_mvp/
- docs/implementation_snapshot/
- docs/longterm_plan/
- docs/midterm_plan/
- docs/operational_plan/
- docs/other/
- docs/rules/

### templates/
- templates/architecture_draft/
- templates/audit_check/
- templates/decision_log/
- templates/idea_to_mvp/
- templates/implementation_snapshot/
- templates/longterm_plan/
- templates/midterm_plan/
- templates/operational_plan/
- templates/other/
- templates/rules/

---

## 4. Naming update

Добавить новые TYPE mapping:
- `other` → `OTH`
- `rules` → `RUL`

Примеры:
- `DOA-OTH-001`
- `DOA-RUL-001`

---

## 5. Metadata update

Для `other` и `rules` действует та же metadata model:
- Project
- Doc type
- ID
- Status
- Date
- Parent

`Parent` может быть `null`, если документ является верхнеуровневым вспомогательным или нормативным артефактом.

---

## 6. Usage policy

### For `other`
Использовать только когда:
- документ полезен проекту
- на него нужно ссылаться
- он не подходит под существующие типы

### For `rules`
Использовать только когда:
- документ задаёт норму поведения
- документ описывает process discipline
- документ повторно используется как operational standard

---

## 7. Risks
- `other` может стать dumping zone
- правила могут дублироваться между `rules` и `decision_log`

## 8. Mitigations
- каждый новый документ должен проходить audit/validation
- для `other` применять stricter review
- важные изменения правил дополнительно фиксировать в `decision_log`

## 9. Definition of Done
Изменение архитектуры считается завершённым, если:
- `DOA-DEC-030` принят
- создана новая версия architecture_draft
- добавлены каталоги `docs/other`, `docs/rules`, `templates/other`, `templates/rules`
- naming для `OTH` и `RUL` зафиксирован
- подготовлен следующий operational_plan на выполнение изменений
