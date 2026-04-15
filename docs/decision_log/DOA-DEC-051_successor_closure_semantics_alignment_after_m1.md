## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-051
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-031

---

## Title

Successor closure semantics not sufficient for baseline remediation evidence

## Context

- В **DOA-DEC-049** принята hybrid model (successor-first + overlay-constrained).
- В M1 (BKT-D + BKT-E) выпущены successor-документы:
  - `DOA-DEC-050` (metadata key normalization path),
  - `DOA-OP-030` (replaces normalization path).
- По evidence rerun в **DOA-IMP-031** blocker subset не уменьшился:
  - `noncanonical_doc_type_key` остался unresolved в `DOA-DEC-027`,
  - `invalid_replaces_format` остался unresolved в `DOA-OP-001_v2...`.
- Следовательно, текущая интерпретация validator/gate не считает один только successor-path достаточным closure-механизмом для legacy source findings.

## Problem

Возник operational gap между:

- document-level remediation model (create-only successor release),
- engine/policy interpretation model (что именно считается resolved в evidence run).

Из-за этого remediation создает новые корректные документы, но baseline blocker не получает измеримого снижения.

## Options considered

1. **Продолжать remediation дальше без дополнительных решений**  
   Риск: наращивание successor-артефактов без operational effect на blocker subset.

2. **Формально признать, что successor-only path не работает как evidence closure в текущем контракте**  
   Плюс: честно фиксирует наблюдаемый факт M1.

3. **Добавить policy/overlay-backed closure semantics для разрешенных классов**  
   Плюс: позволяет фиксировать closure по правилам, не переписывая legacy.
   Риск: при слабых ограничениях overlay может стать скрытым SoT.

4. **Пересмотреть validator/gate contract отдельно до следующих micro-cycles**  
   Плюс: убирает двусмысленность интерпретации findings.
   Минус: требует отдельного alignment цикла перед M2.

## Chosen solution

Принят комбинированный путь **2 + 3 + 4**:

- Формально признать: **successor сам по себе не является достаточным evidence closure** в текущем validator/gate контракте.
- Ввести alignment-first шаг: отдельный policy/interpretation цикл до продолжения M2.
- Разрешить overlay-backed closure только как **явно ограниченный интерпретационный механизм** для конкретных категорий, без превращения overlay в SoT.

## Rules

### 1) Successor sufficiency

- Successor-документ остается обязательным remediation artifact для create-only дисциплины.
- Но successor **не считается автоматически resolved** для legacy finding, пока policy/engine не имеет явного closure-rule.

### 2) Categories where successor-only is insufficient (current evidence)

- `noncanonical_doc_type_key`
- `invalid_replaces_format`

Эти категории показали в M1 отсутствие operational closure despite successor creation.

### 3) Overlay-backed closure admissibility by category

- `metadata normalization` (`noncanonical_doc_type_key`): **допустимо условно** через новую rule family.
- `replaces normalization` (`invalid_replaces_format`): **допустимо условно** через новую rule family.
- `parent remediation` (`unresolved_parent`, `missing_parent_field`): **допустимо условно**, только при жесткой трассируемости к successor-lineage.
- `duplicate ID remediation` (`duplicate_id_registry`): **допустимо условно** для явно перечисленных пар/кластеров.
- `status normalization` (`status_not_in_enum`): **допустимо условно**, но с наибольшими ограничениями из-за масштаба и риска policy-drift.

Общее правило: ни одна overlay-backed closure rule не может вводиться неявно; каждая family должна быть документно и policy-версией зафиксирована.

### 4) Policy/contract requirement

- До M2 требуется отдельный alignment step, который фиксирует:
  - новый policy contract для closure semantics,
  - допустимые overlay rule families и границы применения,
  - mapping: category -> closure interpretation -> gate severity outcome.

### 5) M2 gate condition

- **M2 нельзя запускать прямо сейчас.**
- Допуск к M2 только после завершения alignment-first шага и фиксации его артефактом(ами) в docs.

## Validator/Gate interpretation decision

- Unresolved legacy canonical findings остаются `error` до появления утвержденного closure mapping.
- Для категорий, включенных в новую closure-policy, findings могут понижаться до non-blocking только при:
  - наличии подходящего successor lineage,
  - наличии соответствующего policy/overlay closure rule,
  - прозрачных `resolution_status` и trace markers в report.
- Controlled-zone protection (`gate_status_controlled`) не ослабляется этим решением.

## Why

- Решение устраняет «бессмысленное наращивание successor-документов без эффекта» как наблюденный риск после M1.
- Сохраняет create-only и не требует редактирования historical/accepted документов.
- Предотвращает превращение overlay в скрытый SoT через explicit policy families и versioned contract.

## Trade-offs

- Добавляется отдельный управленческий шаг перед M2, что увеличивает время до следующей remediation-фазы.
- Governance становится сложнее: нужен явный control над closure families.
- Но это снижает риск повторения M1-style no-effect cycles.

## Implication

- **Идти в M2 прямо сейчас нельзя.**
- Сначала нужен отдельный alignment-first operational/document cycle на policy/validator interpretation semantics.
- После его завершения M2 запускается как следующий micro-cycle с обязательным evidence rerun.

## Follow-ups

- Открыть отдельный operational/document cycle: closure semantics alignment (policy + interpretation).
- В этом цикле зафиксировать:
  - category-scoped closure families,
  - acceptance criteria для evidence closure,
  - expected delta rules для blocker subset.
- Только после этого продолжить micro-cycle sequence из `DOA-IMP-030`.
