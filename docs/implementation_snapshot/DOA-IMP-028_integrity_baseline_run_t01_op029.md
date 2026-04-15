## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-028
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-027

---

## Summary

Выполнен baseline run для шага **DOA-OP-029-T01**: запущены validator и gate на текущем canonical состоянии без правок документов/кода. По факту прогона baseline остается заблокированным согласно решению **DOA-DEC-048**.

## Current State

- Шаг **DOA-OP-029-T01** выполнен как отдельный run-only этап.
- Архитектурные и кодовые изменения не выполнялись.
- Исправления нарушений, cleanup и переход к следующим шагам плана не выполнялись.

## What was completed

### Canonical commands used

- Validator:
  - `python scripts/doa_link_id_validator.py | Set-Content -Encoding utf8 reports/doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`
- Gate:
  - `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_004_integrity_baseline_op029_t01.json --dry-run`

### Reports obtained

- `reports/doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`
- `reports/doa_document_gate_run_004_integrity_baseline_op029_t01.json`

### Key statuses and counts

#### Validator summary (`doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`)

- `validator.version`: `0.2.0`
- `scope.files_scanned`: `140`
- `counts.canonical_violations`: `18`
- `counts.legacy_findings`: `45`
- `counts.canonical_resolved_via_overlay`: `2`
- `counts.canonical_unresolved_violations`: `16`
- `counts.cross_zone_violations`: `0`
- `dual_mode.docs_path_zone_counts`: `legacy=128`, `controlled=9`, `boundary=1`

#### Gate summary (`doa_document_gate_run_004_integrity_baseline_op029_t01.json`)

- `gate_status`: **REJECT**
- `gate_status_controlled`: **ACCEPT**
- `counts.total`: `63`
- `counts.error`: `16`
- `counts.warn`: `45`
- `counts.info`: `2`
- `dual_mode_counts.legacy_findings_count`: `61`
- `dual_mode_counts.controlled_findings_count`: `0`
- `dual_mode_counts.cross_zone_violations_count`: `0`
- `dual_mode_counts.other_zone_findings_count`: `2`

### Main violation classes (overview)

- Canonical:
  - `status_not_in_enum` (11)
  - `unresolved_parent` (2)
  - `duplicate_id_registry` (2)
  - `noncanonical_doc_type_key` (1)
  - `missing_parent_field` (1)
  - `invalid_replaces_format` (1)
- Legacy:
  - `legacy_no_canonical_metadata` (43)
  - `root_markdown_outside_docs_model` (2)
- Cross-zone:
  - `cross_zone_violations` = 0 (в validator и gate dual-mode counts)

## Related tasks

- **DOA-OP-029-T01** — baseline run validator/gate.

## Related commits

- N/A (данный snapshot фиксирует результат прогона; remediation-коммиты в рамках T01 отсутствуют).

## Known issues

- baseline блокируется по canonical unresolved нарушениям (`16`), что приводит к `gate_status=REJECT`.
- controlled-зона в этом прогоне остается в `ACCEPT`, но это не снимает общий baseline blocker.

## Next step

- Перейти к **DOA-OP-029-T02** (classification of violations) без изменения фактов, зафиксированных в этом baseline run.
