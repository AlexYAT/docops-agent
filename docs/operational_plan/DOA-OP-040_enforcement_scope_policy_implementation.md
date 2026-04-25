# DOA-OP-040 --- Enforcement Scope Policy Implementation (Detection-only)

## Metadata

Project: docops-agent  
Doc type: operational_plan  
ID: DOA-OP-040  
Status: draft  
Date: 2026-04-25  
Parent: DOA-DEC-068  

---

## Summary

Реализовать enforcement scope policy в validator (режим detection-only).

---

## Goal

Сделать validator context-aware:

- учитывать зоны
- учитывать boundary
- применять severity по policy

---

## Tasks

### T01 — Zone Detection

- определить источник документа (source_zone)
- определить целевой документ (target_zone)

---

### T02 — Boundary Handling

- определить boundary artifact
- внедрить правило разрешённой связи через boundary

---

### T03 — Applicability Rules

- внедрить правила:
  - controlled → controlled (ok)
  - controlled → legacy (violation)
  - controlled → boundary (ok)
  - legacy → any (ignore)

---

### T04 — Severity Mapping

- controlled violations → error
- cross-zone violations → error
- legacy violations → ignored / informational

---

### T05 — Report Update

- добавить поля:
  - source_zone
  - target_zone
  - enforcement_applicable (true/false)

---

## Constraints

- detection-only (без autofix)
- без изменения существующих документов
- без CI/CD

---

## Success Criteria

- validator учитывает зоны
- noise снижен
- legacy не влияет на enforcement
- controlled зона строго валидируется

---

## Next Step

→ IMP: зафиксировать первый enforcement run
