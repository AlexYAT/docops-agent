# DOA-DEC-067 — Validator-first Enforcement Strategy

## Metadata

Project: docops-agent  
Doc type: decision_log  
ID: DOA-DEC-067  
Status: accepted  
Date: 2026-04-25  
Parent: DOA-ARCH-028  

---

## Context

DocOps Agent has stabilized document creation invariants:

- doc_type determines folder
- ID is generated through repository scan
- filename follows naming convention
- document creation follows a controlled workflow

DOA-IDEA-007 identified the lack of enforcement.

DOA-ARCH-028 described a minimal detection-only enforcement architecture.

The system now needs a decision on the MVP enforcement strategy.

---

## Problem

Rules exist, but they are not automatically checked.

Without enforcement:

- document creation errors may remain undetected
- rule compliance depends on user discipline
- the system is not self-validating

---

## Options Considered

### Option 1 — Validator-first enforcement

Extend the existing validator with document creation invariant checks.

Pros:

- minimal architecture change
- reuses existing validation entry point
- keeps enforcement detection-only
- aligns with MVP simplicity
- avoids premature automation

Cons:

- validator grows in responsibility
- later separation may be needed if checks become complex

---

### Option 2 — Gate-first enforcement

Add enforcement checks directly to Document Gate.

Pros:

- aligns with acceptance/rejection flow
- centralizes policy-level decisions

Cons:

- mixes low-level invariant checks with gate policy
- increases complexity too early
- makes Document Gate responsible before validator output is mature

---

### Option 3 — Separate enforcement checker

Create a new dedicated checker for document creation invariants.

Pros:

- clean separation of responsibilities
- easier to evolve independently later

Cons:

- adds new component too early
- duplicates scanning/reporting logic
- increases MVP complexity

---

## Decision

Choose **Option 1 — Validator-first enforcement**.

The MVP enforcement layer should be implemented as additional detection-only checks inside the existing validator flow.

Document Gate may consume validator findings later, but it should not be the first enforcement implementation target.

---

## Rationale

Validator-first enforcement is the simplest strategy that satisfies the current need:

- detect violations
- preserve create-only
- avoid automatic mutation
- avoid pre-commit/CI complexity
- keep Document Gate optional

This keeps the MVP stable and avoids premature automation.

---

## Consequences

### Positive

- system becomes more self-validating
- document creation violations become detectable
- implementation can stay incremental
- existing validator remains the primary quality entry point

### Negative

- validator responsibility increases
- future refactoring may be needed if enforcement grows

---

## Non-Goals

- no autofix
- no mutation of existing documents
- no pre-commit hook
- no CI enforcement
- no external integrations
- no full policy engine

---

## Next Step

Create an operational_plan to implement validator-first enforcement checks.

Expected OP topic:

- add detection-only checks for:
  - doc_type → folder
  - ID format
  - filename naming convention
  - metadata consistency
