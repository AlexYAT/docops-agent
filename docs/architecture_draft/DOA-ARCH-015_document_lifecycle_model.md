# architecture_draft — DOA-ARCH-015

## Metadata

- Project: DOA
- Doc type: architecture_draft
- ID: DOA-ARCH-015
- Status: draft
- Date: 2026-04-13
- Parent: DOA-ARCH-014

---

## Document Lifecycle Model

**Purpose:** Define type-aware lifecycle instead of global status enum.

## Summary

Define lifecycle per document type instead of global status enum.

## Problem

- Current validator treats "planned" as invalid
- Planning documents require "planned"
- System currently mixes lifecycle semantics

## Solution

Introduce type-aware lifecycle model.

---

## Lifecycle Model

### Planning Documents

Types:

- operational_plan
- midterm_plan
- longterm_plan

Allowed statuses:

- draft
- planned
- active
- superseded

Meaning:

- planned = task defined but not executed
- active = currently in execution

---

### Implementation Snapshot

Allowed statuses:

- draft
- recorded
- accepted

Meaning:

- recorded = fact фиксирован
- accepted = проверено и принято

---

### Decision Log

Allowed statuses:

- draft
- accepted
- rejected
- superseded

---

### Architecture Documents

Allowed statuses:

- draft
- accepted
- superseded

---

## Rules

1. Status must be validated per doc_type
2. Global enum is forbidden
3. Validator must become type-aware (future change)
4. "planned" is valid ONLY for planning documents

---

## Lifecycle Flow (conceptual)

idea → decision → plan (planned) → execution → snapshot (recorded)

---

## Notes

- No migration required (create-only system)
- Existing violations interpreted as model gap, not data error
