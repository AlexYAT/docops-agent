# architecture_draft — DOA-ARCH-027

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-027
- Status: accepted
- Date: 2026-04-18
- Parent: DOA-ARCH-026

_Create-only: новые версии — только новым ID._

---

## Title

Project Bootstrap Protocol (DocOps)

---

## Purpose

Зафиксировать **единый канонический порядок** запуска нового проекта в системе DocOps, чтобы старт не зависел от неявных знаний и совпадал с docs-first и lifecycle.

---

## Context

- DocOps требует **docs-first** старта.
- Без формального bootstrap возможны пропуски этапов и несогласованные артефакты.
- Runtime-поведение AI уже зафиксировано (**DOA-OTH-001** — snapshot; **DOA-ARCH-026** — семантика prompt).

---

## Bootstrap Principles

- старт с **system prompt snapshot** (вставка готового блока из snapshot-артефакта);
- **docs-first** обязателен;
- **create-only** для проектных документов обязателен;
- **lifecycle** не сокращать и не пропускать произвольно.

---

## Bootstrap Flow (канонический)

1. Вставить **system prompt** из актуального snapshot.
2. Сформулировать **первую задачу** (цель проекта в терминах DocOps).
3. Создать первый смысловой документ: **idea_to_mvp** (IDEA).
4. Создать **architecture_draft** (ARCH).
5. Создать **operational_plan** (OP).
6. После **accepted** OP — переход к **execution** (задачи только в рамках плана).

---

## Minimal Required Artifacts

Для валидного старта достаточно наличия (в канонических путях):

- **idea_to_mvp**
- **architecture_draft**
- **operational_plan**

Дальнейшие типы — по lifecycle и задачам (DEC, IMP и т.д.).

---

## Naming / Project Isolation

- ID может оставаться в префиксе **DOA-***, если репозиторий трактуется как meta-слой DocOps.
- Отдельный **namespace** префиксов для «обычных» продуктовых репозиториев — вне scope этого документа (возможный будущий DEC).

---

## Rules During Bootstrap

- Работа **без** accepted **operational_plan** допустима **только** до появления первого **accepted** OP (bootstrap-фаза), согласно политике planning-first.
- После первого accepted OP — исполнение **только** через operational_plan (и связанные артефакты по политике).

---

## Forbidden During Bootstrap

- пропуск **IDEA** или **ARCH** ради «быстрого» IMP;
- прямой переход к **implementation_snapshot** без опоры на принятый план;
- переписывание существующих документов вместо create-only (кроме явно оговорённых операционных исключений вне этого протокола).

---

## Consequences

- единообразный старт проектов;
- воспроизводимое onboarding-поведение;
- меньше дрейфа структуры и lifecycle.

---

## Non-goals

- не задаёт стратегию namespace и префиксов для всех репозиториев;
- не описывает CI/CD и автоматизацию bootstrap;
- не изменяет существующие правила репозитория — только фиксирует методику старта.

---

## Next Steps

- при необходимости — **DEC** по namespace для не-meta проектов;
- опционально — шаблон «project starter» (отдельный артефакт).
