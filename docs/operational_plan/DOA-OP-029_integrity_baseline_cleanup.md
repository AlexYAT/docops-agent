## Metadata

- Project: DOA
- Doc type: operational_plan
- ID: DOA-OP-029
- Status: draft
- Date: 2026-04-15
- Parent: DOA-DEC-048

---

## Goal

Закрыть ID/Link integrity baseline до зеленого состояния и снять единственный блокер для перехода к следующему слою реализации.

## Scope

- Входит: цикл baseline run -> классификация -> remediation strategy -> повторные прогоны validator/gate -> фиксация PASS.
- Не входит: запуск реализации следующего слоя, архитектурные изменения, legacy remediation вне согласованной зоны.
- Режим выполнения: строго create-only.

## Tasks

### Task 1

- **Task ID**: DOA-OP-029-T01
- **Description**: baseline run validator/gate на текущем canonical состоянии.
- **Done when**: сохранены валидные артефакты baseline-прогона и зафиксирован список нарушений.

### Task 2

- **Task ID**: DOA-OP-029-T02
- **Description**: классификация нарушений integrity baseline по типам (ID, Parent, Replaces, links, placement).
- **Done when**: для каждого нарушения задан класс и подтвержден статус (blocking/non-blocking) по действующему контракту.
- **Dependencies**: DOA-OP-029-T01

### Task 3

- **Task ID**: DOA-OP-029-T03
- **Description**: определить fix strategy under create-only для каждого класса нарушений.
- **Done when**: утвержден способ устранения без ретро-правок accepted документов и без скрытых изменений.
- **Dependencies**: DOA-OP-029-T02

### Task 4

- **Task ID**: DOA-OP-029-T04
- **Description**: выполнить rerun validator после реализации fix strategy.
- **Done when**: validator показывает зеленый baseline или эквивалентный PASS по текущему контракту.
- **Dependencies**: DOA-OP-029-T03

### Task 5

- **Task ID**: DOA-OP-029-T05
- **Description**: выполнить rerun gate и подтвердить controlled zone remains ACCEPT.
- **Done when**: gate не фиксирует блокирующих integrity-нарушений в canonical зоне.
- **Dependencies**: DOA-OP-029-T04

### Task 6

- **Task ID**: DOA-OP-029-T06
- **Description**: выпустить implementation_snapshot с подтвержденным PASS baseline.
- **Done when**: создан новый DOA-IMP-* с фиксацией результатов T01-T05 и явным статусом GO/NO-GO.
- **Dependencies**: DOA-OP-029-T05

## Dependencies

- DOA-DEC-048 (No-Go decision до PASS baseline).
- Актуальный dual-mode validator/gate контракт из текущей архитектурной линии.

## Definition of Done

- canonical violations = 0 или эквивалентный зеленый baseline по действующему контракту.
- controlled zone remains ACCEPT после повторного gate run.
- Parent/Replaces/ID integrity подтверждены повторным прогоном validator/gate.
- Выпущен новый implementation_snapshot с формальной фиксацией PASS baseline.

## Notes

- Legacy-зону не трогать без отдельного решения.
- Архитектурные изменения в рамках данного плана не выполнять.
- Любые действия вне create-only считаются вне scope этого operational_plan.
