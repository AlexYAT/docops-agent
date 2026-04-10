# audit_check — DOA-AUD-005

## Metadata

- Project: DocOps Agent
- Doc type: audit_check
- ID: DOA-AUD-005
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-IMP-016

---

## Summary

- Система `validator -> gate -> UI` признана архитектурно корректной.
- UI корректно реализован как thin shell.
- Основной риск: metadata consistency и legacy слой.

## Scope

- validator
- gate
- UI
- metadata contract
- document system

## Strengths

- правильное разделение слоев;
- прозрачная policy модель;
- machine-readable отчеты;
- соблюдение create-only и traceability.

## Issues

### Critical

- canonical metadata нарушения (Parent, duplicate ID, Replaces);
- отсутствие metadata у legacy decision_log;
- broken traceability.

### Medium

- большое количество legacy findings -> noise risk;
- грубый severity mapping;
- отсутствие формализованного legacy режима.

### Minor

- requirements без версий;
- фиксированный report path;
- отсутствие exit codes.

## Architectural risks

- двойная реальность: canonical vs legacy;
- risk fatigue из-за warn шума;
- зависимость от ручной дисциплины.

## Recommendations

- закрыть canonical blockers;
- ввести legacy allowlist / mapping;
- добавить strict / baseline-aware режимы;
- ввести no-regression rule;
- подготовить baseline snapshot.

## Recommended next cycle

- audit -> decision -> remediation -> baseline snapshot
