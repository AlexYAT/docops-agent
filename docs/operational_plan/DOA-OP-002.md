## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-002
- Status: draft
- Date: 2026-04-08
- Parent: DOA-MT-001

---

## Goal

Закрыть середина-план `DOA-MT-001`: проверить шаблоны на практике, зафиксировать примеры, подготовить почву для аудита.

## Scope

Только **новые** артефакты в `docs/` и согласованность с `templates/`; **без** изменения исторических файлов и **без** правок legacy-путей в этом цикле.

## Tasks

### Task 1

- **Task ID**: DOA-OP-002-T01
- **Description**: Создать примерные документы по всем doc_types из шаблонов; заполнить осмысленным контентом (тема: DocOps Agent MVP bootstrap)
- **Done when**: 8 новых файлов в ожидаемых путях, metadata и Parent по схеме T03
- **Dependencies**: `DOA-MT-001` принят к исполнению (draft достаточен для bootstrap)

### Task 2

- **Task ID**: DOA-OP-002-T02
- **Description**: Проверить соответствие примеров naming (`DOA-<TYPE>-<NNN>`) и полей Metadata
- **Done when**: внутренняя ревизия без противоречий Doc type vs каталог vs ID

### Task 3

- **Task ID**: DOA-OP-002-T03
- **Description**: Подготовить и выполнить аудит документов (audit_check) по чеклисту: metadata, parent links, структура
- **Done when**: создан `DOA-AUD-001` с результатом и явными рекомендациями по legacy

### Task 4

- **Task ID**: DOA-OP-002-T04
- **Description**: Зафиксировать implementation snapshot состояния после примеров и аудита
- **Done when**: создан `DOA-IMP-009`, перечислены выполненные задачи и следующий шаг (учёт результата audit)

## Dependencies

- Наличие шаблонов T02 во всех `templates/<doc_type>/`
- Родительский midterm `DOA-MT-001`

## Definition of Done

Все четыре задачи имеют явный критерий «Done when» и подтверждены наличием соответствующих артефактов (`DOA-IMP-009`, `DOA-AUD-001`, набор примеров).

## Notes

Legacy-нарушения (например misplaced OP в snapshot) **только документируются** в audit, не исправляются ретроспективно в этом шаге.
