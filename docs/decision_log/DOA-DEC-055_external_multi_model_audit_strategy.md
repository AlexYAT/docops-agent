# DOA-DEC-055 — External multi-model audit strategy

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-055
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-AUD-011

---

## Title

Стратегия внешнего multi-model аудита

---

## Context

Система DocOps Agent достигла состояния, в котором snapshot subsystem уже не только описана документально, но и подтверждена внутренними operational checks.

На текущем этапе зафиксировано:

- snapshot artifact specification определён
- lifecycle snapshot определён
- snapshot creation protocol определён
- snapshot readiness checks определены
- validator/gate получили MVP-поддержку snapshot semantics
- readiness audit выполнен и завершился статусом PASSED
- controlled зона рассматривается как operational truth
- legacy findings сохраняются как historical noise и не блокируют readiness в рамках dual-mode snapshot-driven модели

Это создаёт подходящую точку для внешнего аудита архитектуры и operational semantics средствами нескольких LLM моделей через Cursor.

---

## Options considered

1. Не проводить внешний аудит и двигаться дальше только на основе внутренней валидации
2. Провести единичный внешний аудит одной моделью
3. Провести multi-model внешний аудит несколькими моделями

---

## Chosen solution

Провести внешний multi-model аудит несколькими моделями через Cursor

---

## Why

- снижает риск model-specific bias
- позволяет проверить архитектуру с разных reasoning profiles
- повышает доверие к snapshot-driven design
- помогает выявить скрытые противоречия в validator/gate/readiness semantics
- создаёт более надёжную основу перед следующим fixed snapshot cycle

---

## Audit Strategy

Внешний аудит должен выполняться как серия независимых audit runs.

Каждая модель получает согласованный контекст:

- документы snapshot subsystem
- validator/gate reports
- readiness audit
- действующие dual-mode semantics

Цели аудита:

- проверить корректность snapshot-driven модели
- проверить корректность dual-mode разделения legacy / controlled
- проверить согласованность validator и gate
- проверить адекватность readiness criteria
- выявить архитектурные риски и слабые места

---

## Output Format

Результат каждого внешнего аудита фиксируется отдельным новым документом типа `audit_check`.

Рекомендуемый формат:
- один audit_check на одну модель
- без редактирования уже созданных audit документов
- с явной привязкой к текущему этапу snapshot subsystem

---

## Trade-offs

- возможны противоречивые выводы между моделями
- потребуется последующий consolidation step
- аудит может усилить noise за счёт фокуса на legacy части
- multi-model audit увеличивает количество документов и требует дисциплины интерпретации

---

## Consequences

- система получит внешнюю архитектурную оценку
- появится несколько независимых audit_check документов
- возможно потребуется создание дополнительных decision_log или operational_plan по результатам аудита
- следующий fixed snapshot сможет опираться не только на внутреннюю readiness проверку, но и на внешний audit evidence

---

## Follow-ups

- выполнить внешний audit run через Cursor для первой модели
- зафиксировать результат как отдельный audit_check
- повторить для дополнительных моделей
- при необходимости выполнить consolidation audit / decision step
