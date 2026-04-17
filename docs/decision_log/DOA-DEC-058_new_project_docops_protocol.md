# DOA-DEC-058 — New project DocOps protocol

## Metadata

- Project: docops-agent
- Doc type: decision_log
- ID: DOA-DEC-058
- Status: accepted
- Date: 2026-04-17
- Parent: DOA-FSN-002

---

## Title

Протокол создания и ведения новых проектов в DocOps

---

## Decision

Все новые проекты в DocOps должны следовать фиксированному протоколу.

---

## Rules

### 1. Project entry point

- первый документ: idea_to_mvp
- проект должен ссылаться на DocOps repository

---

### 2. Lifecycle (mandatory)

IDEA → ARCH → DEC → OP → IMP

Пропуск шагов запрещён

---

### 3. Snapshot rule

- все проекты стартуют после DOA-FSN-002
- legacy запрещён для operational use

---

### 4. ChatGPT → Cursor workflow

- ChatGPT генерирует только промты
- Cursor выполняет
- файлы создаются только через Cursor

---

### 5. Prompt contract

Каждый prompt должен:

- содержать задачу
- содержать шаги
- содержать git действия
- содержать формат ответа

---

### 6. Cursor execution contract

Cursor обязан:

- создать файл
- сохранить в repo
- выполнить git add + commit
- вернуть результат

---

### 7. Git discipline

- commit после каждого шага
- atomic commits
- стандарт сообщений

---

### 8. Project isolation

- проекты не смешиваются
- документы принадлежат одному проекту
- cross-project ссылки контролируемы

---

### 9. Source of truth

- DocOps repo = методология
- проектный repo = execution

---

## Consequences

- все новые проекты стандартизированы
- уменьшается хаос
- повышается воспроизводимость
