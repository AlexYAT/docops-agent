## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-029
- Status: draft
- Date: 2026-04-15
- Parent: DOA-IMP-028

---

## Summary

Зафиксирована классификация нарушений integrity baseline для шага **DOA-OP-029-T02** на основе уже зафиксированных артефактов T01. Повторный запуск validator/gate не выполнялся. По текущему контракту и решению **DOA-DEC-048** baseline остается blocked из-за unresolved canonical subset.

## Current State

- Источник истины для T02: baseline reports из T01.
- Объем findings в gate-отчете: `63` (`error=16`, `warn=45`, `info=2`).
- Dual-mode статус:
  - `gate_status=REJECT`
  - `gate_status_controlled=ACCEPT`
  - `cross_zone_violations_count=0`
- Все canonical ошибки в этом baseline находятся в `legacy` зоне; `controlled` и `boundary` blocking findings отсутствуют.

## What was completed

### Source artifacts

- `reports/doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`
- `reports/doa_document_gate_run_004_integrity_baseline_op029_t01.json`

### Classification table

| Category | Count | Zone | Resolution status | Baseline impact | Rationale |
|----------|-------|------|-------------------|-----------------|-----------|
| `status_not_in_enum` | 11 | legacy | unresolved | blocking | В `gate` это `error`; unresolved canonical нарушения удерживают `gate_status=REJECT`. |
| `unresolved_parent` | 1 | legacy | unresolved | blocking | Unresolved parent в canonical subset классифицируется как `error` в gate. |
| `unresolved_parent` | 1 | legacy | resolved_via_overlay | non-blocking | Overlay downgrade до `info`; не участвует в blocker subset. |
| `duplicate_id_registry` | 1 | legacy | unresolved | blocking | Неразрешенный duplicate ID в canonical subset дает `error`. |
| `duplicate_id_registry` | 1 | legacy | resolved_via_overlay | non-blocking | Overlay rule `mapping:duplicate_id` перевела finding в `info`. |
| `noncanonical_doc_type_key` | 1 | legacy | unresolved | blocking | Нарушение metadata key в canonical subset остается `error`. |
| `missing_parent_field` | 1 | legacy | unresolved | blocking | Отсутствие обязательного Parent для canonical документа дает `error`. |
| `invalid_replaces_format` | 1 | legacy | unresolved | blocking | Некорректный формат `Replaces` в canonical subset остается блокирующим `error`. |
| `overlay-resolved findings` | 2 | legacy | resolved_via_overlay | non-blocking | Явно помечены `resolution_status=resolved_via_overlay`; в gate имеют `info`. |
| `legacy-only findings` (`legacy_no_canonical_metadata`) | 43 | legacy | legacy-only | non-blocking | Legacy mode наблюдения (`warn`) не формируют blocker по текущему gate-контракту. |
| `root/outside-docs-model findings` (`root_markdown_outside_docs_model`) | 2 | root | legacy-only | non-blocking / informational | Корневые markdown вне docs-модели фиксируются как legacy warnings. |
| `cross-zone findings` | 0 | n/a | not-applicable | non-blocking | В dual-mode counts `cross_zone_violations_count=0`, значит cross-zone blocker отсутствует. |

### Blocking subset

Фактический blocker для baseline (subset `severity=error` + unresolved):

- Total blocking findings: **16**
- Классы:
  - `status_not_in_enum` — 11
  - `unresolved_parent` — 1
  - `duplicate_id_registry` — 1
  - `noncanonical_doc_type_key` — 1
  - `missing_parent_field` — 1
  - `invalid_replaces_format` — 1

Файлы blocker subset:

- `docs/architecture_draft/DOA-ARCH-003_TZ_final_consolidated.md` (`unresolved_parent`)
- `docs/decision_log/DOA-DEC-027_tz_import_conflict_resolution.md` (`noncanonical_doc_type_key`, `missing_parent_field`, `status_not_in_enum`)
- `docs/implementation_snapshot/DOA-IMP-018_report_generator_mvp_t01_t03.md` (`status_not_in_enum`)
- `docs/implementation_snapshot/DOA-IMP-019_report_generator_mvp_t04_t07.md` (`status_not_in_enum`)
- `docs/implementation_snapshot/DOA-IMP-020_report_generator_human_readable_layer.md` (`status_not_in_enum`)
- `docs/implementation_snapshot/DOA-IMP-021_report_generator_full_ru_static_strings.md` (`status_not_in_enum`)
- `docs/implementation_snapshot/DOA-IMP-022_full_system_snapshot.md` (`status_not_in_enum`)
- `docs/operational_plan/DOA-OP-001_v2_mvp_implementation_bootstrap.md` (`invalid_replaces_format`)
- `docs/operational_plan/DOA-OP-021_document_gate_ui_mvp_implementation.md` + `docs/operational_plan/DOA-OP-021_report_generator_mvp.md` (`duplicate_id_registry`)
- `docs/operational_plan/DOA-OP-021_report_generator_mvp.md` (`status_not_in_enum`)
- `docs/operational_plan/DOA-OP-022_document_system_hardening_cycle.md` (`status_not_in_enum`)
- `docs/operational_plan/DOA-OP-023_overlay_registry_mvp_implementation.md` (`status_not_in_enum`)
- `docs/operational_plan/DOA-OP-024_human_readable_report_generator_layer.md` (`status_not_in_enum`)
- `docs/operational_plan/DOA-OP-025_full_ru_report_static_strings.md` (`status_not_in_enum`)

Вероятные remediation-pattern классов (для подготовки T03, без исправлений в T02):

- enum/status normalization
- parent/reference consistency
- duplicate ID reconciliation
- metadata key normalization
- replaces format normalization

### Non-blocking subset

- `legacy_no_canonical_metadata`: 43 (`warn`, legacy-only).
- `root_markdown_outside_docs_model`: 2 (`warn`, root/legacy-only).
- `resolved_via_overlay`: 2 (`info`).
- Cross-zone subset: 0.

Итого non-blocking findings: **47**.

### Overlay-resolved subset

- Count: **2**
- `unresolved_parent` (`docs/idea_to_mvp/DOA-IDEA-002_docops_document_gate.md`) via `parent_override`.
- `duplicate_id_registry` (`DOA-IMP-014` pair) via `mapping:duplicate_id`.
- Impact: non-blocking (`info`) в текущем gate run.

### Legacy-only subset

- Count: **45**
  - `legacy_no_canonical_metadata`: 43 (zone `legacy`)
  - `root_markdown_outside_docs_model`: 2 (zone `root`)
- Impact: non-blocking в текущем dual-mode gate-контракте для baseline T01.

### Candidate remediation buckets for T03

- **Bucket A — enum normalization cases**
  - Основной массив: `status_not_in_enum`.
- **Bucket B — parent/reference consistency cases**
  - `unresolved_parent` + `missing_parent_field`.
- **Bucket C — duplicate ID resolution cases**
  - `duplicate_id_registry` unresolved subset.
- **Bucket D — metadata key normalization cases**
  - `noncanonical_doc_type_key`.
- **Bucket E — replaces format normalization cases**
  - `invalid_replaces_format`.
- **Bucket F — legacy-only handling continuity**
  - `legacy_no_canonical_metadata` и root/outside-docs-model как отдельный non-blocking поток без влияния на blocker subset.

### Conclusion

- Классификация T02 завершена на основе baseline artifacts T01 без повторного run и без remediation.
- Подтвержден blocker subset: **16 unresolved canonical errors**.
- Baseline status остается **blocked** (соответствует **DOA-DEC-048**).
- Материал для следующего шага **DOA-OP-029-T03** подготовлен в виде remediation buckets и mapping категорий.

## Related tasks

- **DOA-OP-029-T02** — classification of violations.

## Related commits

- N/A (этот snapshot фиксирует аналитический результат шага T02; исправления не выполнялись).

## Known issues

- Baseline blocker остается активным до обработки unresolved canonical subset.
- Возможные remediation-паттерны определены только как классификационные кандидаты; решений и изменений в рамках T02 нет.

## Next step

- Перейти к **DOA-OP-029-T03** для формализации fix strategy under create-only на основе buckets из этого snapshot.
