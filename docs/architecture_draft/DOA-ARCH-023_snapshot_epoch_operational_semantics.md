## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-023
- Status: draft
- Date: 2026-04-15
- Parent: DOA-ARCH-022

---

## Summary

Документ формализует snapshot-driven epoch operational semantics: validator truth остается полной, historical/global verdict сохраняется как audit-layer, а primary operational verdict для активной фазы после boundary определяется controlled zone.

## Goal

Formalize snapshot-driven epoch operational semantics для gate/report интерпретации после fixed snapshot boundary.

## Scope

- В scope: семантика слоев truth/verdict, boundary semantics, brownfield onboarding, ограничения для controlled safety.
- Вне scope: кодовые изменения validator/gate, overlay rule editing, remediation execution.

## Roles & Scenarios

- **Validator layer**: формирует полный truth по всему корпусу.
- **Gate layer**: разделяет primary controlled verdict и secondary historical/global verdict.
- **Operator**: принимает operational решение по active epoch через controlled verdict.

Сценарий brownfield onboarding:

1. Проект входит в DocOps в не-clean состоянии.
2. Fixed snapshot фиксирует hard epoch boundary.
3. Controlled work стартует после boundary.
4. Legacy остается видимым, но не блокирует active controlled phase.

## Document Model

### Core model (three-layer semantics)

1. **Validator truth layer**  
   Полный scan всего корпуса и полная фиксация findings.

2. **Historical/global audit layer**  
   Сводный исторический verdict для аудита и долгосрочного долга.

3. **Active controlled epoch verdict**  
   Primary operational verdict для текущей фазы после snapshot.

### Required semantics

- Validator сканирует full corpus.
- Historical/global report может включать legacy findings без потери видимости.
- Operational readiness текущей эпохи определяется controlled zone.
- Fixed snapshot является единственным санкционированным мостом в legacy context.
- Legacy findings остаются видимыми, но не блокируют current controlled phase.

### Gate semantics

- `gate_status_controlled` — **primary operational verdict** для active epoch.
- `gate_status` (или эквивалент global/historical status) — **secondary historical/audit verdict**.
- Терминология текущей системы сохраняется; меняется приоритет интерпретации, а не naming contract.

### Boundary semantics

- **Pre-snapshot**: legacy zone.
- **Snapshot artifact**: epoch boundary.
- **Post-snapshot**: controlled zone.

## Metadata Model

Для epoch semantics отчеты должны сохранять machine-readable слой traceability:

- zone attribution,
- resolution markers,
- closure contract versioning,
- dual-verdict representation (controlled primary, global secondary).

## Naming Convention

- Existing gate fields сохраняются для backward compatibility.
- Primary/secondary semantics фиксируются policy/architecture-документами без ломки report contract.

## System Rules

1. Overlay не является source of truth.
2. Controlled zone остается strict blocker space для active epoch.
3. Прямые controlled -> legacy reference запрещены, кроме sanctioned bridge через snapshot semantics.
4. Legacy remediation optional и policy-driven, отдельно от controlled readiness.
5. Future fixed snapshots могут открывать новые epochs; этот документ фиксирует semantics для текущей модели.

## Workflow

1. Зафиксировать decision baseline (snapshot-driven semantics).
2. Выравнять architecture + operational wording.
3. Отделить primary controlled verdict от historical/global verdict в governance.
4. Выполнять remediation/activation только если они поддерживают controlled readiness, а не cleanup ради cleanup.

## Constraints

- Без изменения validator/gate code в рамках этого документа.
- Без rerun/remediation в рамках этого документа.
- Без пересмотра overlay registry в рамках этого документа.

## Definition of Done

- Epoch semantics явно определены.
- Primary post-snapshot verdict явно закреплен за controlled zone.
- Роль legacy сведена к non-blocking historical/audit layer для active epoch.
- Brownfield onboarding сценарий явно поддержан.
