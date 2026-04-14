# implementation_snapshot — DOA-IMP-019

## Metadata

- Project: docops-agent
- Doc type: implementation_snapshot
- ID: DOA-IMP-019
- Status: recorded
- Date: 2026-04-14
- Parent: DOA-OP-021

---

## Summary

В **`scripts/doa_report_generator.py`** реализованы задачи **`DOA-OP-021` T04–T07**: обязательные маркеры трассируемости `(source: …)` по строкам, проверки **forbidden** (pattern/string), расширенный блок **provenance** с детерминированным **`source_commit`** (`git rev-parse HEAD` или `unavailable`), структурная **`validate_generated_report`** перед записью файла. Выполнен **успешный smoke run**; обновлён **`reports/report_generator_run_001.md`**.

## T04 — Traceability enforcement (MVP)

- Каждая строка-буллет в разделах `summary`, `state by doc_type`, `risks`, `next steps`, `provenance` генерируется **только** с явным суффиксом `(source: …)` (`gate JSON`, `validator JSON`, комбинации, `DOA-ARCH-019`, `DOA-OP-021`, `generator internal`, `CLI arguments`, `subprocess git rev-parse HEAD`, `unavailable`).
- Функция **`check_traceability_markers`**: для перечисленных секций каждая непустая строка либо буллет с `(source:`, либо ошибка (нет NLP).

## T05 — Forbidden checks (MVP)

- Функция **`check_forbidden_markdown`**: подстроки `Parent:`, `Replaces:`, шаблоны имитации метаданных (`- Doc type:`), буллет `- ID: DOA-…`, заголовок `## Metadata`; при совпадении — stderr и **exit 1** до записи отчёта.

## T06 — Provenance block

- Раздел **`## provenance`** всегда содержит: timestamp UTC, пути входов, версию генератора, **`source_commit`** (результат `git rev-parse HEAD` в обнаруженном корне репозитория или строка **`unavailable`** с тегом `(source: unavailable)`), при наличии в JSON — `engine_version`, `policy_version`, версию validator, поля времени и корня из входов.

## T07 — DoD check (MVP)

- Функция **`validate_generated_report`**: первая непустая строка — заголовок отчёта; наличие обязательных `## summary` … `## provenance`; непустой provenance (≥ 4 буллета); вызовы **`check_traceability_markers`** и **`check_forbidden_markdown`**; при любой ошибке — stderr со списком причин и **exit 1** (генерация без записи файла).
- Полная семантическая проверка «report-only facts» **не** реализована; ограничение обеспечивается шаблонной генерацией и перечисленными проверками (MVP).

## Smoke run

- **Успешен:** да.
- **Команда:** `python scripts/doa_report_generator.py --validator reports/doa_link_id_validator_run_001.json --gate reports/doa_document_gate_run_001.json --out reports/report_generator_run_001.md`
- **Выход:** `reports/report_generator_run_001.md` (перезаписан).
- **Доп. JSON отчёт DoD:** не создавался (вне минимального scope).

## Traceability

- **`DOA-OP-021`** — операционный план.
- **`DOA-DEC-039`** — критерии DoD; реализована структурная подмножество-проверка.
- **`DOA-ARCH-019`** — anti-SoT и структура отчёта; ссылка в тексте summary-буллета.
