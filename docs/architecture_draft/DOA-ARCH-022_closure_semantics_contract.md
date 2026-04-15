## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-022
- Status: draft
- Date: 2026-04-15
- Parent: DOA-DEC-051

---

## Summary

Этот контракт фиксирует closure semantics для evidence-интерпретации validator/gate после вывода из M1: successor-path сам по себе не закрывает legacy findings без явной policy/engine поддержки.

## Goal

Определить, что считается `resolved` на уровне evidence run и как это отражается в gate-решении без нарушения create-only дисциплины и без превращения overlay в скрытый SoT.

## Scope

- В scope: interpretation contract для closure semantics (`successor`, `overlay`, `hybrid`, `none`), category mapping, report fields, gate effect.
- Вне scope: изменение validator/gate кода, изменение overlay registry, remediation execution.

## Roles & Scenarios

- **DocOps operator**: публикует remediation artifacts (successor) и запускает evidence run.
- **Policy owner**: утверждает category-to-closure mapping и version rules.
- **Gate consumer**: принимает решение по `gate_status`/`gate_status_controlled` по контракту интерпретации.

Сценарий:
1. Выпущен successor или policy-backed overlay rule.
2. Validator/gate маркирует finding по closure type.
3. Gate применяет category-specific effect на severity/status.

## Document Model

### Purpose

Определить формальную границу между remediation artifact и closure semantics:

- remediation artifact = факт появления нового артефакта (successor/overlay rule),
- closure semantics = policy-правило, по которому finding получает статус resolved/non-blocking.

### Core concept

`artifact_created != finding_resolved`  
Finding считается resolved только если выполнены category-specific условия контракта и они подтверждены в report.

### Closure types

- **successor-only**: closure только по successor lineage без overlay.
- **overlay-backed**: closure по policy/overlay rule с trace markers.
- **hybrid**: successor + overlay одновременно.
- **none**: unresolved (closure не достигнут).

`successor-only` в текущем контракте разрешается только там, где это явно отмечено в category mapping.

### Category mapping

| Category | Closure type | Allowed | Requires overlay | Gate effect |
|----------|--------------|---------|------------------|-------------|
| `noncanonical_doc_type_key` | hybrid | yes | yes | `error -> info` при valid successor lineage + valid overlay closure rule; иначе `error` |
| `invalid_replaces_format` | hybrid | yes | yes | `error -> info` при valid successor lineage + valid overlay closure rule; иначе `error` |
| `unresolved_parent` | hybrid | yes | yes | `error -> warn/info` только при explicit parent closure rule; иначе `error` |
| `duplicate_id_registry` | hybrid | yes | yes | `error -> info` только для явно перечисленных ID clusters; иначе `error` |
| `status_not_in_enum` | overlay-backed | conditional | yes | `error -> warn/info` только при versioned status-closure family; иначе `error` |

### Resolution conditions

Для finding `resolved` необходимо:

1. **Traceability**
   - присутствует `resolution_source` (`successor`, `overlay`, `hybrid`);
   - присутствует `trace_reference` (ID/path/rule reference).
2. **Category conditions**
   - `noncanonical_doc_type_key`: successor с canonical `Doc type` + overlay closure rule.
   - `invalid_replaces_format`: successor с valid `Replaces` format + overlay closure rule.
   - `unresolved_parent`: successor lineage + explicit parent closure mapping.
   - `duplicate_id_registry`: successor/ID split + explicit duplicate cluster mapping.
   - `status_not_in_enum`: status-normalization family rule (overlay-backed) + trace to target artifacts.
3. **Report confirmation**
   - finding в report имеет `resolution_status=resolved_via_overlay` или `resolved_via_hybrid` (когда будет введено),
   - severity соответствует gate effect для категории.

Если хотя бы одно условие не выполнено, closure type = `none` и finding остается unresolved.

## Metadata Model

Для closure semantics требуется фиксированный набор report metadata:

- `resolution_status`
- `resolution_source` (`successor` / `overlay` / `hybrid` / `none`)
- `trace_reference` (artifact ID или overlay rule key)
- `closure_contract_version`

## Naming Convention

- Closure policy families versioned: `closure/<category>/<version>`.
- Rule keys в overlay/policy должны быть machine-readable и стабильны между reruns.
- Implicit closure (без explicit rule key и trace reference) запрещен.

## System Rules

1. Overlay не является source-of-truth для документа; он только интерпретационный слой closure.
2. Closure rules должны быть versioned и документно зафиксированы до применения в evidence.
3. Successor creation без policy alignment не дает автоматического closure effect.
4. Controlled-zone safety (`gate_status_controlled`) не может ослабляться closure-правилами для legacy remediation.
5. Category mapping действует только на явно перечисленные категории.

## Workflow

1. Зафиксировать closure contract/version.
2. Для категории определить allowed closure type.
3. Выпустить remediation artifacts (create-only).
4. Применить policy/overlay closure rules (без скрытых изменений).
5. Выполнить evidence run и проверить report requirements.
6. Зафиксировать результат в implementation_snapshot.

## Constraints

- Без изменений validator/gate кода в рамках этого архитектурного шага.
- Без изменений overlay registry в рамках этого архитектурного шага.
- Без remediation и rerun в рамках этого архитектурного шага.

## Definition of Done

- Формально определен closure semantics contract.
- Есть category mapping для минимум 5 критичных категорий.
- Явно определено, где successor-only недостаточен.
- Определены report requirements для machine-verifiable closure.
- Зафиксирован запрет на implicit closure и не-versioned rules.
