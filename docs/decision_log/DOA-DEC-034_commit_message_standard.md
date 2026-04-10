# decision_log — DOA-DEC-034

## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-034
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-DEC-033

---

## Title

Standardized commit message format for DocOps Agent

---

## Context

После принятия DOA-DEC-033 все Git-операции выполняются через Cursor prompts.

Однако формат commit message остаётся нестрогим, что приводит к:

- разной структуре истории
- потере контекста изменений
- сложности анализа истории
- несоответствию DocOps-документам

---

## Options considered

### Option A — Свободный формат

Каждый commit message формируется произвольно.

Минусы:
- нет стандарта
- плохая читаемость истории

---

### Option B — Conventional Commits (частично)

Использование типа feat/docs/fix без привязки к DocOps.

Минусы:
- нет связи с документами
- теряется DocOps-контекст

---

### Option C — DocOps-aware commit format (выбранный вариант)

Commit message отражает:

- тип изменения
- DocOps-документы
- краткое содержание

---

## Chosen solution

Принят единый формат commit message:

### Структура

<type>(<scope>): <short summary>

<details block>

---

### Типы (type)

- feat — новая функциональность
- docs — документация
- fix — исправления
- refactor — рефакторинг
- chore — служебные изменения

---

### Scope

- gate
- validator
- docops
- imp
- dec
- op

---

### Правила

1. Первая строка:
   - короткая (до ~72 символов)
   - содержит type + scope

2. Далее (опционально):
   - список изменений
   - ссылки на DocOps ID

3. Обязательно:
   - привязка к DocOps документам (IDEA / DEC / OP / IMP)

---

### Пример

feat(gate): implement Document Gate MVP and first run

- add DOA-IDEA-002
- add DOA-DEC-032 policy model
- implement gate CLI and policy
- generate first report

---

## Why

- делает Git частью DocOps системы
- улучшает читаемость истории
- связывает код и документы
- упрощает аудит

---

## Trade-offs

Минусы:
- требует дисциплины
- длиннее commit messages

Плюсы:
- высокая прозрачность
- системность
- удобство анализа

---

## Follow-ups

- использовать формат во всех новых prompts
- не менять старые commit messages (create-only)
