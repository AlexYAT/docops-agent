# DOA-DEC-068 --- Enforcement Scope Policy

## Metadata

Project: docops-agent  
Doc type: decision_log  
ID: DOA-DEC-068  
Status: accepted  
Date: 2026-04-25  
Parent: DOA-ARCH-029  

---

## Title

Зафиксировать policy применения enforcement layer

---

## Context

ARCH определил модель зон:

- legacy
- controlled
- boundary

Необходимо зафиксировать правила применения enforcement.

---

## Decision

Ввести enforcement policy:

### 1. Zone Rules

- controlled → enforcement обязателен
- legacy → enforcement игнорируется

### 2. Boundary Rules

- boundary является единственной допустимой связью с legacy

### 3. Cross-zone Rules

- controlled → legacy = запрещено
- controlled → boundary = разрешено
- legacy → любое = разрешено

### 4. Severity Rules

- controlled violations → error
- cross-zone violations → error
- legacy violations → ignored / informational

---

## Why

- устраняет noise
- делает validator предсказуемым
- вводит управляемую модель enforcement

---

## Consequences

- validator становится context-aware
- появляется основа для gate logic
- возможна дальнейшая автоматизация

---

## Non-goals

- изменение существующих документов
- автоматическое исправление
- внедрение CI/CD

---

## Next Steps

→ OP: реализовать policy в validator (detection-only)
