# DOA-DEC-060 — Doc type semantics as artifact class

## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-060
- Status: accepted
- Date: 2026-04-18
- Parent: DOA-ARCH-025

---

## Title

Семантика doc_type: класс артефакта, а не зрелость документа

---

## Context

В ходе hardening-цикла выявлено семантическое напряжение между:

- `doc_type`
- `status`
- каноническим путём документа

На практике в системе существуют документы вида:

- `DOA-ARCH-*`
- `Doc type: architecture_draft`
- `Status: accepted`

Это создаёт риск ложной интерпретации: слово `draft` в `doc_type` может ошибочно восприниматься как текущий статус зрелости, а не как исторически закреплённое имя класса артефакта.

---

## Options considered

### Option 1

Трактовать `doc_type` как класс артефакта, независимо от текущего `status`.

### Option 2

Очистить модель и перейти к «чистым» типам (`architecture`, `decision`, `plan` и т.п.), где зрелость задаётся только через `status`.

### Option 3

Ввести promotion model: `architecture_draft` → `architecture` через отдельный create-only lifecycle.

---

## Chosen solution

Выбран **Option 1**.

`doc_type` трактуется как **класс артефакта**.

`status` трактуется как **текущее состояние / зрелость** документа.

---

## Decision

В системе DocOps:

1. `doc_type` и `status` являются **разными осями** семантики.
2. `doc_type` **не обязан** кодировать текущую зрелость документа.
3. Исторически закреплённые типы, такие как `architecture_draft`, **допустимы** даже при `Status: accepted`.
4. Слово `draft` в `architecture_draft` трактуется как **часть имени класса артефакта**, а не как обязательный статус документа.
5. Канонический путь документа продолжает определяться по `doc_type`.
6. **Semantic cleanup** типовой модели **не входит** в текущий hardening-цикл и может быть вынесен в отдельный будущий lifecycle.

---

## Why

- не ломает текущий репозиторий
- сохраняет совместимость с уже принятыми документами
- не требует миграции путей и validator/gate
- минимизирует scope текущего hardening-цикла
- позволяет усилить систему без structural refactor

---

## Consequences

- `architecture_draft` остаётся допустимым типом
- `Status: accepted` для таких документов остаётся допустимым
- path enforcement продолжает опираться на `doc_type`
- semantic tension признаётся, но **не устраняется** в этом цикле
- возможный semantic cleanup переносится в будущее

---

## Non-goals

В рамках данного решения **не** выполняется:

- переименование существующих типов документов
- миграция каталогов
- введение promotion model между типами
- чистка исторических naming choices

---

## Next Steps

- продолжить hardening-цикл следующими DEC
- обновить системный prompt и cursor rules с учётом этой семантики
- при необходимости позже открыть отдельный lifecycle на semantic cleanup doc_type model
