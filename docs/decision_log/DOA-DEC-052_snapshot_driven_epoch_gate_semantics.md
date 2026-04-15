## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-052
- Status: draft
- Date: 2026-04-15
- Parent: DOA-DEC-051

---

## Title

Snapshot-driven epoch semantics for gate and legacy boundary

## Context

- `DOA-IDEA-004` задает fixed snapshot и epoch-oriented модель эволюции.
- `DOA-DEC-049`, `DOA-DEC-051`, `DOA-ARCH-022`, `DOA-OP-031`, `DOA-IMP-033` закрепили closure semantics и dual-вердикты.
- При этом historical legacy findings все еще могут доминировать в глобальном gate-сигнале, что тянет систему в cleanup-first траекторию.
- Это конфликтует с целевой snapshot-driven моделью для onboarding и controlled evolution.

## Problem

- Legacy findings остаются видимыми и способны удерживать общий verdict в blocker-space.
- Это создает implicit pressure на обязательный cleanup pre-snapshot истории.
- Но snapshot model предполагает semantic reset по boundary, а не обязательное историческое «вымывание» перед forward work.

## Options considered

1. **Continue cleanup-first model**  
   Сохранять legacy как обязательный blocker-контур до глубокой исторической очистки.

2. **Hybrid blocker model**  
   Держать legacy blocker до полного закрытия старых findings, даже после snapshot boundary.

3. **Snapshot-driven epoch model**  
   Legacy остается видимым в отчетах, но после boundary не является blocking контуром для active controlled phase.

## Chosen solution

Выбран **Option 3 — snapshot-driven epoch model**.

## Rules

1. **Fixed snapshot is authoritative epoch boundary.**
2. **Post-snapshot operational verdict определяется controlled zone.**
3. **Legacy findings после boundary остаются reportable, но non-blocking для active epoch.**
4. **Historical/global verdict сохраняется как secondary audit/informational truth.**
5. **Нет прямого обязательства ремедиировать pre-snapshot legacy только для unlock controlled work.**
6. **Legacy remediation остается optional, policy-driven, и отделенной от controlled readiness.**
7. **Controlled-zone safety остается strict и блокирующей для current epoch.**

## Implications

- Gate semantics должны явно различать:
  - primary operational verdict (controlled),
  - secondary historical/global audit verdict.
- Future work не должно расширять remediation legacy-категорий только ради искусственного full-green состояния.
- Brownfield onboarding в DocOps становится валидным сценарием: история фиксируется snapshot-границей, а forward-governance идет по controlled zone.

## Why

- Это выравнивает operational semantics с исходным замыслом fixed snapshot epoch model.
- Снимает бессмысленную зависимость controlled readiness от полного legacy cleanup.
- Упрощает внедрение DocOps на существующие неидеальные репозитории без потери исторической прозрачности.

## Trade-offs

- Historical technical debt остается видимым и требует отдельного governance потока.
- Dual-verdict semantics становится более явной и требует дисциплины интерпретации.
- Система становится практичнее для brownfield, но менее «визуально green» в глобальном отчете.

## Follow-ups

- Открыть/поддержать архитектурный и операционный цикл выравнивания gate/report semantics под epoch model.
- Не продолжать M2/M3 expansion до тех пор, пока epoch semantics не отражены в актуальной архитектуре и operational plan.
