# decision_log — DOA-DEC-033

## Metadata

- Project: DOA
- Doc type: decision_log
- ID: DOA-DEC-033
- Status: accepted
- Date: 2026-04-10
- Parent: DOA-IMP-015

---

## Title

Delegation of Git operations (add / commit / push) to Cursor prompts

---

## Context

В текущем workflow:

ChatGPT → Prompt → Cursor → Files → Git

часть Git-операций выполняется вручную, что создаёт:

- риск забыть commit или push
- несогласованные commit messages
- нарушение атомарности изменений
- “мусорные” коммиты
- рассинхронизацию DocOps и Git

---

## Options considered

### Option A — Manual Git (текущее состояние)

Пользователь выполняет git add / commit / push вручную.

Минусы:
- человеческий фактор
- нет гарантии дисциплины

---

### Option B — Внешняя автоматизация (hooks / CI)

Git-операции автоматизируются вне Cursor.

Минусы:
- избыточно для MVP
- усложняет систему

---

### Option C — Git через Cursor prompts (выбранный вариант)

ChatGPT формирует prompt, включающий:
- изменения файлов
- git add
- git commit
- (опционально) git push

Cursor выполняет всё атомарно.

---

## Chosen solution

Принято:

Все Git-операции выполняются через Cursor prompts.

Правила:

1. Каждый логический шаг → один prompt:
   - изменения
   - git add
   - git commit

2. Commit message:
   - формируется ChatGPT
   - не редактируется вручную

3. Push:
   - выполняется либо в том же prompt
   - либо отдельным prompt

4. Пользователь:
   - не выполняет git add / commit вручную
   - только запускает prompt

---

## Why

- устраняется человеческий фактор
- Git становится частью DocOps pipeline
- повышается воспроизводимость
- синхронизируются документы и код
- улучшается читаемость истории

---

## Trade-offs

Минусы:
- меньше гибкости
- зависимость от качества prompt

Плюсы:
- предсказуемость
- чистая история
- дисциплина

---

## Follow-ups

- внедрить git-блок в каждый Cursor prompt
- стандартизировать commit messages (опционально)
- использовать правило: 1 OP → 1 commit block
