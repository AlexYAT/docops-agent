# implementation_snapshot — DOA-IMP-013

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-013
- Status: draft
- Date: 2026-04-10
- Parent: DOA-OP-018

---

## Summary

Выполнен **первый прогон** минимального **link/ID validator** по репозиторию DocOps Agent в рамках **DOA-OP-018** (T06). Результаты сохранены в machine-readable отчёте; нарушения канона и legacy-находки учтены раздельно, в соответствии с **DOA-DEC-031**.

## Context

- **DOA-AUD-003** зафиксировал проблемы машинной валидации ссылок и метаданных.
- **DOA-DEC-031** принял canonical reference contract (metadata SoT, legacy mode, разрешимые Parent/Replaces).
- **DOA-OP-018** определяет внедрение валидатора; данный снимок закрывает задачу **T06 — first validator run snapshot** без правок существующих документов (create-only).

## What was executed

- **Команда запуска:** `python scripts/doa_link_id_validator.py` с перенаправлением вывода в файл отчёта (PowerShell: `Set-Content -Encoding utf8 reports/doa_link_id_validator_run_001.json`).
- **Версия валидатора:** `doa_link_id_validator` **0.1.0**, schema `doa-validator-report/1` (исходник: `scripts/doa_link_id_validator.py`).
- **Область проверки:** все `docs/**/*.md`, а также корневые `README.md` и `WORKFLOW.md` (всего **76** файлов; в подсчёт входит и этот снимок после финальной перегенерации отчёта).

## Results

| Метрика | Значение |
|--------|----------|
| Файлов просканировано | 76 |
| **Canonical violations** | **5** |
| **Legacy findings** | **45** |

**Топ-3 категории (по объёму в отчёте):**

1. **`legacy_no_canonical_metadata`** — 43 (документы в `docs/` без блока `## Metadata` со строгим полем `ID`).
2. **`root_markdown_outside_docs_model`** — 2 (`README.md`, `WORKFLOW.md` вне модели обязательного metadata).
3. **Канонические нарушения по одному случаю каждое:** **`unresolved_parent`** (**DOA-ARCH-003** → `DOA-DOC-IDEA`), **`noncanonical_doc_type_key`** / **`missing_parent_field`** / **`status_not_in_enum`** (**DOA-DEC-027**), **`invalid_replaces_format`** (**DOA-OP-001** — `Replaces: DOA-OP-001 (draft)`).

## Artifacts

- Отчёт (JSON): `reports/doa_link_id_validator_run_001.json`  
- `generated_at_utc` (последняя перегенерация): `2026-04-10T03:39:19Z`.

## Observations

- Документы **без** канонического metadata-блока доминируют в отчёте; это ожидаемо для исторического слоя и совпадает с выводами **DOA-AUD-003**.
- **`DOA-OP-017.md`** в каталоге `implementation_snapshot/` не попал в категорию «folder vs family» в текущей версии скрипта, потому что для него нет канонического `## Metadata` — эвристика «OP-ID в IMP-папке» применяется только к канонически распознанным файлам; при необходимости правила стоит расширить в следующей итерации **T04**.
- Реестр известных ID строится из metadata, имени файла и заголовков; возможны краевые случаи, если один и тот же логический ID появляется в нескольких источниках — в этом прогоне **duplicate_id_registry** не сработал.

## Next steps

- **Усиление правил:** добавить явные legacy-категории для «несоответствие папки и семейства ID» без канонического блока; уточнить обработку второго блока `## Metadata` в одном файле; при необходимости — проверка markdown-ссылок глубже по `docs/`.
- **Новый decision_log:** не обязателен сразу; целесообразен, если меняется контракт полей (**Dependencies**, строгость `Replaces`, выключение legacy mode) — тогда **create-only** новая запись **DEC** с ссылкой на этот **IMP-013**.
- Интеграция в CI и пороги fail/warn — отдельный операционный шаг после стабилизации отчёта.
