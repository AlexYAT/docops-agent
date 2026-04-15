## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-033
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-032

---

## Summary

Выполнен T07 activation step: в gate включена category-scoped closure interpretation только для M1 категорий (`noncanonical_doc_type_key`, `invalid_replaces_format`) при marker `candidate_successor`. Core validator checks не менялись.

## Current State

- Activation включена только для двух категорий M1.
- Категории `unresolved_parent`, `duplicate_id_registry`, `status_not_in_enum` не активировались.
- Controlled-zone protection сохранена (`gate_status_controlled` не деградировал).

## What was completed

### Activated scope

- Script update:
  - `scripts/doa_document_gate.py`
- Feature flag:
  - `closure_semantics_enabled = True`
- Activation condition (all required):
  - category in `{noncanonical_doc_type_key, invalid_replaces_format}`
  - `resolution_status == candidate_successor`
  - `resolution_source == successor`
  - `trace_reference` present
  - `closure_contract_version == closure/1`
- Activation effect:
  - gate severity downgraded to `info`
  - `resolution_status -> resolved_via_successor_activation`
  - `resolution_source` and `trace_reference` preserved

### Not activated

- No activation for:
  - `unresolved_parent`
  - `duplicate_id_registry`
  - `status_not_in_enum`
- No changes to overlay registry.
- No changes to validator core checks/classification rules.

### Evidence rerun commands

- Validator:
  - `python scripts/doa_link_id_validator.py | Set-Content -Encoding utf8 reports/doa_link_id_validator_run_005_t07_closure_activation_m1.json`
- Gate:
  - `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_006_t07_closure_activation_m1.json --dry-run`

### Reports

- `reports/doa_link_id_validator_run_005_t07_closure_activation_m1.json`
- `reports/doa_document_gate_run_006_t07_closure_activation_m1.json`

## Baseline / M1 / T07 comparison

### Validator (canonical unresolved)

| Run | canonical_unresolved_violations | canonical_violations | Note |
|-----|---------------------------------|----------------------|------|
| Baseline T01 (`run_003`) | 16 | 18 | pre-activation baseline |
| M1 (`run_004`) | 16 | 18 | successor artifacts added, no closure effect |
| T07 (`run_005`) | 16 | 18 | validator counts unchanged by design |

### Gate status

| Run | gate_status | gate_status_controlled | error | warn | info |
|-----|-------------|------------------------|-------|------|------|
| Baseline T01 (`run_004`) | REJECT | ACCEPT | 16 | 45 | 2 |
| M1 (`run_005`) | REJECT | ACCEPT | 16 | 45 | 2 |
| T07 (`run_006`) | REJECT | ACCEPT | 14 | 45 | 4 |

### Targeted M1 findings

- `noncanonical_doc_type_key`
  - Baseline/M1: `severity=error`, `resolution_status=unresolved`
  - T07: `severity=info`, `resolution_status=resolved_via_successor_activation`, `trace_reference=DOA-DEC-050`
- `invalid_replaces_format`
  - Baseline/M1: `severity=error`, `resolution_status=unresolved`
  - T07: `severity=info`, `resolution_status=resolved_via_successor_activation`, `trace_reference=DOA-OP-030`

## Related tasks

- T07 closure activation (M1 category scope only).

## Related commits

- N/A in this snapshot (commit is created after document and report artifacts are staged).

## Known issues

- Global blocker subset не закрылся полностью: `gate_status` остается `REJECT`.
- Это ожидаемо, так как activation не применялась к `status_not_in_enum`, `unresolved_parent`, `duplicate_id_registry`.

## Next step

- Продолжать alignment-driven remediation только по согласованным категориям следующего micro-cycle, не расширяя activation scope без отдельного решения.
