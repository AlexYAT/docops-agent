# operational_plan — DOA-OP-021

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-021
- Status: planned
- Date: 2026-04-14
- Parent: DOA-DEC-039

---

## Objective

Реализовать MVP Report Generator, который:

- генерирует отчёт на основе validator/gate outputs
- соответствует Definition of Done (`DOA-DEC-039`)
- соблюдает anti-SoT правила (`DOA-ARCH-019`)
- не нарушает Policy Contract (`DOA-ARCH-018` / `020`)

## Scope (MVP)

### Включено

- генерация одного отчёта по текущему состоянию репозитория
- вход: validator output + gate output (JSON)
- выход: markdown отчёт
- структура отчёта строго по `DOA-ARCH-019`
- проверка DoD (минимальная, детерминированная)

### Не включено

- UI
- автоматический запуск
- интеграция с Git hooks
- расширенная аналитика

## Inputs

- `reports/doa_link_id_validator_run_*.json`
- `reports/doa_document_gate_run_*.json`

## Output

- `reports/report_generator_run_001.md`

## Tasks

### T01 — Input loading

- загрузка validator output
- загрузка gate output
- проверка доступности файлов

### T02 — Basic parsing

- извлечение:
  - findings
  - severity
  - counts
  - doc_type (если есть)

### T03 — Report structure generation

Сформировать разделы:

- summary
- state by doc_type
- risks
- next steps
- provenance

### T04 — Traceability enforcement (MVP)

- каждое утверждение должно:
  - ссылаться на `DOA-*` или
  - ссылаться на validator/gate output

### T05 — Forbidden checks (MVP)

Проверить:

- нет Parent/Replaces
- нет нормативных утверждений
- нет report-only facts

### T06 — Provenance block

Добавить:

- timestamp
- source files (validator/gate)
- commit (если доступен)
- generator version (MVP)

### T07 — DoD check (MVP)

Проверить:

- генерация без ошибки
- все разделы присутствуют
- есть provenance
- есть traceability
- нет forbidden элементов

### T08 — Output writing

- сохранить файл в `reports/`
- имя: `report_generator_run_001.md`

## Acceptance criteria

- отчёт генерируется без ошибок
- структура соответствует `DOA-ARCH-019`
- выполняются все machine-verifiable DoD критерии (`DOA-DEC-039`)
- отсутствуют нарушения anti-SoT

## Risks

- некорректная трассируемость
- появление report-only фактов
- несоответствие структуре отчёта

## Notes

- строго без «умных» интерпретаций
- без NLP
- только детерминированная логика
- минимальная реализация (MVP)
