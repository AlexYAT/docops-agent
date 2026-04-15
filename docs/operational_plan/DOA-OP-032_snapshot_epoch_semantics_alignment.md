## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-032
- Status: draft
- Date: 2026-04-15
- Parent: DOA-OP-031

---

## Goal

Align docs, gate semantics, and rollout governance to snapshot-driven epoch model where controlled verdict is primary and legacy serves as secondary historical/audit layer.

## Scope

- Входит: документное и governance alignment semantics.
- Не входит: кодовые изменения validator/gate, remediation expansion, M2 execution.

## Tasks

### Task 1

- **Task ID**: DOA-OP-032-T01
- **Description**: Confirm decision baseline for snapshot-driven epoch semantics.
- **Done when**: decision line по snapshot-driven модели зафиксирована и принята как управляющая для дальнейших шагов.

### Task 2

- **Task ID**: DOA-OP-032-T02
- **Description**: Align architecture wording with current gate/report model.
- **Done when**: architecture явно различает primary controlled verdict и secondary historical/global verdict.
- **Dependencies**: DOA-OP-032-T01

### Task 3

- **Task ID**: DOA-OP-032-T03
- **Description**: Define report presentation semantics (primary controlled verdict + secondary historical/global verdict).
- **Done when**: presentation contract определен без ломки backward compatibility naming.
- **Dependencies**: DOA-OP-032-T02

### Task 4

- **Task ID**: DOA-OP-032-T04
- **Description**: Define implementation scope for minimal gate/report alignment.
- **Done when**: scope ограничен минимальными изменениями semantics layer без расширения legacy remediation.
- **Dependencies**: DOA-OP-032-T03

### Task 5

- **Task ID**: DOA-OP-032-T05
- **Description**: Define readiness checkpoint before any further activation/remediation expansion.
- **Done when**: формально зафиксирован checkpoint, что M2 остается paused до завершения semantics alignment.
- **Dependencies**: DOA-OP-032-T04

## Dependencies

- DOA-OP-029 (integrity baseline program context).
- DOA-OP-031 (closure alignment baseline).
- Snapshot-driven decision/architecture line текущего цикла.

## Definition of Done

- Decision + architecture + operational line established and cross-linked.
- Для controlled work не требуется дальнейшее расширение legacy remediation как обязательное условие proceed.
- Следующий implementation step сужен до minimal semantics alignment.
- M2 остается paused, пока epoch semantics не зафиксированы и не приняты в governance.

## Notes

- Текущая closure activation работа не отбрасывается; она сохраняется как existing evidence layer.
- Приоритет сдвигается от mandatory legacy fixing к управлению active controlled epoch.
- Любое расширение remediation scope должно проходить через отдельный управляемый цикл после readiness checkpoint.
