# Metadata
Project: docops-agent  
Doc type: decision_log  
ID: DOA-DEC-069  
Status: accepted  
Date: 2026-04-25  
Parent: null  

---

# Title
Execution unit definition: one chat = one IDEA lifecycle

---

# Context
Отсутствует формальное определение execution unit в DocOps workflow.
Это приводит к смешению циклов, росту контекста и потере traceability.

---

# Decision (Invariant)

Execution unit в системе определяется как:

👉 1 chat = 1 IDEA lifecycle

Lifecycle включает:

IDEA → ARCH → DEC → OP → IMP → AUD

---

# Rules

1. Один чат = один lifecycle  
2. После завершения IMP/AUD чат закрывается  
3. Новый lifecycle → новый чат  
4. Запрещено смешивать несколько IDEA в одном чате  

---

# Why

- контроль контекста  
- изоляция reasoning  
- улучшение traceability  
- воспроизводимость  

---

# Consequences

Плюсы:
- детерминированные циклы
- ограниченный контекст
- прозрачная структура работы

Минусы:
- увеличение количества чатов
- необходимость дисциплины

---

# Constraints

- без автоматизации  
- без изменений существующих документов  
- правило применяется только к новым циклам  

---

# Non-goals

- не описывает tooling  
- не вводит enforcement  
- не меняет архитектуру  
