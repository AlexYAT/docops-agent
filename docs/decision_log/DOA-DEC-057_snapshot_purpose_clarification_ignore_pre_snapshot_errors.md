# DOA-DEC-057 — Snapshot purpose clarification: ignore pre-snapshot errors

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-057
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-DEC-056

---

## Title

Уточнение назначения fixed snapshot: игнорирование pre-snapshot ошибок

---

## Context

После readiness audit и внешних multi-model аудитов был временно смещён приоритет на pre-snapshot hardening.

Однако это противоречит исходному назначению fixed snapshot в системе DocOps Agent.

Fixed snapshot вводится не для того, чтобы:

- устранить все исторические ошибки
- довести всю систему до архитектурного идеала
- закрыть весь legacy technical debt
- добиться полного соответствия validator/gate всей policy matrix

Fixed snapshot вводится для того, чтобы:

- зафиксировать текущее состояние как boundary
- отсечь pre-snapshot слой
- начать новую controlled эпоху
- изолировать новые документы и новые проекты от legacy noise
- обеспечить, чтобы future execution опирался только на snapshot и post-snapshot документы

---

## Problem

Курс на обязательный pre-snapshot hardening перед snapshot creation приводит к смещению цели snapshot.

Это создаёт нежелательные эффекты:

- попытка “чинить прошлое” до перехода к новой эпохе
- смешение задач архитектурного улучшения и операционной изоляции
- замедление запуска controlled зоны для новых проектов
- рост зависимости новых инициатив от качества legacy слоя

---

## Clarification

Назначение fixed snapshot в DocOps Agent:

- snapshot является boundary artifact
- snapshot изолирует pre-snapshot ошибки
- snapshot фиксирует текущее состояние “как есть”
- snapshot открывает новую controlled epoch
- snapshot позволяет запускать новые проекты только в controlled зоне
- legacy ошибки и legacy governance gaps не должны блокировать snapshot creation, если controlled semantics остаётся консистентной

---

## Chosen interpretation

Создание fixed snapshot должно трактоваться как:

- intentional freeze of the past
- explicit boundary between legacy and controlled
- operational reset for future work

А не как:

- финальная чистка legacy
- обязательное устранение всех historical gaps
- prerequisite полного hardening всей системы

---

## Decision

Отказаться от трактовки fixed snapshot как результата обязательного pre-snapshot hardening.

Разрешить создание snapshot при условиях, достаточных для controlled execution:

- controlled зона консистентна
- отсутствуют критические ошибки внутри controlled зоны
- snapshot artifact корректен
- create-only и zone isolation сохраняются

Legacy ошибки, governance gaps и частичная незрелость pre-snapshot слоя:

- считаются допустимыми
- не блокируют snapshot creation
- остаются за boundary текущей эпохи

---

## Scope Impact

### Что не должно блокировать snapshot

- legacy findings
- historical gate reject
- draft или governance gaps в pre-snapshot контуре
- неполная реализация warning/info policy
- hardcoded элементы legacy/migration logic
- архитектурные улучшения, не влияющие на controlled execution

### Что продолжает блокировать snapshot

- ошибки внутри controlled зоны
- cross-zone нарушения
- некорректный snapshot artifact
- нарушение boundary semantics
- нарушение create-only discipline в controlled execution

---

## Why

- соответствует исходной идее snapshot as boundary
- защищает новые проекты от legacy noise
- позволяет использовать DocOps как систему для новых controlled инициатив уже сейчас
- отделяет “operationally sufficient” от “architecturally perfect”
- сохраняет эволюционный путь без попытки переписать историю

---

## Trade-offs

Плюсы:

- ускоряется запуск новой эпохи
- новые проекты можно вести в controlled зоне без зависимости от legacy
- уменьшается давление на обязательную миграцию исторического слоя
- snapshot возвращается к своей исходной роли boundary artifact

Минусы:

- legacy technical debt сохраняется
- часть governance gaps остаётся в историческом слое
- validator/gate могут оставаться частично реализованными вне controlled scope
- система принимает осознанную неидеальность прошлого

---

## Consequences

- pre-snapshot hardening не является обязательным prerequisite для snapshot creation
- следующий приоритет после этого решения: snapshot creation execution
- новые проекты DocOps должны запускаться только в controlled зоне
- дальнейшее hardening возможно, но уже не как блокер snapshot creation
- legacy остаётся frozen historical layer

---

## Follow-ups

- создать operational_plan для snapshot creation execution
- создать новый fixed snapshot artifact
- после snapshot вести новые документы и новые проекты только в controlled зоне
- при необходимости выполнять hardening уже внутри новой эпохи или как отдельный follow-up поток

---

## Invariants

- snapshot изолирует прошлое
- legacy ошибки не влияют на future controlled execution
- controlled зона — единственный источник operational truth
- новые проекты должны стартовать только после boundary, а не внутри legacy слоя
