# DOA-DEC-053 — Snapshot lifecycle

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-053
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-IMP-034

---

## Title

Введение lifecycle для snapshot и управления эпохами

---

## Context

Система перешла в snapshot-driven режим:

- существует fixed snapshot boundary
- введена controlled zone
- активная разработка ведётся внутри текущей эпохи

Однако отсутствует формализованный lifecycle snapshot:

- когда создавать новый snapshot
- какие критерии готовности
- как закрывается эпоха
- как начинается новая

Это создаёт риск:

- бесконечной эпохи
- отсутствия контрольных точек
- размывания границ системы

---

## Options considered

1. Не вводить lifecycle (manual / ad-hoc)
2. Ввести строгий lifecycle snapshot
3. Частично формализовать через рекомендации

---

## Chosen solution

Ввести явный lifecycle snapshot с минимальной формализацией

---

## Definition

Snapshot lifecycle включает:

1. Active epoch  
   - работа ведётся внутри controlled zone

2. Stabilization phase  
   - уменьшение критических нарушений
   - стабилизация gate_status_controlled

3. Snapshot readiness  
   - controlled зона соответствует критериям
   - система готова к фиксации

4. Snapshot creation  
   - создаётся новый fixed snapshot

5. New epoch activation  
   - начинается новая operational эпоха

---

## Criteria (MVP)

Snapshot может быть создан, если:

- gate_status_controlled = ACCEPT
- нет критических validator ошибок в controlled зоне
- основные operational документы завершены
- система стабильно работает в текущей эпохе

---

## Why

- делает систему дискретной (epoch-based)
- даёт контрольные точки развития
- уменьшает хаос изменений
- усиливает traceability

---

## Trade-offs

- требует дисциплины
- добавляет формальные этапы
- может замедлить быстрые изменения

---

## Consequences

- каждая эпоха становится изолированной
- snapshot становится ключевым артефактом системы
- validator и gate становятся частью lifecycle

---

## Follow-ups

- operational_plan для snapshot creation protocol
- возможно расширение validator под lifecycle
