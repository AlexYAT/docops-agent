# DOA-IMP-035 — Snapshot validator/gate MVP support

## Metadata

- Project: docops-agent
- Doc type: implementation_snapshot
- ID: DOA-IMP-035
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-OP-035

---

## Summary

Зафиксирована MVP-поддержка fixed snapshot артефактов в validator/gate layer.

Цель изменения:
сделать snapshot не только описанным архитектурно, но и минимально поддержанным в машинной проверке.

---

## Scope of Implementation

Выполнено:

- добавлено базовое распознавание snapshot artifact class
- добавлена минимальная проверка snapshot metadata
- подготовлена базовая severity semantics для snapshot findings
- сохранена совместимость с текущей snapshot-boundary моделью

Не выполнялось:

- полная автоматизация lifecycle
- расширенная snapshot diagnostics
- UI/visualization changes

---

## Changed Files

- scripts/doa_link_id_validator.py
- scripts/doa_document_gate.py
- reports/doa_link_id_validator_run_006_snapshot_mvp.json
- reports/doa_document_gate_run_007_snapshot_mvp.json

---

## Implemented Behavior

Система теперь умеет:

- распознавать `fixed_snapshot`
- распознавать `DOA-FSN-XXX`
- учитывать snapshot findings в validator/gate semantics
- не смешивать snapshot class с обычными canonical document errors

---

## Validation

Выполненные команды:

- `python scripts/doa_link_id_validator.py | Set-Content -Encoding utf8 reports/doa_link_id_validator_run_006_snapshot_mvp.json`
- `python scripts/doa_document_gate.py --root . --out reports/doa_document_gate_run_007_snapshot_mvp.json --dry-run`

Полученные результаты:

- validator run завершился успешно, JSON-отчёт сформирован
- gate run завершился успешно, формат gate-отчёта сохранён
- статусы совместимы с текущей dual-mode моделью (`gate_status=REJECT`, `gate_status_controlled=ACCEPT`)

Ограничения MVP:

- snapshot-specific checks покрывают только базовый metadata/policy слой
- расширенная диагностика snapshot lifecycle остаётся вне текущего шага

---

## Risks / Limitations

- поддержка остаётся минимальной
- policy coverage пока не полная
- возможны будущие уточнения severity matrix

---

## Outcome

Snapshot subsystem переведена из purely documented mode
в minimally executable validation mode.

---

## Follow-up

- расширение snapshot-specific findings
- улучшение gate diagnostics
- возможный отдельный protocol/runbook для snapshot readiness checks
