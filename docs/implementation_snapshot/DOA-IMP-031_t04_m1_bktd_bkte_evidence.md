## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-031
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-030

---

## Summary

Выполнен **T04 micro-cycle M1** по линии **DOA-OP-029** (только **BKT-D + BKT-E**) в create-only модели, согласно **DOA-DEC-049**. Созданы два successor-документа и выполнен evidence rerun validator/gate. По результату rerun целевые blocker findings не уменьшились.

## Current State

- Scope M1: только `noncanonical_doc_type_key` и `invalid_replaces_format`.
- Другие bucket-классы (status/parent/duplicate/legacy-only/cross-zone) в M1 не ремедиировались.
- Controlled zone по evidence run не деградировала (`gate_status_controlled` сохранился `ACCEPT`).

## What was completed

### M1 blocker-cases (from baseline T01)

1. `noncanonical_doc_type_key`
   - file: `docs/decision_log/DOA-DEC-027_tz_import_conflict_resolution.md`
   - detail: `Uses Type: instead of Doc type:`
2. `invalid_replaces_format`
   - file: `docs/operational_plan/DOA-OP-001_v2_mvp_implementation_bootstrap.md`
   - detail: `DOA-OP-001 (draft)`

### Create-only remediation artifacts created

- `docs/decision_log/DOA-DEC-050_dec027_metadata_key_successor_for_m1.md`
  - canonical successor for BKT-D
  - lineage: `Replaces: DOA-DEC-027`
- `docs/operational_plan/DOA-OP-030_op001_replaces_normalization_successor_m1.md`
  - canonical successor for BKT-E
  - lineage: `Replaces: DOA-OP-001`

### Evidence rerun commands used

- Validator:
  - `python scripts/doa_link_id_validator.py | Set-Content -Encoding utf8 reports/doa_link_id_validator_run_004_t04_m1_bktd_bkte.json`
- Gate:
  - `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_005_t04_m1_bktd_bkte.json --dry-run`

### New reports obtained

- `reports/doa_link_id_validator_run_004_t04_m1_bktd_bkte.json`
- `reports/doa_document_gate_run_005_t04_m1_bktd_bkte.json`

### Evidence delta vs baseline T01

#### Validator counts

- Baseline T01 (`run_003`):
  - `canonical_violations=18`
  - `canonical_unresolved_violations=16`
  - `legacy_findings=45`
  - `cross_zone_violations=0`
- M1 rerun (`run_004`):
  - `canonical_violations=18`
  - `canonical_unresolved_violations=16`
  - `legacy_findings=45`
  - `cross_zone_violations=0`

#### Gate counts and statuses

- Baseline T01 (`run_004`):
  - `gate_status=REJECT`
  - `gate_status_controlled=ACCEPT`
  - `counts: total=63, error=16, warn=45, info=2`
- M1 rerun (`run_005`):
  - `gate_status=REJECT`
  - `gate_status_controlled=ACCEPT`
  - `counts: total=63, error=16, warn=45, info=2`

#### Targeted blocker-cases

- `noncanonical_doc_type_key`: baseline `1` -> rerun `1` (same legacy source file `DOA-DEC-027`)
- `invalid_replaces_format`: baseline `1` -> rerun `1` (same legacy source file `DOA-OP-001_v2...`)

## Related tasks

- `DOA-OP-029` — integrity baseline cleanup plan.
- T04 micro-cycle M1 = `BKT-D + BKT-E` (по `DOA-IMP-030` и `DOA-DEC-049`).

## Related commits

- N/A в рамках этого snapshot (коммит с артефактами M1 выполняется после фиксации данного документа).

## Known issues

- Expected снижение blocker subset минимум на 2 findings в M1 evidence run **не подтверждено**.
- Целевые findings остались unresolved в тех же legacy source files.
- Это указывает, что в текущей реализации validator/gate successor-артефакты M1 сами по себе не интерпретируются как closure для этих двух legacy findings.

## Next step

- Не выполнять дополнительные исправления в этом же micro-cycle.
- Зафиксировать M1 как completed-with-no-reduction и перейти к следующему управленческому шагу по `DOA-OP-029`:
  - уточнение интерпретации closure semantics для successor-path в отдельном документированном цикле,
  - затем запуск следующего micro-cycle с отдельным evidence rerun.
