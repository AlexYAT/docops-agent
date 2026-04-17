# DOA-ARCH-024 — Snapshot artifact specification

## Metadata

- Project: docops-agent
- Doc type: architecture_draft
- ID: DOA-ARCH-024
- Status: draft
- Date: 2026-04-17
- Parent: DOA-DEC-053

---

## Overview

Данный документ формализует snapshot как отдельный тип артефакта системы DocOps:

→ DOA-FSN (Fixed Snapshot)

Snapshot является:

- границей эпохи (epoch boundary)
- мостом между legacy и controlled зонами
- точкой фиксации состояния системы

---

## Definition

Snapshot (DOA-FSN) — это immutable документ, который:

- фиксирует состояние системы в момент времени
- определяет boundary между эпохами
- служит единственным допустимым мостом к legacy

---

## Role in System

Snapshot выполняет функции:

1. Boundary  
   - разделяет legacy и controlled зоны

2. Bridge  
   - позволяет ссылаться на legacy через snapshot

3. Anchor  
   - фиксирует состояние системы

---

## Structure

Snapshot должен содержать:

- Metadata
- Summary состояния системы
- Список включённых документов (scope)
- Gate статус на момент snapshot
- Validator статус
- Описание epoch

---

## Metadata Requirements

Обязательные поля:

- Project
- Doc type = fixed_snapshot
- ID = DOA-FSN-XXX
- Status = accepted
- Date
- Parent (предыдущий snapshot или null)

---

## Invariants

Snapshot:

- immutable (не изменяется после создания)
- единственный мост в legacy
- не может ссылаться на будущие документы
- используется как reference root для controlled зоны

---

## Linking Rules

Controlled документы могут ссылаться только на:

- текущий snapshot
- другие controlled документы

Legacy документы:

- не используются напрямую
- доступны только через snapshot

---

## Lifecycle Integration

Snapshot участвует в lifecycle:

- создаётся в фазе snapshot creation
- активирует новую эпоху
- становится boundary для следующего цикла

---

## Risks

- неправильная структура snapshot
- нарушение invariants
- использование snapshot как обычного документа

---

## Expected Result

Система получает:

- формализованный тип DOA-FSN
- единый стандарт snapshot-документа
- основу для validator/gate интеграции

---

## Follow-up

- template для DOA-FSN
- validator rules для snapshot
- integration с gate
