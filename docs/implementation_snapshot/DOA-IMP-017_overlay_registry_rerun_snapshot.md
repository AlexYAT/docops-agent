# implementation_snapshot — DOA-IMP-017

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-017
- Status: draft
- Date: 2026-04-10
- Parent: DOA-OP-023

---

## Summary

Выполнен rerun `validator + gate` после внедрения overlay MVP (T01–T05). Зафиксировано частичное улучшение:
часть canonical blockers теперь помечается как `resolved_via_overlay`, но baseline остается не-green
(`gate_status = REJECT`) из-за оставшихся unresolved canonical нарушений.

## Context

- `DOA-OP-023` задает цикл overlay registry MVP (T06–T08 на этом шаге).
- `DOA-DEC-036` фиксирует remediation strategy через overlay, без in-place правок документов.
- Внедренные изменения в коде:
  - `scripts/doa_link_id_validator.py` — загрузка `overlay_registry.json`, маркеры `resolution_status`.
  - `scripts/doa_document_gate.py` — overlay-aware обработка findings (`resolved_via_overlay -> info`).
- Исторические markdown документы не изменялись (create-only соблюден).

## What was executed

- Запуск обновленного validator:
  - `python scripts/doa_link_id_validator.py`
  - отчет: `reports/doa_link_id_validator_run_002_overlay.json`
- Запуск gate поверх обновленного validator:
  - `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_002_overlay.json`
  - отчет: `reports/doa_document_gate_run_002_overlay.json`
- Проверка, что overlay участвует в run:
  - в findings присутствуют `resolution_status`, `overlay_source`, `overlay_rule_type`;
  - есть случаи `resolved_via_overlay` для `unresolved_parent` и `duplicate_id_registry`.

## Results

### Validator (`doa_link_id_validator_run_002_overlay.json`)

- `files_scanned`: **96**
- `canonical_violations`: **9**
- `legacy_findings`: **45**
- `canonical_resolved_via_overlay`: **2**
- `canonical_unresolved_violations`: **7**
- overlay source: `docs/rules/overlay_registry.json` (loaded: true)

### Gate (`doa_document_gate_run_002_overlay.json`)

- `gate_status`: **REJECT**
- `counts.total`: **54**
- `counts.error`: **7**
- `counts.warn`: **45**
- `counts.info`: **2**
- `resolution_status = resolved_via_overlay` в findings: **2**
- `resolution_status = unresolved` в findings: **52**

## Comparison with previous baseline

Сравнение с предыдущим baseline из `DOA-IMP-015`:

- **Gate outcome:** остается `REJECT` (без изменения по итоговому статусу).
- **Severity distribution (gate):**
  - baseline: `error=7, warn=45, info=0, total=52`
  - overlay rerun: `error=7, warn=45, info=2, total=54`
  - изменение: появились **2 info** за счет `resolved_via_overlay`.
- **Overlay реально закрыл:**
  1) `unresolved_parent` для `DOA-IDEA-002 -> DOA-OP-007` (parent override -> resolved via overlay),
  2) `duplicate_id_registry` для `DOA-IMP-014` (mapping duplicate_id -> resolved via overlay).
- **Overlay пока не покрывает:**
  - остальные canonical blockers (итого **7 unresolved**), включая проблемы в `DOA-ARCH-003`,
    `DOA-DEC-027`, `DOA-OP-001`, а также новые canonical несоответствия, не описанные текущими overlay-правилами.

## Artifacts

- `docs/rules/overlay_registry.json`
- `scripts/doa_link_id_validator.py`
- `scripts/doa_document_gate.py`
- `reports/doa_link_id_validator_run_002_overlay.json`
- `reports/doa_document_gate_run_002_overlay.json`

## Observations

- Overlay слой реально участвует в pipeline и прозрачно виден в машинных отчетах.
- Подход остается create-only: remediation идет через правила overlay, а не через переписывание истории.
- Hardening частичный: часть сигналов downgraded до info, но критичный хвост unresolved сохраняется.
- Текущий baseline можно считать «post-overlay partial hardening», а не финальной стабилизацией.

## Next steps

- Расширить overlay rules точечно (без попытки закрыть все за один шаг).
- Пройти следующий rerun и проверить динамику `canonical_unresolved_violations`.
- На следующем цикле рассмотреть переход к более формальному baseline-aware режиму gate.
