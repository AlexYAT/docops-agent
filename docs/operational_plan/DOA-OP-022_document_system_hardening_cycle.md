# operational_plan — DOA-OP-022

## Metadata

- Project: DocOps Agent
- Doc type: operational_plan
- ID: DOA-OP-022
- Status: planned
- Date: 2026-04-10
- Parent: DOA-DEC-035

---

## Goal

Закрыть canonical blockers и подготовить baseline-aware систему.

## Scope

- canonical metadata
- gate policy
- validator behavior
- baseline snapshot

## Tasks

### T01 — Identify canonical violations

- собрать список всех canonical error из последнего отчета.

### T02 — Design resolution approach

- определить способ устранения без нарушения create-only.

### T03 — Legacy policy design

- определить allowlist / baseline logic (без реализации).

### T04 — Gate improvement

- добавить exit codes;
- подготовить поддержку режимов (design-level).

### T05 — Re-run validator + gate

- выполнить повторный прогон.

### T06 — Evaluate improvement

- сравнить с предыдущим run.

### T07 — Baseline snapshot

- зафиксировать новый implementation_snapshot.

## Success criteria

- уменьшение canonical ошибок;
- контролируемый уровень warn;
- воспроизводимый baseline.

## Out of scope

- UI расширения;
- autofix;
- git automation.

## Next artifact

- DOA-IMP-017 (baseline snapshot)
