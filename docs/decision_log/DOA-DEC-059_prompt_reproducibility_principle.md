# DOA-DEC-059 — Prompt reproducibility principle

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-059
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-058

---

## Decision

Prompt является воспроизводимой единицей изменения системы.

---

## Rules

- каждый prompt должен быть достаточен для повторного выполнения
- результат должен быть воспроизводим через тот же prompt
- запрещены "ручные доработки" вне prompt execution

---

## Consequences

- обеспечивается повторяемость процессов
- упрощается автоматизация
- снижается зависимость от ручных действий
