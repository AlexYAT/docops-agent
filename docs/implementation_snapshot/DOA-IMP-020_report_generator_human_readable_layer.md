# implementation_snapshot — DOA-IMP-020

## Metadata

- Project: docops-agent
- Doc type: implementation_snapshot
- ID: DOA-IMP-020
- Status: recorded
- Date: 2026-04-14
- Parent: DOA-OP-024

---

## Summary

По **`DOA-OP-024`** и **`DOA-DEC-043`** обновлён **`scripts/doa_report_generator.py`**: русские заголовки разделов, блок **«зафиксировано в текущем запуске»**, детерминированный поиск предыдущего отчёта `report_generator_run_XXX.md` в каталоге вывода, блок **«что изменилось»** (сравнение `gate_status`, счётчиков gate `error`/`warn`/`info`, JSON `validator counts`), сохранены проверки **DoD** / **forbidden** / **traceability** для новых заголовков. Выполнены smoke run-ы.

## Новые разделы отчёта

- **`## сводка`** (бывший summary)
- **`## зафиксировано в текущем запуске`**
- **`## состояние по типам документов`**
- **`## риски`**, **`## следующие шаги`**
- **`## что изменилось`**
- **`## происхождение данных`** (provenance)

## Поиск предыдущего отчёта (T03)

- Только каталог **`--out`**, шаблон имени **`report_generator_run_(\d+).md`**, номер строго **меньше** текущего; максимальный из доступных.
- Текущий файл не рассматривается как «предыдущий».

## Delta (T04)

- Из предыдущего файла извлекаются только строки с ключами **`gate_status`**, **`gate counts`**, **`validator counts`** (regex по тому же формату, что пишет генератор).
- При отсутствии файла — буллет «предыдущий запуск не найден»; при ошибке чтения/парсинга — зафиксированные сообщения с `(source: unavailable)`; при равенстве полей — «изменений по доступным полям не обнаружено».

## Smoke run

- **Команда 001:** `python scripts/doa_report_generator.py --validator reports/doa_link_id_validator_run_001.json --gate reports/doa_document_gate_run_001.json --out reports/report_generator_run_001.md`
- **Команда 002 (проверка delta):** тот же ввод, `--out reports/report_generator_run_002.md`
- **Выход:** обновлены **`reports/report_generator_run_001.md`**, создан **`reports/report_generator_run_002.md`**.

## Версия генератора

- **`doa-report-generator/0.2.0-mvp`**

## Traceability

- **`DOA-DEC-043`** — решение о human-readable deterministic слое.
- **`DOA-ARCH-019`** — отчёт не SoT; структура и `(source: …)`.
- **`DOA-DEC-039`** — структурная проверка DoD (расширена под RU-заголовки).
