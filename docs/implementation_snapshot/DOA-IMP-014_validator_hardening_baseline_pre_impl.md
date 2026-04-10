# implementation_snapshot — DOA-IMP-014

## Metadata

- Project: DOA
- Doc type: implementation_snapshot
- ID: DOA-IMP-014
- Status: draft
- Date: 2026-04-10
- Parent: DOA-OP-019

---

## Summary

Зафиксировано **исходное состояние репозитория до начала реализации** плана **DOA-OP-019** (validator hardening / v0.2): на момент снимка действует **doa_link_id_validator** **v0.1.0**, доступен отчёт первого прогона (**DOA-IMP-013**), задачи T01–T06 по усилению валидатора **ещё не выполнялись**.

## Context

- **DOA-OP-018** закрыт первым прогоном валидатора; **DOA-IMP-013** описывает результаты **v0.1.0** и ограничения (в т.ч. отсутствие legacy folder/family mismatch для **DOA-OP-017**, неполная проверка ссылок в `docs/`).
- **DOA-OP-019** определяет следующий этап: довести валидатор до **v0.2.x**, второй прогон и последующий **implementation_snapshot** по завершении T06.
- Данный документ — **baseline «до реализации»** нового этапа, в духе create-only (без правок существующих артефактов).

## What was decided

- Принять текущую линию **OP-019** как обязательный следующий шаг по автоматизации проверок ссылок и ID.
- Зафиксировать **точку отсчёта**: код и отчёты остаются в состоянии после **IMP-013**, до изменений скрипта и **run_002**.

## System state

- **Валидатор:** `scripts/doa_link_id_validator.py`, заявленная версия **0.1.0**, schema `doa-validator-report/1`.
- **Отчёт первого прогона:** `reports/doa_link_id_validator_run_001.json` (см. **DOA-IMP-013**).
- **Документация процесса:** **DOA-DEC-031** (canonical reference contract), **DOA-AUD-003** (аудит ссылок/ID).
- **План hardening:** `docs/operational_plan/DOA-OP-019_validator_hardening_v02.md` — задачи **T01–T06** в статусе «к выполнению» с точки зрения данного снимка.

## Observations

- Основной технический долг **v0.1** сформулирован явно в **DOA-IMP-013** и перенесён в задачи **DOA-OP-019**; дублирование деталей в этом снимке намеренно минимально.
- Контент `docs/` и `templates/` на baseline не менялся ради «зелёного» отчёта; ожидаемо сохранение высокой доли **legacy**-находок до отдельных решений о миграции.

## Risks

- После **v0.2** отчёт может стать **несравним** с **run_001** без явных полей версии/schema — это учтено в **DOA-OP-019** (T04/T05); риск остаётся до реализации.
- Новые эвристики (**T01**, **T02**) могут временно увеличить шум в отчёте до настройки порогов и severity.

## Next steps

- Выполнить **DOA-OP-019** T01–T05 в коде и формате отчёта; затем **T06** — второй прогон и новый **implementation_snapshot** по итогам hardening.
- При смене контракта полей или политики fail/legacy — рассмотреть отдельный **decision_log** (create-only), как отмечено в **DOA-IMP-013**.

## Artifacts

| Артефакт | Назначение |
|----------|------------|
| `docs/operational_plan/DOA-OP-019_validator_hardening_v02.md` | План этапа v0.2 (родительский контекст для этого снимка). |
| `docs/implementation_snapshot/DOA-IMP-013_link_id_validator_first_run.md` | Снимок после первого прогона v0.1. |
| `reports/doa_link_id_validator_run_001.json` | Machine-readable отчёт v0.1. |
| `scripts/doa_link_id_validator.py` | Исходный код валидатора на baseline (v0.1.0). |
