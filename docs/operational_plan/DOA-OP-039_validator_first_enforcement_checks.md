# DOA-OP-039 — Validator-first Enforcement Checks

## Metadata

Project: docops-agent  
Doc type: operational_plan  
ID: DOA-OP-039  
Status: draft  
Date: 2026-04-25  
Parent: DOA-DEC-067  

---

## Summary

This operational plan defines the minimal implementation steps for validator-first enforcement of document creation invariants.

The implementation must remain detection-only and must not mutate existing documents.

---

## Goal

Add validator-level checks that detect violations of document creation invariants.

---

## Scope

### In scope

- add detection-only checks for:
  - doc_type → folder consistency
  - ID format correctness
  - filename naming convention
  - metadata consistency

- preserve existing validator behavior
- produce structured findings

---

### Out of scope

- autofix
- mutation of documents
- pre-commit hooks
- CI integration
- Document Gate changes
- external integrations
- full policy engine

---

## Tasks

### T01 — Inspect current validator behavior

Review the existing validator implementation and identify where invariant checks should be added.

Done when:

- current validator flow is understood
- insertion point for enforcement checks is identified
- no files are changed except implementation files in later execution

---

### T02 — Add doc_type → folder check

Add detection-only validation that compares document metadata `Doc type` with the expected folder.

Done when:

- mismatch is reported as a structured finding
- valid documents are not reported
- no document content is modified

---

### T03 — Add ID format check

Add detection-only validation for canonical document ID format.

Done when:

- invalid ID format is reported
- valid canonical IDs pass
- report includes document path and detected ID

---

### T04 — Add filename naming convention check

Add detection-only validation for filename consistency with document ID and slug convention.

Done when:

- invalid filename is reported
- expected format is clear in finding message
- no rename or autofix is performed

---

### T05 — Add metadata consistency check

Add detection-only validation for consistency between metadata fields and filename/header where applicable.

Done when:

- inconsistent metadata is reported
- missing required metadata remains detectable
- findings are structured

---

### T06 — Run validator and capture report

Run the validator after implementation and save a report under `reports/`.

Done when:

- validator completes
- report file is created
- findings are reviewed
- result is suitable for implementation snapshot

---

### T07 — Create implementation snapshot

Create an implementation_snapshot after successful execution.

Done when:

- implementation result is documented
- report path is referenced
- limitations and next steps are recorded

---

## Acceptance Criteria

- validator detects document creation invariant violations
- implementation is detection-only
- no existing documents are modified
- no autofix is introduced
- no pre-commit hook is introduced
- no CI integration is introduced
- git working tree is clean after commit

---

## Risks

- validator responsibility may grow too much
- legacy documents may produce noise
- filename rules may require precise interpretation
- metadata parsing may have edge cases

---

## Next Step

Execute this operational plan through Cursor and return:

- changed files
- report path
- validator output summary
- commit hash
- git status
