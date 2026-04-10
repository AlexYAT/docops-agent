# implementation_snapshot — DOA-IMP-015

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-015
- Status: draft
- Date: 2026-04-10
- Parent: DOA-OP-020

---

## Summary

Завершён **MVP Document Gate** по **DOA-OP-020**: реализованы **T01–T04** в `scripts/doa_document_gate.py`, выполнен **первый прогон** с **dry-run** по умолчанию, validator используется как **engine**, поверх него применён **policy mapping** severity → **gate_status**; итог зафиксирован в **`reports/doa_document_gate_run_001.json`**.

## Context

- **DOA-IDEA-002** — идея Document Gate (статусы, JSON, без семантических правок).
- **DOA-DEC-031** — canonical reference contract; engine различает canonical / legacy находки.
- **DOA-DEC-032** — policy model MVP: **ACCEPT / ACCEPT_WITH_WARNINGS / REJECT**, маппинг **error / warn / info**, dry-run по умолчанию, autofix только механический и opt-in.
- **DOA-OP-018** / **DOA-OP-019** — линия **link/ID validator** (v0.1 и план hardening v0.2).
- **DOA-OP-020** — операционный план реализации MVP Gate; данный снимок закрывает цикл **T07–T08** в части фиксации первого прогона (код и отчёты уже существуют; повторный запуск в рамках этого шага **не выполнялся**).

## What was executed

- Запуск **`scripts/doa_document_gate.py`** с параметрами по умолчанию (`--root` → репозиторий, **`--dry-run`** включён по умолчанию, **`--autofix`** не использовался).
- **Engine:** подпроцессный вызов **`scripts/doa_link_id_validator.py`** (v0.1.0), разбор JSON-отчёта из stdout.
- **Policy mapping:** назначение **severity** при отсутствии поля в engine (canonical → error, legacy → warn, root_link по правилам скрипта) и агрегация в **gate_status** (**DOA-DEC-032**).
- Запись канонического отчёта **`doa-gate-report/1`** в **`reports/doa_document_gate_run_001.json`**.

## Results

По состоянию артефакта **`reports/doa_document_gate_run_001.json`** (`generated_at_utc`: **2026-04-10T04:48:17Z**):

| Поле | Значение |
|------|-----------|
| **gate_status** | **REJECT** |
| **counts.total** | **52** |
| **counts.error** | **7** |
| **counts.warn** | **45** |
| **counts.info** | **0** |
| **engine_version** | **0.1.0** |
| **policy_version** | **doa-gate-policy/1** (default, отдельный policy-файл не подключался) |

**Связь с validator:** в отчёте gate полный сырой отчёт engine лежит в **`raw.engine_report`** (тот же формат, что выдаёт validator). Отдельно сохранён **`reports/doa_link_id_validator_run_001.json`** — **автономный** прогон engine без слоя gate (на момент его генерации: **76** файлов, **5** canonical violations, **45** legacy findings); цифры **gate** и **standalone validator** могут расходиться из‑за разного времени снимка дерева и того, что **gate** дополнительно классифицирует находки по **severity** и считает **gate_status**, тогда как **validator** отдаёт только списки нарушений/находок без итогового статуса приёмки.

## Artifacts

| Путь | Назначение |
|------|------------|
| `reports/doa_document_gate_run_001.json` | Канонический отчёт **doa-gate-report/1** после первого прогона. |
| `reports/doa_link_id_validator_run_001.json` | Сохранённый отчёт engine **doa-validator-report/1** (сравнение / архив). |
| `scripts/doa_document_gate.py` | Реализация MVP Gate (T01–T04). |

## Observations

- **Engine vs gate:** validator сообщает **факты** (категории, режим canonical/legacy, файлы); **gate** не дублирует правила проверки, а добавляет **severity**, **counts**, **gate_status** и обёртку отчёта — это разные уровни ответственности.
- **Policy:** при отсутствии severity в v0.1 дефолтный маппинг резко поднимает вес **canonical** нарушений до **error**, а **legacy** — до **warn**, что приводит к **REJECT** при любом canonical error даже при большом числе ожидаемых legacy-предупреждений (**ACCEPT_WITH_WARNINGS** без errors недостижим в такой конфигурации репозитория).
- **Legacy findings:** массово идут как **warn**; они не «чинятся» gate и отражают историческое состояние `docs/` согласно **DOA-DEC-031**.
- **Dry-run по умолчанию:** соответствует **DOA-DEC-032**; в текущем MVP автозапись в markdown от gate не выполнялась (**autofix** не реализован).

## Next steps

- **CI integration:** использовать **exit code** и **`gate_status`** в pipeline (отдельный operational шаг; политика fail на **REJECT** vs допуск **ACCEPT_WITH_WARNINGS** — решать явно).
- **Validator v0.2** (**DOA-OP-019**): выровнять **severity** на стороне engine, упростить default policy в gate.
- **Autofix strategy:** только **механический** whitelist и отдельный **decision_log** при расширении (**DOA-DEC-032**).
