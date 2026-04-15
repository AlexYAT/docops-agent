## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-050
- Status: draft
- Date: 2026-04-15
- Parent: DOA-DEC-049
- Replaces: DOA-DEC-027

---

## Title

Create-only successor for DOA-DEC-027 metadata key normalization (M1/BKT-D)

## Context

- В baseline T01 (`doa_link_id_validator_run_003_integrity_baseline_op029_t01.json`) зафиксирован blocker `noncanonical_doc_type_key` для `DOA-DEC-027`.
- В `DOA-IMP-030` и `DOA-DEC-049` для M1 задан create-only remediation path через successor-документ.
- Исходный `DOA-DEC-027` не изменяется.

## Options considered

1. Оставить `DOA-DEC-027` без изменений и без successor.  
2. Править `DOA-DEC-027` in-place.  
3. Выпустить create-only successor с canonical metadata key.

## Chosen solution

Выбрана **Option 3**: выпустить `DOA-DEC-050` как successor к `DOA-DEC-027` с корректным полем `Doc type` и traceable lineage через `Replaces`.

## Why

- Соответствует create-only и не переписывает legacy-историю.
- Делает metadata-ключ machine-readable по текущему контракту.
- Сохраняет явную трассируемость lineage (`Replaces: DOA-DEC-027`).

## Trade-offs

- Исходный legacy-документ остается в репозитории без in-place коррекции.
- Фактическое влияние на blocker subset зависит от текущей интерпретации validator/gate successor-модели.

## Follow-ups

- Проверить evidence rerun validator/gate в рамках M1 (`DOA-OP-029` T04).
- Результат влияния на blocker subset зафиксировать отдельным implementation_snapshot M1.
