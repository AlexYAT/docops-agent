# operational_plan — DOA-OP-024

## Metadata

- Project: docops-agent
- Doc type: operational_plan
- ID: DOA-OP-024
- Status: planned
- Date: 2026-04-14
- Parent: DOA-DEC-043

---

## Objective

Реализовать человеко-читаемый deterministic слой в Report Generator в соответствии с **`DOA-DEC-043`**.

## Scope (MVP)

- RU заголовки
- раздел «зафиксировано в текущем запуске»
- раздел «что изменилось»
- без изменения архитектуры генератора

## Inputs

- `reports/doa_link_id_validator_run_001.json`
- `reports/doa_document_gate_run_001.json`
- предыдущий `report_generator_run_XXX.md` (если есть)

## Output

- обновлённый `report_generator_run_XXX.md`

## Tasks

- **T01** — добавить RU заголовки
- **T02** — добавить раздел «зафиксировано…»
- **T03** — реализовать сравнение с предыдущим отчётом
- **T04** — добавить раздел «что изменилось»
- **T05** — обеспечить `(source: …)` для новых строк
- **T06** — сохранить DoD (T04–T07 checks)
- **T07** — выполнить smoke run

## Acceptance criteria

- отчёт содержит оба новых раздела
- все строки имеют `(source: …)`
- `validate_generated_report` проходит
- нет forbidden markdown

## Risks

- некорректное извлечение предыдущего отчёта
- нарушение deterministic логики

## Notes

- без NLP
- без интерпретации
