## Metadata

- Project: DocOps Agent
- Doc type: decision_log
- ID: DOA-DEC-035
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-AUD-005

---

## Title

Hardening policy for canonical metadata, legacy handling, and gate modes

## Context

По результатам внешних аудитов (OpenClaw + Qwen) архитектура `validator -> gate -> UI` признана корректной, но
ключевой риск сосредоточен в качестве данных: canonical metadata нарушения и исторический legacy-слой создают noise
и снижают предсказуемость gate-решений.

## Decision

1. Canonical blockers — приоритет 1
- unresolved parent
- duplicate ID
- invalid metadata

2. Legacy handling
- legacy не исправляется массово
- вводится explicit handling policy
- будет реализован allowlist / mapping / baseline

3. Gate modes
- strict — для CI и строгой проверки
- baseline-aware — для ежедневной работы с legacy

4. No-regression rule
- новые документы не должны добавлять legacy-классы нарушений

5. Create-only compliance
- исправления выполняются через новые документы или системные механизмы

6. Validator evolution
- допускается введение legacy heuristics (в будущем)
- без изменения смысла документов

## Rationale

- архитектура уже зрелая;
- проблема в данных, а не в коде;
- необходимо снизить noise и повысить доверие к gate.

## Consequences

- появляется controlled remediation cycle;
- снижается риск игнорирования gate;
- улучшается предсказуемость системы.
