# Вывод генератора отчётов

## сводка

- **gate_status** (данные из gate JSON): `REJECT` (source: gate JSON)
- **gate counts** (данные из gate JSON): `{"error": 7, "info": 0, "total": 52, "warn": 45}` (source: gate JSON)
- **validator counts** (данные из validator JSON): `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}` (source: validator JSON)
- **примечание**: значения выше скопированы из входных JSON; файл не является каноническим документом DocOps. (source: DOA-ARCH-019)

## зафиксировано в текущем запуске

- выполнена загрузка входного файла validator `doa_link_id_validator_run_001.json` (source: validator JSON)
- выполнена загрузка входного файла gate `doa_document_gate_run_001.json` (source: gate JSON)
- сформирован файл отчёта `report_generator_run_002.md` (source: generator internal)

## состояние по типам документов

- агрегация **doc_type** **недоступна**: во входах нет поля `doc_type` в строках находок. (source: gate JSON; validator JSON)

## риски

- из **gate** `counts`: error=7, warn=45, info=0 (числовые поля из входного JSON). (source: gate JSON)
- из **validator** `counts`: `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}`. (source: validator JSON)

## следующие шаги

- повторно запустить validator и gate, обновить входы и сгенерировать отчёт заново. (source: DOA-OP-021)
- продолжить операционные задачи по `DOA-OP-021` вне этого генератора. (source: DOA-OP-021)
- человеко-читаемый deterministic слой по `DOA-OP-024` / `DOA-DEC-043`. (source: DOA-OP-024)
- полная русификация статических строк по `DOA-OP-025` / `DOA-DEC-044`. (source: DOA-OP-025)

## что изменилось

- изменений по доступным полям не обнаружено (source: generator internal)

## происхождение данных

- **время генерации отчёта (UTC)**: `2026-04-14T04:09:35Z` (source: generator internal)
- **путь входного файла validator**: `D:/Work/DocOp/Project/reports/doa_link_id_validator_run_001.json` (source: CLI arguments)
- **путь входного файла gate**: `D:/Work/DocOp/Project/reports/doa_document_gate_run_001.json` (source: CLI arguments)
- **версия генератора**: `doa-report-generator/0.3.0-mvp` (source: generator internal)
- **source_commit**: `788ba7d6e574262abff17cb3fdd515d69b678904` (source: subprocess git rev-parse HEAD)
- **gate.engine_version** (из gate JSON): `0.1.0` (source: gate JSON)
- **gate.policy_version** (из gate JSON): `doa-gate-policy/1` (source: gate JSON)
- **validator** версия движка (из validator JSON): `0.1.0` (source: validator JSON)
- **gate.generated_at_utc** (из gate JSON): `2026-04-10T07:25:19Z` (source: gate JSON)
- **validator.generated_at_utc** (из validator JSON): `2026-04-10T08:35:19Z` (source: validator JSON)
- **gate.repo_root** (из gate JSON): `D:\Work\DocOp\Project` (source: gate JSON)
- **validator.root** (из validator JSON): `D:\Work\DocOp\Project` (source: validator JSON)
