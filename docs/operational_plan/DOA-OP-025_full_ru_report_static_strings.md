# operational_plan — DOA-OP-025

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-025
- Status: planned
- Date: 2026-04-14
- Parent: DOA-DEC-044

---

## Title

План: полная русификация статических строк Report Generator

## Objective

Реализовать полную русификацию статических строк отчёта в Report Generator в соответствии с **`DOA-DEC-044`**, без изменения deterministic-логики и без расширения scope.

## Scope

### Включено

- перевод статических заголовков и фраз в отчёте
- сохранение source markers `(source: …)`
- сохранение JSON keys в backticks
- smoke run
- implementation_snapshot

### Не включено

- изменение delta-логики
- изменение provenance-логики
- изменение source markers
- изменение anti-SoT правил
- интерпретация / аналитика

## Inputs

- `scripts/doa_report_generator.py`
- `reports/report_generator_run_001.md`
- `reports/report_generator_run_002.md`
- `docs/decision_log/DOA-DEC-044_report_generator_full_ru_static_strings.md`

## Output

- обновлённый generator
- обновлённый пример отчёта
- новый implementation_snapshot

## Tasks

- **T01** — определить список англоязычных статических строк в отчёте
- **T02** — перевести статические строки на русский
- **T03** — сохранить `(source: …)` без изменений
- **T04** — сохранить JSON keys и значения внутри backticks без перевода
- **T05** — адаптировать structural checks только при необходимости
- **T06** — выполнить smoke run
- **T07** — зафиксировать implementation_snapshot

## Acceptance criteria

- В отчёте отсутствуют англоязычные статические фразы, кроме source markers и JSON keys
- source markers сохранены без изменений
- `validate_generated_report` проходит
- delta-логика работает как раньше
- forbidden checks не ослаблены

## Risks

- случайный перевод source markers
- случайный перевод JSON keys
- нарушение существующих checks

## Notes

- без NLP
- без интерпретации
- минимальный change set
