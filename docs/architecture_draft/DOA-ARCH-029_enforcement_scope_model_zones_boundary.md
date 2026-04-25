# DOA-ARCH-029 --- Enforcement Scope Model (Zones & Boundary)

## Metadata

Project: docops-agent  
Doc type: architecture_draft  
ID: DOA-ARCH-029  
Status: draft  
Date: 2026-04-25  
Parent: DOA-IDEA-008  

---

## Overview

Вводится модель зон для управления применением enforcement layer.

Цель — устранить noise и сделать validator контекстно-осознанным.

---

## Core Concept

Система делится на зоны:

### 1. Legacy Zone

- документы, созданные до boundary
- не подчиняются enforcement
- могут содержать нарушения

### 2. Controlled Zone

- документы после boundary
- полностью подчиняются enforcement
- должны быть валидны

---

## Boundary

Boundary — фиксированная точка (snapshot), разделяющая зоны:

- всё до boundary → legacy
- всё после → controlled

Boundary является единственной точкой перехода.

---

## Enforcement Applicability

| Source Zone | Target Zone | Allowed | Enforcement |
|------------|------------|--------|------------|
| controlled | controlled | yes | strict |
| controlled | legacy     | no  | violation |
| controlled | boundary   | yes | allowed |
| legacy     | any        | yes | ignored |

---

## Severity Model (Conceptual)

- controlled violations → error
- legacy violations → ignored / informational
- cross-zone violations → error

---

## Constraints

- не изменяет существующие документы
- не требует миграции legacy
- совместимо с create-only

---

## Expected Impact

- снижение шума validator
- повышение доверия к enforcement
- возможность постепенного ужесточения правил

---

## Notes

- модель минимальная (MVP)
- детали политики будут определены в DEC

---

## Next Step

→ DEC: зафиксировать enforcement policy
