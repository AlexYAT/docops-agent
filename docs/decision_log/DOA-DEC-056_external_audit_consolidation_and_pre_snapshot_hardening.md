# DOA-DEC-056 — External audit consolidation and pre-snapshot hardening

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-056
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-055

---

## Title

Консолидация внешнего аудита и смещение приоритета на pre-snapshot hardening

---

## Context

После readiness audit и принятия стратегии внешнего multi-model аудита были выполнены два независимых внешних аудита:

- DOA-AUD-012 — external audit Codex run 001
- DOA-AUD-013 — external audit Sonnet run 001

Оба аудита подтверждают, что snapshot-driven архитектура концептуально корректна и operationally workable для MVP.

Одновременно аудиты выявили ряд ограничений и governance gaps:

- хрупкость Git-based zone attribution
- неполное покрытие severity policy (в основном реализован error-slice)
- риск policy-code drift
- draft-статус ключевых архитектурных и operational документов, уже используемых как operational foundation
- hardcoded BOUNDARY_COMMIT в validator logic
- неинтерпретированный `other_zone_findings_count`
- слабый readiness signal при `controlled_findings_count = 0` в молодой controlled зоне

---

## Options considered

1. Продолжать к следующему fixed snapshot cycle немедленно
2. Выполнить ещё несколько внешних аудитов перед любыми действиями
3. Зафиксировать результаты текущих аудитов и сместить ближайший приоритет на targeted hardening перед следующим snapshot cycle

---

## Chosen solution

Сместить ближайший приоритет на targeted pre-snapshot hardening перед следующим fixed snapshot cycle

---

## Why

- два внешних аудита уже дали достаточный signal для принятия решения
- ключевые architectural risks уже выявлены
- продолжение к следующему snapshot без закрытия governance gaps создаёт риск ложной формальной готовности
- система требует не новых общих идей, а локального укрепления слабых мест

---

## Consolidated Findings

### Confirmed by both audits

- snapshot-driven модель архитектурно состоятельна
- dual-mode semantics работоспособна
- zone attribution через Git history является хрупким местом
- severity policy реализована неполно
- возможен drift между документной policy и кодом

### Elevated by Sonnet

- ключевые документы snapshot subsystem имеют `Status: draft`, несмотря на их operational role
- `BOUNDARY_COMMIT` захардкожен в коде
- `other_zone_findings_count` не интерпретирован в readiness semantics
- readiness PASSED следует трактовать как ограниченный MVP-signal, а не как сильное доказательство зрелости зоны

---

## Decision

Перед следующим fixed snapshot cycle система должна пройти targeted hardening как отдельный приоритетный этап.

Минимальный hardening scope:

1. закрыть draft/accepted governance gap для ключевых документов snapshot subsystem
2. задокументировать или устранить closure semantics asymmetry
3. объяснить и закрыть `other_zone_findings_count`
4. расширить policy coverage за пределы error-only snapshot checks
5. определить, как boundary configuration должна эволюционировать без ручной правки кода при смене эпохи

---

## Trade-offs

- следующий fixed snapshot откладывается
- появляется дополнительный этап hardening
- operational velocity снижается краткосрочно
- зато снижается риск закрепления слабой governance-модели в следующей эпохе

---

## Consequences

- readiness PASSED остаётся валидным как MVP-сигнал
- но не считается достаточным основанием для немедленного snapshot creation
- ближайший этап работы — hardening, а не новый snapshot
- следующие планы и execution steps должны быть направлены на закрытие выявленных gaps

---

## Follow-ups

- создать новый operational_plan на pre-snapshot hardening
- затем выполнить implementation steps по выявленным gaps
- после hardening повторить readiness audit
- только после этого переходить к следующему fixed snapshot cycle
