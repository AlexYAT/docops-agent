# DOA-IMP-038 — Validator-first Enforcement Checks

## Metadata

Project: docops-agent  
Doc type: implementation_snapshot  
ID: DOA-IMP-038  
Status: accepted  
Date: 2026-04-25  
Parent: DOA-OP-039  

---

## Summary

This snapshot records the implementation of validator-first enforcement checks for document creation invariants.

The implementation was completed in detection-only mode and does not mutate existing documents.

---

## Implementation Result

Implemented as part of DOA-OP-039:

- validator-first enforcement checks
- structured enforcement findings
- detection-only behavior
- report generation

Execution commit:

- 8d43fdb

---

## Changed Files

- scripts/doa_link_id_validator.py
- reports/doa_enforcement_run_001.json

---

## Implemented Checks

### doc_type → folder

Detects mismatch between document metadata `Doc type` and expected folder.

Finding type:

- doc_type_folder_mismatch

---

### ID format

Detects invalid canonical ID format.

Expected format:

- DOA-[TYPE]-NNN

Finding type:

- invalid_id_format

---

### Filename naming convention

Detects filenames that do not match:

- <ID>_<short_lowercase_slug>.md

Finding type:

- filename_mismatch

---

### Metadata consistency

Detects mismatch between metadata and filename/folder where applicable.

Finding type:

- metadata_inconsistency

---

## Report

Report path:

- reports/doa_enforcement_run_001.json

Summary:

- files scanned: 195
- enforcement findings total: 13
- enforcement errors: 13
- enforcement warnings: 0

---

## Observations

The first enforcement run successfully detected document creation invariant violations.

All enforcement findings in this run are filename mismatch errors.

Most findings are related to older or legacy-style filenames.

This confirms that enforcement is working, but also shows that policy scoping is needed to avoid legacy noise.

---

## Constraints Preserved

- create-only preserved
- no autofix introduced
- no existing documents modified
- no pre-commit hook introduced
- no CI integration introduced
- no external integration introduced

---

## Limitations

- enforcement currently reports findings across the scanned repository
- legacy filename noise is visible
- enforcement policy is not yet boundary-aware
- severity policy may require refinement

---

## Next Step

Create a decision_log to define enforcement scope policy.

Expected DEC topic:

- controlled-only enforcement
- boundary-aware enforcement
- full repository enforcement

Recommended direction:

- boundary-aware / controlled-only enforcement for MVP
