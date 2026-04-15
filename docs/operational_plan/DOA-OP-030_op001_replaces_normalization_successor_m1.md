## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-030
- Status: draft
- Date: 2026-04-15
- Parent: DOA-OP-029
- Replaces: DOA-OP-001

---

## Goal

Выпустить create-only successor для нормализации `Replaces` lineage по M1/BKT-E без in-place правок `DOA-OP-001_v2_mvp_implementation_bootstrap.md`.

## Scope

- Входит: фиксация канонического successor-артефакта с валидным `Replaces`.
- Не входит: изменение исходного `DOA-OP-001`, изменение validator/gate, remediation других bucket-классов.

## Tasks

### Task 1

- **Task ID**: DOA-OP-030-T01
- **Description**: Зафиксировать successor-модель для `DOA-OP-001` в формате create-only.
- **Done when**: создан `DOA-OP-030` с валидным metadata и `Replaces: DOA-OP-001`.

### Task 2

- **Task ID**: DOA-OP-030-T02
- **Description**: Передать артефакт в evidence-run M1 вместе с `DOA-DEC-050`.
- **Done when**: M1 rerun validator/gate выполнен и зафиксирован в implementation snapshot.
- **Dependencies**: DOA-OP-030-T01

## Dependencies

- DOA-OP-029 (integrity baseline cleanup pipeline).
- DOA-DEC-049 (create-only remediation model).

## Definition of Done

- Создан новый operational_plan successor (`DOA-OP-030`) с корректным `Replaces` форматом.
- Lineage между `DOA-OP-030` и `DOA-OP-001` machine-traceable.
- Исходный legacy документ не изменен.

## Notes

- Этот документ является M1 remediation artifact только для BKT-E.
- Дополнительные bucket-классы в рамках `DOA-OP-030` не обрабатываются.
