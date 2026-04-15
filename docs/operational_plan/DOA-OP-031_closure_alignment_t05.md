## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-031
- Status: draft
- Date: 2026-04-15
- Parent: DOA-OP-029

---

## Goal

Запустить alignment-first цикл T05 и формализовать closure semantics contract для интерпретации validator/gate findings перед продолжением remediation micro-cycles.

## Scope

- Входит: документная формализация closure contract, category mapping, gate interpretation, readiness criteria для M2.
- Не входит: изменение validator/gate кода, изменение overlay registry, выполнение remediation, rerun evidence.

## Tasks

### Task 1

- **Task ID**: DOA-OP-031-T05-01
- **Description**: Define closure contract (artifact vs interpretation semantics).
- **Done when**: создан архитектурный документ с явными closure types и resolution conditions.

### Task 2

- **Task ID**: DOA-OP-031-T05-02
- **Description**: Define category mapping for blocker categories.
- **Done when**: есть таблица `category -> closure type -> gate effect` минимум для 5 критичных категорий.
- **Dependencies**: DOA-OP-031-T05-01

### Task 3

- **Task ID**: DOA-OP-031-T05-03
- **Description**: Define gate interpretation rules and severity transitions.
- **Done when**: явно зафиксировано, когда `error` остается `error`, когда допустим downgrade.
- **Dependencies**: DOA-OP-031-T05-02

### Task 4

- **Task ID**: DOA-OP-031-T05-04
- **Description**: Prepare validator/gate alignment package (policy-level only, no code).
- **Done when**: описаны report requirements и versioning rules для closure interpretation.
- **Dependencies**: DOA-OP-031-T05-03

### Task 5

- **Task ID**: DOA-OP-031-T05-05
- **Description**: Confirm readiness gate for M2 start.
- **Done when**: явно зафиксировано, что M2 допускается только после alignment artifacts acceptance.
- **Dependencies**: DOA-OP-031-T05-04

## Dependencies

- `DOA-OP-029` (integrity baseline cleanup).
- `DOA-DEC-049` (create-only remediation model).
- `DOA-DEC-051` (successor closure gap decision).

## Definition of Done

- Contract формализован в отдельном архитектурном документе.
- Критичные категории покрыты mapping table.
- Явно определено, где successor-only разрешен/запрещен.
- Определены report fields для closure traceability.
- Сформирован readiness criterion для перехода к M2.

## Notes

- T05 является alignment-first циклом и не включает remediation.
- Любая попытка продолжить M2 до закрытия T05 считается нарушением текущего governance решения.
