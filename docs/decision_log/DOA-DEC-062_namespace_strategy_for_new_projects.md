# DOA-DEC-062 — Namespace Strategy for New Projects

## Metadata

- Project: DocOps Agent
- Doc type: decision_log
- ID: DOA-DEC-062
- Status: accepted
- Date: 2026-04-19
- Parent: DOA-DEC-061

---

## Title

Namespace Strategy for New Projects

---

## Context

После принятия решения о restart проекта (**DOA-DEC-061**) необходимо определить стратегию namespace для новых проектов, создаваемых по методике DocOps.

При первом запуске был использован project-specific namespace (**RAG-IDEA-001**), что привело к потенциальному конфликту с текущей системой.

---

## Problem

Отсутствует единая стратегия именования документов:

- текущая система DocOps использует единый namespace (**DOA-***);
- новый проект начал использовать project-specific namespace (**RAG-***).

Риски:

- несовместимость validator/gate;
- нарушение traceability;
- усложнение поддержки.

---

## Options

### Option 1 — Unified namespace (DOA-*)

Все проекты используют единый namespace: **DOA-IDEA**, **DOA-ARCH**, **DOA-DEC** и т.д. Различие проектов — через поле **Metadata** (например Project).

### Option 2 — Project-specific namespace

Каждый проект использует свой namespace: **RAG-IDEA**, **CRM-IDEA** и т.д.

---

## Decision

Выбран **Option 1**: использовать **единый namespace DOA-*** для всех проектов.

---

## Why

- совместимость с текущими validator/gate;
- отсутствие необходимости менять систему;
- упрощение traceability;
- единая модель для всех проектов.

---

## Consequences

**Плюсы:**

- стабильная система;
- единая валидация;
- меньше сложности.

**Минусы:**

- ID не отражает продукт напрямую (компенсируется **Metadata**).

---

## Non-goals

- не вводить multi-project namespace сейчас;
- не менять существующие правила validator;
- не реализовывать сложную routing-логику.

---

## Next Steps

1. Использовать **DOA-*** namespace при новом bootstrap.
2. Перезапустить проект с чистого состояния.
3. Контролировать ID уже на этапе IDEA.
