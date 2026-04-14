# Report Generator Output

## сводка

- **gate_status** (from gate JSON): `REJECT` (source: gate JSON)
- **gate counts** (from gate JSON): `{"error": 7, "info": 0, "total": 52, "warn": 45}` (source: gate JSON)
- **validator counts** (from validator JSON): `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}` (source: validator JSON)
- **note**: values above are copied from JSON inputs; this file is not a canonical DocOps document. (source: DOA-ARCH-019)

## зафиксировано в текущем запуске

- выполнена загрузка validator input `doa_link_id_validator_run_001.json` (source: validator JSON)
- выполнена загрузка gate input `doa_document_gate_run_001.json` (source: gate JSON)
- сформирован отчёт `report_generator_run_002.md` (source: generator internal)

## состояние по типам документов

- doc_type aggregation **unavailable** from current inputs (no `doc_type` field on finding rows). (source: gate JSON; validator JSON)

## риски

- From **gate** `counts`: error=7, warn=45, info=0 (numeric fields from input JSON). (source: gate JSON)
- From **validator** `counts`: `{"canonical_resolved_via_overlay": 2, "canonical_unresolved_violations": 7, "canonical_violations": 9, "legacy_findings": 45}`. (source: validator JSON)

## следующие шаги

- Re-run validator and gate to refresh inputs, then regenerate this report. (source: DOA-OP-021)
- Continue operational tasks per `DOA-OP-021` outside this generator. (source: DOA-OP-021)
- Человеко-читаемый deterministic слой по `DOA-OP-024` / `DOA-DEC-043`. (source: DOA-OP-024)

## что изменилось

- изменений по доступным полям не обнаружено (source: generator internal)

## происхождение данных

- **report generated at (UTC)**: `2026-04-14T03:56:48Z` (source: generator internal)
- **validator input path**: `D:/Work/DocOp/Project/reports/doa_link_id_validator_run_001.json` (source: CLI arguments)
- **gate input path**: `D:/Work/DocOp/Project/reports/doa_document_gate_run_001.json` (source: CLI arguments)
- **generator version**: `doa-report-generator/0.2.0-mvp` (source: generator internal)
- **source_commit**: `39a45425069f1be192f58a6a5535ffe4aa9aab31` (source: subprocess git rev-parse HEAD)
- **gate engine_version** (from gate JSON): `0.1.0` (source: gate JSON)
- **gate policy_version** (from gate JSON): `doa-gate-policy/1` (source: gate JSON)
- **validator engine version** (from validator JSON): `0.1.0` (source: validator JSON)
- **gate.generated_at_utc** (from gate JSON): `2026-04-10T07:25:19Z` (source: gate JSON)
- **validator.generated_at_utc** (from validator JSON): `2026-04-10T08:35:19Z` (source: validator JSON)
- **gate.repo_root** (from gate JSON): `D:\Work\DocOp\Project` (source: gate JSON)
- **validator.root** (from validator JSON): `D:\Work\DocOp\Project` (source: validator JSON)
